"""Recibo da semana: as músicas mais ouvidas nos últimos 7 dias, no Last.fm.

    LASTFM_API_KEY=... LASTFM_USER=... python tools/recibo.py

Sem as variáveis, gera o recibo com dados de exemplo (e carimbo de EXEMPLO).
"""
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from kit import ANIL, CRACHA, PAUTA, TINTA, fita, linha, salvar, t

API = "https://ws.audioscrobbler.com/2.0/"
EXEMPLO = {
    "faixas": [
        ("Mitski", "My Love Mine All Mine", 31),
        ("Lorde", "Broken Glass", 27),
        ("Sabrina Carpenter", "Manchild", 22),
        ("Mitski", "Where's My Phone?", 19),
        ("Billie Eilish", "Birds of a Feather", 15),
        ("Lorde", "What Was That", 13),
        ("Charli xcx", "Apple", 11),
        ("Mitski", "Washing Machine Heart", 9),
    ],
    "total": 214,
}


def chamar(metodo, **params):
    q = urllib.parse.urlencode({"method": metodo, "user": os.environ["LASTFM_USER"],
                                "api_key": os.environ["LASTFM_API_KEY"], "format": "json", **params})
    with urllib.request.urlopen(f"{API}?{q}", timeout=30) as r:
        return json.load(r)


def dados_reais():
    top = chamar("user.gettoptracks", period="7day", limit=8)["toptracks"]["track"]
    faixas = [(f["artist"]["name"], f["name"], int(f["playcount"])) for f in top]
    desde = int(time.time()) - 7 * 86400
    rec = chamar("user.getrecenttracks", limit=1, **{"from": desde})
    total = int(rec["recenttracks"]["@attr"]["total"])
    return {"faixas": faixas, "total": total}


def cortar(s, n):
    return s if len(s) <= n else s[: n - 1] + "…"


