"""Recibo da semana: as músicas mais ouvidas nos últimos 7 dias, no Last.fm.

    LASTFM_API_KEY=... LASTFM_USER=... python tools/recibo.py

Redesenha só a tira "musica" da colagem. Sem as variáveis, sai com dados de
exemplo (e carimbo de EXEMPLO).
"""
import json
import os
import time
import urllib.parse
import urllib.request

import colagem

API = "https://ws.audioscrobbler.com/2.0/"


def chamar(metodo, **params):
    q = urllib.parse.urlencode({"method": metodo, "user": os.environ["LASTFM_USER"],
                                "api_key": os.environ["LASTFM_API_KEY"], "format": "json", **params})
    with urllib.request.urlopen(f"{API}?{q}", timeout=30) as r:
        return json.load(r)


def dados_reais():
    top = chamar("user.gettoptracks", period="7day", limit=6)["toptracks"]["track"]
    faixas = [(f["artist"]["name"], f["name"], int(f["playcount"])) for f in top]
    desde = int(time.time()) - 7 * 86400
    rec = chamar("user.getrecenttracks", limit=1, **{"from": desde})
    return {"faixas": faixas, "total": int(rec["recenttracks"]["@attr"]["total"])}


if __name__ == "__main__":
    real = bool(os.environ.get("LASTFM_API_KEY") and os.environ.get("LASTFM_USER"))
    colagem.gerar(dados_reais() if real else None, so=["musica"])
