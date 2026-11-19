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


### Validação de entradas e testes de regressão

Durante a etapa de testes exploratórios, foram identificadas inconsistências no tratamento de entradas inválidas nos componentes de geometria e sanitização da pontuação de risco. As falhas envolveram a propagação de valores não numéricos (`NaN`) e a utilização de parâmetros de limite espacial inválidos.

Após a identificação desses comportamentos, foram implementadas validações adicionais nas funções `sanitizar_score()` e `avaliar_invasao_espacial()`, acompanhadas da ampliação da suíte automatizada.

Na execução de regressão, realizada em ambiente Linux com Python 3.13.3, Pytest 9.2.0 e pytest-cov 7.1.0, foram executados 29 casos de teste, todos aprovados, sem falhas ou erros. A execução teve duração de 0,31 segundo.

A análise de cobertura, considerando os módulos `qa/pamia_sdk/geometria.py` e `qa/pamia_sdk/threshold.py`, apresentou 100% de cobertura das 39 instruções e dos 26 branches instrumentados, sem instruções não executadas ou branches parcialmente cobertos.

Os resultados demonstram a correção dos comportamentos identificados no escopo testado e a manutenção da compatibilidade com os casos de teste anteriores. Ressalta-se que a cobertura apresentada se restringe aos módulos auxiliares de QA, não representando a cobertura integral dos componentes de áudio, vídeo ou da aplicação móvel do PAMIA.

### Avaliação de repetibilidade do processamento local

Com o objetivo de avaliar a repetibilidade do processamento das funções auxiliares do PAMIA, foram realizadas cinco execuções independentes de um microbenchmark desenvolvido em Python e integrado à suíte Pytest.

Cada execução compreendeu 50 ciclos de processamento, totalizando 250 ciclos avaliados. Todos os ciclos produziram os resultados funcionais esperados, correspondendo a uma taxa de sucesso de 100%.

Os tempos médios por ciclo registrados nas cinco execuções foram, respectivamente, 0,0077 ms, 0,0077 ms, 0,0076 ms, 0,0059 ms e 0,0099 ms. A média das cinco medições foi de 0,00776 ms, com mediana de 0,0077 ms.

O experimento foi executado em ambiente Linux, utilizando processador AMD Ryzen 5 7535HS e Python 3.13.3.

**Limitações:** o experimento contempla exclusivamente funções auxiliares de geometria e decisão multimodal. Não foram executadas inferências reais dos modelos MediaPipe e YAMNet, nem realizadas medições de consumo energético, temperatura ou desempenho em dispositivos Android. Dessa maneira, os resultados não comprovam integralmente o atendimento ao requisito RNF01, constituindo evidência parcial de desempenho do processamento lógico local.