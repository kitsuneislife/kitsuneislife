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
```

- `tools/colagem.py`: a cena inteira. As posições ficam em `montar()`, e as
  tiras (altura, link e texto alternativo) em `TIRAS`.
- `tools/kit.py`: paleta, fontes, fita crepe, sombras.
- `assets/art/`: seus desenhos. `assets/art/recortes/`: objetos recortados do
  layout do site (comidinhas, Nendoroids, prancheta, o "Gostou?").
  Troque um PNG com o mesmo nome e rode o build de novo.
- `assets/art/nuvens-ceu.png`: a foto de nuvens que vira a textura do céu na
  capa e no fim (`NUVENS` em `tools/colagem.py`). Ela entra de cabeça pra
  baixo, só como branco transparente por baixo dos pontinhos, e com as pontas
  misturadas pra repetir sem emenda enquanto anda.
- `tools/fonts/`: Gochi Hand, Bagel Fat One, Dela Gothic One, Lilita One e
  DotGothic16 (todas OFL), já cortadas.

Depois de mexer em `TIRAS`, regenere o README:

```sh
python -c "import sys; sys.path.insert(0,'tools'); import colagem; open('README.md','w').write(colagem.readme()+'\n\n<br clear=\"all\">\n')"
```

## boletim

O "o que eu sei fazer" é um boletim escolar com as notas tiradas dos
repositórios. `tools/boletim.py` busca os repositórios públicos (sem fork),
soma os bytes de cada linguagem e grava `assets/readme/boletim.json`; a
maior linguagem tira 10 e as outras vão pela raiz quarta da proporção.
Frequência e faltas são os dias com e sem contribuição no último ano.

O workflow `.github/workflows/boletim.yml` roda todo dia usando o
`GITHUB_TOKEN` do próprio Actions, sem precisar configurar nada. Agendamento
só roda na branch padrão, então ele começa quando isso estiver na `main`;
antes disso dá pra rodar na mão em Actions → boletim → Run workflow.

Sem o json, o boletim sai com dados de exemplo. O que eu tô aprendendo
(`CURSANDO`) e as atividades extras (`EXTRAS`) ficam fixos em
`tools/colagem.py`.

O then and now e o recibo da semana estão guardados em `archive/colagem/`.
