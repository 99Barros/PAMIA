"""
geometria.py — Cálculo de distância euclidiana 3D e classificação de invasão espacial.

Módulo local (Edge Computing) do SDK PAMIA:
- Calcula a distância 3D entre keypoint do motorista e o limite virtual da área do passageiro.
- Classifica o resultado conforme classes de equivalência definidas no Módulo B.
"""

import math


def calcular_distancia_euclidiana(
    ponto_a: tuple[float, float, float],
    ponto_b: tuple[float, float, float],
) -> float:
    """
    Calcula a distância euclidiana 3D entre dois keypoints (em cm).

    Args:
        ponto_a: Coordenadas (x, y, z) do keypoint do motorista.
        ponto_b: Coordenadas (x, y, z) do limite virtual da área do passageiro.

    Returns:
        Distância euclidiana em centímetros (float).

    Raises:
        ValueError: Se qualquer coordenada for NaN ou Inf (quadro inválido do MediaPipe).
    """
    for coord in (*ponto_a, *ponto_b):
        if math.isnan(coord) or math.isinf(coord):
            raise ValueError("Coordenada inválida (NaN ou Inf) — descartando quadro.")

    dx = ponto_b[0] - ponto_a[0]
    dy = ponto_b[1] - ponto_a[1]
    dz = ponto_b[2] - ponto_a[2]
    return math.sqrt(dx**2 + dy**2 + dz**2)


def avaliar_invasao_espacial(distancia_cm: float, limite_cm: float = 35.0) -> str:
    """
    Classifica a distância conforme classes de equivalência e análise de valor-limite (AVL).

    Classes de Equivalência:
        CE1 (Válida) — d > 35.0  → SEM_INVASAO
        CE2 (Válida) — 0.0 ≤ d ≤ 35.0 → TRIGGER_ESPACIAL
        CE3 (Inválida) — d < 0.0 → DISTANCIA_INVALIDA
        CE4 (Inválida) — NaN / Inf → ENTRADA_INVALIDA

    Args:
        distancia_cm: Distância calculada em centímetros.
        limite_cm: Limiar de invasão espacial (padrão = 35.0 cm).

    Returns:
        String com o estado classificado.
    """
    if math.isnan(distancia_cm) or math.isinf(distancia_cm):
        return "ENTRADA_INVALIDA"
    if distancia_cm < 0.0:
        return "DISTANCIA_INVALIDA"
    if distancia_cm <= limite_cm:
        return "TRIGGER_ESPACIAL"
    return "SEM_INVASAO"
