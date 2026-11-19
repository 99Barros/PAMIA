# Design de Testes Funcionais, IHC e Usabilidade — Módulo B

**Projeto:** PAMIA — Prevenção ao Assédio contra Mulheres com Inteligência Artificial  
**Disciplina:** Qualidade de Software — PFC

## 1. Classes de Equivalência e Análise de Valor-Limite (AVL)

### 1.1 Rotina 1 — Sanitização do Score (0 a 100)

A função `sanitizar_score()` restringe a pontuação ao intervalo de 0 a 100. Ela não aciona alertas; a decisão multimodal é avaliada separadamente.

| Classe | Condição | Resultado esperado |
|---|---|---|
| CE1 — Válida | 0 ≤ Score ≤ 100 | Preservar valor |
| CE2 — Fora da faixa | Score < 0 | Retornar 0 |
| CE3 — Fora da faixa | Score > 100 | Retornar 100 |
| CE4 — Inválida | NaN, +Inf ou -Inf | Lançar `ValueError` |

**Valores-limite testados:**

| Entrada | Resultado esperado |
|---:|---:|
| -0,1 | 0 |
| 0 | 0 |
| 0,1 | 0,1 |
| 69,9 | 69,9 |
| 70 | 70 |
| 100 | 100 |
| 100,1 | 100 |
| NaN / ±Inf | `ValueError` |

Os valores 69,9 e 70 verificam preservação numérica; não comprovam acionamento de alerta ao atingir 70.

### 1.2 Rotina 2 — Distância Euclidiana e Invasão Espacial

A função `avaliar_invasao_espacial()` classifica a distância entre pontos com base em um limiar experimental de 35 unidades, tratado no protótipo como centímetros.

\[
d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}
\]

| Classe | Condição | Resultado esperado |
|---|---|---|
| CE1 — Válida | d > 35 | `SEM_INVASAO` |
| CE2 — Válida | 0 ≤ d ≤ 35 | `TRIGGER_ESPACIAL` |
| CE3 — Inválida | d < 0 | `DISTANCIA_INVALIDA` |
| CE4 — Inválida | NaN ou Inf | `ENTRADA_INVALIDA` |

**Valores-limite testados:**

| Entrada | Resultado esperado |
|---:|---|
| -0,1 | DISTANCIA_INVALIDA |
| 0 / 0,1 | TRIGGER_ESPACIAL |
| 34,9 / 35 | TRIGGER_ESPACIAL |
| 35,1 | SEM_INVASAO |
| NaN / Inf | ENTRADA_INVALIDA |

Foram também testados limites configuráveis inválidos, incluindo `NaN`, infinito e valores negativos.

**Limitação:** o cálculo geométrico é válido para coordenadas no mesmo referencial. A correspondência do limiar com 35 centímetros físicos depende de calibração e não foi demonstrada nesta suíte.

## 2. Tabela de Decisão — Fusão Multimodal

A função `avaliar_threshold_multimodal()` considera os triggers de vídeo e áudio e o indicador de decaimento temporal.

| Regra | Vídeo | Áudio | Decaimento | Ação esperada |
|---|---|---|---|---|
| TD-01 | F | F | F | MANTER_ESTADO |
| TD-02 | F | V | F | ACUMULAR_RISCO |
| TD-03 | V | F | F | ACUMULAR_RISCO |
| TD-04 | V | V | F | ACIONAR_ALERTA_LOCAL |
| TD-05 | F | F | V | MANTER_ESTADO |
| TD-06 | F | V | V | MANTER_ESTADO |
| TD-07 | V | F | V | MANTER_ESTADO |
| TD-08 | V | V | V | MANTER_ESTADO |

As oito combinações foram validadas por testes parametrizados do Pytest.

A implementação atual estabelece prioridade para `time_decay=True`, retornando `MANTER_ESTADO`. Não realiza cálculo numérico de acúmulo, redução temporal ou comparação do score com 70.

