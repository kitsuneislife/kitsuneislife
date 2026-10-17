"""Peças compartilhadas pra montar os SVGs do README.

O GitHub mostra SVG via <img>, então nada externo carrega lá dentro:
fonte e imagem vão embutidas em base64, e animação só em CSS.
"""
import base64
import functools
import io
import re
from html import escape
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
ART = ROOT / "assets" / "art"
OUT = ROOT / "assets" / "readme"

# paleta tirada do banner antigo
TINTA = "#1d1c22"
PAPEL = "#f8f9fc"
PAUTA = "#c7d5ee"
MARGEM = "#e7788a"
MANILA = "#ecc98b"
MANILA_ESCURO = "#d6ad66"
AZUL = "#3a78f2"
LARANJA = "#ff7444"
LIMA = "#d3ec3c"
ANIL = "#5a62df"
CRACHA = "#b7213f"
AMARELO = "#f8cf3a"
CORTICA = "#c9946a"

FAMILIAS = {
    "mao": "GochiHand-Regular.ttf",
    "titulo": "LilitaOne-Regular.ttf",
    "recibo": "DotGothic16-Regular.ttf",
    "bolha": "BagelFatOne-Regular.ttf",
    "revista": "DelaGothicOne-Regular.ttf",
}


def font_face(familia, texto):
    """Subseta a fonte só com os caracteres usados e devolve o @font-face."""
    f = TTFont(FONTS / FAMILIAS[familia])
    opts = subset.Options()
    opts.flavor = "woff2"
    s = subset.Subsetter(opts)
    s.populate(text=texto + " ")
    s.subset(f)
    buf = io.BytesIO()
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:{familia};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"


@functools.lru_cache(maxsize=None)
def imagem(nome, largura, qualidade=82):
    """Lê um PNG de assets/art, reduz pra largura (px reais) e devolve data URI webp."""
    im = Image.open(ART / nome)
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=qualidade, method=4)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


_metricas = {}


def medir(familia, texto, px):
    """Largura aproximada do texto em px, pelas larguras de avanço da fonte."""
    if familia not in _metricas:
        f = TTFont(FONTS / FAMILIAS[familia])
        _metricas[familia] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    cmap, hmtx, upm = _metricas[familia]
    total = sum(hmtx[cmap[ord(c)]][0] for c in texto if ord(c) in cmap)
    return total * px / upm


def tamanho(nome):
    return Image.open(ART / nome).size


def t(texto):
    return escape(texto, quote=False)


def linha(x, y, texto, px=21, cor=TINTA, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{px}" fill="{cor}" class="mao" {extra}>{t(texto)}</text>'


BASE_CSS = """
.mao{font-family:mao,'Comic Sans MS',cursive}
.titulo{font-family:titulo,Impact,sans-serif}
.recibo{font-family:recibo,'Courier New',monospace}
.bolha{font-family:bolha,'Arial Black',sans-serif}
.revista{font-family:revista,'Arial Black',sans-serif}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""

DEFS = f"""
<filter id="sombra" x="-20%" y="-20%" width="140%" height="150%">
  <feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#2a1d10" flood-opacity=".22"/>
</filter>
<filter id="sombra-leve" x="-20%" y="-20%" width="140%" height="150%">
  <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#2a1d10" flood-opacity=".25"/>
</filter>
<filter id="papel" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 .45  0 0 0 0 .38  0 0 0 0 .3  0 0 0 .07 0" result="g"/>
  <feComposite in="g" in2="SourceGraphic" operator="in" result="gg"/>
  <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="gg"/></feMerge>
</filter>
"""


def fita(x, y, w, h, angulo, cor="#f3eccd", opacidade=0.82):
    """Fita crepe com as pontas serrilhadas."""
    dente = 4
    n = max(2, int(h // dente))
    esq = " ".join(f"L{x + (2 if i % 2 else 0)} {y + i * h / n:.1f}" for i in range(n + 1))
    dir_ = " ".join(f"L{x + w - (2 if i % 2 else 0)} {y + h - i * h / n:.1f}" for i in range(n + 1))
    d = f"M{x} {y} L{x + w} {y} {dir_} L{x} {y + h} {esq} Z"
    cx, cy = x + w / 2, y + h / 2
    return (f'<path d="{d}" fill="{cor}" opacity="{opacidade}" '
            f'transform="rotate({angulo} {cx} {cy})" filter="url(#sombra-leve)"/>')


def svg(largura, altura, corpo, fontes, css="", titulo="", viewbox=None):
    """Monta o arquivo final. fontes = {familia: texto_usado}."""
    faces = "".join(font_face(f, txt) for f, txt in fontes.items() if txt)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{largura}" height="{altura}" viewBox="{viewbox or f"0 0 {largura} {altura}"}" role="img">'
        f"<title>{t(titulo)}</title>"
        f"<style>{faces}{BASE_CSS}{css}</style><defs>{DEFS}</defs>{corpo}</svg>"
    )


def textos(corpo, classe):
    """Junta o texto de todos os <text>/<tspan> com a classe dada, pra subsetar a fonte."""
    achados = re.findall(rf'<text[^>]*class="[^"]*\b{classe}\b[^"]*"[^>]*>(.*?)</text>', corpo, re.S)
    limpo = re.sub(r"<[^>]+>", "", "".join(achados))
    from html import unescape
    return unescape(limpo)


def salvar(nome, largura, altura, corpo, css="", titulo="", viewbox=None):
    fontes = {f: textos(corpo, f) for f in FAMILIAS}
    OUT.mkdir(parents=True, exist_ok=True)
    caminho = OUT / nome
    caminho.write_text(svg(largura, altura, corpo, fontes, css, titulo, viewbox), encoding="utf-8")
    print(f"{nome}: {caminho.stat().st_size / 1024:.0f} KB")
