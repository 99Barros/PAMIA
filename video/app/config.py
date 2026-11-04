# config.py
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
MODELS_DIR = PROJECT_DIR / 'models'
VIDEOS_DIR = PROJECT_DIR / 'videos'

# Modelo "full" é mais preciso que o "lite" com corpo parcial (sentado, cortado pelo banco)
MODEL_PATH = str(MODELS_DIR / 'pose_landmarker_full.task')

# Vídeo padrão (pode ser trocado pela linha de comando: python main.py outro.mp4 ou python main.py 0 para webcam)
VIDEO_PATH = str(VIDEOS_DIR / 'uber2.mp4')

# Confiança mínima do MediaPipe (valores baixos aceitam esqueletos "fantasma")
MIN_DETECTION_CONFIDENCE = 0.5
MIN_PRESENCE_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Visibilidade mínima de um ponto da mão (pulso ou indicador) para ele contar
MIN_VISIBILITY = 0.5

# Máximo de pessoas procuradas no frame
MAX_POSES = 3

# Zonas dos bancos: retângulos (x1, y1, x2, y2) em coordenadas normalizadas (0 a 1).
# Cada câmera/vídeo precisa das suas zonas. Gere com: python calibrate.py <video>
# Valores abaixo: aproximados para uber.mp4 (câmera no para-brisa olhando para trás).
ZONES = {
    'motorista': (0.41, 0.24, 0.87, 0.86),
    'passageiro_frente': (0.0, 0.29, 0.41, 1.0),
}

# Procurar de novo, no recorte de cada zona vazia, por pessoas pequenas (ex.: banco de trás).
# Melhora muito a detecção de quem está longe, mas cada zona vazia custa uma detecção a mais por frame.
# Veja zone_crop.py para a explicação completa.
USE_ZONE_CROP = True

# Quanto tempo (segundos) uma mão precisa ficar na zona de outra pessoa para virar alerta
INVASION_SECONDS = 1.5
