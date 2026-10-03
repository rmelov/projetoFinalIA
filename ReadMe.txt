==================================================================
 LABIRINTO ISOMÉTRICO + LABORATÓRIO DE BUSCA
 ReadMe.txt
==================================================================

Este projeto tem DUAS interfaces gráficas:

  1) O JOGO (labirinto isométrico com perseguidor por IA)
  2) O LABORATÓRIO DE BUSCA (interface pedida na atividade: selecionar
     método, definir estado inicial/objetivo, executar, ver o caminho
     encontrado e seu custo, e a imagem do problema com o caminho
     desenhado)

Os métodos de busca (amplitude, profundidade, profundidade limitada,
aprofundamento iterativo, bidirecional, custo uniforme, greedy, A-estrela
e AIA-estrela) estão implementados em algoritmos/busca/buscaNP.py e
algoritmos/busca/BuscaP.py, com base no código disponibilizado pelo
professor. Esses dois arquivos NÃO foram alterados.

------------------------------------------------------------------
1. BIBLIOTECAS E SOFTWARE NECESSÁRIOS
------------------------------------------------------------------

- Python 3.10 ou superior (testado com Python 3.12)
- pip
- Biblioteca Python: pygame >= 2.5.0 (única dependência, listada em
  requirements.txt)
- Um ambiente com suporte gráfico (SDL). Em servidores sem tela, use um
  X server virtual:  xvfb-run -a python3 main.py

------------------------------------------------------------------
2. COMO INSTALAR E EXECUTAR
------------------------------------------------------------------

  cd projetoFinalIA
  python3 -m venv .venv
  source .venv/bin/activate          (Windows: .venv\Scripts\activate)
  pip install -r requirements.txt
  python3 main.py

O jogo abre em tela cheia. Se estiver rodando sem monitor (servidor),
use "xvfb-run -a python3 main.py".

------------------------------------------------------------------
3. FUNCIONAMENTO DA INTERFACE 1: O JOGO
------------------------------------------------------------------

No menu principal, escolha "JOGAR":
  - Escolha o método de busca que o perseguidor vai usar para te
    encontrar (Profundidade, Profundidade Limitada, Aprofundamento
    Iterativo, Amplitude ou Bidirecional).
  - Opcionalmente, digite origem e destino personalizados (formato
    "linha,coluna"). Deixe em branco para posições aleatórias.
  - Clique em JOGAR (ou Enter) para iniciar.

Controles durante a partida:
  W A S D ou setas .... mover
  Espaço ............... usar poção de coragem
  R ..................... reiniciar / avançar de fase (após vitória/derrota)
  Esc .................. voltar ao menu

------------------------------------------------------------------
4. FUNCIONAMENTO DA INTERFACE 2: LABORATÓRIO DE BUSCA
------------------------------------------------------------------

No menu principal, escolha "LABORATÓRIO DE BUSCA". Esta tela:

  a) REAPROVEITA O LABIRINTO DA PARTIDA EM ANDAMENTO
     Se você já jogou nesta sessão, o Laboratório abre mostrando
     exatamente o mesmo labirinto, a mesma posição do jogador (origem
     padrão) e a mesma saída (destino padrão) da partida em curso — o
     texto acima da grade mostra "Labirinto: partida em andamento".
     Se você ainda não jogou, ele gera um labirinto de exemplo (mesmo
     gerador usado pelo jogo) e mostra "labirinto de exemplo (nenhuma
     partida em andamento)".
     O botão "USAR LABIRINTO ATUAL (N)" atualiza a tela com o estado
     mais recente da partida (por exemplo, depois de avançar de nível).

  b) SELETOR DE MÉTODO (painel à esquerda)
     Lista com os 9 métodos exigidos na atividade. Navegue com W/S (ou
     as setas) ou clique diretamente sobre o nome do método. Métodos
     marcados "(ponderado)" usam custo de movimento diferente por
     direção (BuscaP.py); os demais contam passos (buscaNP.py).

  c) DEFINIÇÃO DO ESTADO INICIAL E DO OBJETIVO (imagem central)
     A imagem mostra TODOS os estados do problema: cada quadrado é uma
     célula livre (clara) ou parede (escura). Origem e destino já vêm
     preenchidos (ver item a), mas podem ser trocados:
       - Clique ESQUERDO numa célula livre define a ORIGEM (verde).
       - Clique DIREITO numa célula livre define o DESTINO (vermelho).

  d) BOTÃO EXECUTAR
     Roda o método selecionado entre a origem e o destino atuais.
     Também pode ser acionado com Enter/Espaço.

  e) ÁREA DE RESULTADO (painel à direita)
     Mostra, após a execução: se um caminho foi encontrado, o CUSTO do
     caminho, o número de passos, o tempo de execução em milissegundos
     e a sequência completa de estados do caminho. Se não houver
     caminho, mostra "Caminho não encontrado."

  f) IMAGEM DO PROBLEMA COM O CAMINHO
     Depois de executar, o caminho é desenhado sobre o grid, na cor
     associada ao método selecionado.

  Esc: volta ao menu principal.

