from algoritmos.busca.buscaNP import buscaNP
import algoritmos.busca.utils as fa
from os import system

op = 1
while(op!='3'):
    system("cls")
    print("**** TIPO DE EXECUÇÃO ****\n")
    print("1. GRAFO")
    print("2. GRID")
    print("3. SAIR")
    op = input("Sua opção: ")
    
    flag_menu = True
    if op=='1':
        #---------------- Executa Grafo -----------------------------
        arquivo = "Romenia_Sem_Pesos.txt"
        grafo = fa.Gera_Problema_Grafo_NP(arquivo)
        print("\n====== LISTA DE NÓS ======")
        for no in grafo:
            print(no, end=' ')
        origem  = input("\n\n\nOrigem......: ").upper()
        destino = input("Destino.....: ").upper()
        flag_origem  = origem in grafo
        flag_destino = destino in grafo
        flag_dados = flag_origem and flag_destino
        flag_grafo = True
        #------------------------------------------------------------
    elif op=='2':
        #---------------- Executa Grig ------------------------------
        arquivo = "mapa4.txt"
        mapa,dx,dy = fa.Gera_Problema_Grid_Fixo(arquivo)
        for x in mapa:
            print(x)
        # Entrada de dados para busca em grid
        origem  = tuple(map(int, input("Digite a origem (x y): ").split()))
        destino = tuple(map(int, input("Digite o destino (x y): ").split()))
        flag_origem  = (0<=origem[0]<dx)  and (0<=origem[1]<dy)  and (mapa[origem[0]][origem[1]]==0)
        flag_destino = (0<=destino[0]<dx) and (0<=destino[1]<dy) and (mapa[destino[0]][destino[1]]==0)
        flag_dados = flag_origem and flag_destino
        flag_grafo = False
    else:
        flag_menu = False      
        #------------------------------------------------------------

    if flag_menu:
        if flag_dados:
            sol = buscaNP()
            
            # AMPLITUDE
            if flag_grafo:
                caminho = sol.amplitude_grafo(origem,destino,grafo)
            else:
                caminho = sol.amplitude_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("AMPLITUDE", caminho, len(caminho))
            else:
                print("AMPLITUDE\nCAMINHO NÃO ENCONTRADO")
            
            # PROFUNDIDADE
            if flag_grafo:
                caminho = sol.profundidade_grafo(origem,destino,grafo)
            else:
                caminho = sol.profundidade_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("PROFUNDIDADE", caminho, len(caminho))
            else:
                print("PROFUNDIDADE\nCAMINHO NÃO ENCONTRADO")    
           
            # PROFUNDIDADE LIMITADA
            limite = 3
            if flag_grafo:
                caminho = sol.prof_limitada_grafo(origem,destino,grafo,limite)
            else:
                caminho = sol.prof_limitada_grid(origem,destino,dx,dy,mapa,limite)
            if caminho!=None:
                fa.imprimeCaminho("PROFUNDIDADE LIMITADA", caminho, len(caminho))
            else:
                print("PROFUNDIDADE LIMITADA\nCAMINHO NÃO ENCONTRADO")
            
            # APROFUNDAMENTO ITERATIVO
            if flag_grafo:
                l_max = len(grafo)
                caminho = sol.aprof_iterativo_grafo(origem,destino,grafo,l_max)
            else:
                l_max = dx + dy
                caminho = sol.aprof_iterativo_grid(origem,destino,dx,dy,mapa,l_max)
            if caminho!=None:
                fa.imprimeCaminho("APROFUNDAMENTO ITERATIVO", caminho, len(caminho))
            else:
                print("APROFUNDAMENTO ITERATIVO\nCAMINHO NÃO ENCONTRADO")

            # BIDIRECIONAL
            if flag_grafo:
                caminho = sol.bidirecional_grafo(origem,destino,grafo)
            else:
                caminho = sol.bidirecional_grid(origem,destino,dx,dy,mapa)
            if caminho!=None:
                fa.imprimeCaminho("BIDIRECIONAL", caminho, len(caminho))
            else:
                print("BIDIRECIONAL\nCAMINHO NÃO ENCONTRADO")# PROFUNDIDADE
                if flag_grafo:
                    caminho = sol.profundidade_grafo(origem,destino,grafo)
                else:
                    caminho = sol.profundidade_grid(origem,destino,dx,dy,mapa)
                if caminho!=None:
                    fa.imprimeCaminho("PROFUNDIDADE", caminho, len(caminho))
                else:
                    print("PROFUNDIDADE\nCAMINHO NÃO ENCONTRADO")    
                    
        else:
            print("Estados inválidos!")
           
        op = input("Pressione ENTER para continuar!")