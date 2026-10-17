"""Gera os SVGs fixos do README em assets/readme/.

    python tools/build.py

O recibo da semana tem gerador próprio (tools/recibo.py), que roda no Actions.
"""
from kit import (AMARELO, ANIL, AZUL, CORTICA, CRACHA, LARANJA, LIMA, MANILA,
                 MANILA_ESCURO, MARGEM, PAPEL, PAUTA, TINTA, fita, icone,
                 imagem, linha, medir, salvar, t, tamanho)


def estrela(cx, cy, r, classe="", atraso=0):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    estilo = f' style="animation-delay:{atraso}s"' if atraso else ""
    return (f'<polygon class="{classe}"{estilo} points="{" ".join(pts)}" fill="{AMARELO}" '
            f'stroke="{TINTA}" stroke-width="3.5" stroke-linejoin="round"/>')


def titulo_adesivo(x, y, texto, px, angulo=0, preenchimento="#fff", ancora="start"):
    """Título no estilo do banner: letra branca, contorno grosso e sombra deslocada."""
    a = f'transform="rotate({angulo} {x} {y})"' if angulo else ""
    base = f'x="{x}" y="{y}" font-size="{px}" text-anchor="{ancora}" class="titulo"'
    return (f'<g {a}>'
            f'<text {base} dx="5" dy="6" fill="{TINTA}" stroke="{TINTA}" stroke-width="{px * .15:.1f}" '
            f'stroke-linejoin="round">{t(texto)}</text>'
            f'<text {base} fill="{preenchimento}" stroke="{TINTA}" stroke-width="{px * .13:.1f}" '
            f'stroke-linejoin="round" paint-order="stroke">{t(texto)}</text></g>')


# ---------------------------------------------------------------- capa

