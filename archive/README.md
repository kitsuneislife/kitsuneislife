# archive

Tudo que veio antes, guardado. Nada daqui aparece no README.

## colagem/

Partes da colagem atual que saíram do README por enquanto.

- `then-and-now.svg`: o fichário de jeans aberto, com eu em 2016 na página
  vermelha e em 2026 na amarela.
- `no-fone-essa-semana.svg`: o recibo da semana com as músicas do Last.fm,
  com os dados de exemplo.
- `banner-habilidades.png`: a prancheta antiga do "o que eu sei fazer", com o
  "so cold..." e o Danoninho.
- `tools/colagem.py`: o gerador do jeito que estava com o then and now e o
  recibo (`fichario()` e `musica()`), com as coordenadas de antes.
- `tools/recibo.py` e `workflows/recibo.yml`: o que buscava o Last.fm todo
  domingo. O workflow fica aqui fora de `.github/` pra não rodar.

Pra trazer uma parte de volta: copiar a função de `colagem/tools/colagem.py`
pra `tools/colagem.py`, chamar em `montar()`, abrir espaço com
`Cena.subir()` e pôr a tira de volta em `TIRAS`. O recibo também precisa do
`recibo.py` em `tools/` e do workflow em `.github/workflows/`.

## old/

A pasta `old/` que existia na raiz: o site antigo (`index.html`,
`script.js`, `style.css`, `assets/`, `scripts/`), a pasta `Legacy/` com as
versões mais antigas e o banner do README de 2025 (`banner-2025.png`).

## branches/

Uma cópia dos arquivos de cada branch do jeito que estavam antes de serem
apagadas:

- `main/`: a `main` no commit `fa59cff` ("Modify image in README and add a
  caption"), com o README antigo, `banner.png`, `i_love_claude.png` e a
  `old/` dela.
- `kitsune/` e `src/`: as duas no mesmo commit, `b322dfc` ("update import
  states"), com o site antigo (home, blog, media log, animes, filmes,
  séries).

O histórico de commits continua no git mesmo depois de apagar as branches,
enquanto algum commit apontar pra ele; essas pastas são pra achar os
arquivos sem precisar mexer no git.
