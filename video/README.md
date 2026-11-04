# Módulo de vídeo — PAMIA

Protótipo Python de análise de pose e invasão espacial em cabine, migrado do
repositório antigo. Usa OpenCV e MediaPipe com modelos locais. A inferência pode
ser executada offline após a instalação das dependências.

## Organização

```text
video/
├── app/
│   ├── main.py          # Captura, inferência, visualização e alertas
│   ├── config.py        # Caminhos, zonas e limiares
│   ├── zones.py         # Geometria e temporizador
│   ├── zone_crop.py     # Detecção adicional em recortes
│   └── calibrate.py     # Calibração automática e manual
├── models/              # Pose Landmarker lite, full e heavy
├── videos/              # Todos os MP4, sem cópias idênticas duplicadas
├── testemediapipe.py     # Experimento interativo com webcam
└── requirements.txt
```

Os oito vídeos mantêm os nomes originais: `before_sunrise_trem.mp4`,
`before_surise_encontro.mp4`, `Driver_touches_passenger_knee_20261012135539.mp4`,
`falso_assedio.mp4`, `ia_tocando_coxa.mp4`, `uber.mp4`, `uber2.mp4` e
`video_teste.mp4`. Os nomes não constituem anotações validadas dos eventos.

## Instalação e execução

Na raiz do repositório PAMIA, usando Python 3.12 no Windows:

```powershell
py -3.12 -m venv video/.venv
./video/.venv/Scripts/python.exe -m pip install -r video/requirements.txt
./video/.venv/Scripts/python.exe -m video.app.main
```

O vídeo padrão é `videos/uber2.mp4` e o modelo padrão é `models/pose_landmarker_full.task`.
Esses caminhos são resolvidos a partir de `config.py`, independentemente da pasta
de execução. Caminhos fornecidos na linha de comando são relativos à pasta atual:

```powershell
./video/.venv/Scripts/python.exe -m video.app.main video/videos/uber.mp4
./video/.venv/Scripts/python.exe -m video.app.main 0
```

ESPAÇO pausa/continua; ESC encerra. A execução direta também é suportada:
`py video/app/main.py`. Com as dependências já instaladas, `py` pode substituir
o caminho do Python do ambiente virtual nos comandos.

## Calibração

Cada posição de câmera precisa de zonas adequadas. A calibração grava o bloco
`ZONES` em `video/app/config.py`; use um trecho com os ocupantes sentados normalmente.

```powershell
./video/.venv/Scripts/python.exe -m video.app.calibrate video/videos/uber2.mp4 --inicio 0 --segundos 3
./video/.venv/Scripts/python.exe -m video.app.calibrate video/videos/uber2.mp4 --manual
```

A calibração automática nomeia o ocupante mais à direita como motorista e usa
a largura dos ombros para estimar frente/trás. Revise as zonas para cada câmera.

## Regra implementada

O ponto médio dos ombros determina o banco. Pulsos e indicadores visíveis dentro
de outro banco ocupado alimentam um acumulador temporal. Ele sobe durante a
invasão, decai na ausência e gera alerta a partir de 1,5 segundo por padrão.
A busca por recortes complementa a detecção na imagem inteira.

A análise é 2D, depende de câmera fixa e pode falhar com oclusão ou troca de banco
estimado. O alerta indica invasão espacial estimada e não comprova assédio.

## Migração e verificação

Foram preservados os parâmetros e a lógica de detecção do código existente em
`antigo/`, incluindo as alterações locais de `config.py`. Os ajustes da migração
são de caminhos, imports e organização. Modelos e vídeos foram copiados com
verificação SHA-256; duplicatas idênticas foram consolidadas. O repositório antigo
foi mantido como cópia de segurança, sem copiar seu histórico Git ou caches.

`testemediapipe.py` é uma demonstração que abre a webcam, não um teste automatizado:

```powershell
./video/.venv/Scripts/python.exe video/testemediapipe.py
```

Este módulo ainda não está integrado à captura do aplicativo móvel em `pamia/`.