def recibo(d, exemplo):
    W = 880
    hoje = datetime.now(timezone(timedelta(hours=-3)))
    inicio = hoje - timedelta(days=7)
    faixas = d["faixas"] or [("—", "nada tocou essa semana", 0)]
    linhas_h = 48 * len(faixas)
    altura_papel = 250 + linhas_h + 120
    H = altura_papel + 70
    x0, largura = 70, 330
    p = []  # papel do recibo, que vai "sair da impressora"
    dentes = "".join(f"L{x0 + i * 10 + 5} {altura_papel + 34} L{x0 + (i + 1) * 10} {altura_papel + 26} "
                     for i in range(largura // 10))
    p.append(f'<path d="M{x0} 30 H{x0 + largura} V{altura_papel + 26} {dentes} L{x0} {altura_papel + 26} Z" '
             f'fill="#fbfbf6" filter="url(#sombra)"/>')
    cx = x0 + largura / 2
    p.append(f'<text x="{cx}" y="86" font-size="26" text-anchor="middle" fill="{TINTA}" class="recibo">KITSUNEISLIFE</text>')
    p.append(f'<text x="{cx}" y="112" font-size="15" text-anchor="middle" fill="{TINTA}" class="recibo">RECIBO DA SEMANA</text>')
    p.append(f'<text x="{cx}" y="136" font-size="14" text-anchor="middle" fill="#55555c" class="recibo">'
             f'{inicio:%d/%m/%Y} - {hoje:%d/%m/%Y}</text>')
    tracejado = "-" * 34
    p.append(f'<text x="{x0 + 18}" y="166" font-size="14" fill="#55555c" class="recibo">{tracejado}</text>')
    p.append(f'<text x="{x0 + 18}" y="190" font-size="14" fill="{TINTA}" class="recibo">#  FAIXA</text>')
    p.append(f'<text x="{x0 + largura - 18}" y="190" font-size="14" text-anchor="end" fill="{TINTA}" class="recibo">PLAYS</text>')
    y = 226
    for i, (artista, faixa, plays) in enumerate(faixas, 1):
        p.append(f'<text x="{x0 + 18}" y="{y}" font-size="15" fill="{TINTA}" class="recibo">'
                 f'{i:02d} {t(cortar(faixa.upper(), 22))}</text>')
        p.append(f'<text x="{x0 + largura - 18}" y="{y}" font-size="15" text-anchor="end" fill="{TINTA}" class="recibo">{plays}</text>')
        p.append(f'<text x="{x0 + 46}" y="{y + 20}" font-size="13" fill="#6b6b73" class="recibo">{t(cortar(artista, 28))}</text>')
        y += 48
    p.append(f'<text x="{x0 + 18}" y="{y}" font-size="14" fill="#55555c" class="recibo">{tracejado}</text>')
    p.append(f'<text x="{x0 + 18}" y="{y + 28}" font-size="16" fill="{TINTA}" class="recibo">TOTAL DE PLAYS</text>')
    p.append(f'<text x="{x0 + largura - 18}" y="{y + 28}" font-size="16" text-anchor="end" fill="{TINTA}" class="recibo">{d["total"]}</text>')
    # código de barras com a soma dos plays de semente, pra mudar toda semana
    semente = d["total"] * 7919
    bx = x0 + 40
    barras = []
    for i in range(46):
        semente = (semente * 1103515245 + 12345) % 2 ** 31
        w = 1 + semente % 4
        if i % 2 == 0:
            barras.append(f'<rect x="{bx}" y="{y + 52}" width="{w}" height="46" fill="{TINTA}"/>')
        bx += w + 1
    p.append("".join(barras))
    p.append(f'<text x="{cx}" y="{y + 124}" font-size="14" text-anchor="middle" fill="#55555c" class="recibo">OBRIGADO POR OUVIR :)</text>')


    c = []
    c.append(f'<clipPath id="saida"><rect x="{x0 - 30}" y="24" width="{largura + 60}" height="{H}"/></clipPath>')
    c.append(f'<g clip-path="url(#saida)"><g class="imprime">{"".join(p)}</g></g>')
    # boca da impressora
    c.append(f'<rect x="{x0 - 24}" y="10" width="{largura + 48}" height="24" rx="12" fill="#2f2f36" filter="url(#sombra-leve)"/>'
             f'<rect x="{x0 - 8}" y="20" width="{largura + 16}" height="5" rx="2.5" fill="#111"/>')

    # caderno do lado
    nx, ny, nw, nh = 460, 70, 380, min(H - 110, 470)
    n = [f'<g transform="rotate(1.8 {nx + nw / 2} {ny + nh / 2})">',
         f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="4" fill="#fff" filter="url(#sombra)"/>']
    for i in range(int((nh - 70) // 40)):
        n.append(f'<line x1="{nx}" y1="{ny + 90 + i * 40}" x2="{nx + nw}" y2="{ny + 90 + i * 40}" stroke="{PAUTA}" stroke-width="1.4"/>')
    for i in range(int(nh // 34)):
        yy = ny + 22 + i * 34
        n.append(f'<circle cx="{nx + 2}" cy="{yy}" r="5" fill="#e9e9ee"/>'
                 f'<path d="M{nx - 12} {yy - 4} q14 -8 18 4" fill="none" stroke="#8d94a0" stroke-width="3.5" stroke-linecap="round"/>')
    artista_top = max(((a, sum(p_ for a2, _, p_ in faixas if a2 == a)) for a, _, _ in faixas), key=lambda x: x[1])[0]
    faixa_top = faixas[0]
    n.append(linha(nx + 36, ny + 80, "essa semana deu", 24, "#5a5a63"))
    n.append(linha(nx + 36, ny + 160, cortar(artista_top, 18), 46, TINTA))
    n.append(linha(nx + 36, ny + 200, "no repeat.", 24, "#5a5a63"))
    n.append(linha(nx + 36, ny + 280, "mais tocada:", 22, "#5a5a63"))
    n.append(linha(nx + 36, ny + 318, cortar(faixa_top[1], 26), 26, ANIL))
    n.append(linha(nx + 36, ny + 398, f"{d['total']} plays em 7 dias", 22, "#5a5a63"))
    if exemplo:
        sx, sy = nx + nw - 110, ny + nh - 50
        n.append(f'<g transform="rotate(-9 {sx} {sy})"><rect x="{sx - 90}" y="{sy - 26}" width="180" height="52" rx="6" '
                 f'fill="none" stroke="{CRACHA}" stroke-width="4" opacity=".8"/>'
                 f'<text x="{sx}" y="{sy + 12}" font-size="30" text-anchor="middle" fill="{CRACHA}" opacity=".8" class="titulo">EXEMPLO</text></g>')
    n.append("</g>")
    c.append("".join(n))
    c.append(fita(nx + 130, ny - 14, 120, 30, 4))

    css = f"""
.imprime{{animation:imprime 2.8s cubic-bezier(.3,.7,.4,1) .3s both}}
@keyframes imprime{{from{{transform:translateY(-{altura_papel + 40}px)}}to{{transform:translateY(0)}}}}
"""
    desc = "Recibo da semana: " + "; ".join(f"{f} de {a} ({p_} plays)" for a, f, p_ in faixas)
    salvar("recibo.svg", W, H, "".join(c), css, desc)


if __name__ == "__main__":
    real = bool(os.environ.get("LASTFM_API_KEY") and os.environ.get("LASTFM_USER"))
    recibo(dados_reais() if real else EXEMPLO, exemplo=not real)