## 3. Análise Crítica de IHC e Usabilidade

Foi realizada uma inspeção estática das telas de login, cadastro e menu do aplicativo demonstrativo PAMIA, desenvolvido em React Native. A avaliação considerou affordance, comunicabilidade, visibilidade do estado do sistema e prevenção de erros, com base nas heurísticas de Nielsen.

| Critério | Observação | Proposta de melhoria |
|---|---|---|
| Affordance falsa | Cartões do menu possuem aparência interativa, mas não executam ações | Implementar navegação demonstrativa ou indicar opções indisponíveis |
| Comunicabilidade | Login e cadastro simulam operações sem informar explicitamente essa condição | Identificar as telas como demonstração, sem autenticação ou persistência real |
| Prevenção de erros | Validação de e-mail exige `.com`, rejeitando domínios legítimos | Utilizar validação de formato mais abrangente |
| Visibilidade do estado | Não há confirmação explícita de que o cadastro é apenas simulado | Apresentar mensagem informativa antes de retornar à tela anterior |

**Delimitação do protótipo:** não serão implementados backend de autenticação, banco de dados de usuários ou persistência de cadastro nesta etapa. Essas funcionalidades são simuladas exclusivamente para demonstrar o fluxo de navegação.

A inspeção identificou oportunidades de melhoria relacionadas à clareza das interações e à prevenção de erros. As observações foram fundamentadas no código-fonte React Native, não em testes presenciais com usuários.

## 4. Casos de Teste Formais

| ID | Cenário e pré-condição | Procedimento | Resultado esperado |
|---|---|---|---|
| CT-01 | Vídeo e áudio ativos, decaimento falso | Executar `avaliar_threshold_multimodal(True, True, False)` | ACIONAR_ALERTA_LOCAL |
| CT-02 | Decaimento ativo | Executar a função com vídeo e áudio ativos e `time_decay=True` | MANTER_ESTADO |
| CT-03 | Score negativo | Executar `sanitizar_score(-5)` | 0 |
| CT-04 | Score NaN | Executar `sanitizar_score(NaN)` | `ValueError` |
| CT-05 | Distância de 35 | Executar `avaliar_invasao_espacial(35)` | TRIGGER_ESPACIAL |
| CT-06 | Distância de 35,1 | Executar `avaliar_invasao_espacial(35.1)` | SEM_INVASAO |
| CT-07 | Limite espacial inválido | Executar com limite `NaN`, infinito ou negativo | Não retornar classificação espacial normal |
| CT-08 | Coordenada 3D inválida | Executar cálculo com uma coordenada NaN | `ValueError` |
| CT-09 | Todas as condições booleanas | Executar os oito cenários parametrizados | Resultados conforme tabela de decisão |

**Ambiente:** Linux, Python 3.13.3, Pytest 9.2.0.

**Resultado da suíte:** 32 testes aprovados e 100% de cobertura das instruções e branches instrumentados nos módulos auxiliares `geometria.py` e `threshold.py`.

Os casos acima representam uma seleção formal dos cenários automatizados. A avaliação da interface e a integração com os modelos reais permanecem pendentes de evidências específicas.

## 5. Conclusão

As técnicas de classes de equivalência, valores-limite e tabela de decisão permitiram validar comportamentos definidos e identificar problemas de tratamento de entradas inválidas, posteriormente corrigidos.

Os resultados demonstram conformidade dos componentes auxiliares com os casos testados, sem representar validação integral do SDK móvel, da inferência acústica e visual ou da experiência de uso.

## Referências

- ISO/IEC/IEEE 29119 — *Software Testing*.
- PRESSMAN, R.; MAXIM, B. *Engenharia de Software: Uma Abordagem Profissional*. 9. ed., 2021.
- NIELSEN, J. *10 Usability Heuristics for User Interface Design*. Nielsen Norman Group.