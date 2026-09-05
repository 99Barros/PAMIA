import sounddevice as sd
import numpy as np
import queue
import librosa 
import tensorflow as tf
import csv
import urllib
import os
import vosk
import json
import time

# ==========================================
# CONFIGURAÇÕES GERAIS DE ÁUDIO
# ==========================================
SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 16000
DEVICE_INDEX = None # Mude para o número do seu microfone se der erro -1

audio_queue = queue.Queue()

# ==========================================
# CLASSIFICADOR YAMNET
# ==========================================
class ClassificadorYAMNet:
    def __init__(self, model_path='yamnet.tflite', class_map_path='yamnet_class_map.csv'):
        # 1. Verifica e baixa os arquivos automaticamente (Apenas na primeira execução!)
        self._garantir_arquivos_locais(model_path, class_map_path)
        
        print("🧠 [IA] Carregando modelo YAMNet na memória (Edge)...")
        # Usando tf.lite.Interpreter garantimos a compatibilidade futura com Android
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.classes = self._carregar_mapa_classes(class_map_path)
        
        self.classes_alerta = ['Screaming', 'Yell', 'Crying, sobbing', 'Siren']

    def _garantir_arquivos_locais(self, model_path, csv_path):
        """Baixa o modelo TFLite e o CSV se não estiverem na pasta."""
        url_tflite = "https://storage.googleapis.com/audioset/yamnet.tflite"
        url_csv = "https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv"
        
        if not os.path.exists(model_path):
            print(f"📥 Baixando {model_path} pela primeira vez (Offline ready)...")
            urllib.request.urlretrieve(url_tflite, model_path)
            
        if not os.path.exists(csv_path):
            print(f"📥 Baixando {csv_path} pela primeira vez...")
            urllib.request.urlretrieve(url_csv, csv_path)
            
    def _carregar_mapa_classes(self, csv_path):
        class_names = []
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader) 
                for row in reader:
                    class_names.append(row[2])
        except Exception as e:
            print(f"Erro ao carregar CSV: {e}")
            return [f"Classe_{i}" for i in range(521)]
        return class_names

    def classificar_bloco(self, audio_chunk):
        # A lógica de inferência permanece a mesma...
        input_shape = self.input_details[0]['shape']
        tamanho_esperado = input_shape[1] if len(input_shape) > 1 else input_shape[0]
        
        if len(audio_chunk) > tamanho_esperado:
            audio_chunk = audio_chunk[:tamanho_esperado]
        elif len(audio_chunk) < tamanho_esperado:
            audio_chunk = np.pad(audio_chunk, (0, tamanho_esperado - len(audio_chunk)))
            
        input_data = audio_chunk.astype(np.float32)
        
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        
        classe_vencedora_idx = np.argmax(output_data[0])
        probabilidade = output_data[0][classe_vencedora_idx]
        nome_classe = self.classes[classe_vencedora_idx]
        
        return nome_classe, probabilidade



class MotorDeRisco:
    def __init__(self, limite_alarme=100, decaimento_por_segundo=5):
        self.score = 0.0
        self.limite_alarme = limite_alarme
        self.decaimento_por_segundo = decaimento_por_segundo
        self.ultimo_tempo = time.time()

    def processar_evento(self, pontos_novos):
        """Atualiza o decaimento pelo tempo que passou e soma os novos pontos."""
        tempo_atual = time.time()
        tempo_passado = tempo_atual - self.ultimo_tempo
        
        # O furo no balde: reduz o score com o passar do tempo, mas trava no zero
        self.score = max(0.0, self.score - (self.decaimento_por_segundo * tempo_passado))
        self.ultimo_tempo = tempo_atual
        
        # Joga água no balde
        if pontos_novos > 0:
            self.score += pontos_novos
            
        return self.score >= self.limite_alarme

class TranscritorVosk:
    def __init__(self, model_path="modelo_pt", sample_rate=16000):
        print("🗣️ [NLP] Carregando modelo Vosk na memória (Edge)...")
        
        # Desliga os logs prolixos do Vosk em C++
        vosk.SetLogLevel(-1) 
        
        try:
            self.model = vosk.Model(model_path)
            self.recognizer = vosk.KaldiRecognizer(self.model, sample_rate)
        except Exception as e:
            print(f"Erro ao carregar Vosk. Verifique se a pasta '{model_path}' existe. Erro: {e}")
            exit(1)
            
