# kitsuneislife: README do perfil

O README do perfil do GitHub é uma colagem. A ideia é a estética de site
pessoal dos anos 2000 (Neocities), só que no meu estilo: céu azul de
pontinhos, nuvens de papelão, meus desenhos à mão e recortes de objetos de
verdade (fita crepe, clipe, tachinha, comidinha, cabecinha de Nendoroid).
Tudo junto e encavalado, nada de componentes soltos e espaçados.

## Regras

- Trabalhar na branch `rework`.
- Commits saem como `kitsuneislife <kitsuneislif3@gmail.com>`. Sem
  `Co-Authored-By`, sem `Claude-Session`, sem trailer nenhum.
- Nunca usar meu nome real, em lugar nenhum (texto, alt, commit). No crachá
  e nos textos o nome é "kitsune".
- Não criar PR nem juntar na `main` sem eu pedir.
- Este CLAUDE.md fica só na `rework`: nunca vai pra `main`, nem no histórico.
  A `rework` é a `main` mais o commit deste arquivo, então pra mandar pra
  `main` é squash, tirando ele:

  ```sh
  git fetch origin main && git merge origin/main      # na rework: traz os commits do boletim
  git checkout -B main origin/main
  git merge --squash rework && git rm -q --cached CLAUDE.md
  git commit -m "o que mudou" && git push origin main
  rm CLAUDE.md                                        # ficou solto; volta no checkout
  git checkout rework && git merge origin/main && git push origin rework
  ```
- Conversa em português, do jeito que eu escrevo (informal).
- A tira da bio linka pro `kitsuneislife.github.io` (a placa "site novo!").
  Lá o site antigo tá guardado em `archive/2025/` e, por enquanto, a página
  inicial é a de "site em obra", no mesmo estilo do README. O jogo `lover`
  (`kitsuneislife.github.io/lover/`) é outro repo.

## Estilo

- Paleta (`tools/kit.py`): céu `#3d8ce6` → `#9fd2fa`, tinta `#1d1c22`,
  lima `#d3ec3c`, rosa `#ffb3d1`, vermelho do crachá `#b7213f`, amarelo das
  estrelas `#f8cf3a`, anil dos links `#5a62df`.
- Fontes (subsetadas e embutidas em cada SVG, `tools/fonts/`):
  - **Bagel Fat One**: logotipo de adesivo, cada letra torta, contorno
    preto, borda branca e sombra azul-escura (`logo()`).
  - **Dela Gothic One**: títulos, e tem japonês (ようこそ!).
  - **Gochi Hand**: letra à mão dos bilhetes, igual à do banner original.
  - **DotGothic16**: o recibo da semana.
- Recortes são PNG de verdade com fundo transparente (`assets/art/recortes/`).
  Fita é sempre recorte de verdade, nunca desenhada em SVG: a crepe
  (`fita.png`, `fita-preta.png`) ou as washi (`washi-*.png`,
  `washi-rasgada-*.png`). Bilhetes vão presos com clipe, tachinha, alfinete
  ou prendedor (`prendedor-rosa.png`).
- Também tem: tesoura, lupa (o vidro é transparente), caneta Bic, lápis,
  régua, esquadro, lacre, tachinha vermelha, cursores de pixel
  (`mao-pixel.png`, `seta-pixel.png`) e a barra de ferramentas do Paint.
- Eu amo neobrutalismo: os adesivos em SVG com contorno preto grosso (a
  setinha amarela gordinha, as estrelas, os corações, as etiquetas) são
  pra manter. O papel quadriculado vetorizado também.
- Nada de strass/pedrinhas.
- Animação: na capa e no resto, pouca e sutil (eu flutuando, estrelas
  piscando, o letreiro). Nos projetinhos pode ter mais movimento, cada
  objeto do jeito dele: o logo pula, o botão afunda quando a setinha
  clica, as teclas apertam, os corações batem, o balão treme, o cursor do
  ingresso pisca. Sempre respeitando `prefers-reduced-motion`.
