# Relatório Final de Qualidade — Módulo C

**Projeto:** PAMIA — Prevenção ao Assédio contra Mulheres com Inteligência Artificial  
**Disciplina:** Qualidade de Software — PFC  
**Ambiente:** Linux, Python 3.13.3, Pytest 9.2.0 e pytest-cov 7.1.0  
**Data das evidências iniciais:** 18/11/2026

## 1. Automação e Execução

A validação foi realizada com Pytest, utilizando testes parametrizados (`@pytest.mark.parametrize`), análise de valores-limite, classes de equivalência, tabela de decisão, mocks, testes exploratórios e microbenchmark.

Execução a partir do diretório `qa/`:

```bash
python -m pytest tests/ -v \
  --cov=pamia_sdk \
  --cov-branch \
  --cov-report=term-missing \
  --junitxml=resultado-testes.xml
```

### Resultados da última execução informada

| Métrica | Resultado |
|---|---:|
| Testes executados | 32 |
| Testes aprovados | 32 |
| Testes reprovados | 0 |
| Taxa de aprovação | 100% |
| Instruções cobertas | 39/39 |
| Branches cobertos | 26/26 |
| Cobertura dos módulos auxiliares | 100% |

A cobertura compreende exclusivamente os arquivos `qa/pamia_sdk/geometria.py` e `qa/pamia_sdk/threshold.py`. Não representa a cobertura total do aplicativo PAMIA.

A suíte evoluiu de 23 para 29 e, posteriormente, 32 testes, incluindo verificações adicionais de entradas inválidas e cenários de decisão multimodal.

## 2. Matriz de Rastreabilidade

| Requisito | Casos — Módulo B | Testes automatizados | Situação |
|---|---|---|---|
| RF01 — Detecção espacial | CT-05, CT-06, CT-07, CT-08 | `test_avl_invasao_espacial`, `test_calculo_distancia_e_inferencia_mockada`, `test_calculo_distancia_rejeita_nan` e testes adicionais de validação | Auxiliar aprovado |
| RF02 — Detecção acústica | CT-01, CT-09 | `test_threshold_multimodal` com sinal acústico simulado | Parcial |
| RF03 — Decisão multimodal | CT-01 a CT-04, CT-09 | `test_threshold_multimodal`, `test_avl_sanitizacao_score` e validações adicionais | Auxiliar aprovado |
| RNF01 — Desempenho local | Teste de desempenho | `test_desempenho_local_50_ciclos` | Parcial |

Os cenários acústicos avaliam o tratamento de um sinal booleano simulado, não a classificação real de áudio. Os testes de geometria e decisão também não demonstram integração completa com os componentes de produção.

## 3. Registro de Defeitos e Regressão

| ID | Severidade estimada | Problema identificado | Correção / Verificação |
|---|---|---|---|
| BUG-01 | Alta | Coordenadas não finitas poderiam comprometer o cálculo geométrico auxiliar | Validação de `NaN` e infinito, com rejeição por `ValueError` |
| BUG-02 | Média | Ausência de tratamento consistente de valores fora da faixa de pontuação | Sanitização para o intervalo de 0 a 100 |
| BUG-03 | Média | Parâmetros espaciais inválidos poderiam produzir classificações inadequadas | Validação de limites negativos, `NaN` e infinito |

As correções foram submetidas a testes de regressão. A última execução informada apresentou 32 casos aprovados, sem falhas.

Os defeitos se referem aos módulos auxiliares de QA. Não há evidência de que essas ocorrências tenham sido reproduzidas durante inferência real de MediaPipe ou YAMNet.

## 4. Teste de Desempenho

Foi executado um microbenchmark das funções auxiliares de geometria e decisão multimodal, com cinco execuções independentes de 50 ciclos cada.

| Execução | Ciclos corretos | Tempo médio por ciclo |
|---|---:|---:|
| 1 | 50/50 | 0,0077 ms |
| 2 | 50/50 | 0,0077 ms |
| 3 | 50/50 | 0,0076 ms |
| 4 | 50/50 | 0,0059 ms |
| 5 | 50/50 | 0,0099 ms |
| **Total / Média** | **250/250** | **0,00776 ms** |

**Taxa de erros funcionais observados:** 0%.

Os valores representam o tempo médio do processamento lógico medido pelo experimento, sem incluir captura de câmera, microfone, inferência de modelos ou latência completa do SDK.

## 5. Avaliação de Qualidade e Limitações

A automação apresentou resultados satisfatórios no escopo avaliado, com aprovação dos casos funcionais e cobertura integral dos módulos auxiliares instrumentados.

Entretanto, permanecem limitações relevantes:

- RF02: ausência de execução real dos classificadores acústicos.
- RF03: lógica booleana simplificada, sem acumulação numérica ou decaimento temporal contínuo.
- RNF01: ausência de medições de consumo energético e desempenho em smartphone Android.
- IHC: avaliação realizada por inspeção estática do aplicativo demonstrativo, sem teste presencial com usuários.
- Integração: módulos auxiliares ainda não comprovadamente integrados ao fluxo completo de produção.

## 6. Conclusão

Os testes automatizados do PAMIA demonstraram comportamento consistente dos módulos auxiliares de geometria, sanitização e decisão multimodal, incluindo tratamento de entradas inválidas e verificação de cenários parametrizados.

O processo permitiu identificar problemas, aplicar correções e verificar regressões. Os resultados constituem evidências de qualidade do escopo testado, não uma certificação da aplicação completa.

O protótipo permanece sujeito a futuras avaliações de integração audiovisual, desempenho em dispositivo Android e usabilidade com usuários.