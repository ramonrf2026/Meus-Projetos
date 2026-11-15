import sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
d={v:np.fromfile(f'{v}.bin',dtype=np.float32).reshape(-1,1,256) for v in ['pf_dora','pm_alex','pm_santa']}
np.savez('voices.npz',**d)
k=Kokoro('model.onnx','voices.npz')
VOZ=sys.argv[1] if len(sys.argv)>1 else 'pm_alex'
CENAS=[ # (início s, duração s, texto)
 (0,6.5,"Como funciona a constelação de satélites da Istárlink? Vamos ver em seis passos."),
 (6.5,9.5,"Passo um: órbita baixa. Os satélites ficam a uns quinhentos quilômetros de altura. Os geoestacionários ficam a trinta e seis mil. Mais perto, menos atraso."),
 (16,10,"Passo dois: a constelação. São milhares de satélites, em várias camadas e planos orbitais, cobrindo quase todo o planeta."),
 (26,10,"Passo três: tudo em movimento. Cada satélite viaja a uns vinte e sete mil quilômetros por hora, e a antena troca de satélite sozinha."),
 (36,11,"Passo quatro: o caminho do sinal. Seu pedido sobe da antena ao satélite, desce numa estação terrestre e segue por fibra até a internet. A resposta volta pelo mesmo caminho."),
 (47,11,"Passo cinco: lêisers. No meio do oceano não há estação por perto. Então os satélites repassam o sinal entre si, por lêiser, até chegar a uma estação."),
 (58,11,"Passo seis: ciclo de vida. Os satélites sobem em lotes no foguete Fálcon Nove. No fim da vida útil, saem de órbita e queimam na atmosfera."),
 (69,9,"Resumo: antena, satélite, lêiser quando precisa, estação terrestre e internet. Internet via espaço, com baixa latência."),
]
SR=24000; total=np.zeros(int(78*SR),dtype=np.float32)
for i,(t0,dur,txt) in enumerate(CENAS):
    speed=1.0
    while True:
        a,sr=k.create(txt,voice=VOZ,speed=speed,lang='pt-br')
        L=len(a)/sr
        if L<=dur-0.6 or speed>=1.3: break
        speed=round(speed+0.05,2)
    print(f'cena {i}: {L:.2f}s / {dur}s  speed={speed}')
    s=int((t0+0.35)*SR); total[s:s+len(a)]+=a[:len(total)-s]
sf.write(f'narracao_{VOZ}.wav',total,SR)