------------------------------------------------------------------
5. OBSERVAÇÕES SOBRE OS MÉTODOS
------------------------------------------------------------------

- "Profundidade Limitada" usa um limite propositalmente pequeno (3
  passos) no Laboratório de Busca, do mesmo jeito que no exemplo do
  professor — por isso ela costuma FALHAR em encontrar o destino
  quando ele está longe da origem. Isso é esperado: mostra na prática
  a limitação do método. No JOGO, esse mesmo método usa um limite maior
  (50 passos), senão o inimigo nunca se moveria.
- "Aprofundamento Iterativo" usa um limite generoso (conta as células
  livres do grid) para garantir que encontre o caminho sempre que ele
  existir, repetindo a busca com limites crescentes.
- Os arquivos algoritmos/busca/principalBuscaComPesos.py e
  principalBuscaSemPesos.py são os scripts de linha de comando do
  professor, mantidos como referência. Não fazem parte da interface
  gráfica e alguns exigem arquivos de mapa/grafo que não acompanham
  este repositório (Mapa_P1.txt, Grafo_Prova.txt, mapa4.txt).

------------------------------------------------------------------
6. ARQUITETURA DO PROJETO
------------------------------------------------------------------

O projeto segue arquitetura em camadas, com a regra de que as setas de
dependência só apontam para dentro (a camada de fora conhece a de
dentro; nunca o contrário):

  apresentacao  →  aplicacao  →  dominio
  infraestrutura → aplicacao  →  dominio
  algoritmos/busca (congelado, não alterado)

algoritmos/busca/     Código de busca do professor — NÃO alterado.

dominio/              Regras do jogo, sem pygame e sem I/O:
  mapa/                 Coordenada, Labirinto, GeradorLabirinto
  entidades/            Jogador, Perseguidor (recebe o buscador por
                         injeção — não conhece buscaNP/BuscaP)
  itens/                PocaoCoragem, Vortex, Saida (só estado)
  progresso/            Placar, Mochila, ProgressoJogador
  regras/               Constantes de pontuação, tempo e nível
  coordenadas/          ParserCoordenada, ValidadorCoordenada

aplicacao/            Orquestração dos casos de uso:
  metodosBusca.py       Catálogo único dos 9 métodos (única fonte de
                         verdade — para acrescentar um método novo no
                         futuro, basta editar este arquivo)
  partida.py            Substitui a antiga EstadoJogo (351 linhas, 7
                         responsabilidades); aqui só orquestra
  preparadorFase.py, posicionadorAleatorio.py, arbitroPartida.py,
  controladorPerseguidor.py, portaBuscaCaminho.py, resultadoBusca.py

infraestrutura/       Fala com o mundo externo:
  busca/adaptadorBusca.py     Único lugar que importa buscaNP/BuscaP
  persistencia/repositorioRecorde.py   Cacheia o recorde em memória

apresentacao/         Tudo que usa pygame:
  recursos/             Fontes, CacheImagens, AnimadorSprite, FabricaSprites
  entrada/              Acao (enum), MapeadorTeclas
  cena/                 RenderizadorCena e as camadas (chão, paredes,
                         entidades, itens, rastro, rota da saída,
                         mini-mapa, textos flutuantes)
  hud/                  Hud, PainelRecorde
  ui/                   Botao
  telas/                TelaMenu, TelaModos, TelaCoordenadas, TelaTexto
                         (serve tutorial e sobre), TelaLaboratorioBusca,
                         NavegadorTelas
  loopJogo.py           Laço principal de uma partida

composicaoRaiz.py     Único lugar que decide QUEM implementa cada peça
                       e conecta tudo (composition root).
main.py               5 linhas: chama composicaoRaiz e inicia.
