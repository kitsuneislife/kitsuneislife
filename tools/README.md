# como o README é montado

O README é uma colagem só, de 880 de largura, cortada em tiras horizontais
(`assets/readme/colagem-*.svg`). Cada tira é a mesma cena com outro viewBox,
então o que atravessa uma emenda aparece certinho dos dois lados.

No README as tiras usam `width="100%" align="left"`: é o único jeito de o
GitHub empilhar imagens sem fresta entre elas. Lado a lado não dá (ele põe 20px
de padding em imagem alinhada), então cada tira pode ser um link inteiro, e só.

Fonte e desenho vão embutidos em base64 dentro do SVG, porque o GitHub não
carrega nada externo de dentro de uma imagem. Animação é só CSS.

```sh
pip install fonttools brotli pillow
python tools/colagem.py   # gera todas as tiras
python tools/recibo.py    # só a tira da música (sem chave do Last.fm sai com EXEMPLO)
```

- `tools/colagem.py`: a cena inteira. As posições ficam em `montar()`, e as
  tiras (altura, link e texto alternativo) em `TIRAS`.
- `tools/kit.py`: paleta, fontes, fita crepe, sombras.
- `assets/art/`: seus desenhos. `assets/art/recortes/`: objetos recortados do
  layout do site (comidinhas, Nendoroids, prancheta, o "Gostou?").
  Troque um PNG com o mesmo nome e rode o build de novo.
- `tools/fonts/`: Gochi Hand, Bagel Fat One, Dela Gothic One, Lilita One e
  DotGothic16 (todas OFL), já cortadas.

Depois de mexer em `TIRAS`, regenere o README:

```sh
python -c "import sys; sys.path.insert(0,'tools'); import colagem; open('README.md','w').write(colagem.readme()+'\n\n<br clear=\"all\">\n')"
```

## recibo da semana

O workflow `.github/workflows/recibo.yml` roda todo domingo. Pra ele usar os seus dados:

1. Crie uma chave de API em https://www.last.fm/api/account/create
2. No repositório: Settings → Secrets and variables → Actions
   - em **Secrets**, crie `LASTFM_API_KEY` com a chave
   - em **Variables**, crie `LASTFM_USER` com o seu usuário do Last.fm
3. Actions → recibo da semana → Run workflow, pra gerar o primeiro.

Se você ouve no Spotify, ligue o scrobble do Spotify no Last.fm (Settings → Applications).
