# Labirinto Isométrico

Projeto final de Inteligência Artificial: labirinto isométrico com
perseguidor por IA, em que o jogador tenta escapar do perseguidor usando
uma combinação de movimentos, poções e itens especiais.

Os algoritmos de busca são disponibilizados pelo professor em
`algoritmos/busca/` (`buscaNP.py` e `BuscaP.py`) e são usados dentro do
jogo para o comportamento do perseguidor.

## Instalação rápida

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Arquitetura

O projeto segue arquitetura em camadas (dominio → aplicacao →
apresentacao/infraestrutura), detalhada em `ReadMe.txt`.
Convenção de código: camelCase, em português, adotada deliberadamente para
este projeto.
