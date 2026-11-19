"""
test_desempenho_local.py — Teste de desempenho concorrente do processamento local (Módulo C).

Valida a resiliência e a vazão do ciclo completo de inferência local do SDK PAMIA
(geometria euclidiana + fusão multimodal) executado em threads concorrentes,
simulando a carga de borda (Edge Computing) no dispositivo do motorista.

Executar diretamente:
    python tests/test_desempenho_local.py

Ou como teste pytest (sem assert de valor — apenas valida ausência de erros):
    pytest tests/test_desempenho_local.py -v
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from pamia_sdk.geometria import avaliar_invasao_espacial, calcular_distancia_euclidiana
from pamia_sdk.threshold import avaliar_threshold_multimodal

# ---------------------------------------------------------------------------
# Simulação do ciclo de inferência local
# ---------------------------------------------------------------------------

def simular_ciclo_inferencia_local() -> tuple[bool, float]:
    """
    Executa um ciclo completo de avaliação local (geometria 3D + threshold multimodal).

    Cenário fixo:
        - Motorista em (15.0, 10.0, 5.0) → distância ≈ 18.7 cm (< 35 cm → TRIGGER_ESPACIAL)
        - Áudio: trigger ativo
        - Resultado esperado: ACIONAR_ALERTA_LOCAL

    Returns:
        Tupla (sucesso: bool, duração_em_segundos: float).
    """
    inicio = time.perf_counter()

    dist = calcular_distancia_euclidiana((15.0, 10.0, 5.0), (0.0, 0.0, 0.0))
    video_trig = avaliar_invasao_espacial(dist) == "TRIGGER_ESPACIAL"
    status = avaliar_threshold_multimodal(video_trig, True, False)

    duracao = time.perf_counter() - inicio
    return status == "ACIONAR_ALERTA_LOCAL", duracao


# ---------------------------------------------------------------------------
# Executor de carga
# ---------------------------------------------------------------------------

def executar_teste_desempenho_local(concorrencia: int = 50) -> dict:
    """
    Executa N ciclos concorrentes e coleta métricas de desempenho.

    Args:
        concorrencia: Número de ciclos paralelos (threads) a executar.

    Returns:
        Dicionário com métricas: total, sucessos, tempo_medio_ms.
    """
    sucessos = 0
    tempos: list[float] = []

    with ThreadPoolExecutor(max_workers=concorrencia) as executor:
        futuros = [
            executor.submit(simular_ciclo_inferencia_local)
            for _ in range(concorrencia)
        ]
        for futuro in as_completed(futuros):
            ok, duracao = futuro.result()
            if ok:
                sucessos += 1
            tempos.append(duracao)

    tempo_medio_ms = (sum(tempos) / len(tempos)) * 1000

    print(
        f"\nProcessamento Local | Ciclos: {concorrencia} | "
        f"Sucessos: {sucessos} | Tempo médio: {tempo_medio_ms:.4f} ms"
    )

    return {
        "total": concorrencia,
        "sucessos": sucessos,
        "tempo_medio_ms": tempo_medio_ms,
    }


# ---------------------------------------------------------------------------
# Teste pytest: valida ausência de falhas e tempo médio razoável
# ---------------------------------------------------------------------------

def test_desempenho_local_50_ciclos():
    """
    Valida que 50 ciclos concorrentes de inferência local completam sem falhas
    e dentro de um tempo médio aceitável para Edge Computing (< 50 ms por ciclo).

    Rastreabilidade: RNF01 (Desempenho Local / Borda)
    """
    resultado = executar_teste_desempenho_local(concorrencia=50)

    assert resultado["sucessos"] == resultado["total"], (
        f"Esperado 100% de sucesso, obtido {resultado['sucessos']}/{resultado['total']}"
    )
    assert resultado["tempo_medio_ms"] < 50.0, (
        f"Tempo médio por ciclo ({resultado['tempo_medio_ms']:.4f} ms) excedeu 50 ms"
    )


# ---------------------------------------------------------------------------
# Execução direta
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    executar_teste_desempenho_local()
