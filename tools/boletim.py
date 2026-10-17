"""Boletim escolar: as notas saem dos meus repositórios no GitHub.

    GITHUB_TOKEN=... python tools/boletim.py

Busca os repositórios públicos (sem fork), soma os bytes de cada linguagem,
conta os dias com contribuição no último ano e os repositórios mexidos por
último. Grava em assets/readme/boletim.json e redesenha a tira "habilidades".
Sem token roda com o que a API pública deixar; a frequência precisa do token.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import colagem

USUARIO = os.environ.get("GITHUB_USER", "kitsuneislife")
API = "https://api.github.com"
SAIDA = Path(__file__).resolve().parent.parent / "assets" / "readme" / "boletim.json"


def pedir(url, corpo=None):
    cab = {"Accept": "application/vnd.github+json", "User-Agent": "kitsuneislife-boletim"}
    if os.environ.get("GITHUB_TOKEN"):
        cab["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    dados = json.dumps(corpo).encode() if corpo else None
    with urllib.request.urlopen(urllib.request.Request(url, dados, cab), timeout=30) as r:
        return json.load(r)


def frequencia():
    q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
           totalContributions weeks{contributionDays{contributionCount}}}}}}"""
    cal = pedir(f"{API}/graphql", {"query": q, "variables": {"u": USUARIO}})
    cal = cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    dias = [d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]]
    return {"dias": len(dias), "presente": sum(1 for d in dias if d), "contribuicoes": cal["totalContributions"]}


def coletar():
    repos = [r for r in pedir(f"{API}/users/{USUARIO}/repos?per_page=100&type=owner&sort=pushed")
             if not r["fork"]]
    linguagens = {}
    for r in repos:
        for nome, b in pedir(r["languages_url"]).items():
            atual = linguagens.setdefault(nome, {"bytes": 0, "repos": 0})
            atual["bytes"] += b
            atual["repos"] += 1
    agora = datetime.now(timezone.utc)
    recentes = []
    for r in repos[:4]:
        quando = datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00"))
        recentes.append({"nome": r["name"], "dias": (agora - quando).days})
    dados = {
        "repos": len(repos),
        "estrelas": sum(r["stargazers_count"] for r in repos),
        "linguagens": linguagens,
        "recentes": recentes,
        "atualizado": agora.strftime("%d/%m/%Y"),
    }
    if os.environ.get("GITHUB_TOKEN"):
        try:
            dados["frequencia"] = frequencia()
        except (OSError, KeyError, TypeError) as e:
            print(f"sem frequência: {e}")
    return dados


if __name__ == "__main__":
    SAIDA.write_text(json.dumps(coletar(), ensure_ascii=False, indent=1), encoding="utf-8")
    colagem.gerar(so=["habilidades"])
