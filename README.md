# Labirinto Isométrico Aleatório v2

Jogo em Python/Pygame com labirinto isométrico, IA perseguindo o jogador, itens de poção e reinício de fase.

## Requisitos

- Python 3.10+ (foi validado com Python 3.12)
- pip
- Ambiente gráfico do Linux/Windows/macOS com suporte a SDL/Pygame
- Git opcional

## Dependências

O projeto depende somente de:

- pygame>=2.5.0

Arquivo de dependência:

- `requeriments.txt`

## Como rodar

1. Abra o terminal na raiz do projeto:

```bash
cd /home/pessoal/projetoFinalIA
```

2. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requeriments.txt
```

4. Execute o jogo:

```bash
python3 main.py
```

## Observação importante sobre execução

O jogo usa `pygame.FULLSCREEN` e tenta abrir a janela em tela cheia com a resolução atual da máquina. Por isso:

- ele precisa de um ambiente com display disponível;
- em máquinas sem interface gráfica, use um X server virtual, por exemplo:

```bash
xvfb-run -a python3 main.py
```

Se o ambiente for local e você estiver em desktop, normalmente basta rodar o comando sem `xvfb-run`.

## Controles

- `W`, `A`, `S`, `D` ou setas do teclado: movimentação
- `Espaço`: usar poção
- `R`: reiniciar / avançar para o próximo labirinto (quando a condição do jogo permitir)
- `Esc`: sair do jogo

## Estrutura principal

- `main.py`: ponto de entrada do jogo
- `utilidades/config.py`: configurações gerais do jogo
- `utilidades/gerenciadorJogo.py`: loop principal e eventos
- `utilidades/controles.py`: leitura das teclas
- `renderizacao/`: classes de renderização
- `componentes/`: lógica do labirinto, conversão isométrica e inteligência artificial
- `assets/`: fontes, imagens e tiles usados pelo jogo

## Validação executada

Foi testado em ambiente limpo com:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requeriments.txt
python3 main.py
```

O projeto iniciou corretamente e permaneceu em execução sem erros de importação ou dependência.
