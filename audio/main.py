import sounddevice as sd
import numpy as np
import queue

# Configurações obrigatórias para o YAMNet e Vosk
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 16000  # Captura blocos de 1 segundo (16.000 amostras)

# Fila thread-safe para armazenar os blocos de áudio sem perder dados
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    """
    Função chamada automaticamente pela placa de som a cada bloco capturado.
    Deve ser EXTREMAMENTE rápida. Sem processamento pesado aqui!
    """
    if status:
        # Debug clássico: avisa se houver buffer underflow/overflow (latência)
        print(f"⚠️ Status de Áudio: {status}", flush=True)
    
    # 1. Transforma o áudio bidimensional (frames, canais) em um array 1D
    # 2. Garante o formato float32 esperado pelo YAMNet
    audio_data = indata.flatten().astype(np.float32)
    
    # Coloca na fila para ser processado no loop principal
    audio_queue.put(audio_data)

def iniciar_escuta():
    print("Iniciando microfone... Pressione Ctrl+C para parar.")
    
    # Dica de Debug: Se o código falhar ao iniciar, rode sd.query_devices() no console
    # para achar o índice correto do seu microfone e passe o parâmetro device=X abaixo.
    
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, 
                            channels=CHANNELS, 
                            blocksize=BLOCK_SIZE,
                            callback=audio_callback):
            
            while True:
                # O loop principal pega o áudio da fila assim que estiver disponível
                audio_chunk = audio_queue.get()
                
                # CÁLCULO DE ENERGIA (RMS - Root Mean Square)
                # Explicação didática: O RMS mede a 'força' ou volume do sinal sonoro.
                # Como o áudio varia entre negativos e positivos (ondas), elevamos ao quadrado (np.square)
                # tiramos a média (np.mean) e fazemos a raiz quadrada (np.sqrt).
                rms_volume = np.sqrt(np.mean(np.square(audio_chunk)))
                
                print(f"Bloco capturado! Volume (RMS): {rms_volume:.5f}")
                
                # João: É AQUI que nas próximas etapas chamaremos suas funções
                # de extração de MFCC e Mel-Espectrograma!
                # Paulo: E depois, passaremos esse chunk tratado para o YAMNet e Vosk!
                
    except KeyboardInterrupt:
        print("\nCaptura encerrada pelo usuário.")
    except Exception as e:
        print(f"Erro na captura de áudio: {e}")

if __name__ == "__main__":
    iniciar_escuta()