==================================================================
 LABIRINTO ISOMÉTRICO
==================================================================

Este projeto é um jogo de labirinto isométrico com perseguidor por IA.
O jogador tenta escapar do perseguidor, usando movimentos, poções e
itens especiais, enquanto o inimigo aplica métodos de busca para
localizar o caminho até a saída.

------------------------------------------------------------------
1. REQUISITOS DO SISTEMA
------------------------------------------------------------------

Antes de começar, certifique-se de que o computador possui:

- Python 3.10 ou superior
- pip instalado
- Git (opcional, apenas se for clonar o repositório)
- Um ambiente gráfico com suporte a SDL/Pygame

Em Linux, normalmente basta ter o Python e as bibliotecas padrão do
sistema. Em um servidor sem interface gráfica, será necessário usar um
X server virtual, como no exemplo abaixo.

------------------------------------------------------------------
2. BAIXAR O PROJETO
------------------------------------------------------------------

Se o projeto já estiver em sua máquina, entre na pasta do repositório.
Exemplo:

  cd /caminho/para/projetoFinalIA

Se for clonar do GitHub:

  git clone <URL_DO_REPOSITORIO>
  cd projetoFinalIA

------------------------------------------------------------------
3. CRIAR AMBIENTE VIRTUAL
------------------------------------------------------------------

Linux/macOS:

  python3 -m venv .venv
  source .venv/bin/activate

Windows (PowerShell):

  py -m venv .venv
  .\.venv\Scripts\Activate.ps1

Windows (cmd):

  py -m venv .venv
  .\.venv\Scripts\activate.bat

------------------------------------------------------------------
4. INSTALAR DEPENDÊNCIAS
------------------------------------------------------------------

Na pasta do projeto, com o ambiente virtual ativado, execute:

  pip install --upgrade pip
  pip install -r requirements.txt

O arquivo requirements.txt contém a única dependência do projeto:

  pygame>=2.5.0

------------------------------------------------------------------
5. EXECUTAR O JOGO
------------------------------------------------------------------

Com o ambiente virtual ativado, rode:

  python main.py

Ou, no Linux, com versão explícita:

  python3 main.py

O jogo inicia a partir de main.py, que chama a composição da raiz e
abre a interface gráfica do jogo.

------------------------------------------------------------------
6. EXECUÇÃO EM SERVIDOR / SEM TELA GRÁFICA
------------------------------------------------------------------

Se o projeto estiver sendo executado em um servidor, container ou em um
ambiente sem monitor, use um X virtual:

  xvfb-run -a python3 main.py

Isso é especialmente útil em ambientes de teste automatizado ou em
servidores remotos sem interface gráfica.

------------------------------------------------------------------
7. COMO JOGAR
------------------------------------------------------------------

No menu principal:

- Escolha a opção "JOGAR"
- Escolha o método de busca usado pelo perseguidor
- Opcionalmente informe origem e destino personalizados no formato
  linha,coluna
- Deixe em branco para que o sistema escolha posições aleatórias
- Clique em "JOGAR" ou pressione Enter

Durante a partida:

  W / A / S / D   ou setas -> mover o jogador
  Espaço         -> usar poção de coragem
  R              -> reiniciar/avançar de fase depois de vitória ou derrota
  Esc            -> voltar ao menu

------------------------------------------------------------------
8. OBSERVAÇÕES IMPORTANTES
------------------------------------------------------------------

- O projeto usa arquivos de busca em algoritmos/busca/ como referência
  do professor. Esses arquivos não devem ser alterados, e a interface
  gráfica usa a camada de aplicação para integrar esse código.
- O jogo foi estruturado em camadas para separar domínio, aplicação,
  infraestrutura e apresentação.
- O jogo foi testado com Python 3.10+ e Pygame 2.5+

------------------------------------------------------------------
9. SOLUÇÃO DE PROBLEMAS
------------------------------------------------------------------

Se o comando "python main.py" não funcionar:

- Verifique se o ambiente virtual está ativado
- Confirme que o Python usado é o 3.10 ou superior
- Atualize o pip e reinstall as dependências

Comandos úteis:

  python --version
  pip --version
  pip install -r requirements.txt

Se o erro for relacionado à biblioteca gráfica, confirme que o sistema
possui suporte para SDL/Pygame e, em caso de ausência de interface,
utilize xvfb-run.

------------------------------------------------------------------
10. ESTRUTURA PRINCIPAL DO PROJETO
------------------------------------------------------------------

- main.py              → ponto de entrada do jogo
- composicaoRaiz.py    → montagem da aplicação
- apresentacao/        → interface e renderização
- aplicacao/           → regras e fluxo do jogo
- dominio/             → lógica do labirinto e entidades
- infraestrutura/      → persistência e adaptadores
- algoritmos/busca/    → algoritmos de busca de referência
- requirements.txt     → dependências do projeto

------------------------------------------------------------------
11. RESUMO DE EXECUÇÃO DO ZERO
------------------------------------------------------------------

1. Instale o Python 3.10+
2. Abra a pasta do projeto
3. Crie um ambiente virtual
4. Ative o ambiente virtual
5. Instale as dependências com pip install -r requirements.txt
6. Execute: python main.py

Se tudo estiver correto, o jogo será iniciado e a interface gráfica
será carregada.

==================================================================
FIM DO README
==================================================================