def capa():
    W, H = 880, 640
    c = []
    # pasta
    c.append(f'<g transform="rotate(-1.4 440 340)" filter="url(#sombra)">'
             f'<path d="M40 114 q0-16 16-16 h520 l14-27 q5-9 15-9 h224 q14 0 14 14 v536 q0 16-16 16 H56 q-16 0-16-16 Z" fill="{MANILA_ESCURO}"/>'
             f'<rect x="40" y="98" width="800" height="520" rx="16" fill="{MANILA}" filter="url(#papel)"/>'
             f'</g>')
    c.append(linha(612, 88, "arquivo: kitsune", 22, "#6b4f22", 'transform="rotate(-1.4 440 340)"'))
    # folha de trás
    c.append(f'<rect x="318" y="112" width="520" height="470" fill="#fff" transform="rotate(4.5 580 350)" filter="url(#sombra-leve)"/>')
    # folha principal, pautada
    folha = [f'<rect x="298" y="98" width="552" height="500" fill="{PAPEL}" filter="url(#sombra)"/>']
    for i in range(8):
        y = 236 + i * 44
        folha.append(f'<line x1="298" y1="{y}" x2="850" y2="{y}" stroke="{PAUTA}" stroke-width="1.6"/>')
    folha.append(f'<line x1="338" y1="98" x2="338" y2="598" stroke="{MARGEM}" stroke-width="1.6"/>')
    # clipe de papel
    folha.append('<path d="M352 150 V78 q0-18 17-18 q17 0 17 18 V160 q0 12-11 12 q-11 0-11-12 V92" '
                 'fill="none" stroke="#9aa0ab" stroke-width="5" stroke-linecap="round"/>')
    folha.append('<path d="M352 150 V78 q0-18 17-18 q17 0 17 18 V160 q0 12-11 12 q-11 0-11-12 V92" '
                 'fill="none" stroke="#e7eaf0" stroke-width="1.6" stroke-linecap="round"/>')
    folha.append(estrela(424, 140, 30, "brilho"))
    folha.append(estrela(398, 186, 18, "brilho", 0.6))
    folha.append(estrela(456, 98, 13, "brilho", 1.2))
    folha.append(titulo_adesivo(478, 196, "KITSUNEISLIFE", 58, -4))
    bio = [
        (273, "Costumam escrever muitas coisas por aqui, né?"),
        (317, "Tem gente que quer falar sobre o quanto eh bom, ou"),
        (361, "o quanto eh apaixonado pelo que faz.."),
        (449, "Bom, eu gosto de fazer alguns projetinhos e"),
        (493, "quero trabalhar na área"),
    ]
    for y, s in bio:
        folha.append(linha(352, y, s, 21.5))
    folha.append(linha(628, 420, "( e de lasanha )", 15))
    folha.append(linha(616, 488, "( . o . )", 19))
    folha.append(f'<path d="M640 500 q4 26 34 20" fill="none" stroke="{TINTA}" stroke-width="2.2" stroke-linecap="round"/>'
                 f'<path d="M634 509 l6-10 l7 9" fill="none" stroke="{TINTA}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    folha.append(linha(680, 526, "EU", 17))
    c.append(f'<g transform="rotate(1.4 574 348)">{"".join(folha)}</g>')

    # crachá, pendurado e balançando
    mw, mh = tamanho("mascote-cracha.png")
    lw = 262
    lh = round(mh * lw / mw)
    cr = []
    cr.append(f'<path d="M168 -20 L178 152 L200 152 L210 -20 Z" fill="#ecebfb"/>'
              f'<path d="M180 -20 L186 152 M198 -20 L192 152" stroke="{ANIL}" stroke-width="2.4" opacity=".55"/>')
    cr.append('<circle cx="189" cy="164" r="13" fill="none" stroke="#8d94a0" stroke-width="5"/>'
              '<rect x="178" y="170" width="22" height="44" rx="6" fill="#b8bec8" stroke="#7d8490" stroke-width="2"/>'
              '<rect x="185" y="176" width="8" height="26" rx="3" fill="#e9ecf1"/>')
    cr.append(f'<path d="M206 176 l12 -8 l7 10 l-12 8 Z" fill="#f59ac0" stroke="{TINTA}" stroke-width="1.5"/>'
              f'<rect x="208" y="190" width="16" height="24" rx="4" fill="#7fdc6a" stroke="{TINTA}" stroke-width="1.5" transform="rotate(-14 216 202)"/>')
    cr.append('<g filter="url(#sombra)">'
              '<rect x="60" y="206" width="258" height="360" rx="18" fill="#fbfbfd" stroke="#d3d7df" stroke-width="2"/>'
              f'<path d="M268 206 h32 q18 0 18 18 v324 q0 18-18 18 h-32 Z" fill="{CRACHA}"/>'
              '</g>')
    cr.append('<rect x="160" y="220" width="58" height="10" rx="5" fill="#dde0e8"/>')
    cr.append(f'<rect x="80" y="246" width="168" height="176" rx="3" fill="#e9eaef" stroke="{CRACHA}" stroke-opacity=".35"/>')
    cr.append(f'<image x="40" y="226" width="{lw}" height="{lh}" href="{imagem("mascote-cracha.png", 560)}"/>')
    cr.append(f'<line x1="84" y1="488" x2="250" y2="488" stroke="{CRACHA}" stroke-opacity=".5" stroke-width="1.3"/>')
    cr.append(linha(86, 482, "kitsune", 30))
    cr.append(linha(86, 506, "nome", 14, CRACHA))
    cr.append(f'<line x1="84" y1="538" x2="250" y2="538" stroke="{CRACHA}" stroke-opacity=".5" stroke-width="1.3"/>')
    cr.append(linha(86, 532, "faz projetinhos", 21))
    cr.append(linha(86, 555, "cargo", 14, CRACHA))
    c.append(f'<g transform="rotate(-4 189 -20)"><g class="balanco">{"".join(cr)}</g></g>')

    css = """
.balanco{transform-origin:189px -20px;animation:balanco 7s ease-in-out infinite}
@keyframes balanco{0%,100%{transform:rotate(-1.6deg)}50%{transform:rotate(1.8deg)}}
.brilho{transform-box:fill-box;transform-origin:center;animation:brilho 3.4s ease-in-out infinite}
@keyframes brilho{0%,70%,100%{transform:scale(1) rotate(0)}80%{transform:scale(1.18) rotate(8deg)}}
"""
    salvar("capa.svg", W, H, "".join(c), css,
           "Pasta de arquivo com o crachá do kitsune e um bilhete: Costumam escrever muitas coisas por aqui, né?")


# ---------------------------------------------------------------- etiquetas de contato

def etiqueta(nome, cor, texto, cor_texto="#fff", slug=None, angulo=-2):
    W, H = 290, 96
    x0 = 18 if not slug else 62
    c = [f'<g transform="rotate({angulo} 145 48)" filter="url(#sombra)">'
         f'<rect x="12" y="16" width="266" height="62" rx="9" fill="{cor}"/>'
         f'<rect x="12" y="16" width="266" height="62" rx="9" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="2"/>']
    if slug:
        c.append(icone(slug, 28, 32, 30, cor_texto))
    c.append(linha(x0 + 6, 58, texto, 25, cor_texto))
    c.append("</g>")
    salvar(nome, W, H, "".join(c), titulo=texto)


# ---------------------------------------------------------------- projetos

def cabecalho(nome, texto, sub, cor=LIMA, angulo=-1.5):
    W, H = 880, 120
    largura = medir("titulo", texto, 44) + 64
    c = [fita(40, 34, largura, 66, angulo, cor, 0.95)]
    c.append(titulo_adesivo(64, 82, texto, 44, angulo))
    if sub:
        sx = 40 + largura + 26
        sw = medir("mao", sub, 21) + 32
        c.append(f'<rect x="{sx}" y="48" width="{sw}" height="40" fill="#fff" transform="rotate(1.5 {sx} 68)" filter="url(#sombra-leve)"/>')
        c.append(linha(sx + 16, 75, sub, 21, TINTA, f'transform="rotate(1.5 {sx} 68)"'))
    salvar(nome, W, H, "".join(c), titulo=texto)


def card_artcode():
    W, H = 430, 330
    c = ['<g transform="rotate(-1.6 215 170)">',
         f'<rect x="18" y="30" width="394" height="282" rx="4" fill="#fffdf5" filter="url(#sombra)"/>',
         f'<line x1="18" y1="92" x2="412" y2="92" stroke="{MARGEM}" stroke-width="1.8"/>']
    for i in range(6):
        c.append(f'<line x1="18" y1="{126 + i * 30}" x2="412" y2="{126 + i * 30}" stroke="{PAUTA}" stroke-width="1.3"/>')
    c.append(titulo_adesivo(40, 80, "artcode", 40, 0, "#fff"))
    c.append(f'<image x="238" y="40" width="160" height="50" href="{imagem("foto-artcode.png", 400)}" '
             f'transform="rotate(4 318 65)" filter="url(#sombra-leve)"/>')
    for i, s in enumerate(["minha própria linguagem de programação,",
                           "interpretada e escrita em Rust.",
                           "tá na v0.5.1, e a v0.6 já tá saindo."]):
        c.append(linha(40, 120 + i * 30, s, 21))
    c.append(f'<circle cx="60" cy="262" r="24" fill="#e2552b" stroke="{TINTA}" stroke-width="2.5"/>')
    c.append(icone("rust", 46, 248, 28, "#fff"))
    c.append(linha(94, 270, "Rust", 22))
    c.append(linha(300, 286, "abrir repo", 19, ANIL, 'text-decoration="underline"'))
    c.append("</g>")
    c.append(fita(160, 14, 110, 30, 3))
    salvar("projeto-artcode.svg", W, H, "".join(c),
           titulo="artcode: minha própria linguagem de programação, interpretada e escrita em Rust")


def card_lover():
    W, H = 430, 330
    c = ['<g transform="rotate(1.4 215 170)">',
         f'<rect x="20" y="24" width="390" height="290" rx="14" fill="#fff" stroke="{TINTA}" stroke-width="3" filter="url(#sombra)"/>',
         f'<path d="M20 64 h390" stroke="{TINTA}" stroke-width="2.5"/>',
         f'<path d="M66 64 v-24 q0-6 6-6 h196 q6 0 6 6 v24" fill="#f2f3f7" stroke="{TINTA}" stroke-width="2.5"/>',
         linha(80, 57, "não feche esta aba.", 17),
         f'<path d="M250 44 l8 8 M258 44 l-8 8" stroke="{TINTA}" stroke-width="2" stroke-linecap="round"/>',
         '<clipPath id="tela-lover"><rect x="30" y="72" width="370" height="164" rx="6"/></clipPath>',
         f'<image x="30" y="66" width="370" height="238" preserveAspectRatio="xMidYMin slice" '
         f'clip-path="url(#tela-lover)" href="{imagem("foto-lover.png", 760)}"/>',
         linha(34, 266, "um jogo de quebra-cabeça em que o", 20),
         linha(34, 292, "controle é o seu navegador.", 20),
         f'<g transform="rotate(-12 352 196)"><circle cx="352" cy="196" r="36" fill="#fff" fill-opacity=".85" stroke="{CRACHA}" stroke-width="3.5"/>'
         f'<text x="352" y="204" font-size="21" text-anchor="middle" fill="{CRACHA}" class="titulo">JOGAR</text></g>',
         "</g>",
         f'<circle cx="215" cy="20" r="11" fill="{LARANJA}" stroke="{TINTA}" stroke-width="2.5" filter="url(#sombra-leve)"/>',
         '<circle cx="211" cy="16" r="3.5" fill="#fff" opacity=".7"/>']
    salvar("projeto-lover.svg", W, H, "".join(c),
           titulo="lover: um jogo de quebra-cabeça em que o controle é o seu navegador. Clique pra jogar.")


def card_clios():
    W, H = 430, 330
    c = ['<g transform="rotate(-1 215 170)">',
         '<rect x="18" y="26" width="394" height="290" rx="6" fill="#000" filter="url(#sombra)"/>',
         titulo_adesivo(40, 84, "clios", 42, 0, "#fff"),
         '<rect class="cursor" x="146" y="54" width="14" height="30" fill="#ff5a1f"/>',
         '<clipPath id="tela-clios"><rect x="210" y="44" width="186" height="130" rx="4"/></clipPath>',
         f'<image x="210" y="44" width="186" height="130" preserveAspectRatio="xMidYMid slice" '
         f'clip-path="url(#tela-clios)" href="{imagem("foto-clios.png", 420)}"/>',
         '<rect x="210" y="44" width="186" height="130" rx="4" fill="none" stroke="#fff" stroke-opacity=".35"/>',
         linha(40, 128, "um desktop Linux", 22, "#fff"),
         linha(40, 156, "feito pro terminal.", 22, "#fff"),
         linha(40, 214, "Arch, Hyprland e Quickshell,", 20, "#cfcfd4"),
         linha(40, 240, "com um binário em Rust", 20, "#cfcfd4"),
         linha(40, 266, "cuidando do sistema.", 20, "#cfcfd4"),
         icone("archlinux", 336, 236, 26, "#fff"),
         icone("rust", 372, 236, 26, "#fff"),
         "</g>",
         fita(28, 14, 96, 28, -8)]
    css = ".cursor{animation:pisca 1.1s steps(1) infinite}@keyframes pisca{50%{opacity:0}}"
    salvar("projeto-clios.svg", W, H, "".join(c), css,
           "clios: um desktop Linux feito pro terminal, com Arch, Hyprland, Quickshell e Rust")


def card_hackintosh():
    W, H = 430, 330
    c = ['<g transform="rotate(2 215 170)">',
         '<rect x="34" y="20" width="362" height="298" rx="3" fill="#fff" filter="url(#sombra)"/>',
         '<clipPath id="foto-hack"><rect x="52" y="38" width="326" height="196"/></clipPath>',
         f'<image x="52" y="38" width="326" height="196" preserveAspectRatio="xMidYMid slice" '
         f'clip-path="url(#foto-hack)" href="{imagem("foto-hackintosh.jpg", 700)}"/>',
         linha(56, 268, "macOS Sequoia num Acer Nitro V15,", 20),
         linha(56, 296, "com o desktop acelerado na RTX 3050", 20),
         "</g>",
         fita(300, 8, 104, 30, 18)]
    salvar("projeto-hackintosh.svg", W, H, "".join(c),
           titulo="Hackintosh: macOS Sequoia num Acer Nitro V15, com o desktop acelerado na RTX 3050")


def tag(nome, cor, titulo, linhas, angulo, descricao):
    W, H = 290, 190
    c = [f'<g transform="rotate({angulo} 145 100)">',
         f'<path d="M30 40 h230 q12 0 12 12 v118 q0 12-12 12 h-230 q-12 0-12-12 v-90 Z" fill="{cor}" filter="url(#sombra)"/>',
         '<circle cx="44" cy="62" r="8" fill="#fff" stroke="#000" stroke-opacity=".2" stroke-width="2"/>',
         f'<path d="M44 62 q-30 -40 -10 -58" fill="none" stroke="#b08a5a" stroke-width="2.5"/>',
         titulo_adesivo(64, 76, titulo, 30, 0),
         ]
    for i, s in enumerate(linhas):
        c.append(linha(34, 112 + i * 25, s, 19))
    c.append("</g>")
    salvar(nome, W, H, "".join(c), titulo=descricao)


def pasta_mais():
    W, H = 880, 110
    c = [f'<g filter="url(#sombra)"><path d="M40 98 V40 q0-12 12-12 h170 q9 0 14 8 l12 20 h590 q12 0 12 12 v30 Z" fill="{MANILA_ESCURO}"/>'
         f'<rect x="40" y="62" width="800" height="40" rx="8" fill="{MANILA}"/></g>',
         linha(64, 50, "mais projetinhos", 20, "#6b4f22"),
         linha(270, 92, "tem mais coisa aqui dentro, clica pra abrir a pasta", 21, "#5a4019")]
    salvar("pasta-mais.svg", W, H, "".join(c), titulo="Abrir a pasta com mais projetos")


# ---------------------------------------------------------------- o que eu sei fazer

LINGUAGENS = [
    ("python", "#2d3440", "#ffd43b", False),
    ("php", "#4f5b93", "#fff", False),
    ("html5", "#e34f26", "#fff", False),
    ("css3", "#1f7fd6", "#fff", False),
    ("svelte", "#ff3e00", "#fff", False),
    ("react", "#1c2833", "#61dafb", False),
    ("dart", "#00a7a0", "#fff", True),
    ("java", "#e2302b", "#fff", True),
    ("kotlin", "#8c4fff", "#fff", True),
    ("rust", "#e2552b", "#fff", True),
]
FERRAMENTAS = [
    ("git", "git", "#f05032"), ("npm", "npm", "#cb3837"),
    ("redis", "redis", "#dc382d"), ("express", "express", TINTA),
    ("docker", "docker", "#2496ed"), ("expo", "Expo", TINTA),
]


def xicara(cx, cy, cor):
    """O Java não tem ícone livre no simple-icons, então vai uma xícara com fumaça."""
    return (f'<g fill="none" stroke="{cor}" stroke-width="4.5" stroke-linecap="round">'
            f'<path d="M{cx - 20} {cy - 4} h34 v10 q0 16 -17 16 q-17 0 -17 -16 Z" fill="{cor}"/>'
            f'<path d="M{cx + 14} {cy} q12 0 10 9 q-2 7 -12 6"/>'
            f'<path d="M{cx - 24} {cy + 27} h46"/>'
            f'<path d="M{cx - 8} {cy - 12} q-6 -7 0 -13 q6 -6 0 -13"/>'
            f'<path d="M{cx + 4} {cy - 12} q-6 -7 0 -13 q6 -6 0 -13"/></g>')


def habilidades():
    W, H = 880, 640
    c = []
    # prancheta
    c.append(f'<g transform="rotate(-1.2 300 340)">'
             f'<rect x="24" y="48" width="548" height="572" rx="28" fill="{CORTICA}" filter="url(#sombra)"/>'
             f'<rect x="24" y="48" width="548" height="572" rx="28" fill="none" stroke="#9c6b44" stroke-width="3"/>'
             f'<rect x="56" y="100" width="484" height="496" rx="4" fill="#f6f6f3" filter="url(#papel)"/>')
    c.append(f'<rect x="64" y="118" width="468" height="84" rx="16" fill="#f7df1e" filter="url(#sombra-leve)"/>')
    c.append(linha(96, 168, "Essa eh braba", 26))
    c.append(linha(140, 190, "◡", 22))
    c.append(f'<text x="510" y="184" font-size="56" text-anchor="end" fill="{TINTA}" class="titulo">JS</text>')
    s, g = 102, 20
    for i, (slug, fundo, cor, aprendendo) in enumerate(LINGUAGENS):
        col, lin = i % 4, i // 4
        x = 64 + col * (s + g)
        y = 222 + lin * (s + 28)
        c.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="20" fill="{fundo}" filter="url(#sombra-leve)"/>')
        c.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="20" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="2"/>')
        if slug == "java":
            c.append(xicara(x + s / 2, y + s / 2 + 4, cor))
        else:
            c.append(icone(slug, x + 25, y + 25, 52, cor))
        if aprendendo:
            c.append(f'<rect x="{x + 6}" y="{y + s - 8}" width="{s - 12}" height="22" rx="3" fill="#35c84a" transform="rotate(-2 {x + s / 2} {y + s})"/>')
            c.append(linha(x + s / 2, y + s + 9, "aprendendo", 16, "#fff", 'text-anchor="middle"'))
    c.append(linha(330, 520, "Em breve...", 24))
    c.append(linha(360, 552, ">_<", 24))
    c.append("</g>")
    # presilha de metal
    c.append('<g filter="url(#sombra)"><rect x="198" y="26" width="200" height="54" rx="14" fill="#c3c8d0" stroke="#868d99" stroke-width="3"/>'
             '<rect x="226" y="40" width="144" height="18" rx="9" fill="#e9ecf1"/>'
             '<circle cx="298" cy="22" r="16" fill="none" stroke="#868d99" stroke-width="6"/></g>')
    # bilhete das ferramentas
    n = ['<g transform="rotate(2.5 730 220)">',
         '<rect x="604" y="70" width="256" height="290" fill="#fff" filter="url(#sombra)"/>']
    for i, (slug, nome, cor) in enumerate(FERRAMENTAS):
        x = 624 + (i % 2) * 120
        y = 104 + (i // 2) * 84
        if slug == "express":
            n.append(linha(x, y + 28, nome, 26))
        else:
            n.append(icone(slug, x, y, 34, cor))
            n.append(linha(x + 42, y + 28, nome, 22))
    n.append(linha(624, 336, "e o que mais precisar", 19, "#6a6a72"))
    n.append("</g>")
    n.append(f'<circle cx="736" cy="70" r="12" fill="{ANIL}" stroke="{TINTA}" stroke-width="2.5" filter="url(#sombra-leve)"/>')
    c.append("".join(n))
    # post-it e o friorento
    c.append('<g transform="rotate(-3 700 500)">'
             '<rect x="576" y="398" width="176" height="196" fill="#eef08a" filter="url(#sombra)"/>'
             + "".join(linha(592, 444 + i * 36, s_, 20) for i, s_ in enumerate(
                 ["Se você não", "sabe nem isso,", "não recomendo", "continuar"]))
             + "</g>")
    c.append(fita(620, 386, 100, 26, -6))
    fw, fh = tamanho("so-cold.png")
    ch = 262
    cw = round(fw * ch / fh)
    c.append(f'<g class="frio"><image x="{W - cw - 6}" y="{H - ch - 8}" width="{cw}" height="{ch}" '
             f'href="{imagem("so-cold.png", 400)}" filter="url(#sombra-leve)"/></g>')
    css = """
.frio{animation:frio 4.5s infinite}
@keyframes frio{0%,86%,100%{transform:translate(0,0)}88%{transform:translate(-2px,1px)}90%{transform:translate(2px,0)}
92%{transform:translate(-2px,-1px)}94%{transform:translate(2px,1px)}96%{transform:translate(-1px,0)}}
"""
    salvar("habilidades.svg", W, H, "".join(c), css,
           "O que eu sei fazer: JavaScript, Python, PHP, HTML, CSS, Svelte, React; aprendendo Dart, Java, Kotlin e Rust. "
           "Ferramentas: git, npm, Redis, Express, Docker, Expo.")


# ---------------------------------------------------------------- divisórias do site

def divisoria(nome, cor, texto, cor_texto=TINTA):
    W, H = 290, 110
    c = [f'<g filter="url(#sombra)"><path d="M14 104 V44 q0-10 10-10 h40 q8 0 12-8 l8-14 q4-8 12-8 h90 q8 0 12 8 l8 14 q4 8 12 8 h48 q10 0 10 10 v60 Z" fill="{cor}"/></g>',
         f'<text x="145" y="84" font-size="34" text-anchor="middle" fill="{cor_texto}" class="titulo">{t(texto)}</text>']
    salvar(nome, W, H, "".join(c), titulo=texto)


if __name__ == "__main__":
    capa()
    etiqueta("contato-discord.svg", AZUL, "@thur3inhos", slug="discord", angulo=-2)
    etiqueta("contato-frase.svg", LARANJA, "“Penso, logo desisto.”", angulo=1.5)
    etiqueta("contato-love.svg", LIMA, "love you forever", TINTA, angulo=-1)
    cabecalho("titulo-projetos.svg", "projetinhos", "clica num card pra abrir")
    card_artcode()
    card_lover()
    card_clios()
    card_hackintosh()
    pasta_mais()
    tag("projeto-clipmon.svg", LIMA, "clipmon",
        ["descobre qual dos 151 Pokémon", "é pela imagem, com CLIP.", "acerta 91,4% de primeira."], -2,
        "clipmon: descobre qual dos 151 Pokémon é pela imagem, com CLIP. 91,4% de acerto no Top-1.")
    tag("projeto-merlin.svg", "#9fc4ff", "merlin",
        ["observa a artcode, planeja,", "testa e abre PR sozinho.", "o merge continua humano."], 1.5,
        "artcode-merlin: observa a artcode, planeja, testa e abre pull request sozinho. O merge continua humano.")
    tag("projeto-nmx.svg", "#ffb38f", "nmx-intel",
        ["leva a tela Intel do Nitro", "pro macOS, portando o i915", "do Linux pro xnu."], -1,
        "nmx-intel: leva a tela Intel do Acer Nitro pro macOS, portando o driver i915 do Linux pro xnu.")
    cabecalho("titulo-habilidades.svg", "o que eu sei fazer?", "", "#b9c0ff", 1)
    habilidades()
    cabecalho("titulo-musica.svg", "no fone essa semana", "atualiza sozinho todo domingo", "#ffc2dc", -1)
    divisoria("site-artbook.svg", "#ffb3d1", "artbook")
    divisoria("site-portfolio.svg", "#9fc4ff", "portfolio")
    divisoria("site-medialog.svg", LIMA, "media log")
