# zone_crop.py
# Detecção extra dentro do recorte de cada zona, para achar pessoas pequenas (ex.: banco de trás).
#
# POR QUE ISSO EXISTE
# O MediaPipe Pose foi feito para uma pessoa grande e perto da câmera. Antes de procurar
# a pessoa, ele reduz a imagem inteira para um tamanho pequeno e fixo (~256 px). Numa câmera
# grande-angular de cabine, quem está no banco de trás vira poucos pixels depois dessa redução
# e o detector não acha a pessoa. No vídeo de teste, a passageira de trás era encontrada
# em só 61% dos frames.
#
# COMO RESOLVE
# Recortamos só o retângulo da zona (ex.: o banco de trás) e passamos ESSE pedaço ao MediaPipe.
# Ele reduz o recorte para o mesmo tamanho fixo, mas agora a pessoa ocupa boa parte da imagem,
# então funciona como um "zoom" (não é preciso ampliar o recorte, a redução interna já faz o
# efeito). No mesmo vídeo, a passageira passou a ser encontrada em 98% dos frames.
#
# QUANDO É USADO
# Só nas zonas onde a detecção na imagem inteira não encontrou ninguém. Quem está perto
# (o motorista) continua vindo da imagem inteira, que enxerga o braço dele atravessando
# para outro banco; um recorte cortaria esse braço.
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

if __package__:
    from . import config
    from .zones import seat_of
else:
    import config
    from zones import seat_of

# Folga em volta da zona ao recortar (fração da imagem), para não cortar a cabeça ou os joelhos
CROP_MARGIN = 0.05


class Point:
    """Ponto do corpo já convertido para a imagem inteira (mesmos campos que o MediaPipe usa)."""

    def __init__(self, x, y, visibility):
        self.x, self.y, self.visibility = x, y, visibility


def create_crop_detector():
    """
    Detector para recortes: procura no máximo 1 pessoa (cada banco tem uma pessoa só).
    """
    options = vision.PoseLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=config.MODEL_PATH),
        running_mode=vision.RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
        min_pose_presence_confidence=config.MIN_PRESENCE_CONFIDENCE,
        min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
    )
    return vision.PoseLandmarker.create_from_options(options)


def create_zone_detectors():
    """
    Um detector por zona. Precisam ser separados porque, no modo VÍDEO, o MediaPipe lembra
    a pessoa do frame anterior para acompanhá-la; misturar recortes de zonas diferentes
    no mesmo detector bagunçaria esse acompanhamento.
    """
    return {name: create_crop_detector() for name in config.ZONES}


def detect_in_region(detector, frame, region, timestamp_ms):
    """Procura uma pessoa só no recorte da região (x1, y1, x2, y2). Devolve a pose em coordenadas da imagem inteira, ou None."""
    h, w = frame.shape[:2]
    x1, y1, x2, y2 = region
    # Recorte = região + folga, sem passar da borda da imagem
    x1, y1 = max(0.0, x1 - CROP_MARGIN), max(0.0, y1 - CROP_MARGIN)
    x2, y2 = min(1.0, x2 + CROP_MARGIN), min(1.0, y2 + CROP_MARGIN)
    crop = frame[int(y1 * h):int(y2 * h), int(x1 * w):int(x2 * w)]

    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    result = detector.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb), timestamp_ms)
    if not result.pose_landmarks:
        return None

    # O MediaPipe devolve x e y de 0 a 1 relativos ao RECORTE.
    # Para voltar à imagem inteira: posição do recorte + posição dentro dele * tamanho do recorte.
    return [Point(x1 + p.x * (x2 - x1), y1 + p.y * (y2 - y1), p.visibility)
            for p in result.pose_landmarks[0]]


def add_missing_people(poses, frame, timestamp_ms, zone_detectors):
    """
    Completa a lista de poses da imagem inteira com quem só aparece no recorte das zonas vazias.
    A pessoa achada no recorte só é aceita se o meio dos ombros dela cair dentro daquela zona
    (evita pegar, por exemplo, o ombro do motorista que entrou na borda do recorte).
    """
    occupied = {seat_of(pose, config.ZONES) for pose in poses}
    poses = list(poses)
    for name, zone in config.ZONES.items():
        if name in occupied:
            continue
        pose = detect_in_region(zone_detectors[name], frame, zone, timestamp_ms)
        if pose is not None and seat_of(pose, {name: zone}) == name:
            poses.append(pose)
    return poses
