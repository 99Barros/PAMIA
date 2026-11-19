# Relatório Final de Qualidade — Módulo C
# Projeto: PAMIA — Prevenção ao Assédio contra Mulheres com Inteligência Artificial
# Disciplina: Qualidade de Software (PFC)

---

> [!NOTE]
> Evidências reais geradas em **18/11/2026** — Python 3.13.3, pytest 9.2.0.
> **23/23 testes aprovados | Cobertura total: 100%.**

---

## 1. Comandos de Execução (Terminal do VS Code)

```bash
# 1. Instalar dependências (apenas na primeira vez)
pip install pytest pytest-cov

# 2. Executar suíte com cobertura — cole o output abaixo
pytest --cov=pamia_sdk --cov-report=term-missing -v

# 3. Executar teste de desempenho local — cole o output abaixo
python tests/test_desempenho_local.py
```

---

## 2. Resumo de Execução e Cobertura (`pytest --cov`)

```
=============================== test session starts ===============================
platform linux -- Python 3.13.3, pytest-9.2.0, pluggy-1.7.0 -- /home/joaobarros/Documentos/Repositorios/PAMIA/audio/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/joaobarros/Documentos/Repositorios/PAMIA/qa
plugins: platformdirs-4.12.4, cov-7.1.0
collected 23 items

tests/test_desempenho_local.py::test_desempenho_local_50_ciclos PASSED      [  4%]
tests/test_sdk_local.py::test_threshold_multimodal[False-False-True-MANTER_ESTADO] PASSED [  8%]
tests/test_sdk_local.py::test_threshold_multimodal[True-True-False-ACIONAR_ALERTA_LOCAL] PASSED [ 13%]
tests/test_sdk_local.py::test_threshold_multimodal[True-False-False-ACUMULAR_RISCO] PASSED [ 17%]
tests/test_sdk_local.py::test_threshold_multimodal[False-True-False-ACUMULAR_RISCO] PASSED [ 21%]
tests/test_sdk_local.py::test_threshold_multimodal[False-False-False-MANTER_ESTADO] PASSED [ 26%]
tests/test_sdk_local.py::test_avl_sanitizacao_score[-0.1-0.0] PASSED        [ 30%]
tests/test_sdk_local.py::test_avl_sanitizacao_score[0.0-0.0] PASSED         [ 34%]
tests/test_sdk_local.py::test_avl_sanitizacao_score[0.1-0.1] PASSED         [ 39%]
tests/test_sdk_local.py::test_avl_sanitizacao_score[69.9-69.9] PASSED       [ 43%]
tests/test_sdk_local.py::test_avl_sanitizacao_score[70.0-70.0] PASSED       [ 47%]
tests/test_sdk_local.py::test_avl_sanitizacao_score[100.0-100.0] PASSED     [ 52%]
tests/test_sdk_local.py::test_avl_sanitizacao_score[100.1-100.0] PASSED     [ 56%]
tests/test_sdk_local.py::test_avl_invasao_espacial[-0.1-DISTANCIA_INVALIDA] PASSED [ 60%]
tests/test_sdk_local.py::test_avl_invasao_espacial[0.0-TRIGGER_ESPACIAL] PASSED [ 65%]
tests/test_sdk_local.py::test_avl_invasao_espacial[0.1-TRIGGER_ESPACIAL] PASSED [ 69%]
tests/test_sdk_local.py::test_avl_invasao_espacial[34.9-TRIGGER_ESPACIAL] PASSED [ 73%]
tests/test_sdk_local.py::test_avl_invasao_espacial[35.0-TRIGGER_ESPACIAL] PASSED [ 78%]
tests/test_sdk_local.py::test_avl_invasao_espacial[35.1-SEM_INVASAO] PASSED [ 82%]
tests/test_sdk_local.py::test_avl_invasao_espacial[nan-ENTRADA_INVALIDA] PASSED [ 86%]
tests/test_sdk_local.py::test_avl_invasao_espacial[inf-ENTRADA_INVALIDA] PASSED [ 91%]
tests/test_sdk_local.py::test_calculo_distancia_e_inferencia_mockada PASSED [ 95%]
tests/test_sdk_local.py::test_calculo_distancia_rejeita_nan PASSED          [100%]

================================= tests coverage ==================================
_________________ coverage: platform linux, python 3.13.3-final-0 _________________

Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
pamia_sdk/__init__.py        0      0   100%
pamia_sdk/geometria.py      17      0   100%
pamia_sdk/threshold.py      14      0   100%
------------------------------------------------------
TOTAL                       31      0   100%
=============================== 23 passed in 0.30s ================================
```

---

## 3. Resultado do Teste de Desempenho Local

```
[ PREENCHER APÓS EXECUÇÃO — cole aqui o output do terminal ]

Exemplo do formato esperado:
Processamento Local | Ciclos: 50 | Sucessos: 50 | Tempo médio: X.XXXX ms
```

---

## 4. Matriz de Rastreabilidade

| Requisito (PFC) | Caso de Teste (Módulo B) | Função Pytest (Módulo C) | Status |
|:---|:---|:---|:---:|
| RF01 — Detecção Espacial / Vídeo | CT-01 / AVL Invasão Espacial | `test_avl_invasao_espacial`, `test_calculo_distancia_e_inferencia_mockada` | ✅ Aprovado |
| RF02 — Detecção Acústica / DSP | CT-01 (Fusão Áudio) | `test_threshold_multimodal` (cenários com `audio=True`) | ✅ Aprovado |
| RF03 — Threshold & Decaimento | CT-02, CT-03 | `test_threshold_multimodal`, `test_avl_sanitizacao_score` | ✅ Aprovado |
| RNF01 — Desempenho Local / Borda | Teste de Concorrência | `test_desempenho_local_50_ciclos` | ✅ Aprovado |

> Após executar os testes, atualize a coluna **Status** com `Aprovado` ou `Reprovado` e
> registre eventuais defeitos na seção abaixo.

---

## 5. Registro de Defeitos Identificados e Corrigidos

| ID | Severidade | Módulo | Descrição do Defeito | Correção Aplicada | Status |
|:---|:---:|:---|:---|:---|:---:|
| BUG-01 | Alta | `geometria.py` | Coordenadas `NaN` emitidas em quadros ocluídos do MediaPipe propagavam erro matemático não tratado na thread de fundo. | Validação explícita com `math.isnan` / `math.isinf` descarta o quadro inválido e levanta `ValueError` controlado. | ✅ Corrigido |
| BUG-02 | Média | `threshold.py` | Score negativo em transição rápida reduzia o acumulador abaixo de zero. | Implementação de `sanitizar_score()` aplicando piso `0.0` e teto `100.0`. | ✅ Corrigido |

> Adicione novos defeitos encontrados durante a execução real nesta tabela.
