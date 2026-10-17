"""A colagem do README: uma cena só, fatiada em tiras.

    python tools/colagem.py

A cena inteira tem 880 de largura. Cada tira é a mesma cena com outro viewBox,
levando só os elementos que encostam nela, então o que atravessa a emenda
aparece certinho dos dois lados. No README as tiras ficam com align="left"
e width="100%", que é o jeito de o GitHub empilhar imagem sem fresta.

O then and now e o recibo da semana saíram daqui e estão guardados em archive/.
"""
import json
import math
import random
from pathlib import Path

from kit import (AMARELO, ANIL, CRACHA, LIMA, PAUTA, TINTA, fita, imagem,
                 linha, medir, salvar, t, tamanho)

W = 880
AMARELO_PAG, ROSA_BILHETE = "#f4ec55", "#ffd3e3"
CEU_TOPO, CEU_MEIO, CEU_FUNDO = "#3d8ce6", "#9fd2fa", "#4f9ae9"

# nome, y inicial, altura, link, descrição (alt)
TIRAS = [
    ("capa", 0, 440, None,
     "Uma barrinha de letreiro rolando no topo: ようこそ! boas-vindas ao meu cantinho. "
     "kitsuneislife em letra de adesivo, num céu azul. Um arco-íris de papelão e eu sentado numa nuvem, de fone."),
    ("bio", 440, 340, None,
     "Uma prancheta com um bilhete: Nunca soube o que escrever em uma bio ou em um sobre-mim. Curioso né? "
     "Então fiz essa página pra contar um pouquinho de quem sou eu. Eu gosto de fazer alguns projetinhos "
     "(e de lasanha) e quero trabalhar na área. Discord: @thurzinhos. “Penso, logo desisto.” love you forever. "
     "Do lado, a turma correndo com uma placa: olha os projetinhos."),
    ("projetos", 780, 180, "https://github.com/kitsuneislife?tab=repositories",
     "projetinhos (e de lasanha). Clica nos cards pra abrir cada um."),
    ("artcode", 960, 270, "https://github.com/kitsuneislife/artcode",
     "artcode: minha própria linguagem de programação, interpretada e escrita em Rust. Tá na v0.5.1."),
    ("lover", 1230, 270, "https://kitsuneislife.github.io/lover/",
     "lover: um jogo de quebra-cabeça em que o controle é o seu navegador. Clica pra jogar."),
    ("clios", 1500, 270, "https://github.com/kitsuneislife/clios",
     "clios: um desktop Linux feito pro terminal. Arch, Hyprland e Quickshell, com um binário em Rust."),
    ("hackintosh", 1770, 270, "https://github.com/kitsuneislife/Acer-Nitro-V15-ANV15-51-Hackintosh",
     "Hackintosh: macOS Sequoia num Acer Nitro V15, com o desktop acelerado na RTX 3050."),
    ("mais", 2040, 110, "https://github.com/kitsuneislife?tab=repositories",
     "Tem mais projetinhos no meu perfil."),
    ("habilidades", 2150, 690, None,
     "O que eu sei fazer, num boletim escolar com as notas tiradas dos meus repositórios no GitHub: "
     "cada linguagem com quantos repos usam ela, a nota e se passou. Dart, Java e Kotlin estão em curso. "
     "Atividades extras: git, npm, Redis, Express, Docker, Expo. Deveres entregues: os repositórios "
     "mexidos por último. Carimbo de aprovado."),
    ("fim", 2840, 440, None,
     "Anoitece. Gostou? Sei fazer bem mais. Eu abraçando uma pelúcia do Claude, com a lua e umas estrelinhas. "
     "Embaixo, botõezinhos de site antigo: feito à mão por kitsune, 100% SVG, movido a lasanha, "
     "melhor visto em qualquer um, sem cookies. kitsuneislife, 2026."),
]
H = TIRAS[-1][1] + TIRAS[-1][2]


class Cena:
    def __init__(self):
        self.els = []  # (z, ordem, (x0, y0, x1, y1), svg)

    def add(self, svg, caixa, z=0):
        self.els.append((z, len(self.els), caixa, svg))

    def subir(self, a_partir, d):
        """Sobe d tudo que começa abaixo de a_partir."""
        novos = []
        for z, o, (x0, y0, x1, y1), s in self.els:
            if y0 >= a_partir:
                s, y0, y1 = f'<g transform="translate(0 {-d})">{s}</g>', y0 - d, y1 - d
            novos.append((z, o, (x0, y0, x1, y1), s))
        self.els = novos

    def img(self, nome, x, y, w, rot=0, z=0, classe="", sombra="sombra-leve", px=None):
        iw, ih = tamanho(nome)
        h = w * ih / iw
        cx, cy = x + w / 2, y + h / 2
        uri = imagem(nome, min(iw, round(px or w * 2)))
        f = f' filter="url(#{sombra})"' if sombra else ""
        tr = f' transform="rotate({rot} {cx:.1f} {cy:.1f})"' if rot else ""
        corpo = f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="{uri}"{f}{tr}/>'
        if classe:
            corpo = f'<g class="{classe}">{corpo}</g>'
        self.add(corpo, caixa_girada(x, y, w, h, rot), z)
        return h


def caixa_girada(x, y, w, h, rot, folga=24):
    cx, cy = x + w / 2, y + h / 2
    a = math.radians(rot)
    xs, ys = [], []
    for px_, py_ in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
        dx, dy = px_ - cx, py_ - cy
        xs.append(cx + dx * math.cos(a) - dy * math.sin(a))
        ys.append(cy + dx * math.sin(a) + dy * math.cos(a))
    return (min(xs) - folga, min(ys) - folga, max(xs) + folga, max(ys) + folga)


def logo(texto, x, y, px, cor, giros, sobe, contorno=TINTA, borda="#fff", sombra="#1b2f78", classe="bolha"):
    """Logotipo de adesivo: cada letra torta, contorno preto, borda branca e sombra."""
    rot = " ".join(str(g) for g in giros[: len(texto)])
    dy = " ".join(str(d) for d in sobe[: len(texto)])
    base = f'x="{x}" y="{y}" font-size="{px}" class="{classe}" rotate="{rot}" dy="{dy}" stroke-linejoin="round"'
    s = t(texto)
    return (f'<text {base} fill="{sombra}" stroke="{sombra}" stroke-width="{px * .42:.1f}" transform="translate(6 8)">{s}</text>'
            f'<text {base} fill="{borda}" stroke="{borda}" stroke-width="{px * .40:.1f}">{s}</text>'
            f'<text {base} fill="{cor}" stroke="{contorno}" stroke-width="{px * .16:.1f}" paint-order="stroke">{s}</text>')


