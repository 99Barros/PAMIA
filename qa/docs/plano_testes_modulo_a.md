# Plano de Testes — Módulo A (ISO/IEC 29119)
# Projeto: PAMIA — Prevenção ao Assédio contra Mulheres com Inteligência Artificial
# Disciplina: Qualidade de Software (PFC)

---

## 1. Identificação

| Campo | Valor |
|---|---|
| **Projeto** | PAMIA SDK Mobile (Android / React Native) |
| **Versão** | MVP — Entrega Única Final |
| **Equipe** | 4 integrantes (2 técnicos Dev/QA + 2 documentação) |
| **Padrão** | ISO/IEC 29119 |

---

## 2. Escopo

### 2.1 Itens Testados

| Módulo | Descrição |
|---|---|
| **Vídeo (MediaPipe/OpenCV)** | Extração de keypoints e cálculo de distância euclidiana 3D para detecção de invasão espacial |
| **Áudio (DSP/YAMNet TFLite)** | Pré-filtragem DSP e classificação acústica local para detecção de padrões de pânico |
| **Lógica de Integração** | Fusão multimodal, threshold probabilístico e decaimento temporal (*time decay*) local |

### 2.2 Itens **Não** Testados (Fora do Escopo)

- Servidor B2B de destino das centrais de monitoramento
- Disparo de webhooks externos / HTTPS para terceiros
- Infraestrutura de nuvem das empresas de transporte parceiras
- Detecção do sinal universal de socorro

---

## 3. Estratégia de Teste

- Testes **unitários e de integração** automatizados em Python (`pytest`).
- Técnicas de **caixa-preta**: Particionamento em Classes de Equivalência e Análise de Valor-Limite (AVL) em 2 rotinas do SDK.
- **Tabela de Decisão** para a fusão multimodal (vídeo + áudio + decaimento temporal).
- **Mocks** (`unittest.mock`) para isolar extratores de pose (MediaPipe) e classificadores acústicos (YAMNet) sem dependência de hardware.
- **Simulação de carga concorrente** (50 threads) para validar o desempenho do processamento local de borda.

---

## 4. Ambiente de Teste

| Item | Requisito |
|---|---|
| **Linguagem** | Python 3.11+ |
| **Framework de Testes** | `pytest` + `pytest-cov` |
| **Dependências** | `math`, `unittest.mock`, `concurrent.futures` (stdlib) |
| **Instalação** | `pip install pytest pytest-cov` |

---

## 5. Critérios de Entrada

- Código-fonte do SDK estruturado nos módulos `pamia_sdk/geometria.py` e `pamia_sdk/threshold.py`.
- Ambiente Python configurado com `pytest` e `pytest-cov` instalados.
- Suíte de testes presente em `tests/test_sdk_local.py` e `tests/test_desempenho_local.py`.

---

## 6. Critérios de Saída

- 100% dos casos de teste críticos (*Must Have*) executados e aprovados.
- Relatório de cobertura gerado via `pytest --cov=pamia_sdk --cov-report=term-missing -v`.
- Defeitos críticos (severidade **Alta**) corrigidos e fechados antes da entrega.

---

## 7. Análise de Pontos de Função (APF) — Escopo Local

| Componente / Função | Tipo | Complexidade | PFB |
|:---|:---:|:---:|:---:|
| Módulo de Vídeo (MediaPipe/OpenCV) | Entrada Externa (EI) | Média | 4 |
| Módulo de Áudio (DSP/YAMNet) | Entrada Externa (EI) | Média | 4 |
| Lógica de Threshold (Fusão Multimodal) | Consulta Externa (EQ) | Simples | 3 |
| Acionamento de Alerta Local (Callback SDK) | Saída Externa (EO) | Simples | 4 |
| Configurações e Limiares do SDK | Arquivo Lógico Interno (ALI) | Simples | 7 |
| Estado de Risco e Log Local | Arquivo Lógico Interno (ALI) | Simples | 7 |
| Modelos Pré-Treinados (MediaPipe / YAMNet) | Arquivo de Interface Externa (AIE) | Simples | 5 |
| **Total de Pontos de Função Brutos (PFB)** | | | **34** |

> **ALI** — Dados mantidos internamente pelo SDK/aplicação local.  
> **AIE** — Referências/modelos externos consumidos em memória/disco apenas para leitura durante a inferência.

---

## 8. Modelo COCOMO II — Estimativa de Esforço

### 8.1 Parâmetros de Entrada

| Parâmetro | Valor |
|---|---|
| **Tamanho (SLOC)** | ≈ 2.500 linhas (Python / TypeScript / Java nativo integrado) → KSLOC = 2.5 |
| **Modo** | Semi-Detached (equipe mista com experiência intermediária/avançada) |
| **Coeficientes** | A = 2.94 · B = 1.09 · C = 3.67 · D = 0.28 |

### 8.2 Memória de Cálculo

**Esforço Nominal (PM):**

$$PM = A \times (KSLOC)^B = 2{,}94 \times (2{,}5)^{1{,}09} \approx 8{,}1 \text{ Pessoas-Mês}$$

**Prazo de Desenvolvimento (TDEV):**

$$TDEV = C \times (PM)^D = 3{,}67 \times (8{,}1)^{0{,}28} \approx 4{,}8 \text{ meses}$$

**Dimensionamento médio:**

$$\text{Equipe} = \frac{PM}{TDEV} = \frac{8{,}1}{4{,}8} \approx 1{,}7 \text{ pessoas ativas}$$

### 8.3 Alocação dos 4 Integrantes

| Métrica / Recurso | Valor Calculado | Alocação Real |
|---|---|---|
| Esforço Total | 8,1 Pessoas-Mês | Distribuído entre desenvolvimento e testes |
| Prazo Estimado | 4,8 Meses | Alinhado ao cronograma do PFC |
| Equipe Técnica (Dev/QA) | ~1,7 FTE | **2 integrantes** (código, IA, automação) |
| Equipe de Apoio | — | **2 integrantes** (documentação e relatórios) |

> A divisão 2 técnicos + 2 documentação valida o dimensionamento: os 2 integrantes de documentação
> absorvem a carga textual sem onerar os multiplicadores de esforço da engenharia, ajustando
> positivamente os EM de PCAP e PLEX.