- Os desenhos são meus. Não colocar imagem do Pinterest ou de outra
  pessoa na colagem; o Pinterest é só referência.

## Referências

- O banner antigo do README: `archive/old/banner-2025.png`.
- O layout do site no Figma (o `website.png` do References.zip) e meus
  desenhos que vieram junto.
- Pinterest: <https://br.pinterest.com/kitsuneislif3/to-shuffles/> e
  <https://br.pinterest.com/kitsuneislif3/fontes/>. Sem login só aparecem
  uns 23 pins por board; se precisar de mais, me pedir as imagens.
- O que guia: capa de revista japonesa, interface de Persona, página de
  diário cheia de adesivo, scrapbook.

## Como a colagem funciona

Tudo em `tools/` (detalhes em `tools/README.md`):

- `tools/colagem.py` monta uma cena só, de 880 de largura, e fatia em tiras
  (`TIRAS`). Cada tira é a mesma cena com outro `viewBox`, então o que
  atravessa a emenda continua do outro lado. Gera
  `assets/readme/colagem-*.svg`.
- No README cada tira é `<img width="100%" align="left">`. É o único jeito
  de o GitHub empilhar imagem sem fresta (lado a lado ele põe 20px de
  padding). Link só dá por tira inteira.
- Elemento animado tem que ficar inteiro dentro de uma tira só, senão a
  animação dessincroniza na emenda.
- `Cena.subir(a_partir, d)` sobe tudo que vem abaixo de um ponto; usar isso
  em vez de mexer coordenada por coordenada.
- Depois de mudar a cena: `python tools/colagem.py` e regerar o README com
  `colagem.readme()` (ver `tools/README.md`). Validar o XML dos SVGs.
- O README foca nos projetinhos e no que eu sei fazer. A ordem é capa,
  bio, projetinhos (numa folha quadriculada amarela), o que eu sei fazer e
  o fim.
- O céu anoitece no fim: começa azul na capa, passa pelo rosa e roxo atrás
  do boletim e termina azul-marinho no rodapé, com lua, estrelinhas e a
  fileira de botõezinhos 88x31.
- O "o que eu sei fazer" é um boletim escolar dinâmico: `tools/boletim.py`
  tira as notas das linguagens dos repositórios e o workflow
  `.github/workflows/boletim.yml` atualiza todo dia (com o `GITHUB_TOKEN`).
- O then and now (fichário de jeans), o recibo da semana do Last.fm e a
  prancheta antiga do "o que eu sei fazer" estão em `archive/colagem/`.
- `archive/` guarda tudo que veio antes: `archive/old/` (o site antigo e o
  banner de 2025) e `archive/branches/` (cópia da `main`, `kitsune` e `src`
  antes de serem apagadas).
- `assets/conferencias/`: prints e recortes de teste usados pra conferir a
  colagem. Não entram no README.
- Sempre conferir olhando: print da página com Playwright, de preferência
  do GitHub de verdade, no desktop e com 390px de largura, sem rolagem
  lateral.

## Skills

Instalar em `~/.claude/skills` no começo da sessão (o container é efêmero):

- Escrita: [humanizer](https://www.skills.sh/blader/humanizer/humanizer),
  [no-ai-slop](https://www.skills.sh/petergyang/no-ai-slop/no-ai-slop).
- Design: [impeccable](https://www.skills.sh/pbakaus/impeccable/impeccable),
  [web-design-guidelines](https://www.skills.sh/vercel-labs/agent-skills/web-design-guidelines),
  [frontend-design](https://www.skills.sh/anthropics/skills/frontend-design),
  [claudedesignskills](https://github.com/freshtechbro/claudedesignskills),
  [higgsfield-claude-skills](https://github.com/AKCodez/higgsfield-claude-skills).

## Pendente

- Se o recibo voltar: usuário do Last.fm e a API key.
- Export da prancheta da bio sem a turma, pra letra ficar maior.
- O site novo de verdade no `kitsuneislife.github.io` (hoje é só a página de
  "site em obra").
