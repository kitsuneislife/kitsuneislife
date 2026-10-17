# como o README é montado

Cada pedaço do README é um SVG em `assets/readme/`, gerado por script. O GitHub
mostra SVG como imagem, então fonte e desenho vão embutidos (base64) e a
animação é só CSS.

```sh
pip install fonttools brotli pillow
python tools/build.py    # capa, contatos, projetos, habilidades, divisórias
python tools/recibo.py   # recibo da semana (sem chave do Last.fm sai com dados de exemplo)
```

- `tools/kit.py`: paleta, fontes, fita crepe, sombras, helpers.
- `assets/art/`: os desenhos. Troque um PNG aqui e rode o build de novo.
- `tools/fonts/`: Gochi Hand, Lilita One e DotGothic16 (OFL), já cortadas pro alfabeto latino.
- `tools/icons/`: ícones do [simple-icons](https://simpleicons.org) (CC0).

## recibo da semana

O workflow `.github/workflows/recibo.yml` roda todo domingo. Pra ele usar os seus dados:

1. Crie uma chave de API em https://www.last.fm/api/account/create
2. No repositório: Settings → Secrets and variables → Actions
   - em **Secrets**, crie `LASTFM_API_KEY` com a chave
   - em **Variables**, crie `LASTFM_USER` com o seu usuário do Last.fm
3. Actions → recibo da semana → Run workflow, pra gerar o primeiro.

Se você ouve no Spotify, ligue o scrobble do Spotify no Last.fm (Settings → Applications).
