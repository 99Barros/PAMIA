# main.py
# Programa principal: lê o vídeo frame a frame, encontra as pessoas, verifica invasões
# entre as zonas dos bancos e mostra o resultado na tela e no terminal.
#
# Uso:  python main.py            (vídeo do config.py)
#       python main.py outro.mp4  (outro vídeo)
#       python main.py 0          (webcam)
# Teclas: ESPAÇO pausa/continua, ESC sai.
#
# Fluxo de cada frame:
#   1. MediaPipe na imagem inteira            -> detect_poses
#   2. Recorte das zonas vazias (pessoa pequena) -> zone_crop.add_missing_people
#   3. Quem está em qual banco e quem invadiu  -> zones.find_invasions
#   4. Conta o tempo de cada invasão           -> zones.InvasionTimer
#   5. Desenha e imprime os alertas            -> draw
import sys

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

if __package__:
    from . import config
    from .zone_crop import add_missing_people, create_zone_detectors
    from .zones import InvasionTimer, find_invasions, HAND_POINTS, LEFT_SHOULDER, RIGHT_SHOULDER
else:
    import config
    from zone_crop import add_missing_people, create_zone_detectors
    from zones import InvasionTimer, find_invasions, HAND_POINTS, LEFT_SHOULDER, RIGHT_SHOULDER

GRAY, GREEN, YELLOW, RED = (180, 180, 180), (0, 255, 0), (0, 255, 255), (0, 0, 255)


def create_detector():
    """Detector principal, que olha a imagem inteira e procura até MAX_POSES pessoas."""
    options = vision.PoseLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=config.MODEL_PATH),
        running_mode=vision.RunningMode.VIDEO,  # usa os frames anteriores: pontos mais estáveis
        num_poses=config.MAX_POSES,
        min_pose_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
        min_pose_presence_confidence=config.MIN_PRESENCE_CONFIDENCE,
        min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
    )
    return vision.PoseLandmarker.create_from_options(options)


def detect_poses(detector, frame, timestamp_ms):
    """
    Roda o MediaPipe em um frame. Devolve uma lista de poses; cada pose tem 33 pontos
    com x e y de 0 a 1 (fração da largura/altura da imagem) e a visibilidade do ponto.
    O timestamp é obrigatório no modo VÍDEO e precisa sempre aumentar.
    """
    # O OpenCV lê as cores em BGR e o MediaPipe espera RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    return detector.detect_for_video(image, timestamp_ms).pose_landmarks


def to_px(point, w, h):
    return int(point.x * w), int(point.y * h)


def draw(frame, poses, seats, timer):
    """Desenha zonas, pessoas, mãos e o painel de alertas por cima do frame (só visualização)."""
    h, w = frame.shape[:2]
    alerts = timer.alerts()
    victims = {victim for _, victim in alerts}

    # Zonas: cinza normal, vermelho se alguém está invadindo
    for name, (x1, y1, x2, y2) in config.ZONES.items():
        color = RED if name in victims else GRAY
        cv2.rectangle(frame, (int(x1 * w), int(y1 * h)), (int(x2 * w), int(y2 * h)), color, 2)
        cv2.putText(frame, name, (int(x1 * w) + 5, int(y1 * h) + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Pessoas: banco escrito no meio dos ombros e círculo nos pontos da mão
    for pose, seat in zip(poses, seats):
        mid_x = int((pose[LEFT_SHOULDER].x + pose[RIGHT_SHOULDER].x) / 2 * w)
        mid_y = int((pose[LEFT_SHOULDER].y + pose[RIGHT_SHOULDER].y) / 2 * h)
        cv2.circle(frame, (mid_x, mid_y), 8, YELLOW, -1)
        cv2.putText(frame, seat or 'fora das zonas', (mid_x + 10, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, YELLOW, 2)
        for idx in HAND_POINTS:
            if pose[idx].visibility >= config.MIN_VISIBILITY:
                cv2.circle(frame, to_px(pose[idx], w, h), 10, GREEN, -1)

    # Painel: tempo acumulado de cada invasão
    y = 40
    for (invader, victim), t in timer.elapsed.items():
        if t <= 0:
            continue
        color = RED if (invader, victim) in alerts else YELLOW
        label = 'ALERTA' if color == RED else 'atencao'
        cv2.putText(frame, f"{label}: {invader} -> {victim} ({t:.1f}s)", (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        y += 40


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else config.VIDEO_PATH
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not cap.isOpened():
        raise RuntimeError(f"Não foi possível abrir o vídeo: {source}")

    # fps define o tempo de cada frame; webcams às vezes informam 0, por isso o padrão 30
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    detector = create_detector()
    zone_detectors = create_zone_detectors() if config.USE_ZONE_CROP else None
    timer = InvasionTimer(config.INVASION_SECONDS)
    active_alerts = set()

    window = 'Monitoramento de Espaco'
    cv2.namedWindow(window, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow(window, 1280, 720)

    frame_idx = 0
    paused = False
    while True:
        if not paused:
            ok, frame = cap.read()
            if not ok:
                break
            timestamp_ms = int(frame_idx * 1000 / fps)
            frame_idx += 1

            poses = detect_poses(detector, frame, timestamp_ms)
            if zone_detectors:
                # Procura de novo, só no recorte, nos bancos onde ninguém foi achado (ver zone_crop.py)
                poses = add_missing_people(poses, frame, timestamp_ms, zone_detectors)
            seats, invasions = find_invasions(poses, config.ZONES, config.MIN_VISIBILITY)
            # Cada frame dura 1/fps segundos; é isso que soma (ou desconta) no tempo de invasão
            timer.update(invasions, 1 / fps)

            # Log no terminal quando um alerta começa ou termina
            alerts = set(timer.alerts())
            for invader, victim in alerts - active_alerts:
                print(f"[{timestamp_ms / 1000:7.1f}s] ALERTA: {invader} -> {victim}")
            for invader, victim in active_alerts - alerts:
                print(f"[{timestamp_ms / 1000:7.1f}s] fim:    {invader} -> {victim}")
            active_alerts = alerts

            draw(frame, poses, seats, timer)
            cv2.imshow(window, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        if key == ord(' '):
            paused = not paused

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
