# Design de Testes Funcionais, IHC & Usabilidade — Módulo B
# Projeto: PAMIA — Prevenção ao Assédio contra Mulheres com Inteligência Artificial
# Disciplina: Qualidade de Software (PFC)

---

## 1. Rotina 1 — Threshold de Risco Acumulado (`Score` de 0 a 100)

### 1.1 Particionamento em Classes de Equivalência

| Classe | Faixa / Condição | Comportamento Esperado |
|:---|:---|:---|
| **CE1 (Válida)** | 0 ≤ Score ≤ 69 | Operação normal — nenhum alerta disparado |
| **CE2 (Válida)** | 70 ≤ Score ≤ 100 | Alerta crítico local acionado |
| **CE3 (Inválida)** | Score < 0 | Rejeitar/sanitizar para piso `0.0` (BUG-02 corrigido) |
| **CE4 (Inválida)** | Score > 100 | Rejeitar/sanitizar para teto `100.0` |

### 1.2 Análise de Valor-Limite (AVL)

| Valor de Teste | Classe | Resultado Esperado |
|---:|:---:|:---|
| `-0.1` | CE3 | Sanitizado → `0.0` |
| `0.0` | CE1 | `0.0` (piso válido) |
| `0.1` | CE1 | `0.1` |
| `69.9` | CE1 | `69.9` (abaixo do limiar crítico) |
| `70.0` | CE2 | `70.0` (limiar crítico) |
| `70.1` | CE2 | `70.1` |
| `99.9` | CE2 | `99.9` |
| `100.0` | CE2 | `100.0` (teto válido) |
| `100.1` | CE4 | Sanitizado → `100.0` |

---

## 2. Rotina 2 — Distância Euclidiana 3D / Invasão Espacial (`d` em cm)

Fórmula aplicada pelo módulo de vídeo (MediaPipe):

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}$$

### 2.1 Particionamento em Classes de Equivalência

| Classe | Faixa / Condição | Comportamento Esperado |
|:---|:---|:---|
| **CE1 (Válida)** | d > 35.0 cm | Fora da zona de invasão → `SEM_INVASAO` |
| **CE2 (Válida)** | 0.0 ≤ d ≤ 35.0 cm | Zona crítica → `TRIGGER_ESPACIAL` |
| **CE3 (Inválida)** | d < 0.0 | Distância fisicamente impossível → `DISTANCIA_INVALIDA` |
| **CE4 (Inválida)** | NaN ou Inf | Erro de inferência do MediaPipe → `ENTRADA_INVALIDA` (BUG-01 corrigido) |

### 2.2 Análise de Valor-Limite (AVL)

| Valor de Teste | Classe | Resultado Esperado |
|---:|:---:|:---|
| `-0.1` | CE3 | `DISTANCIA_INVALIDA` |
| `0.0` | CE2 | `TRIGGER_ESPACIAL` (piso da zona crítica) |
| `0.1` | CE2 | `TRIGGER_ESPACIAL` |
| `34.9` | CE2 | `TRIGGER_ESPACIAL` |
| `35.0` | CE2 | `TRIGGER_ESPACIAL` (limite superior da zona crítica, inclusivo) |
| `35.1` | CE1 | `SEM_INVASAO` |
| `float("nan")` | CE4 | `ENTRADA_INVALIDA` |
| `float("inf")` | CE4 | `ENTRADA_INVALIDA` |

---

## 3. Tabela de Decisão — Fusão Multimodal Local

| Condições / Regras | Regra 1 | Regra 2 | Regra 3 | Regra 4 |
|:---|:---:|:---:|:---:|:---:|
| Vídeo detecta invasão (`TRIGGER_ESPACIAL`) | F | V | F | V |
| Áudio detecta pânico/grito (≥ limiar YAMNet) | F | F | V | V |
| Decaimento temporal ativo (`time_decay`) | V | F | F | F |
| **Ação do Sistema** | `MANTER_ESTADO` | `ACUMULAR_RISCO` | `ACUMULAR_RISCO` | `ACIONAR_ALERTA_LOCAL` |

---

## 4. Análise de Usabilidade & IHC (App Simulador React Native)

| Critério | Avaliação |
|:---|:---|
| **Affordance e Visibilidade de Status** | Indicador discreto (ícone verde/vermelho) no rodapé da interface, sinalizando que o SDK está ativo e monitorando sem obstruir comandos de navegação. |
| **Comunicabilidade** | Em caso de revogação de permissão de câmera ou microfone no Android, a interface exibe aviso imediato e claro informando a indisponibilidade do monitoramento. |
| **Prevenção de Erros** | A exigência de convergência multimodal (vídeo + áudio) **e** ausência de decaimento temporal evita falsos positivos por ruídos isolados cotidianos. |

---

## 5. Casos de Teste Formais

| ID | Cenário | Pré-condições | Passos de Execução | Oráculo (Resultado Esperado) |
|:---|:---|:---|:---|:---|
| **CT-01** | Disparo por Limiar Crítico | SDK ativo localmente; `time_decay = False` | 1. Simular invasão espacial (d ≤ 35 cm → `video_trigger = True`). 2. Injetar trigger acústico (`audio_trigger = True`). | Retorna `ACIONAR_ALERTA_LOCAL`. |
| **CT-02** | Decaimento Temporal | Score parcial acumulado (`Score = 40`) | 1. Ativar flag `time_decay = True` sem novos estímulos de vídeo ou áudio. | Retorna `MANTER_ESTADO`; score não avança. |
| **CT-03** | Sanitização de Entradas Inválidas | Módulos instanciados | 1. Passar `Score = -5` → verificar sanitização. 2. Passar coordenada `NaN` → verificar rejeição. | Sistema sanitiza/rejeita sem lançar exceção não tratada. |
