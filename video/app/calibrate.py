# calibrate.py
# Gera as zonas dos bancos e grava o bloco ZONES no config.py.
#
# Modo automático (padrão): roda o MediaPipe nos primeiros segundos do vídeo, com todos
# sentados normalmente, e cria uma zona em volta do corpo de cada pessoa.
# Procura na imagem inteira e também em 3 faixas recortadas, para achar quem está pequeno.
#   python calibrate.py                      (vídeo do config.py)
#   python calibrate.py uber.mp4             (outro vídeo)
#   python calibrate.py uber.mp4 --inicio 10 (analisa a partir do segundo 10)
#   python calibrate.py 0                    (webcam)
#
# Modo manual: você desenha um retângulo para cada banco com o mouse.
#   python calibrate.py uber.mp4 --manual
#   Para cada zona: arraste o retângulo e aperte ENTER. Para pular, aperte ENTER sem desenhar.
import argparse
import re
import statistics

import cv2

if __package__:
    from . import config
    from .main import create_detector, detect_poses
    from .zone_crop import create_crop_detector, detect_in_region
else:
    import config
    from main import create_detector, detect_poses
    from zone_crop import create_crop_detector, detect_in_region

# Pontos usados para a caixa do corpo: nariz, ombros, cotovelos, pulsos, quadris e joelhos
BODY_POINTS = (0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26)
MARGIN = 0.05           # folga em volta do corpo (fração da imagem)
SAME_PERSON_DIST = 0.15 # distância máxima dos ombros para considerar a mesma pessoa entre frames
BACK_SEAT_RATIO = 0.7   # ombros menores que 70% dos do motorista = banco de trás (mais longe)

# Faixas verticais da imagem (com sobreposição) onde também procuramos pessoas.
# Mesmo motivo do zone_crop.py: o MediaPipe perde quem é pequeno na imagem inteira
# (ex.: banco de trás), mas acha essa pessoa num recorte. Aqui ainda não existem zonas,
# então recortamos a imagem em 3 faixas fixas.
STRIPS = ((0.0, 0.0, 0.45, 1.0), (0.275, 0.0, 0.725, 1.0), (0.55, 0.0, 1.0, 1.0))


def open_video(source, start_second):
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not cap.isOpened():
        raise RuntimeError(f"Não foi possível abrir o vídeo: {source}")
    cap.set(cv2.CAP_PROP_POS_MSEC, start_second * 1000)
    return cap


def shoulders_mid(pose):
    return (pose[11].x + pose[12].x) / 2, (pose[11].y + pose[12].y) / 2


