import math

"""
threshold.py — Sanitização de score e lógica de fusão multimodal (Edge Computing).

Módulo local do SDK PAMIA:
- sanitizar_score(): garante que o acumulador de risco permaneça em [0.0, 100.0].
- avaliar_threshold_multimodal(): implementa a Tabela de Decisão do Módulo B.
"""


def sanitizar_score(score: float) -> float:
    if not math.isfinite(score):
        raise ValueError("Score inválido: NaN ou infinito.")

    if score < 0.0:
        return 0.0

    if score > 100.0:
        return 100.0

    return score


def avaliar_threshold_multimodal(
    video_trigger: bool,
    audio_trigger: bool,
    time_decay: bool,
) -> str:
    """
    Lógica de acionamento 100% local baseada em fusão multimodal (Tabela de Decisão — Módulo B).

    Regras:
        Regra 1: time_decay=True (qualquer entrada)   → MANTER_ESTADO
        Regra 2: vídeo=True,  áudio=False, decay=False → ACUMULAR_RISCO
        Regra 3: vídeo=False, áudio=True,  decay=False → ACUMULAR_RISCO
        Regra 4: vídeo=True,  áudio=True,  decay=False → ACIONAR_ALERTA_LOCAL
        (default)                                       → MANTER_ESTADO

    Args:
        video_trigger: True se o módulo de vídeo (MediaPipe) detectou invasão espacial.
        audio_trigger: True se o módulo de áudio (YAMNet/DSP) detectou padrão de pânico.
        time_decay:    True se o decaimento temporal está ativo (reduzindo o score acumulado).

    Returns:
        String com a ação do sistema.
    """
    if time_decay:
        return "MANTER_ESTADO"
    if video_trigger and audio_trigger:
        return "ACIONAR_ALERTA_LOCAL"
    if video_trigger or audio_trigger:
        return "ACUMULAR_RISCO"
    return "MANTER_ESTADO"
