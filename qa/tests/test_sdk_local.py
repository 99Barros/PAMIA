"""
test_sdk_local.py — Suíte principal de testes unitários do SDK PAMIA (Módulo C).

Cobre:
  - Tabela de Decisão Multimodal (Módulo B — Tabela de Decisão)
  - AVL do Score Acumulado / Rotina 1 (Módulo B — CE/AVL Threshold)
  - AVL da Distância Euclidiana / Rotina 2 (Módulo B — CE/AVL Invasão Espacial)
  - Cálculo 3D com Mock do extrator de pose (MediaPipe)
  - Rejeição de coordenadas NaN (BUG-01 corrigido)

Executar:
    pytest --cov=pamia_sdk --cov-report=term-missing -v
"""

import math
from unittest.mock import Mock

import pytest

from pamia_sdk.geometria import (
    avaliar_invasao_espacial,
    calcular_distancia_euclidiana,
)
from pamia_sdk.threshold import (
    avaliar_threshold_multimodal,
    sanitizar_score,
)


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def limite_zona_passageiro() -> tuple[float, float, float]:
    """Coordenada de referência (origem) da área virtual do passageiro em cm."""
    return (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Tabela de Decisão Multimodal (CT-01 / CT-02 / CT-03)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "video, audio, decay, esperado",
    [
        (False, False, False, "MANTER_ESTADO"),
        (False, True,  False, "ACUMULAR_RISCO"),
        (True,  False, False, "ACUMULAR_RISCO"),
        (True,  True,  False, "ACIONAR_ALERTA_LOCAL"),

        (False, False, True, "MANTER_ESTADO"),
        (False, True,  True, "MANTER_ESTADO"),
        (True,  False, True, "MANTER_ESTADO"),
        (True,  True,  True, "MANTER_ESTADO"),
    ],
)
def test_threshold_multimodal(video, audio, decay, esperado):
    assert avaliar_threshold_multimodal(
        video, audio, decay
    ) == esperado



# ---------------------------------------------------------------------------
# Rotina 1: AVL do Score Acumulado — CE/AVL Threshold (0 a 100)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "score_entrada, esperado",
    [
        # CE3 (Inválida) — abaixo de 0: sanitizar para piso 0.0
        (-0.1,  0.0),
        # Valor-Limite inferior: exatamente 0.0 → válido
        (0.0,   0.0),
        # CE1 (Válida) — logo acima do piso
        (0.1,   0.1),
        # CE1 (Válida) — abaixo do limiar crítico
        (69.9,  69.9),
        # Valor-Limite do alerta: exatamente 70.0 → válido
        (70.0,  70.0),
        # CE2 (Válida) — teto máximo
        (100.0, 100.0),
        # CE4 (Inválida) — acima de 100: sanitizar para teto 100.0
        (100.1, 100.0),
    ],
)
def test_avl_sanitizacao_score(score_entrada: float, esperado: float):
    """Valida limites inferior e superior do score acumulado (Rotina 1 — AVL)."""
    assert sanitizar_score(score_entrada) == pytest.approx(esperado)


# ---------------------------------------------------------------------------
# Rotina 2: AVL da Distância Euclidiana / Invasão Espacial
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "distancia, esperado",
    [
        # CE3 (Inválida) — distância negativa: fisicamente impossível
        (-0.1,          "DISTANCIA_INVALIDA"),
        # Valor-Limite inferior: exatamente 0.0 → zona crítica
        (0.0,           "TRIGGER_ESPACIAL"),
        # CE2 (Válida) — logo acima de 0
        (0.1,           "TRIGGER_ESPACIAL"),
        # CE2 (Válida) — abaixo do limite de 35 cm
        (34.9,          "TRIGGER_ESPACIAL"),
        # Valor-Limite superior da zona crítica: exatamente 35.0 → ainda crítico
        (35.0,          "TRIGGER_ESPACIAL"),
        # CE1 (Válida) — fora da zona de invasão
        (35.1,          "SEM_INVASAO"),
        # CE4 (Inválida) — NaN (keypoint ocluído pelo MediaPipe — BUG-01)
        (float("nan"),  "ENTRADA_INVALIDA"),
        # CE4 (Inválida) — Inf (overflow de cálculo)
        (float("inf"),  "ENTRADA_INVALIDA"),
    ],
)
def test_avl_invasao_espacial(distancia: float, esperado: str):
    """Valida valores-limite e entradas inválidas da rotina de invasão espacial (Rotina 2 — AVL)."""
    assert avaliar_invasao_espacial(distancia) == esperado


# ---------------------------------------------------------------------------
# Integração: Cálculo 3D + Classificação com Mock do extrator de pose
# ---------------------------------------------------------------------------

def test_calculo_distancia_e_inferencia_mockada(limite_zona_passageiro):
    """
Valida o cálculo geométrico e a classificação de invasão.

Utiliza unittest.mock.Mock para simular coordenadas
produzidas por um extrator de pose.

O teste não executa o MediaPipe e não valida sua
integração com a aplicação móvel.
    """
    extrator_pose_mock = Mock(return_value=(20.0, 0.0, 0.0))
    keypoint_mao = extrator_pose_mock()

    distancia = calcular_distancia_euclidiana(keypoint_mao, limite_zona_passageiro)

    assert distancia == pytest.approx(20.0)
    assert avaliar_invasao_espacial(distancia) == "TRIGGER_ESPACIAL"
    extrator_pose_mock.assert_called_once()


def test_calculo_distancia_rejeita_nan(limite_zona_passageiro):
    """
    Garante que coordenadas NaN (quadro ocluído do MediaPipe) disparem ValueError controlado.

    Correção do BUG-01: validação explícita com math.isnan/math.isinf descarta o quadro
    sem propagar erro matemático não tratado na thread de fundo.
    """
    with pytest.raises(ValueError, match="Coordenada inválida"):
        calcular_distancia_euclidiana((math.nan, 0.0, 0.0), limite_zona_passageiro)
