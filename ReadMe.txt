==================================================================
 LABIRINTO ISOMÉTRICO
==================================================================

Este projeto é um jogo de labirinto isométrico com perseguidor por IA.

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
  X server virtual: xvfb-run -a python3 main.py

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
3. FUNCIONAMENTO DO JOGO
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
4. OBSERVAÇÕES SOBRE OS MÉTODOS
------------------------------------------------------------------

- "Profundidade Limitada" usa um limite propositalmente pequeno (3
  passos) no jogo, do mesmo jeito que no exemplo do professor — por isso
  ela costuma falhar em encontrar o destino quando ele está longe da
  origem. Isso é esperado: mostra na prática a limitação do método.
- "Aprofundamento Iterativo" usa um limite generoso (conta as células
  livres do grid) para garantir que encontre o caminho sempre que ele
  existir, repetindo a busca com limites crescentes.
- Os arquivos algoritmos/busca/principalBuscaComPesos.py e
  principalBuscaSemPesos.py são os scripts de linha de comando do
  professor, mantidos como referência. Não fazem parte da interface
  gráfica e alguns exigem arquivos de mapa/grafo que não acompanham
  este repositório (Mapa_P1.txt, Grafo_Prova.txt, mapa4.txt).

------------------------------------------------------------------
5. ARQUITETURA DO PROJETO
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
  metodosBusca.py       Catálogo único dos 9 métodos
  partida.py            Substitui a antiga EstadoJogo
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
                         (serve tutorial e sobre), NavegadorTelas
  loopJogo.py           Laço principal de uma partida

composicaoRaiz.py     Único lugar que decide QUEM implementa cada peça
                       e conecta tudo (composition root).
main.py               5 linhas: chama composicaoRaiz e inicia.

------------------------------------------------------------------
6. PRINCIPAIS CORREÇÕES FEITAS NESTA REFATORAÇÃO
------------------------------------------------------------------

- BUG CRÍTICO: EstadoJogo recebia o modo de busca escolhido no menu mas
  NUNCA repassava ao Perseguidor — o inimigo sempre perseguia com
  "amplitude", não importa o que o jogador escolhesse. Corrigido: o
  modo agora chega até o Perseguidor (Partida._prepararFaseCompleta).
- BUG: Perseguidor usava hasattr() com os nomes ERRADOS de dois
  métodos ("profundidade_limitada_grid" e "aprofundamento_iterativo_grid",
  que não existem em buscaNP.py), fazendo esses dois modos caírem
  silenciosamente em amplitude. Corrigido: o catálogo único guarda o
  nome REAL de cada método; sem hasattr.
- BUG: BuscaP.py compara `atual.estado == fim` sem converter `fim` para
  tupla, então custo uniforme, greedy, A* e AIA* nunca achavam caminho
  se destino fosse passado como lista (chegava a estourar
  ZeroDivisionError em AIA*). Corrigido no adaptador, sem tocar em
  BuscaP.py.
- BUG: o recorde era lido do disco a cada frame (~30x/segundo).
  Corrigido: RepositorioRecorde cacheia em memória.
- DRY: quatro listas diferentes com os mesmos 5 modos de busca (menu,
  recorde, perseguidor, validação) viraram uma só (metodosBusca.py).
- DRY: a linha tracejada e a detecção de "atrás de parede" estavam
  copiadas entre dois renderizadores; agora vivem em
  apresentacao/cena/caminho/.
- DRY: RenderizadorRotaSaida tinha seu próprio BFS, duplicando
  amplitude_grid; agora usa o mesmo AdaptadorBusca via injeção.
- DRY: Inventario/InventarioPartida e Pontuacao/PontuacaoPartida (pares
  quase idênticos) viraram Mochila e Placar, uma implementação cada.
- SRP: EstadoJogo (351 linhas, 7 responsabilidades) foi dividida em
  Partida, PreparadorFase, PosicionadorAleatorio, ArbitroPartida e
  ControladorPerseguidor.
- SRP: menu.py (325 linhas, 6 responsabilidades) foi dividido em
  TelaMenu, TelaModos, TelaCoordenadas, TelaTexto e NavegadorTelas.
- Removido: RenderizadorMiniMapa (wrapper que só repassava chamadas),
  Hud.calcular_posicoes_campos (código morto), os parâmetros
  texto_origem/texto_destino/campo_ativo (nunca usados), o
  "while rodando" com pygame.quit() inalcançável.
- Números mágicos (9/0 de parede/livre, 7/3/2 de pontos, 2000/10000 de
  duração) viraram constantes nomeadas em dominio/mapa e dominio/regras.
- Todo o código novo segue camelCase (arquivos, classes, métodos,
  variáveis) — convenção diferente do PEP 8 padrão, adotada de forma
  deliberada para este projeto.
