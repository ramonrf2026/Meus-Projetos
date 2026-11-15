# Starlink — como funciona a constelação (pixel art 9:16)

Animação em pixel art (180×320, exportada em 1080×1920) explicando em 6 passos:
órbita baixa × geoestacionária, planos orbitais, rastreio/troca de satélite,
caminho do sinal (antena → satélite → estação terrestre → internet),
links a laser entre satélites e ciclo de vida (lançamento e reentrada).

- `index.html` — abre no navegador; clique pausa, ← → trocam de cena, `?t=12` congela num instante.
- `render.mjs` — `node render.mjs [saida.mp4] [fps]` grava o vídeo (precisa de Playwright e ffmpeg).
- `starlink-9x16.mp4` — vídeo pronto, 78 s, 30 fps, sem áudio.

Números arredondados de propósito (altitude ~500 km, ~27.000 km/h, volta ≈ 95 min,
GEO ~36.000 km). Distâncias da cena 1 em escala aproximada.

## Narração (TTS aberto)

`starlink-9x16-narrado.mp4` tem narração em português gerada localmente com
[Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache 2.0) via `kokoro-onnx`, voz `pm_alex`.

Para gerar de novo (modelo e vozes de `onnx-community/Kokoro-82M-v1.0-ONNX` no Hugging Face):

    pip install kokoro-onnx soundfile
    # baixe onnx/model.onnx e voices/pm_alex.bin (e pf_dora, pm_santa) para a pasta
    python narrar.py pm_alex     # gera narracao_pm_alex.wav (78 s, alinhada às cenas)
    ffmpeg -i starlink-9x16.mp4 -i narracao_pm_alex.wav -map 0:v -map 1:a -c:v copy \
      -af loudnorm=I=-16:TP=-1.5 -c:a aac -b:a 160k starlink-9x16-narrado.mp4

Palavras escritas foneticamente no roteiro: "Istárlink", "lêiser", "Fálcon Nove".
