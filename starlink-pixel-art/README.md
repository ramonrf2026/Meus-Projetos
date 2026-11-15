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
