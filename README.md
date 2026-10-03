# Labirinto Isométrico + Laboratório de Busca

Projeto final de Inteligência Artificial: labirinto isométrico com
perseguidor por IA, mais um Laboratório de Busca que expõe os 9 métodos
de busca exigidos na atividade (amplitude, profundidade, profundidade
limitada, aprofundamento iterativo, bidirecional, custo uniforme,
greedy, A-estrela e AIA-estrela).

Os algoritmos de busca são os disponibilizados pelo professor, em
`algoritmos/busca/` (`buscaNP.py` e `BuscaP.py`) — não foram alterados.

**Instruções completas de instalação, execução e uso das duas
interfaces gráficas: veja [`ReadMe.txt`](./ReadMe.txt).**

## Instalação rápida

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Arquitetura

O projeto segue arquitetura em camadas (dominio → aplicacao →
apresentacao/infraestrutura), detalhada na seção 6 do `ReadMe.txt`.
Convenção de código: **camelCase**, em português — decisão deliberada
para este projeto.
