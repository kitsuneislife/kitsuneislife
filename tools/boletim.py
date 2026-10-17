"""Boletim escolar: as notas saem dos meus repositórios no GitHub.

    GITHUB_TOKEN=... python tools/boletim.py

Busca os repositórios públicos (sem fork), soma os bytes de cada linguagem,
conta os dias com contribuição no último ano, os repositórios mexidos por
último e as ferramentas que aparecem nos arquivos de cada um (Dockerfile,
package.json e as dependências dele, Cargo.toml...). Grava em
assets/readme/boletim.json, baixa os ícones que faltarem do Simple Icons
pra assets/readme/icones.json e redesenha a tira "habilidades".
Sem token roda com o que a API pública deixar; a frequência precisa do token.
"""
import base64
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import colagem

USUARIO = os.environ.get("GITHUB_USER", "kitsuneislife")
API = "https://api.github.com"
SAIDA = Path(__file__).resolve().parent.parent / "assets" / "readme" / "boletim.json"
ICONES = Path(__file__).resolve().parent.parent / "assets" / "readme" / "icones.json"
SIMPLE_ICONS = "https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons"

# ferramenta: (ícone no Simple Icons, arquivos na raiz do repo, dependências do package.json)
FERRAMENTAS = {
    "git": ("git", None, ()),  # todo repo conta
    "npm": ("npm", ("package.json",), ()),
    "Docker": ("docker", ("Dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"), ()),
    "Actions": ("githubactions", (".github",), ()),
    "Cargo": ("rust", ("Cargo.toml",), ()),
    "pip": ("pypi", ("requirements.txt", "pyproject.toml", "setup.py"), ()),
    "Vite": ("vite", (), ("vite",)),
    "Tailwind": ("tailwindcss", (), ("tailwindcss",)),
    "React": ("react", (), ("react",)),
    "Next.js": ("nextdotjs", (), ("next",)),
    "Express": ("express", (), ("express",)),
    "Redis": ("redis", (), ("redis", "ioredis")),
    "Expo": ("expo", (), ("expo",)),
    "Electron": ("electron", (), ("electron",)),
    "Prisma": ("prisma", (), ("prisma", "@prisma/client")),
    "Bun": ("bun", ("bun.lockb", "bun.lock"), ()),
    "pnpm": ("pnpm", ("pnpm-lock.yaml",), ()),
    "Nix": ("nixos", ("flake.nix", "shell.nix"), ()),
    "Arch": ("archlinux", ("PKGBUILD",), ()),
}


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


def ferramentas(repos):
    """Quantos repos usam cada ferramenta, olhando os arquivos da raiz e as dependências."""
    contagem = {}
    for r in repos:
        try:
            raiz = {f["name"] for f in pedir(f"{API}/repos/{r['full_name']}/contents")}
        except (urllib.error.HTTPError, OSError):
            continue  # repo vazio
        deps = set()
        if "package.json" in raiz:
            try:
                pkg = pedir(f"{API}/repos/{r['full_name']}/contents/package.json")
                pkg = json.loads(base64.b64decode(pkg["content"]))
                for chave in ("dependencies", "devDependencies"):
                    deps |= set(pkg.get(chave) or {})
            except (urllib.error.HTTPError, OSError, ValueError, KeyError):
                pass
        for nome, (_icone, arquivos, pacotes) in FERRAMENTAS.items():
            if arquivos is None or raiz & set(arquivos) or deps & set(pacotes):
                contagem[nome] = contagem.get(nome, 0) + 1
    return [{"nome": n, "repos": q} for n, q in sorted(contagem.items(), key=lambda kv: -kv[1])]


def baixar_icones(nomes):
    """Guarda o desenho (path) de cada ícone que ainda não tá em icones.json."""
    try:
        icones = json.loads(ICONES.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        icones = {}
    for nome in nomes:
        slug = FERRAMENTAS.get(nome, (None,))[0]
        if not slug or nome in icones:
            continue
        try:
            with urllib.request.urlopen(f"{SIMPLE_ICONS}/{slug}.svg", timeout=30) as r:
                svg = r.read().decode()
            icones[nome] = re.search(r'<path d="([^"]+)"', svg).group(1)
        except (OSError, AttributeError) as e:
            print(f"sem ícone pra {nome}: {e}")
    ICONES.write_text(json.dumps(icones, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


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
        "ferramentas": ferramentas(repos),
        "atualizado": agora.strftime("%d/%m/%Y"),
    }
    if os.environ.get("GITHUB_TOKEN"):
        try:
            dados["frequencia"] = frequencia()
        except (OSError, KeyError, TypeError) as e:
            print(f"sem frequência: {e}")
    return dados


if __name__ == "__main__":
    dados = coletar()
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    baixar_icones([f["nome"] for f in dados["ferramentas"]] + colagem.EXTRAS)
    colagem.gerar(so=["habilidades"])