def letreiro(c):
    """Faixa de letreiro rolando no topo, tipo <marquee>, torta como fita de cuidado."""
    frase = "ようこそ! boas-vindas ao meu cantinho"
    px = 15
    unidade = medir("revista", frase, px) + 56
    n = math.ceil((W + 200 + unidade) / unidade) + 1
    itens = []
    for i in range(n):
        x = -100 + i * unidade
        itens.append(f'<text x="{x:.1f}" y="21" font-size="{px}" class="revista" fill="#fff" opacity=".9">{t(frase)}</text>')
        itens.append(f'<text x="{x + unidade - 34:.1f}" y="21" font-size="{px}" class="revista" fill="{LIMA}">✦</text>')
    corpo = (f'<rect x="0" y="0" width="{W}" height="30" fill="{TINTA}"/>'
             f'<clipPath id="faixa"><rect x="0" y="0" width="{W}" height="30"/></clipPath>'
             f'<g clip-path="url(#faixa)"><g class="letreiro" style="--volta:-{unidade:.1f}px">{"".join(itens)}</g></g>')
    c.add(corpo, (0, 0, W, 40), z=9)


def estrela(cx, cy, r, atraso=0, cor=AMARELO):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return (f'<polygon class="brilho" style="animation-delay:{atraso}s" points="{" ".join(pts)}" fill="{cor}" '
            f'stroke="{TINTA}" stroke-width="3" stroke-linejoin="round"/>')


def bilhete(x, y, w, linhas, rot=0, cor="#fffef6", px=21, pautado=True):
    """Pedaço de papel com texto à mão. Devolve (svg, caixa)."""
    h = 34 + len(linhas) * (px + 11)
    cx, cy = x + w / 2, y + h / 2
    s = [f'<g transform="rotate({rot} {cx} {cy})">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{cor}" filter="url(#sombra)"/>']
    for i, ln in enumerate(linhas):
        by = y + 30 + i * (px + 11) + px * 0.35
        if pautado:
            s.append(f'<line x1="{x}" y1="{by + 7}" x2="{x + w}" y2="{by + 7}" stroke="{PAUTA}" stroke-width="1.3"/>')
        if isinstance(ln, tuple):
            texto, cor_l = ln
        else:
            texto, cor_l = ln, TINTA
        s.append(linha(x + 18, by, texto, px, cor_l))
    s.append("</g>")
    return "".join(s), caixa_girada(x, y, w, h, rot)


# ---------------------------------------------------------------- a cena

def montar():
    c = Cena()

    # nuvens de papelão no fundo
    for nome_, x, y, w, rot, cl in [("nuvem.png", 700, 1180, 220, -6, ""), ("nuvem.png", -60, 1700, 230, 5, ""),
                                    ("nuvem.png", 690, 2600, 240, -3, ""), ("nuvem.png", -80, 3500, 260, 4, ""),
                                    ("nuvem.png", 650, 4100, 250, -5, "")]:
        c.img(nome_, x, y, w, rot, z=0, classe=cl, sombra=None)

    # ---- capa
    c.img("arco-iris.png", 450, 150, 420, -4, z=1)
    # uma nuvem em cada pé do arco-íris, e eu sentado onde elas se encontram
    c.img("nuvem.png", 410, 288, 280, -3, z=2, sombra="sombra-leve")
    c.img("nuvem.png", 660, 270, 260, 4, z=2, sombra="sombra-leve")
    c.img("sentado.png", 590, 120, 210, 0, z=3, classe="flutua", px=411)
    letreiro(c)
    giros = [-6, 4, -3, 5, -4, 3, -5, 6, -2, 4, -6, 3, -4]
    sobe = [0, -6, 8, -4, 6, -8, 5, -3, 7, -6, 4, -5, 6]
    c.add(logo("kitsuneislife", 30, 196, 98, LIMA, giros, sobe), (0, 70, 760, 270), z=7)
    for i, (sx, sy, sr) in enumerate([(700, 120, 26), (52, 262, 18), (520, 76, 13), (560, 330, 16)]):
        c.add(estrela(sx, sy, sr, i * 0.7), (sx - 40, sy - 40, sx + 40, sy + 40), z=8)

    # ---- bio
    # o export da prancheta já vem cortado na esquerda e embaixo: encosta na borda
    # e a folha dos projetinhos cobre o corte de baixo
    c.img("banner-bio.png", 0, 516, 880, 0, z=4, sombra="sombra", px=1238)
    c.add(f'<g transform="rotate(-22 803 856)">{linha(752, 852, "olha os", 22)}{linha(742, 880, "projetinhos!", 22)}</g>',
          (720, 810, 880, 900), z=5)

    # ---- projetinhos, numa folha quadriculada amarela que vai até o "tem mais"
    folha = (f'<g transform="rotate(-0.8 440 2100)" filter="url(#sombra)">'
             f'<rect x="-30" y="1392" width="940" height="1500" fill="{AMARELO_PAG}"/>'
             f'<rect x="-30" y="1392" width="940" height="1500" fill="url(#quadriculado)"/>'
             f'<rect x="-30" y="1392" width="940" height="26" fill="url(#xadrez)"/></g>')
    c.add(folha, (-30, 1370, 910, 2910), z=4)
    c.add(fita(318, 1376, 150, 44, -6) + fita(640, 1366, 150, 44, 7), (300, 1340, 800, 1430), z=11)
    projetinhos(c)

    # ---- o que eu sei fazer: um boletim, com as notas tiradas dos repositórios
    boletim(c)

    # ---- fim: anoitece
    rodape(c)

    # a cena foi desenhada com o then and now e o recibo no meio; sem eles,
    # o fim sobe 720, os projetinhos sobem 440 e tudo da bio pra baixo sobe 240
    c.subir(3600, 720)
    c.subir(1300, 440)
    c.subir(470, 240)
    return c


ROSA, ROSA_ESCURO, AZUL_VIVO, VERDE = "#f25ca8", "#c93d86", "#3f7cf4", "#7fd65b"


def serrilha(x, y, w, semente, amp=4, passo=9):
    """Borda de papel rasgado, da esquerda pra direita."""
    r = random.Random(semente)
    pts = [f"{x + i:.1f} {y + r.uniform(-amp, amp):.1f}" for i in range(0, int(w) + 1, passo)]
    return " L".join(pts)


