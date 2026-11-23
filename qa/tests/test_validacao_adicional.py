
import pytest

from pamia_sdk.geometria import avaliar_invasao_espacial
from pamia_sdk.threshold import sanitizar_score


@pytest.mark.parametrize("score", [
    float("nan"),
    float("inf"),
    float("-inf"),
])
def test_score_invalido_rejeitado(score):
    with pytest.raises(ValueError):
        sanitizar_score(score)


@pytest.mark.parametrize("limite", [
    float("nan"),
    float("inf"),
    -1.0,
])
def test_limite_invalido_nao_deve_produzir_classificacao_normal(limite):
    resultado = avaliar_invasao_espacial(20.0, limite)

    assert resultado not in (
        "TRIGGER_ESPACIAL",
        "SEM_INVASAO"
    )
