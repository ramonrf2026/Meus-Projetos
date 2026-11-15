import numpy as np, soundfile as sf, json
from kokoro_onnx import Kokoro
k=Kokoro('/root/tasks/starlink-pixel-art/tts/model.onnx','/root/tasks/starlink-pixel-art/tts/voices.npz')
FALAS=[
 "Flamengo: a história do Mengão em trinta segundos.",
 "Tudo começou em mil oitocentos e noventa e cinco, no Rio de Janeiro, como um clube de remo.",
 "Em mil novecentos e onze, nasceu o time de futebol, de vermelho e preto.",
 "Em oitenta e um, com Zico, vieram a Libertadores e o Mundial, com três a zero no Líverpul.",
 "Em dois mil e dezenove, o Mengão voltou ao topo da América. E tem a maior torcida do Brasil.",
 "Uma vez Flamengo, sempre Flamengo!",
]
import sys; sp=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
out=[]
for i,t in enumerate(FALAS):
    a,sr=k.create(t,voice='pm_alex',speed=sp,lang='pt-br'); sf.write(f'/root/tasks/flamengo-30s/fala{i}.wav',a,sr); out.append(round(len(a)/sr,2))
print(out, sum(out))
