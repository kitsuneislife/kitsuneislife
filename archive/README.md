# guardado

Partes da colagem que saíram do README por enquanto, pra ele focar nos
projetinhos e no que eu sei fazer.

- `then-and-now.svg`: o fichário de jeans aberto, com eu em 2016 na página
  vermelha e em 2026 na amarela.
- `no-fone-essa-semana.svg`: o recibo da semana com as músicas do Last.fm.
  Tá com os dados de exemplo.
- `banner-habilidades.png`: a prancheta antiga do "o que eu sei fazer",
  com o "so cold..." e o Danoninho.
- `tools/colagem.py`: o gerador do jeito que estava com as duas partes
  (`fichario()` e `musica()`), com as coordenadas de antes.
- `tools/recibo.py` e `workflows/recibo.yml`: o que buscava o Last.fm todo
  domingo. O workflow fica aqui fora de `.github/` pra não rodar.

Os desenhos que elas usam continuam em `assets/art/` (`eu-2016.png`,
`eu-2026.png`, `fone.png`, as comidinhas e as cabecinhas de Nendoroid).

Pra trazer de volta: copiar a função de `archive/tools/colagem.py` pra
`tools/colagem.py`, chamar em `montar()`, abrir espaço com `Cena.subir()` e
pôr a tira de volta em `TIRAS`. O recibo também precisa do `recibo.py` em
`tools/` e do workflow em `.github/workflows/`.
