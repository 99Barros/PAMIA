```markdown
# PAMIA - Prevenção ao Assédio contra Mulheres com IA 🚨

Módulo de Processamento Acústico e Multimodal projetado para identificar situações de risco, assédio e violência no interior de veículos de transporte por aplicativo. O sistema opera sob o paradigma de **Edge Computing** (100% offline), garantindo a privacidade dos usuários e mitigando problemas de latência ou falta de conectividade.

## 🧠 Arquitetura do Sistema

O motor de inferência combina duas abordagens de Inteligência Artificial processadas simultaneamente no mesmo bloco de áudio (16kHz, Mono):

1. **Contexto Acústico (YAMNet - TFLite):** Rede neural profunda quantizada que analisa as frequências sonoras em busca de padrões de emergência (gritos, choro, sirenes).
2. **Contexto Semântico (Vosk - NLP):** Motor de reconhecimento de fala offline que transcreve o áudio e busca por marcadores verbais de agressividade, assédio ou pedidos de socorro.
3. **Threshold Multimodal (Leaky Bucket):** Motor de risco temporal que soma os gatilhos acústicos e semânticos. Os pontos sofrem decaimento gradual ao longo do tempo, acionando o alarme apenas quando o limite configurado é ultrapassado, evitando falsos positivos causados por ruídos isolados do trânsito.

---

## 🛠️ Pré-requisitos e Instalação

### 1. Dependências do Sistema Operacional (Hardware de Áudio)
A biblioteca de captura em tempo real necessita do motor C++ `portaudio` instalado na sua máquina:
* **macOS:** `brew install portaudio`
* **Linux (Ubuntu/Debian):** `sudo apt-get install libasound2-dev portaudio19-dev`
* **Windows:** Geralmente não requer instalação externa (embutido na biblioteca Python).

### 2. Configurando o Ambiente Virtual (VENV)
É obrigatório isolar as dependências do projeto. No terminal, na raiz do projeto, execute:

```
**No macOS/Linux:**

```
python3 -m venv venv
source venv/bin/activate
```

**No Windows:**

```powershell
python -m venv venv
.\venv\Scripts\activate

```

### 3. Instalando as Bibliotecas Python

Com o ambiente ativado `(venv)`, instale as dependências de Processamento Digital de Sinais (DSP) e IA:

```bash
pip install --upgrade pip
pip install sounddevice numpy librosa tensorflow vosk

```

### 4. Configurando o Modelo de NLP (Vosk)

O modelo acústico do YAMNet é baixado automaticamente pelo código na primeira execução, mas o modelo do Vosk precisa ser configurado manualmente:

1. Acesse a página de modelos do Vosk: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
2. Baixe o modelo leve em português (ex: `vosk-model-small-pt-0.3`).
3. Extraia o arquivo `.zip`.
4. Renomeie a pasta extraída para `modelo_pt` e coloque-a na mesma pasta do arquivo `main.py`.

---

## 🚀 Como Executar

Certifique-se de que o seu microfone está ativado e possui permissão no sistema operacional.

```bash
# Lembre-se de sempre ativar o venv antes de rodar!
python main.py

```

**Comportamento Esperado:**

1. O script verificará a existência dos arquivos `yamnet.tflite` e `yamnet_class_map.csv` (baixando-os se necessário).
2. O microfone será ativado e filtrará silêncios usando cálculo vetorial de RMS.
3. Diga palavras-chave (ex: "socorro", "solta", "saia") para ver a pontuação subir no motor de risco.
