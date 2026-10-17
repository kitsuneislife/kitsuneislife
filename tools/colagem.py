"""A colagem do README: uma cena só, fatiada em tiras.

    python tools/colagem.py

A cena inteira tem 880 de largura. Cada tira é a mesma cena com outro viewBox,
levando só os elementos que encostam nela, então o que atravessa a emenda
aparece certinho dos dois lados. No README as tiras ficam com align="left"
e width="100%", que é o jeito de o GitHub empilhar imagem sem fresta.

O recibo da semana é desenhado aqui também (tira "musica"); tools/recibo.py
busca os dados no Last.fm e chama gerar(dados, so=["musica"]).
"""
import math
from datetime import datetime, timedelta, timezone

from kit import (AMARELO, ANIL, CRACHA, LIMA, PAUTA, TINTA, fita, imagem,
                 linha, medir, salvar, t, tamanho)

W = 880
CEU_TOPO, CEU_MEIO, CEU_FUNDO = "#3d8ce6", "#9fd2fa", "#4f9ae9"

# nome, y inicial, altura, link, descrição (alt)
TIRAS = [
    ("capa", 0, 440, None,
     "kitsuneislife, escrito em letra de adesivo, num céu azul com nuvens de papelão. "
     "Um arco-íris de papelão e eu sentado numa nuvem, de fone. ようこそ!"),
    ("bio", 440, 400, "https://github.com/kitsuneislife?tab=repositories",
     "Uma prancheta com um bilhete: Nunca soube o que escrever em uma bio ou em um sobre-mim. Curioso né? "
     "Então fiz essa página pra contar um pouquinho de quem sou eu. Eu gosto de fazer alguns projetinhos "
     "(e de lasanha) e quero trabalhar na área. Discord: @thurzinhos. “Penso, logo desisto.” love you forever. "
     "Do lado, a turma correndo com uma placa: clica aqui."),
    ("tempo", 840, 380, None,
     "Eu em 2016, com 8 anos, e eu em 2026, com 18, rodeado de cabecinhas de Nendoroid."),
    ("projetos", 1220, 180, "https://github.com/kitsuneislife?tab=repositories",
     "projetinhos (e de lasanha). Clica nos cards pra abrir cada um."),
    ("artcode", 1400, 270, "https://github.com/kitsuneislife/artcode",
     "artcode: minha própria linguagem de programação, interpretada e escrita em Rust. Tá na v0.5.1."),
    ("lover", 1670, 270, "https://kitsuneislife.github.io/lover/",
     "lover: um jogo de quebra-cabeça em que o controle é o seu navegador. Clica pra jogar."),
    ("clios", 1940, 270, "https://github.com/kitsuneislife/clios",
     "clios: um desktop Linux feito pro terminal. Arch, Hyprland e Quickshell, com um binário em Rust."),
    ("hackintosh", 2210, 270, "https://github.com/kitsuneislife/Acer-Nitro-V15-ANV15-51-Hackintosh",
     "Hackintosh: macOS Sequoia num Acer Nitro V15, com o desktop acelerado na RTX 3050."),
    ("mais", 2480, 110, "https://github.com/kitsuneislife?tab=repositories",
     "Tem mais projetinhos no meu perfil."),
    ("habilidades", 2590, 690, None,
     "O que eu sei fazer: JavaScript (essa eh braba), Python, PHP, HTML, CSS, Svelte, React. "
     "Aprendendo Dart, Java, Kotlin e Rust. Ferramentas: git, npm, Redis, Express, Docker, Expo. "
     "Se você não sabe nem isso, não recomendo continuar. So cold..."),
    ("musica", 3280, 720, None, "Recibo da semana com as músicas que eu mais ouvi nos últimos 7 dias."),
    ("fim", 4000, 380, None,
     "Gostou? Sei fazer bem mais. Eu abraçando uma pelúcia do Claude. kitsuneislife, 2026."),
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


def foto(cena, nome, x, y, w, rot, z, moldura="#fff", pad=12, rodape=12):
    """Foto impressa com borda, como polaroid ou print."""
    iw, ih = tamanho(nome)
    h = w * ih / iw
    fw, fh = w + 2 * pad, h + pad + rodape
    cx, cy = x + fw / 2, y + fh / 2
    uri = imagem(nome, min(iw, round(w * 2)))
    svg = (f'<g transform="rotate({rot} {cx:.1f} {cy:.1f})">'
           f'<rect x="{x}" y="{y}" width="{fw:.1f}" height="{fh:.1f}" fill="{moldura}" filter="url(#sombra)"/>'
           f'<image x="{x + pad}" y="{y + pad}" width="{w}" height="{h:.1f}" href="{uri}" preserveAspectRatio="xMidYMid slice"/></g>')
    cena.add(svg, caixa_girada(x, y, fw, fh, rot), z)
    return fw, fh


# ---------------------------------------------------------------- a cena

def montar(dados_recibo):
    c = Cena()

    # nuvens de papelão no fundo
    for nome_, x, y, w, rot, cl in [("nuvem.png", -70, 30, 300, -4, "deriva"), ("nuvem.png", 640, -10, 270, 6, "deriva-2"),
                                    ("nuvem.png", 700, 1180, 220, -6, ""), ("nuvem.png", -60, 1700, 230, 5, ""),
                                    ("nuvem.png", 690, 2600, 240, -3, ""), ("nuvem.png", -80, 3500, 260, 4, ""),
                                    ("nuvem.png", 650, 4100, 250, -5, "")]:
        c.img(nome_, x, y, w, rot, z=0, classe=cl, sombra=None)

    # ---- capa
    c.img("arco-iris.png", 450, 150, 420, -4, z=1)
    # uma nuvem em cada pé do arco-íris, e eu sentado onde elas se encontram
    c.img("nuvem.png", 410, 288, 280, -3, z=2, sombra="sombra-leve")
    c.img("nuvem.png", 660, 270, 260, 4, z=2, sombra="sombra-leve")
    c.img("sentado.png", 590, 120, 210, 0, z=3, classe="flutua", px=411)
    bolha_ = ('<g transform="rotate(-7 150 70)"><path d="M70 40 h170 q18 0 18 18 v34 q0 18 -18 18 h-120 l-22 22 l4 -22 h-32 '
              'q-18 0 -18 -18 v-34 q0 -18 18 -18 Z" fill="#fff" stroke="#1d1c22" stroke-width="4" filter="url(#sombra-leve)"/>'
              f'<text x="155" y="87" font-size="30" text-anchor="middle" class="revista" fill="{CRACHA}">ようこそ!</text></g>')
    c.add(bolha_, (40, 20, 280, 150), z=6)
    giros = [-6, 4, -3, 5, -4, 3, -5, 6, -2, 4, -6, 3, -4]
    sobe = [0, -6, 8, -4, 6, -8, 5, -3, 7, -6, 4, -5, 6]
    c.add(logo("kitsuneislife", 34, 236, 92, LIMA, giros, sobe), (0, 120, 760, 300), z=7)
    for i, (sx, sy, sr) in enumerate([(700, 120, 26), (40, 300, 18), (430, 120, 14), (560, 330, 16)]):
        c.add(estrela(sx, sy, sr, i * 0.7), (sx - 40, sy - 40, sx + 40, sy + 40), z=8)

    # ---- bio
    # o export da prancheta já vem cortado na esquerda e embaixo: encosta na borda
    # e as nuvens cobrem o corte de baixo
    c.img("banner-bio.png", 0, 516, 880, 0, z=4, sombra="sombra", px=1238)
    for x, y, w, rot in [(-40, 914, 250, 3), (186, 940, 236, -1), (400, 918, 250, 4), (630, 910, 260, -3)]:
        c.img("nuvem.png", x, y, w, rot, z=7, sombra="sombra-leve")
    c.img("recortes/croissant.png", 744, 990, 110, 14, z=8)

    # ---- 2016 → 2026
    c.img("eu-2016.png", 70, 1110, 172, -2, z=3, px=205)
    c.img("eu-2026.png", 620, 1076, 186, 2, z=3, px=312)
    anos = (f'<text x="262" y="1210" font-size="56" class="revista" fill="#fff" stroke="{TINTA}" stroke-width="7" paint-order="stroke">2016</text>'
            + linha(270, 1250, "8 anos", 26, TINTA)
            + f'<text x="606" y="1392" font-size="56" text-anchor="end" class="revista" fill="#fff" stroke="{TINTA}" stroke-width="7" paint-order="stroke">2026</text>'
            + linha(598, 1432, "18 anos", 26, TINTA, 'text-anchor="end"')
            + f'<path d="M300 1280 C 360 1360, 440 1250, 520 1316" fill="none" stroke="{TINTA}" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="2 10"/>'
            + f'<path d="M506 1302 l18 14 l-21 7" fill="none" stroke="{TINTA}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    c.add(anos, (240, 1140, 640, 1450), z=4)
    for nome_, x, y, w, rot in [("recortes/deku.png", 506, 1104, 86, -8), ("recortes/hinata.png", 790, 1082, 88, 10),
                                ("recortes/killua.png", 792, 1300, 88, -6), ("recortes/gon.png", 500, 1196, 76, 6),
                                ("recortes/bakugo.png", 400, 1092, 84, -12)]:
        c.img(nome_, x, y, w, rot, z=5)

    # ---- projetinhos
    c.add(logo("projetinhos", 40, 1562, 74, "#ffb3d1", giros[1:], sobe[2:]), (10, 1480, 600, 1610), z=6)
    c.add(fita(62, 1578, 240, 46, -2) + linha(92, 1609, "(e de lasanha)", 22, TINTA, 'transform="rotate(-2 180 1600)"'),
          (50, 1570, 320, 1630), z=7)
    svg, cx_ = bilhete(600, 1508, 220, [("clica nos cards", TINTA), ("pra abrir cada um", "#5a5a63")], 4, cor="#eef08a", pautado=False, px=20)
    c.add(svg, cx_, z=6)
    c.img("recortes/tachinha.png", 776, 1486, 38, 8, z=7)

    def projeto(y0, nome_foto, lado, titulo, linhas, rot, deco, moldura="#fff", rodape=12, cor_titulo=LIMA, extra=""):
        larg = 360
        if lado == "esq":
            fx, nx = 46, 466
        else:
            fx, nx = 450, 46
        fw, fh = foto(c, nome_foto, fx, y0 + 18, larg, rot, z=4, moldura=moldura, rodape=rodape)
        c.add(fita(fx + fw / 2 - 56, y0 + 2, 112, 36, rot * 2), (fx, y0 - 20, fx + fw, y0 + 50), z=5)
        tx = fx + 10 if lado == "esq" else fx + 20
        g = [-4, 3, -2, 4, -3, 2, -4, 3, -2, 4]
        c.add(logo(titulo, tx, y0 + 56, 44, cor_titulo, g, [0] * 12), (tx - 20, y0, tx + 380, y0 + 80), z=6)
        svg, cx_ = bilhete(nx, y0 + 70, 372, linhas, -rot * 0.7, px=20)
        c.add(svg + extra, cx_, z=5)
        c.img("recortes/clipe.png", nx + 336, y0 + 34, 26, 6 if lado == "esq" else -6, z=6, px=120)
        n, dx, dy, dw, drot = deco
        c.img(n, dx, y0 + dy, dw, drot, z=6)

    projeto(1640, "foto-artcode.png", "esq", "artcode",
            ["minha própria linguagem de programação,", "interpretada e escrita em Rust.",
             "tá na v0.5.1, e a v0.6 já tá saindo.", ("clica pra abrir o repo", ANIL)],
            -3, ("recortes/waffle.png", 760, 168, 104, 10))
    projeto(1910, "foto-lover.png", "dir", "lover",
            ["um jogo de quebra-cabeça em que", "o controle é o seu navegador.", "são 32 páginas em dois atos.",
             ("clica pra jogar", ANIL)],
            3, ("recortes/pizza.png", 330, 196, 104, -12), cor_titulo="#ffb3d1")
    projeto(2180, "foto-clios.png", "esq", "clios",
            ["um desktop Linux feito pro terminal.", "Arch, Hyprland e Quickshell,", "com um binário em Rust.",
             ("clica pra abrir o repo", ANIL)],
            -2, ("recortes/taiyaki.png", 752, 176, 116, 8), moldura="#000", cor_titulo="#fff")
    projeto(2450, "foto-hackintosh.jpg", "dir", "hackintosh",
            ["macOS Sequoia num Acer Nitro V15,", "com o desktop acelerado na RTX 3050.",
             ("clica pra abrir o repo", ANIL)],
            2.5, ("recortes/ovo.png", 360, 170, 96, -8), rodape=40, cor_titulo="#9fc4ff")
    svg, cx_ = bilhete(250, 2738, 380, [("tem mais projetinhos no meu perfil", TINTA)], -1.5, cor="#eef08a", pautado=False)
    c.add(svg, cx_, z=5)
    c.img("recortes/leite-caixinha.png", 650, 2722, 62, 10, z=6)
    c.img("recortes/tachinha.png", 578, 2708, 40, -6, z=6)

    # ---- o que eu sei fazer (a prancheta do banner antigo)
    c.img("banner-habilidades.png", 18, 2856, 848, 0.8, z=4, sombra="sombra", px=1124)
    c.img("recortes/panqueca-urso.png", -10, 3380, 150, -6, z=6)

    # ---- música
    musica(c, 3520, dados_recibo)

    # ---- fim
    papel = ('<g transform="rotate(-2 330 4390)"><path d="M48 4272 L612 4256 L626 4500 L60 4522 Z" fill="#111" filter="url(#sombra)"/></g>')
    c.add(papel, (20, 4230, 660, 4550), z=3)
    c.img("recortes/gostou.png", 96, 4296, 430, -2, z=4, sombra=None)
    c.img("abraco-claude.png", 584, 4250, 270, 5, z=5, px=700)
    c.add(fita(550, 4538, 264, 48, 2) + linha(584, 4571, "kitsuneislife, 2026", 22, TINTA, 'transform="rotate(2 680 4563)"'),
          (540, 4530, 820, 4590), z=6)
    # a bio e tudo que vem depois sobem 240, pra prancheta encaixar embaixo da capa
    c.subir(470, 240)
    return c


def musica(c, y0, d):
    exemplo = d is None
    if exemplo:
        d = {"faixas": [("Mitski", "My Love Mine All Mine", 31), ("Lorde", "Broken Glass", 27),
                        ("Sabrina Carpenter", "Manchild", 22), ("Mitski", "Where's My Phone?", 19),
                        ("Billie Eilish", "Birds of a Feather", 15), ("Lorde", "What Was That", 13)], "total": 214}
    faixas = (d["faixas"] or [("—", "nada tocou essa semana", 0)])[:6]
    hoje = datetime.now(timezone(timedelta(hours=-3)))
    inicio = hoje - timedelta(days=7)

    # título
    c.add(fita(36, y0, medir("revista", "no fone essa semana", 28) + 96, 58, -2, preta=True, opacidade=1) +
          f'<text x="72" y="{y0 + 40}" font-size="28" class="revista" fill="#fff" transform="rotate(-2 210 {y0 + 28})">no fone essa semana</text>',
          (30, y0 - 10, 400, y0 + 70), z=7)

    x0, lw = 64, 300
    py = y0 + 74
    alt_papel = 236 + 44 * len(faixas) + 112
    p = []
    dentes = "".join(f"L{x0 + i * 10 + 5} {py + alt_papel + 8} L{x0 + (i + 1) * 10} {py + alt_papel} " for i in range(lw // 10))
    p.append(f'<path d="M{x0} {py} H{x0 + lw} V{py + alt_papel} {dentes} L{x0} {py + alt_papel} Z" fill="#fbfbf6" filter="url(#sombra)"/>')
    cx = x0 + lw / 2

    def r(x, y, s, px, cor=TINTA, anc="start"):
        return f'<text x="{x}" y="{y}" font-size="{px}" text-anchor="{anc}" fill="{cor}" class="recibo">{t(s)}</text>'

    p.append(r(cx, py + 50, "KITSUNEISLIFE", 24, anc="middle"))
    p.append(r(cx, py + 76, "RECIBO DA SEMANA", 14, anc="middle"))
    p.append(r(cx, py + 98, f"{inicio:%d/%m/%Y} - {hoje:%d/%m/%Y}", 13, "#55555c", "middle"))
    p.append(r(x0 + 16, py + 126, "-" * 31, 13, "#55555c"))
    p.append(r(x0 + 16, py + 150, "#  FAIXA", 13))
    p.append(r(x0 + lw - 16, py + 150, "PLAYS", 13, anc="end"))
    y = py + 184
    for i, (artista, faixa, plays) in enumerate(faixas, 1):
        nome_f = faixa.upper() if len(faixa) <= 21 else faixa.upper()[:20] + "…"
        art = artista if len(artista) <= 26 else artista[:25] + "…"
        p.append(r(x0 + 16, y, f"{i:02d} {nome_f}", 14))
        p.append(r(x0 + lw - 16, y, str(plays), 14, anc="end"))
        p.append(r(x0 + 42, y + 18, art, 12, "#6b6b73"))
        y += 44
    p.append(r(x0 + 16, y, "-" * 31, 13, "#55555c"))
    p.append(r(x0 + 16, y + 26, "TOTAL DE PLAYS", 15))
    p.append(r(x0 + lw - 16, y + 26, str(d["total"]), 15, anc="end"))
    semente, bx, barras = d["total"] * 7919, x0 + 36, []
    for i in range(44):
        semente = (semente * 1103515245 + 12345) % 2 ** 31
        w = 1 + semente % 4
        if i % 2 == 0:
            barras.append(f'<rect x="{bx}" y="{y + 44}" width="{w}" height="40" fill="{TINTA}"/>')
        bx += w + 1
    p.append("".join(barras))
    p.append(r(cx, y + 104, "OBRIGADO POR OUVIR :)", 13, "#55555c", "middle"))

    impressora = (f'<rect x="{x0 - 22}" y="{py - 18}" width="{lw + 44}" height="24" rx="12" fill="#2f2f36" filter="url(#sombra-leve)"/>'
                  f'<rect x="{x0 - 8}" y="{py - 8}" width="{lw + 16}" height="5" rx="2.5" fill="#111"/>')
    c.add(f'<clipPath id="saida"><rect x="{x0 - 30}" y="{py - 4}" width="{lw + 60}" height="{alt_papel + 60}"/></clipPath>'
          f'<g clip-path="url(#saida)"><g class="imprime">{"".join(p)}</g></g>' + impressora,
          (x0 - 30, py - 30, x0 + lw + 30, py + alt_papel + 40), z=5)

    c.img("fone.png", 376, y0 + 190, 160, 0, z=6, px=208)

    nx, ny, nw, nh = 520, y0 + 84, 330, 430
    n = [f'<g transform="rotate(2 {nx + nw / 2} {ny + nh / 2})">',
         f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="4" fill="#fff" filter="url(#sombra)"/>']
    for i in range(9):
        n.append(f'<line x1="{nx}" y1="{ny + 80 + i * 40}" x2="{nx + nw}" y2="{ny + 80 + i * 40}" stroke="{PAUTA}" stroke-width="1.4"/>')
    for i in range(12):
        yy = ny + 22 + i * 34
        n.append(f'<circle cx="{nx + 2}" cy="{yy}" r="5" fill="#e9e9ee"/>'
                 f'<path d="M{nx - 12} {yy - 4} q14 -8 18 4" fill="none" stroke="#8d94a0" stroke-width="3.5" stroke-linecap="round"/>')
    soma = {}
    for a, _, pl in faixas:
        soma[a] = soma.get(a, 0) + pl
    top = max(soma, key=soma.get)
    top = top if len(top) <= 16 else top[:15] + "…"
    mais = faixas[0][1] if len(faixas[0][1]) <= 24 else faixas[0][1][:23] + "…"
    n.append(linha(nx + 32, ny + 70, "essa semana deu", 23, "#5a5a63"))
    n.append(linha(nx + 32, ny + 148, top, 44, TINTA))
    n.append(linha(nx + 32, ny + 190, "no repeat.", 23, "#5a5a63"))
    n.append(linha(nx + 32, ny + 270, "mais tocada:", 21, "#5a5a63"))
    n.append(linha(nx + 32, ny + 308, mais, 25, ANIL))
    n.append(linha(nx + 32, ny + 388, f"{d['total']} plays em 7 dias", 21, "#5a5a63"))
    if exemplo:
        sx, sy = nx + nw - 92, ny + 104
        n.append(f'<g transform="rotate(-9 {sx} {sy})"><rect x="{sx - 84}" y="{sy - 24}" width="168" height="48" rx="6" '
                 f'fill="none" stroke="{CRACHA}" stroke-width="4" opacity=".8"/>'
                 f'<text x="{sx}" y="{sy + 11}" font-size="28" text-anchor="middle" fill="{CRACHA}" opacity=".8" class="bolha">EXEMPLO</text></g>')
    n.append("</g>")
    c.add("".join(n), (nx - 30, ny - 30, nx + nw + 30, ny + nh + 30), z=5)
    c.img("recortes/tachinha.png", nx + nw / 2 - 18, ny - 30, 46, -10, z=6)
    c.img("recortes/bolo-morango.png", 470, y0 + 506, 112, -8, z=7)
    c.img("recortes/leite-garrafa.png", 812, y0 + 470, 58, 8, z=7)


# ---------------------------------------------------------------- fundo e saída

def fundo(y0, h):
    return (f'<rect x="0" y="{y0}" width="{W}" height="{h}" fill="url(#ceu)"/>'
            f'<rect x="0" y="{y0}" width="{W}" height="{h}" fill="url(#pontos)" mask="url(#some)"/>')


DEFS_CENA = f"""
<linearGradient id="ceu" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{H}">
  <stop offset="0" stop-color="{CEU_TOPO}"/><stop offset=".12" stop-color="#7fbdf3"/>
  <stop offset=".3" stop-color="{CEU_MEIO}"/><stop offset=".5" stop-color="#78b8f2"/>
  <stop offset=".7" stop-color="{CEU_MEIO}"/><stop offset=".9" stop-color="#78b8f2"/>
  <stop offset="1" stop-color="{CEU_FUNDO}"/>
</linearGradient>
<pattern id="pontos" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.7" fill="#fff"/></pattern>
<linearGradient id="g-some" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">
  <stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".45" stop-color="#fff" stop-opacity=".06"/>
  <stop offset="1" stop-color="#fff" stop-opacity=".3"/>
</linearGradient>
<mask id="some" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#g-some)"/></mask>
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
.imprime{animation:imprime 2.8s cubic-bezier(.3,.7,.4,1) .3s both}
@keyframes imprime{from{transform:translateY(-640px)}to{transform:translateY(0)}}
"""


def gerar(dados_recibo=None, so=None):
    cena = montar(dados_recibo)
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
