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


## 1. O Padrão Produtor-Consumidor (Threads e Filas)
O áudio em tempo real não espera o processador terminar de pensar. Se o microfone captar som enquanto a IA está calculando, o áudio se perde. Vocês resolveram isso com o padrão Produtor-Consumidor.

*   **O Produtor (`audio_callback`):** Esta função roda em uma thread (linha de execução) separada, gerenciada pela placa de som. A única função dela é empacotar o som em uma caixa (`audio_data`) e jogar na esteira (`audio_queue.put`). Ela faz isso extremamente rápido e volta a escutar.
*   **O Consumidor (`while True`):** Este é o cérebro principal. Ele pega a caixa da esteira (`audio_queue.get()`) e processa. 
*   **A Esteira Limitada (`maxsize=5`):** Se o Consumidor (IA) for mais lento que o Produtor (Microfone), as caixas vão acumular. Ao limitar a esteira, garantimos que, no pior cenário de gargalo de CPU, o sistema descarta áudio antigo em vez de travar o hardware por falta de RAM.

## 2. DSP: O Noise Gate com RMS
O microfone capta 16.000 amostras por segundo. Uma onda sonora flutua entre valores positivos (pressão empurrando o ar) e negativos (pressão puxando o ar). 

```python
rms_volume = np.sqrt(np.mean(np.square(audio_chunk)))
```
Se você calcular apenas a média simples dessas pressões positivas e negativas, o resultado dá próximo de zero, mesmo que alguém esteja gritando. O cálculo RMS (Root Mean Square) corrige isso:
1.  **`np.square`:** Eleva todas as 16.000 amostras ao quadrado. Um valor negativo (ex: `-0.5 * -0.5 = 0.25`) vira positivo. Agora temos a energia real.
2.  **`np.mean`:** Tira a média dessa energia total no intervalo de 1 segundo.
3.  **`np.sqrt`:** Extrai a raiz quadrada para voltar a escala original.

O resultado é um número preciso de volume. Se for menor que `0.005`, o sistema dá um `continue` e volta para o início do loop. A IA nem acorda. Isso economiza até 80% de bateria e CPU no Edge.

## 3. O Motor Acústico (YAMNet)
O YAMNet é uma rede neural inflexível: ela exige exatas 15.600 amostras para analisar 0.975 segundos de áudio.

```python
if len(audio_chunk) < tamanho_esperado:
    audio_chunk = np.pad(audio_chunk, (0, tamanho_esperado - len(audio_chunk)))
```
Se a placa de som entregar 15.000 amostras em vez de 16.000 (o que é comum em oscilações de hardware), o TensorFlow lite daria um erro fatal (Crash). A função `np.pad` salva o sistema preenchendo o final do array com zeros (silêncio) até atingir o tamanho exato que a IA exige, mantendo a estabilidade.

Ao entrar no YAMNet, a primeira camada interna da rede neural aplica a Transformada de Fourier e gera o **Mel-Espectrograma** silenciosamente, convertendo o array 1D (tempo) em uma imagem 2D (frequências). É essa "imagem" que a rede analisa para dizer se é um grito ou uma sirene.

## 4. O Motor Semântico (Vosk e Conversão)
O hardware do microfone trabalha nativamente em formato analógico. O Python (`sounddevice`) entrega isso normalizado em `float32` (valores com vírgula de -1.0 a 1.0). Porém, motores de NLP em C++ antigos, como o Kaldi (coração do Vosk), não entendem floats, apenas números inteiros de 16 bits (`int16`).

```python
audio_clipado = np.clip(audio_chunk_float32, -1.0, 1.0)
audio_int16 = (audio_clipado * 32767).astype(np.int16)
```
Um número `int16` vai de -32.768 até 32.767. Multiplicar o float (-1.0 a 1.0) por 32.767 é uma regra de três matemática que estica a onda sonora para caber na escala que o Vosk exige. O `np.clip` antes garante que um som estourado (ex: +1.2) não vire um número maior que 32.767, o que causaria o *Integer Overflow*, invertendo a onda e criando um ruído digital terrível.

A lógica de matemática de conjuntos (`novas_palavras_a_avaliar = palavras_ditas - palavras_penalizadas_na_frase_atual`) resolve o problema de sobreposição sem usar loops `for` pesados. O C++ interno do Python resolve a subtração de conjuntos em microssegundos.

## 5. O Motor de Risco (Leaky Bucket)
O conceito do "Balde Furado" em processamento de sinais serve para modelar o **esquecimento no tempo**.

```python
self.score = max(0.0, self.score - (self.decaimento_por_segundo * tempo_passado))
```
Se o sistema ouvir "cala a boca", o balde ganha 30 pontos. Se não ouvir mais nada de errado nos próximos 6 segundos (e o decaimento for de 5 pontos/segundo), o balde esvazia de volta para zero. A função `max(0.0, ...)` é a trava matemática que impede o score de ficar negativo (ex: -15 pontos), o que criaria uma "imunidade" indesejada para a próxima agressão.

http://googleusercontent.com/lmdx_content/ltfmDZDvrCXFhBDmQPwHjBdFWAyzxwPeguVkoMSBlGknxHuyBlhpzbQovtMRbtXpdJRSvxIyiualFWvVlRnzHJeShAqsjCOOpjjZTnCFTRfEhdIidKHjpIaBrDifwJuMNDajCzkXVSHZftDajXDmknLeNWWVUKfiKjISuUkHYBKwi40561