def body_box(pose):
    points = [pose[i] for i in BODY_POINTS if pose[i].visibility >= config.MIN_VISIBILITY]
    if len(points) < 3:
        return None
    xs, ys = [p.x for p in points], [p.y for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def collect_people(cap, seconds):
    """Roda o detector por alguns segundos e junta, para cada pessoa, as caixas do corpo e a largura dos ombros."""
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    detector = create_detector()
    strip_detectors = [create_crop_detector() for _ in STRIPS]
    people = []  # cada pessoa: {'mid': (x, y), 'boxes': [...], 'widths': [...]}
    last_frame = None

    for frame_idx in range(int(seconds * fps)):
        ok, frame = cap.read()
        if not ok:
            break
        last_frame = frame
        timestamp_ms = int(frame_idx * 1000 / fps)
        poses = list(detect_poses(detector, frame, timestamp_ms))

        # Pessoas achadas só nas faixas: aceitas apenas se não forem alguém que a imagem inteira
        # já encontrou neste frame (uma faixa pode cortar o motorista ao meio e gerar uma caixa errada)
        for strip, strip_detector in zip(STRIPS, strip_detectors):
            pose = detect_in_region(strip_detector, frame, strip, timestamp_ms)
            if pose is None:
                continue
            sx, sy = shoulders_mid(pose)
            if all(abs(sx - shoulders_mid(p)[0]) + abs(sy - shoulders_mid(p)[1]) > SAME_PERSON_DIST for p in poses):
                poses.append(pose)

        for pose in poses:
            box = body_box(pose)
            if box is None:
                continue
            mx, my = shoulders_mid(pose)
            # Procura a pessoa já vista mais próxima; se nenhuma estiver perto, é uma pessoa nova
            nearest = min(people, key=lambda p: abs(p['mid'][0] - mx) + abs(p['mid'][1] - my), default=None)
            if nearest is None or abs(nearest['mid'][0] - mx) + abs(nearest['mid'][1] - my) > SAME_PERSON_DIST:
                nearest = {'mid': (mx, my), 'boxes': [], 'widths': []}
                people.append(nearest)
            nearest['boxes'].append(box)
            nearest['widths'].append(abs(pose[11].x - pose[12].x))

    # Descarta "pessoas" que apareceram em poucos frames (detecções falsas)
    min_frames = max(3, max((len(p['boxes']) for p in people), default=0) // 4)
    return [p for p in people if len(p['boxes']) >= min_frames], last_frame


def auto_zones(people):
    """
    Transforma cada pessoa em uma zona e dá um nome pela posição.
    Altura da zona: do topo da cabeça aos joelhos (mediana dos frames + folga).
    Largura: o espaço entre duas pessoas vizinhas é dividido ao meio, assim as zonas
    não se sobrepõem e uma mão que atravessa metade do caminho já entra na zona do outro.
    """
    zones = []
    for p in people:
        x1, y1, x2, y2 = (statistics.median(b[i] for b in p['boxes']) for i in range(4))
        zones.append({'box': [max(0.0, x1 - MARGIN), max(0.0, y1 - MARGIN), min(1.0, x2 + MARGIN), min(1.0, y2 + MARGIN)],
                      'x': p['mid'][0],
                      'width': statistics.median(p['widths'])})

    if not zones:
        return {}

    # Da direita para a esquerda; divide ao meio o espaço entre vizinhos
    zones.sort(key=lambda z: z['x'], reverse=True)
    for right, left in zip(zones, zones[1:]):
        middle = (right['x'] + left['x']) / 2
        right['box'][0] = middle
        left['box'][2] = middle

    # Motorista = pessoa mais à direita da imagem (câmera no para-brisa olhando para trás, carro brasileiro)
    driver = zones[0]
    named = {'motorista': driver['box']}
    back_count = front_count = 0
    for z in zones[1:]:
        # O nome é só um rótulo para a tela; a regra de invasão não depende dele
        if z['width'] < BACK_SEAT_RATIO * driver['width']:
            back_count += 1
            name = 'banco_tras' if back_count == 1 else f'banco_tras_{back_count}'
        else:
            front_count += 1
            name = 'passageiro_frente' if front_count == 1 else f'passageiro_frente_{front_count}'
        named[name] = z['box']

    return {name: tuple(round(v, 2) for v in box) for name, box in named.items()}


def manual_zones(frame):
    scale = min(1.0, 1280 / frame.shape[1], 720 / frame.shape[0])
    frame = cv2.resize(frame, None, fx=scale, fy=scale)
    h, w = frame.shape[:2]
    zones = {}
    for name in ('motorista', 'passageiro_frente', 'banco_tras'):
        x, y, bw, bh = cv2.selectROI(f"Desenhe a zona '{name}' e aperte ENTER", frame, showCrosshair=False)
        cv2.destroyAllWindows()
        if bw == 0 or bh == 0:
            continue
        zones[name] = (round(x / w, 2), round(y / h, 2), round((x + bw) / w, 2), round((y + bh) / h, 2))
        cv2.rectangle(frame, (x, y), (x + bw, y + bh), (180, 180, 180), 2)
    return zones


def zones_text(zones):
    lines = ["ZONES = {"] + [f"    '{name}': {box}," for name, box in zones.items()] + ["}"]
    return "\n".join(lines)


def save_to_config(zones):
    path = config.APP_DIR / 'config.py'
    text = path.read_text(encoding='utf-8')
    text = re.sub(r"ZONES = \{.*?\n\}", lambda _: zones_text(zones), text, count=1, flags=re.DOTALL)
    path.write_text(text, encoding='utf-8')


def show_preview(frame, zones):
    h, w = frame.shape[:2]
    for name, (x1, y1, x2, y2) in zones.items():
        cv2.rectangle(frame, (int(x1 * w), int(y1 * h)), (int(x2 * w), int(y2 * h)), (0, 255, 255), 2)
        cv2.putText(frame, name, (int(x1 * w) + 5, int(y1 * h) + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    window = 'Zonas geradas (aperte qualquer tecla)'
    cv2.namedWindow(window, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(window, 1280, 720)
    cv2.imshow(window, frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description='Gera as zonas dos bancos e grava no config.py')
    parser.add_argument('video', nargs='?', default=config.VIDEO_PATH, help='arquivo de vídeo ou 0 para webcam')
    parser.add_argument('--inicio', type=float, default=0, help='segundo do vídeo onde começar')
    parser.add_argument('--segundos', type=float, default=3, help='quantos segundos analisar no modo automático')
    parser.add_argument('--manual', action='store_true', help='desenhar as zonas com o mouse')
    args = parser.parse_args()

    cap = open_video(args.video, args.inicio)
    if args.manual:
        ok, frame = cap.read()
        if not ok:
            raise RuntimeError(f"Não foi possível ler o vídeo: {args.video}")
        zones = manual_zones(frame)
    else:
        people, frame = collect_people(cap, args.segundos)
        zones = auto_zones(people)
    cap.release()

    if not zones:
        print("Nenhuma pessoa encontrada. Tente outro trecho (--inicio) ou o modo --manual.")
        return

    save_to_config(zones)
    print("Zonas gravadas no config.py:\n")
    print(zones_text(zones))
    if frame is not None:
        show_preview(frame, zones)


if __name__ == '__main__':
    main()