# Dicionário categorizado com pesos diferentes para o Threshold
        self.dicionario_risco = {
            "emergencia": {"palavras": ["socorro", "ajuda", "polícia", "gostosa"], "peso": 100}, # Transborda na hora
            "assedio": {"palavras": ["saia", "linda", "namorado", "solteira", "cheirosa"], "peso": 30},
            "agressividade": {"palavras": ["cala", "burra", "desce", "solta"], "peso": 30}
        }

    def processar_audio(self, audio_chunk_float32):
        """
        Recebe o array float32, normaliza o volume, converte para int16 e passa para o Vosk.
        """
        # 1. Normalização de Pico (Maximiza o volume do bloco dinamicamente)
        max_amp = np.max(np.abs(audio_chunk_float32))
        
        # Evita divisão por zero em casos de silêncio absoluto
        if max_amp > 0:
            audio_normalizado = audio_chunk_float32 / max_amp
        else:
            audio_normalizado = audio_chunk_float32
            
        # 2. Conversão otimizada e segura para Int16
        audio_int16 = (audio_normalizado * 32767).astype(np.int16)
        
        # 3. Converte a matriz para bytes puros
        dados_bytes = audio_int16.tobytes()
        
        texto_detectado = ""
        
        if self.recognizer.AcceptWaveform(dados_bytes):
            resultado = json.loads(self.recognizer.Result())
            texto_detectado = resultado.get("text", "")
        else:
            resultado = json.loads(self.recognizer.PartialResult())
            texto_detectado = resultado.get("partial", "")
            
        return texto_detectado.lower()
def processar_audio(self, audio_chunk_float32):
        # 1. Normalização de Pico (Maximiza o volume do bloco dinamicamente)
        max_amp = np.max(np.abs(audio_chunk_float32))
        
        # Evita divisão por zero em casos de silêncio absoluto
        if max_amp > 0:
            audio_normalizado = audio_chunk_float32 / max_amp
        else:
            audio_normalizado = audio_chunk_float32
            
        # 2. Conversão otimizada e segura para Int16
        audio_int16 = (audio_normalizado * 32767).astype(np.int16)
        dados_bytes = audio_int16.tobytes()
        
        texto_detectado = ""
        if self.recognizer.AcceptWaveform(dados_bytes):
            resultado = json.loads(self.recognizer.Result())
            texto_detectado = resultado.get("text", "")
        else:
            resultado = json.loads(self.recognizer.PartialResult())
            texto_detectado = resultado.get("partial", "")
            
        return texto_detectado.lower()

# ==========================================
# CAPTURA E DSP
# ==========================================
def audio_callback(indata, frames, time, status):
    if status:
        print(f"⚠️ Status de Áudio: {status}", flush=True)
    audio_data = indata.flatten().astype(np.float32)
    audio_queue.put(audio_data)

def iniciar_escuta():
    # 1. INICIALIZA AS IAs ANTES DE ABRIR O MICROFONE
    classificador = ClassificadorYAMNet('yamnet.tflite', 'yamnet_class_map.csv')
    transcritor = TranscritorVosk(model_path="modelo_pt")
    
    # 2. INSTANCIA O MOTOR DE RISCO AQUI
    motor_risco = MotorDeRisco(limite_alarme=100, decaimento_por_segundo=5)

    print("\n🎤 Iniciando microfone... Teste o motor de risco! (Ctrl+C para parar)")

    try:
        with sd.InputStream(device=DEVICE_INDEX, samplerate=SAMPLE_RATE, channels=CHANNELS, 
                            blocksize=BLOCK_SIZE, callback=audio_callback):
            while True:
                audio_chunk = audio_queue.get()
                
                # Filtro de Volume (RMS)
                rms_volume = np.sqrt(np.mean(np.square(audio_chunk)))
                
                if rms_volume < 0.005:
                    continue # Silêncio, ignora bloco
                
                print(f"\n🔊 Som (RMS: {rms_volume:.5f}) - Analisando...")
                
                # ----------------------------------------------------
                # INFERÊNCIA MULTIMODAL E PONTUAÇÃO (THRESHOLD)
                # ----------------------------------------------------
                pontos_neste_bloco = 0
                
                # 1. Análise Acústica (YAMNet)
                classe_som, prob = classificador.classificar_bloco(audio_chunk)
                if classe_som in classificador.classes_alerta:
                    print(f"🧠 Acústico: {classe_som} detectado! (+40 pts)")
                    pontos_neste_bloco += 40
                
                # 2. Análise Semântica (Vosk)
                texto = transcritor.processar_audio(audio_chunk)
                if texto:
                    print(f"📝 Vosk ouviu: '{texto}'")
                    palavras_ditas = texto.split()
                    
                    # Busca por palavras e atribui os pesos
                    for categoria, config in transcritor.dicionario_risco.items():
                        if any(p in palavras_ditas for p in config["palavras"]):
                            peso = config["peso"]
                            print(f"⚠️ Semântico: Marcador de {categoria} detectado! (+{peso} pts)")
                            pontos_neste_bloco += peso
                            break # Evita pontuar duas vezes a mesma categoria na mesma frase

                # 3. Atualiza o Balde Furado
                alarme_disparado = motor_risco.processar_evento(pontos_neste_bloco)
                
                if pontos_neste_bloco > 0:
                    print(f"📊 SCORE DE RISCO: {motor_risco.score:.1f} / {motor_risco.limite_alarme}\n")
                
                if alarme_disparado:
                    print("🚨🚨🚨 ALARME MÁXIMO: CONTEXTO DE VIOLÊNCIA CONFIRMADO! 🚨🚨🚨")
                    # Reseta o score após o alarme para não ficar apitando em loop
                    motor_risco.score = 0 
                
    except KeyboardInterrupt:
        print("\nCaptura encerrada pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
if __name__ == "__main__":
    iniciar_escuta()