def folha_rasgada(x, y, w, h, rot, semente):
    """Folha arrancada do caderno: topo rasgado com os furos, quadriculado azul."""
    topo = serrilha(x, y, w, semente)
    d = f"M{topo} L{x + w} {y + h} L{x} {y + h} Z"
    furos = "".join(f'<circle cx="{x + 30 + i * 46}" cy="{y + 20}" r="6" fill="{AMARELO_PAG}" stroke="#d9d2a0" stroke-width="1"/>'
                    for i in range(int((w - 40) // 46) + 1))
    return (f'<g transform="rotate({rot} {x + w / 2:.1f} {y + h / 2:.1f})">'
            f'<path d="{d}" fill="#fdfdfb" filter="url(#sombra)"/>'
            f'<path d="{d}" fill="url(#grade-azul)"/>{furos}</g>')


def etiqueta(x, y, texto, fundo, rot=0, cor=TINTA, px=14):
    """Etiqueta de adesivo com contorno preto, tipo as de aviso das referências."""
    w = medir("revista", texto, px) + 22
    h = px + 16
    return (f'<g transform="rotate({rot} {x + w / 2:.1f} {y + h / 2:.1f})" filter="url(#sombra-leve)">'
            f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="5" fill="{fundo}" stroke="{TINTA}" stroke-width="2.5"/>'
            f'<text x="{x + 11}" y="{y + h / 2 + px * .36:.1f}" font-size="{px}" class="revista" fill="{cor}">{t(texto)}</text></g>'), w


def brilhinho(cx, cy, r, cor="#fff", atraso=None):
    """Estrelinha de quatro pontas."""
    d = (f"M{cx} {cy - r} Q{cx + r * .18} {cy - r * .18} {cx + r} {cy} Q{cx + r * .18} {cy + r * .18} {cx} {cy + r} "
         f"Q{cx - r * .18} {cy + r * .18} {cx - r} {cy} Q{cx - r * .18} {cy - r * .18} {cx} {cy - r} Z")
    cl = f' class="brilho" style="animation-delay:{atraso}s"' if atraso is not None else ""
    return f'<path{cl} d="{d}" fill="{cor}" stroke="{TINTA}" stroke-width="2.5" stroke-linejoin="round"/>'


def cursor(x, y, rot=0, escala=1):
    """Setinha amarela de mouse, gordinha, clicando."""
    d = "M0 0 L0 46 L12 35 L21 55 L30 51 L21 32 L37 32 Z"
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({escala})" filter="url(#sombra-leve)">'
            f'<path d="{d}" transform="translate(4 4)" fill="#d79a00" stroke="{TINTA}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{AMARELO}" stroke="{TINTA}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M-10 -6 l-9 -7 M-2 -12 l-2 -11 M8 -9 l6 -9" stroke="{TINTA}" stroke-width="3" stroke-linecap="round"/></g>')


def tecla(x, y, texto, rot=0, w=None):
    """Tecla de teclado, como adesivo."""
    w = w or medir("revista", texto, 15) + 26
    return (f'<g transform="rotate({rot} {x + w / 2:.1f} {y + 22})" filter="url(#sombra-leve)">'
            f'<rect x="{x}" y="{y}" width="{w:.1f}" height="46" rx="9" fill="#9aa3b5" stroke="{TINTA}" stroke-width="2.5"/>'
            f'<rect x="{x + 4}" y="{y + 3}" width="{w - 8:.1f}" height="34" rx="7" fill="#eef1f7"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 26}" font-size="15" text-anchor="middle" class="revista" fill="{TINTA}">{t(texto)}</text></g>'), w


def coracao(cx, cy, r, cor=ROSA, rot=0):
    d = (f"M{cx} {cy + r * .9} C{cx - r * 1.6} {cy - r * .1}, {cx - r * .7} {cy - r * 1.2}, {cx} {cy - r * .35} "
         f"C{cx + r * .7} {cy - r * 1.2}, {cx + r * 1.6} {cy - r * .1}, {cx} {cy + r * .9} Z")
    return (f'<g transform="rotate({rot} {cx} {cy})" filter="url(#sombra-leve)"><path d="{d}" fill="{cor}" stroke="{TINTA}" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<circle cx="{cx - r * .45}" cy="{cy - r * .35}" r="{r * .16}" fill="#fff"/></g>')


def print_adesivo(c, nome, x, y, w, rot, z, moldura="#fff", borda=10, lupa=None):
    """O print do projeto colado como adesivo grosso. lupa = (u, v, r, zoom, cx, cy)."""
    iw, ih = tamanho(nome)
    h = w * ih / iw
    uri = imagem(nome, min(iw, round(w * 2.4)))
    fw, fh = w + 2 * borda, h + 2 * borda
    cx, cy = x + fw / 2, y + fh / 2
    s = [f'<g transform="rotate({rot} {cx:.1f} {cy:.1f})">',
         f'<rect x="{x}" y="{y}" width="{fw:.1f}" height="{fh:.1f}" rx="6" fill="{moldura}" filter="url(#sombra)"/>',
         f'<image x="{x + borda}" y="{y + borda}" width="{w}" height="{h:.1f}" href="{uri}" preserveAspectRatio="xMidYMid slice"/>']
    if lupa:
        u, v, r, zoom, lx, ly = lupa
        px_, py_ = x + borda + u * w, y + borda + v * h
        uri2 = imagem(nome, iw)
        # o vidro da lupa.png fica em (0.3245, 0.3165) da imagem, com raio de 0.2817 da largura
        lw = r / .2817
        lh = lw * 530 / 520
        s.append(f'<clipPath id="lente"><circle cx="{lx}" cy="{ly}" r="{r}"/></clipPath>'
                 f'<circle cx="{lx}" cy="{ly}" r="{r}" fill="#fff"/>'
                 f'<g clip-path="url(#lente)"><image x="{lx - (px_ - x - borda) * zoom:.1f}" y="{ly - (py_ - y - borda) * zoom:.1f}" '
                 f'width="{w * zoom:.1f}" height="{h * zoom:.1f}" href="{uri2}"/></g>'
                 f'<image x="{lx - .3245 * lw:.1f}" y="{ly - .3165 * lh:.1f}" width="{lw:.1f}" height="{lh:.1f}" '
                 f'href="{imagem("recortes/lupa.png", 520)}" filter="url(#sombra-leve)"/>')
    s.append("</g>")
    c.add("".join(s), caixa_girada(x, y, fw, fh, rot), z)
    return fw, fh


def cartao(c, x, y, rot, numero, titulo, cor_titulo, linhas, tags, semente):
    """A folha de cada projeto: número, título de adesivo, o texto à mão e as etiquetas."""
    w, h = 410, 238
    s = [folha_rasgada(x, y, w, h, rot, semente), f'<g transform="rotate({rot} {x + w / 2:.1f} {y + h / 2:.1f})">']
    s.append(f'<text x="{x + 24}" y="{y + 66}" font-size="26" class="revista" fill="{ROSA}" stroke="{TINTA}" stroke-width="5" paint-order="stroke">{numero}</text>')
    s.append(logo(titulo, x + 84, y + 70, 40, cor_titulo, [-4, 3, -2, 4, -3, 2, -4, 3, -2, 4], [0] * 12))
    for i, ln in enumerate(linhas):
        texto, cor_l = ln if isinstance(ln, tuple) else (ln, TINTA)
        s.append(linha(x + 26, y + 112 + i * 28, texto, 20, cor_l))
    tx = x + 24
    for texto, fundo, cor_t in tags:
        e, ew = etiqueta(tx, y + h - 50, texto, fundo, cor=cor_t, px=13)
        s.append(e)
        tx += ew + 8
    s.append("</g>")
    c.add("".join(s), caixa_girada(x, y - 40, w, h + 40, rot), z=6)
    c.img("recortes/prendedor-rosa.png", x + w - 112, y - 50, 62, rot * 3 + 4, z=7, px=180)


def projetinhos(c):
    # cabeçalho: o logo, o "(e de lasanha)" e a setinha clicando
    c.add(logo("projetinhos", 40, 1562, 74, "#ffb3d1", [4, -3, 5, -4, 3, -5, 6, -2, 4, -6, 3], [-6, 8, -4, 6, -8, 5, -3, 7, -6, 4, -5]),
          (10, 1480, 600, 1610), z=6)
    c.add(fita(62, 1578, 240, 46, -2) + linha(92, 1609, "(e de lasanha)", 22, TINTA, 'transform="rotate(-2 180 1600)"'),
          (50, 1570, 320, 1630), z=7)
    setas = "".join(f'<path d="M{596 + i * 30} 1512 l20 16 l-20 16 Z" fill="{AZUL_VIVO}" stroke="{TINTA}" stroke-width="2.5" stroke-linejoin="round"/>'
                    for i in range(4))
    c.add(f'<g transform="rotate(-4 660 1528)" filter="url(#sombra-leve)">{setas}</g>'
          + linha(600, 1586, "clica nos cards pra abrir", 21, TINTA, 'transform="rotate(-4 700 1580)"')
          + cursor(812, 1534, -14), (580, 1490, 860, 1636), z=7)
    c.img("recortes/tesoura.png", 520, 1560, 62, 58, z=7, px=160)
    c.add(estrela(560, 1500, 16, 0.4, "#ffb3d1") + brilhinho(842, 1490, 13, AMARELO, 1.2), (530, 1470, 870, 1530), z=7)

    # 01 artcode: o logo vermelho, a folha e um ingresso da versão
    print_adesivo(c, "foto-artcode.png", 36, 1676, 380, -3, z=5)
    c.img("recortes/washi-01.png", 4, 1664, 120, -32, z=6, px=300)
    cartao(c, 424, 1660, 1.5, "01", "artcode", LIMA,
           ["minha própria linguagem de programação,", "interpretada e escrita em Rust.", ("clica pra abrir o repo", ANIL)],
           [("Rust", "#ff8a5c", TINTA), ("interpretada", "#fff", TINTA), ("v0.5.1", TINTA, "#fff")], 11)
    ingresso = (f'<g transform="rotate(-6 200 1868)" filter="url(#sombra-leve)">'
                f'<path d="M80 1836 h240 v20 a12 12 0 0 0 0 24 v20 h-240 v-20 a12 12 0 0 0 0 -24 Z" fill="#ffb3d1" stroke="{TINTA}" stroke-width="2.5"/>'
                f'<line x1="256" y1="1840" x2="256" y2="1896" stroke="{TINTA}" stroke-width="2" stroke-dasharray="4 5"/>'
                f'<text x="98" y="1862" font-size="13" class="revista" fill="{TINTA}">PRÓXIMA PARADA</text>'
                f'<text x="98" y="1888" font-size="22" class="revista" fill="{TINTA}">v0.6</text>'
                f'<text x="166" y="1888" font-size="13" class="recibo" fill="{TINTA}">já tá saindo</text>'
                f'<circle cx="288" cy="1868" r="9" fill="{AMARELO}" stroke="{TINTA}" stroke-width="2.5"/></g>')
    c.add(ingresso, (70, 1820, 340, 1915), z=7)
    c.add(estrela(64, 1676, 20, 0.2) + brilhinho(410, 1700, 12, "#fff", 0.9), (30, 1640, 440, 1730), z=8)

    # 02 lover: a janela do jogo, com a setinha clicando no botão
    cartao(c, 40, 1934, -1.5, "02", "lover", "#ffb3d1",
           ["um jogo de quebra-cabeça em que", "o controle é o seu navegador.", ("clica pra jogar", ANIL)],
           [("32 páginas", AMARELO, TINTA), ("dois atos", "#fff", TINTA), ("navegador", AZUL_VIVO, "#fff")], 22)
    print_adesivo(c, "foto-lover.png", 446, 1920, 380, 3, z=5)
    c.img("recortes/washi-09.png", 736, 1902, 110, 34, z=6, px=300)
    bolha_ = (f'<g transform="rotate(8 760 1922)" filter="url(#sombra-leve)">'
              f'<path d="M700 1900 h110 q14 0 14 14 v18 q0 14 -14 14 h-70 l-18 16 l2 -16 h-24 q-14 0 -14 -14 v-18 q0 -14 14 -14 Z" fill="{ROSA}" stroke="{TINTA}" stroke-width="3"/>'
              f'<text x="755" y="1931" font-size="19" text-anchor="middle" class="bolha" fill="#fff">não fecha!</text></g>')
    c.add(bolha_, (680, 1880, 840, 1975), z=8)
    c.img("recortes/mao-pixel.png", 530, 2092, 40, -6, z=8, sombra="sombra-leve", px=140)
    c.add(coracao(436, 1952, 18, ROSA, -12) + coracao(838, 2118, 14, "#ff8a5c", 14), (410, 1925, 860, 2140), z=8)

    # 03 clios: o terminal, com as teclas dos atalhos
    print_adesivo(c, "foto-clios.png", 34, 2196, 360, -2.5, z=5, moldura=TINTA)
    c.img("recortes/washi-rasgada-07.png", 2, 2186, 120, -30, z=6, px=300)
    cartao(c, 428, 2214, 1.2, "03", "clios", "#fff",
           ["um desktop Linux feito pro terminal,", "com um binário em Rust.", ("clica pra abrir o repo", ANIL)],
           [("Arch", "#7fc8ff", TINTA), ("Hyprland", VERDE, TINTA), ("Quickshell", "#fff", TINTA)], 33)
    t1, w1 = tecla(260, 2404, "super", -6)
    t2, _ = tecla(260 + w1 + 6, 2410, "F2", 4, w=52)
    c.add(t1 + t2, (240, 2380, 420, 2470), z=8)

    # 04 hackintosh: o print do Acer com uma lupa em cima do "MacBook Pro"
    cartao(c, 40, 2480, -1.2, "04", "hackintosh", "#9fc4ff",
           ["macOS Sequoia num Acer Nitro V15,", "com o desktop acelerado na RTX 3050.", ("clica pra abrir o repo", ANIL)],
           [("macOS 15", "#fff", TINTA), ("OpenCore", AMARELO, TINTA), ("RTX 3050", VERDE, TINTA)], 44)
    print_adesivo(c, "foto-hackintosh.jpg", 450, 2470, 376, 2.5, z=5, lupa=(.5, .37, 50, 2.6, 560, 2600))
    c.img("recortes/washi-rasgada-02.png", 772, 2690, 110, -28, z=6, px=300)
    c.add(etiqueta(690, 2700, "psiu: é um Acer", "#fff", 5)[0], (680, 2690, 820, 2740), z=8)
    c.add(brilhinho(458, 2492, 14, AMARELO, 0.5) + estrela(842, 2496, 18, 1.4, "#9fc4ff"), (430, 2470, 870, 2520), z=8)

    # tem mais
    svg, cx_ = bilhete(250, 2742, 380, [("tem mais projetinhos no meu perfil", TINTA)], -1.5, cor=ROSA_BILHETE, pautado=False)
    c.add(svg, cx_, z=5)
    c.img("recortes/alfinete.png", 226, 2722, 92, -10, z=6, px=280)
    c.img("recortes/seta-pixel.png", 642, 2768, 34, -8, z=7, sombra="sombra-leve", px=120)
    c.add(brilhinho(694, 2756, 12, "#fff", 1.8), (670, 2730, 720, 2800), z=7)


def botao_88(x, y, linhas, fundo, cor, borda="#fff", icone=""):
    """Botãozinho 88x31 de site dos anos 2000, com borda em relevo."""
    s = [f'<rect x="{x}" y="{y}" width="88" height="31" fill="{fundo}"/>',
         f'<path d="M{x} {y + 31} V{y} H{x + 88}" fill="none" stroke="{borda}" stroke-width="2" opacity=".85"/>',
         f'<path d="M{x} {y + 31} H{x + 88} V{y}" fill="none" stroke="#000" stroke-width="2" opacity=".55"/>', icone]
    for i, (texto, px) in enumerate(linhas):
        s.append(f'<text x="{x + 44}" y="{y + 31 / 2 + (i - (len(linhas) - 1) / 2) * (px + 1) + px * .36:.1f}" font-size="{px}" '
                 f'text-anchor="middle" class="recibo" fill="{cor}">{t(texto)}</text>')
    return "".join(s)


def lua(cx, cy, r):
    """Lua minguante de adesivo, com o contorno grosso: um círculo menos outro deslocado."""
    def meia(rr, cor):
        return (f'<mask id="lua-{rr:.0f}"><circle cx="{cx}" cy="{cy}" r="{rr}" fill="#fff"/>'
                f'<circle cx="{cx + r * .5}" cy="{cy - r * .3}" r="{rr * .82}" fill="#000"/></mask>'
                f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{cor}" mask="url(#lua-{rr:.0f})"/>')
    return f'<g filter="url(#sombra-leve)">{meia(r + 3.5, TINTA)}{meia(r, AMARELO)}</g>'


def rodape(c):
    # céu de noite: lua e estrelinhas piscando
    c.add(lua(700, 4262, 28), (660, 4226, 740, 4300), z=2)
    for i, (sx, sy, sr, cor) in enumerate([(552, 4282, 10, "#fff"), (852, 4300, 12, AMARELO), (840, 4646, 9, "#fff"),
                                           (858, 4440, 9, "#ffb3d1")]):
        c.add(brilhinho(sx, sy, sr, cor, i * .8), (sx - 30, sy - 30, sx + 30, sy + 30), z=2)

    # o "Gostou?" num papel preto com borda branca e sombra dura, bem neobrutalista
    papel = ('<g transform="rotate(-2 330 4396)">'
             '<path d="M62 4290 L626 4274 L640 4560 L74 4580 Z" fill="#d3ec3c" stroke="#1d1c22" stroke-width="4" stroke-linejoin="round"/>'
             '<path d="M50 4278 L614 4262 L628 4548 L62 4568 Z" fill="#111" stroke="#fff" stroke-width="6" stroke-linejoin="round"/></g>')
    c.add(papel, (20, 4236, 660, 4600), z=3)
    c.img("recortes/gostou.png", 96, 4298, 372, -2, z=4, sombra=None)
    c.img("recortes/washi-04.png", 18, 4256, 120, -30, z=5, px=300)
    c.img("abraco-claude.png", 590, 4282, 262, 5, z=5, px=700)

    # a fileira de botõezinhos 88x31, que todo site pessoal tinha no rodapé
    coracao_px = '<path d="M{x} {y} h2 v-2 h2 v2 h2 v-2 h2 v2 h2 v4 h-2 v2 h-2 v2 h-2 v2 h-2 v-2 h-2 v-2 h-2 v-2 h-2 Z" fill="#ff5c8a"/>'
    botoes = [
        ([("feito à mão", 11), ("por kitsune", 11)], "#ffb3d1", TINTA, ""),
        ([("100% SVG", 13)], TINTA, LIMA, ""),
        ([("movido a", 10), ("lasanha", 13)], "#ff8a5c", TINTA, ""),
        ([("melhor visto", 10), ("em qualquer um", 10)], "#3f7cf4", "#fff", ""),
        ([("sem cookies", 12)], "#fff", TINTA, ""),
    ]
    bx, by, s = 0, 0, []
    for i, (linhas, fundo, cor, ic) in enumerate(botoes):
        s.append(f'<g transform="rotate({(-2, 1.5, -1, 2, -1.5)[i]} {bx + 44} {by + 15})">{botao_88(bx, by, linhas, fundo, cor, icone=ic)}</g>')
        bx += 96
    c.add(f'<g transform="translate(60 4606) scale(1.25)" filter="url(#sombra-leve)">{"".join(s)}</g>', (40, 4590, 680, 4660), z=6)
    c.add(fita(572, 4566, 264, 48, 2) + linha(606, 4599, "kitsuneislife, 2026", 22, TINTA, 'transform="rotate(2 700 4590)"'),
          (550, 4556, 850, 4626), z=6)


# cores das linguagens, as mesmas do GitHub
CORES_LING = {"JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5", "Rust": "#dea584",
              "PHP": "#4F5D95", "HTML": "#e34c26", "CSS": "#563d7c", "Svelte": "#ff3e00", "Shell": "#89e051",
              "Dart": "#00B4AB", "Java": "#b07219", "Kotlin": "#A97BFF", "C": "#555555", "C++": "#f34b7d",
              "Lua": "#000080", "QML": "#44a51c", "Vue": "#41b883", "SCSS": "#c6538c", "Go": "#00ADD8"}
CURSANDO = ["Dart", "Java", "Kotlin"]  # o que eu tô aprendendo, mesmo sem código ainda
EXTRAS = ["git", "npm", "Redis", "Express", "Docker", "Expo"]
BOLETIM_JSON = Path(__file__).resolve().parent.parent / "assets" / "readme" / "boletim.json"
BOLETIM_EXEMPLO = {
    "repos": 24, "estrelas": 31, "atualizado": None,
    "linguagens": {"JavaScript": {"bytes": 1840000, "repos": 12}, "Rust": {"bytes": 960000, "repos": 4},
                   "Svelte": {"bytes": 410000, "repos": 3}, "Python": {"bytes": 300000, "repos": 5},
                   "CSS": {"bytes": 260000, "repos": 9}, "HTML": {"bytes": 190000, "repos": 10},
                   "PHP": {"bytes": 120000, "repos": 2}, "Shell": {"bytes": 40000, "repos": 3}},
    "recentes": [{"nome": "artcode", "dias": 1}, {"nome": "clios", "dias": 3},
                 {"nome": "lover", "dias": 9}, {"nome": "kitsuneislife", "dias": 0}],
    "frequencia": {"dias": 365, "presente": 238, "contribuicoes": 1412},
}


def carregar_boletim():
    try:
        return json.loads(BOLETIM_JSON.read_text(encoding="utf-8")), False
    except (OSError, ValueError):
        return BOLETIM_EXEMPLO, True


def nota_de(b, maior):
    """A maior linguagem tira 10; as outras pela raiz quarta da proporção, de meio em meio ponto."""
    return round(20 * (b / maior) ** .25) / 2


def virgula(n):
    return f"{n:.1f}".replace(".", ",")


def boletim(c):
    d, exemplo = carregar_boletim()
    ling = sorted(d["linguagens"].items(), key=lambda kv: -kv[1]["bytes"])
    maior = ling[0][1]["bytes"] if ling else 1
    linhas = [(n, v["repos"], nota_de(v["bytes"], maior)) for n, v in ling[:8 - len(CURSANDO)]]
    for n in CURSANDO:
        if n not in d["linguagens"] and len(linhas) < 8:
            linhas.append((n, 0, None))

    # título, colado na beirada da folha amarela
    c.add(logo("o que eu sei fazer?", 40, 2872, 50, LIMA, [-4, 3, -2, 4, -3, 2, -4, 3, -2, 4, -3, 2, -4, 3, -2, 4, -3, 2, 3],
               [0, -4, 5, -3, 4, -5, 3, -2, 4, -4, 3, -3, 4, -5, 3, -2, 4, -3, 0]), (10, 2810, 620, 2900), z=9)

    x, y, w, rot = 30, 2904, 572, -1.2
    h = 236 + 30 * len(linhas) + 122
    s = [f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fbfaf4" filter="url(#sombra)"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#grade-azul)" opacity=".45"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="56" fill="{AZUL_VIVO}"/>',
         f'<text x="{x + 24}" y="{y + 39}" font-size="26" class="revista" fill="#fff">BOLETIM ESCOLAR</text>',
         f'<text x="{x + w - 24}" y="{y + 40}" font-size="28" text-anchor="end" class="bolha" fill="{AMARELO}" '
         f'stroke="{TINTA}" stroke-width="5" paint-order="stroke">2026</text>']

    def campo(cx, cy, rotulo, valor, largura):
        return (f'<text x="{cx}" y="{cy}" font-size="12" class="revista" fill="#6b6b78">{rotulo}</text>'
                f'<line x1="{cx}" y1="{cy + 30}" x2="{cx + largura}" y2="{cy + 30}" stroke="#9aa6bd" stroke-width="1.4"/>'
                + linha(cx + 4, cy + 26, valor, 23, ANIL))

    yy = y + 76
    s.append(campo(x + 24, yy, "ALUNO(A)", "kitsune", 300))
    s.append(campo(x + 24, yy + 46, "TURMA", "@kitsuneislife", 140))
    s.append(campo(x + 184, yy + 46, "REPOSITÓRIOS", str(d["repos"]), 140))
    fq = d.get("frequencia")
    if fq:
        pct = round(100 * fq["presente"] / max(1, fq["dias"]))
        s.append(campo(x + 24, yy + 92, "FREQUÊNCIA", f"{pct}%", 140))
        s.append(campo(x + 184, yy + 92, "FALTAS", f"{fq['dias'] - fq['presente']} dias", 140))
    else:
        s.append(campo(x + 24, yy + 92, "ESTRELAS DE BOM COMPORTAMENTO", str(d["estrelas"]), 300))
    # foto 3x4, presa com clipe
    s.append(f'<rect x="{x + w - 140}" y="{y + 72}" width="112" height="140" fill="#fff" stroke="#c9ccd6" stroke-width="1.5"/>'
             f'<image x="{x + w - 134}" y="{y + 78}" width="100" height="128" preserveAspectRatio="xMidYMid slice" '
             f'href="{imagem("3x4.png", 220)}"/>')

    # a tabela das notas
    ty = y + 212
    s.append(f'<rect x="{x + 16}" y="{ty}" width="{w - 32}" height="30" fill="{TINTA}"/>')
    for cx_, rot_, anc in [(x + 30, "MATÉRIA", "start"), (x + 300, "REPOS", "middle"), (x + 384, "NOTA", "middle"),
                           (x + w - 30, "SITUAÇÃO", "end")]:
        s.append(f'<text x="{cx_}" y="{ty + 21}" font-size="13" letter-spacing="1" text-anchor="{anc}" class="revista" fill="#fff">{rot_}</text>')
    for i, (nome, nrepos, nota) in enumerate(linhas):
        ly = ty + 30 + i * 30
        if i % 2:
            s.append(f'<rect x="{x + 16}" y="{ly}" width="{w - 32}" height="30" fill="#e9eefb" opacity=".8"/>')
        s.append(f'<line x1="{x + 16}" y1="{ly + 30}" x2="{x + w - 16}" y2="{ly + 30}" stroke="#c3cbe0" stroke-width="1"/>')
        s.append(f'<circle cx="{x + 38}" cy="{ly + 15}" r="6.5" fill="{CORES_LING.get(nome, "#bbb")}" stroke="{TINTA}" stroke-width="1.6"/>')
        s.append(f'<text x="{x + 54}" y="{ly + 21}" font-size="15" class="revista" fill="{TINTA}">{t(nome)}</text>')
        s.append(f'<text x="{x + 300}" y="{ly + 21}" font-size="15" text-anchor="middle" class="recibo" fill="{TINTA}">{nrepos or "-"}</text>')
        if nota is None:
            s.append(linha(x + 384, ly + 24, "—", 24, "#8a8a96", 'text-anchor="middle"'))
            sit, cor_sit, fundo_sit = "cursando", TINTA, AMARELO
        else:
            cor_nota = "#2f55d4" if nota >= 6 else "#d42f3a"
            s.append(linha(x + 384, ly + 24, virgula(nota), 24, cor_nota, f'text-anchor="middle" transform="rotate({(-3, 2, -1, 3)[i % 4]} {x + 384} {ly + 15})"'))
            sit, cor_sit, fundo_sit = ("aprovado", "#fff", "#2fa35a") if nota >= 6 else ("recuperação", "#fff", "#d42f3a")
        sw = medir("revista", sit, 11) + 18
        s.append(f'<rect x="{x + w - 30 - sw:.1f}" y="{ly + 5}" width="{sw:.1f}" height="20" rx="10" fill="{fundo_sit}" stroke="{TINTA}" stroke-width="1.6"/>'
                 f'<text x="{x + w - 30 - sw / 2:.1f}" y="{ly + 19}" font-size="11" text-anchor="middle" class="revista" fill="{cor_sit}">{sit}</text>')

    # observações do professor, de caneta vermelha
    oy = ty + 30 + len(linhas) * 30 + 24
    s.append(f'<text x="{x + 24}" y="{oy}" font-size="12" class="revista" fill="#6b6b78">OBSERVAÇÕES</text>')
    top = linhas[0][0] if linhas else "JavaScript"
    s.append(linha(x + 24, oy + 28, f"{top}: essa eh braba.", 23, "#d42f3a", f'transform="rotate(-1 {x + 200} {oy + 30})"'))
    s.append(linha(x + 24, oy + 54, "se você não sabe nem isso,", 21, "#d42f3a", f'transform="rotate(-1 {x + 200} {oy + 60})"'))
    s.append(linha(x + 24, oy + 80, "não recomendo continuar.", 21, "#d42f3a", f'transform="rotate(-1 {x + 200} {oy + 60})"'))
    rodape = f"atualizado em {d['atualizado']}" if d.get("atualizado") else "(dados de exemplo)"
    s.append(f'<text x="{x + w - 20}" y="{y + h - 14}" font-size="11" text-anchor="end" class="recibo" fill="#8a8a96">{t(rodape)}</text>')
    s.append("</g>")
    c.add("".join(s), caixa_girada(x, y, w, h, rot), z=6)
    c.img("recortes/clipe.png", x + w - 96, y + 52, 28, 8, z=7, px=120)

    # carimbo de aprovado, com tinta falhada
    sx, sy = x + w - 140, y + h - 70
    c.add(f'<g transform="rotate(-14 {sx} {sy})" filter="url(#carimbo)" opacity=".85">'
          f'<rect x="{sx - 108}" y="{sy - 34}" width="216" height="68" rx="10" fill="none" stroke="#d42f3a" stroke-width="6"/>'
          f'<rect x="{sx - 98}" y="{sy - 24}" width="196" height="48" rx="6" fill="none" stroke="#d42f3a" stroke-width="2"/>'
          f'<text x="{sx}" y="{sy + 13}" font-size="36" letter-spacing="4" text-anchor="middle" class="revista" fill="#d42f3a">APROVADO</text></g>',
          (sx - 140, sy - 80, sx + 140, sy + 80), z=8)
    c.add(fita(x + 210, y - 22, 150, 44, -3), (x + 190, y - 50, x + 380, y + 40), z=9)

    # do lado: o que eu uso além das linguagens, e os deveres de casa entregues
    nx, ny, nw = 626, 2930, 236
    tags, tx, ty2 = [], nx + 18, ny + 70
    for i, e in enumerate(EXTRAS):
        eti, ew = etiqueta(tx, ty2, e, ["#fff", AMARELO, "#7fc8ff", VERDE, "#ffb3d1", "#fff"][i % 6], (-3, 2, -2, 3)[i % 4], px=14)
        if tx + ew > nx + nw - 10:
            tx, ty2 = nx + 18, ty2 + 42
            eti, ew = etiqueta(tx, ty2, e, ["#fff", AMARELO, "#7fc8ff", VERDE, "#ffb3d1", "#fff"][i % 6], (-3, 2, -2, 3)[i % 4], px=14)
        tags.append(eti)
        tx += ew + 8
    nh = ty2 - ny + 64
    c.add(f'<g transform="rotate(2.5 {nx + nw / 2} {ny + nh / 2})"><rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" fill="{ROSA_BILHETE}" filter="url(#sombra)"/>'
          + linha(nx + 18, ny + 44, "atividades extras", 24, TINTA) + "".join(tags) + "</g>",
          caixa_girada(nx, ny, nw, nh, 2.5), z=6)
    c.img("recortes/tachinha-vermelha.png", nx + nw / 2 - 16, ny - 34, 38, -8, z=7, px=140)

    ay = ny + nh + 34
    rec = d.get("recentes", [])[:4]
    ah = 70 + 40 * len(rec) + 20
    a = [f'<g transform="rotate(-2 {nx + nw / 2} {ay + ah / 2})"><rect x="{nx}" y="{ay}" width="{nw}" height="{ah}" fill="#fff" filter="url(#sombra)"/>']
    for i in range(len(rec) + 1):
        a.append(f'<line x1="{nx}" y1="{ay + 58 + i * 40}" x2="{nx + nw}" y2="{ay + 58 + i * 40}" stroke="{PAUTA}" stroke-width="1.3"/>')
    a.append(f'<line x1="{nx + 32}" y1="{ay}" x2="{nx + 32}" y2="{ay + ah}" stroke="#f0a0aa" stroke-width="1.5"/>')
    a.append(linha(nx + 42, ay + 44, "deveres entregues", 23, TINTA))
    for i, r in enumerate(rec):
        ry = ay + 88 + i * 40
        quando = "hoje" if r["dias"] == 0 else ("ontem" if r["dias"] == 1 else f"há {r['dias']} dias")
        nome = r["nome"] if len(r["nome"]) <= 14 else r["nome"][:13] + "…"
        a.append(f'<path d="M{nx + 10} {ry - 8} l6 7 l11 -14" fill="none" stroke="#2fa35a" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
        a.append(linha(nx + 42, ry, nome, 21, ANIL))
        a.append(linha(nx + nw - 12, ry, quando, 17, "#6b6b78", 'text-anchor="end"'))
    a.append("</g>")
    c.add("".join(a), caixa_girada(nx, ay, nw, ah, -2), z=6)
    c.add(fita(nx + 60, ay - 18, 110, 36, 4), (nx + 40, ay - 40, nx + 190, ay + 30), z=7)
    c.img("recortes/lacre.png", nx + nw - 44, ay + ah - 22, 66, 12, z=8, px=200)
    c.img("recortes/caneta.png", x + w - 150, y + h - 150, 80, 34, z=9, px=220)
    c.img("recortes/regua.png", -46, y + h - 170, 190, 0, z=5, px=420)
    c.img("recortes/lapis.png", nx + 20, ay + ah + 8, 150, -4, z=8, px=340)
    c.add(estrela(640, ay + ah + 74, 16, 0.6, "#ffb3d1") + brilhinho(612, ay + ah + 40, 12, AMARELO, 1.6),
          (590, ay + ah - 10, 875, ay + ah + 60), z=8)


# ---------------------------------------------------------------- fundo e saída

def fundo(y0, h):
    return (f'<rect x="0" y="{y0}" width="{W}" height="{h}" fill="url(#ceu)"/>'
            f'<rect x="0" y="{y0}" width="{W}" height="{h}" fill="url(#pontos)" mask="url(#some)"/>')


DEFS_CENA = f"""
<linearGradient id="ceu" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{H}">
  <stop offset="0" stop-color="{CEU_TOPO}"/><stop offset=".12" stop-color="#7fbdf3"/>
  <stop offset=".3" stop-color="{CEU_MEIO}"/><stop offset=".5" stop-color="#78b8f2"/>
  <stop offset=".64" stop-color="{CEU_MEIO}"/><stop offset=".74" stop-color="#f4b6c8"/>
  <stop offset=".81" stop-color="#9a86dc"/><stop offset=".89" stop-color="#2d3a82"/>
  <stop offset="1" stop-color="#121a44"/>
</linearGradient>
<pattern id="pontos" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.7" fill="#fff"/></pattern>
<linearGradient id="g-some" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">
  <stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".45" stop-color="#fff" stop-opacity=".06"/>
  <stop offset="1" stop-color="#fff" stop-opacity=".3"/>
</linearGradient>
<mask id="some" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#g-some)"/></mask>
<pattern id="grade-azul" width="18" height="18" patternUnits="userSpaceOnUse">
  <path d="M18 0 H0 V18" fill="none" stroke="#bcd3f2" stroke-width="1" opacity=".7"/>
</pattern>
<pattern id="quadriculado" width="24" height="24" patternUnits="userSpaceOnUse">
  <path d="M24 0 H0 V24" fill="none" stroke="#c9b92c" stroke-width="1" opacity=".55"/>
</pattern>
<pattern id="xadrez" width="20" height="20" patternUnits="userSpaceOnUse">
  <rect width="20" height="20" fill="#fff"/><rect width="10" height="10" fill="{TINTA}"/><rect x="10" y="10" width="10" height="10" fill="{TINTA}"/>
</pattern>
<filter id="carimbo" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="3" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.5" result="m"/>
  <feComposite in="SourceGraphic" in2="m" operator="in"/>
</filter>
<clipPath id="borda"><rect x="0" y="0" width="{W}" height="{H}" rx="22"/></clipPath>
"""

CSS = """
.deriva{animation:deriva 18s ease-in-out infinite alternate}
.deriva-2{animation:deriva 22s ease-in-out infinite alternate-reverse}
@keyframes deriva{from{transform:translateX(-14px)}to{transform:translateX(18px)}}
.flutua{animation:flutua 4.6s ease-in-out infinite}
@keyframes flutua{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
.brilho{transform-box:fill-box;transform-origin:center;animation:brilho 3.4s ease-in-out infinite}
@keyframes brilho{0%,70%,100%{transform:scale(1) rotate(0)}80%{transform:scale(1.2) rotate(10deg)}}
.letreiro{animation:letreiro 22s linear infinite}
@keyframes letreiro{to{transform:translateX(var(--volta))}}
"""


def gerar(so=None):
    cena = montar()
    for nome, y0, h, _link, alt in TIRAS:
        if so and nome not in so:
            continue
        dentro = sorted((e for e in cena.els if e[2][1] < y0 + h and e[2][3] > y0), key=lambda e: (e[0], e[1]))
        corpo = (f'<g clip-path="url(#borda)">{fundo(y0, h)}' + "".join(e[3] for e in dentro) + "</g>")
        salvar(f"colagem-{nome}.svg", W, h, f"<defs>{DEFS_CENA}</defs>{corpo}", CSS, alt, viewbox=f"0 {y0} {W} {h}")


def readme():
    """As linhas do README que montam a colagem."""
    partes = []
    for nome, _y, _h, link, alt in TIRAS:
        img = f'<img src="assets/readme/colagem-{nome}.svg" width="100%" align="left" alt="{t(alt)}">'
        partes.append(f'<a href="{link}">{img}</a>' if link else img)
    return "".join(partes)


if __name__ == "__main__":
    gerar()
