import numpy as np  
import random as rd
#-----------------------------------------------------------------------------
# IMPORTA O GRAFO DE ARQUIVO TEXTO
#-----------------------------------------------------------------------------
def Gera_Problema_Grafo_NP(arquivo):
    f = open(arquivo,"r",encoding="utf-8")
    grafo = {}
    for str1 in f:
        str1 = str1.strip("\n")
        str1 = str1.split(",")
        grafo[str1[0]] = str1[1:]
    return grafo
#-----------------------------------------------------------------------------
# GERA GRID ALEATÓRIO
#-----------------------------------------------------------------------------
def Gera_Problema_Grid_Ale(nx,ny,qtd):
    mapa = np.zeros((nx,ny),int)
    
    k = 0
    while k<qtd:
        i = rd.randrange(0,nx)
        j = rd.randrange(0,ny)
        if mapa[i][j]==0:
            mapa[i][j] = 9
            k+=1
    return mapa,nx,ny
#-----------------------------------------------------------------------------
# GERA O GRID DE ARQUIVO TEXTO
#-----------------------------------------------------------------------------
def Gera_Problema_Grid_Fixo(arquivo):
    file = open(arquivo)
    mapa = []
    for line in file:
        aux_str = line.strip("\n")
        aux_str = aux_str.split(",")
        aux_int = [int(x) for x in aux_str]
        mapa.append(aux_int)
    nx = len(mapa)
    ny = len(mapa[0])
    return mapa,nx,ny

def imprimeCaminho(texto,caminho,custo):
    print("\n*****",texto,"*****")
    print("Caminho: ",caminho)
    print("Custo..: ",len(caminho)-1)

#--------------------------------------------------------------------------
# IMPORTA DADOS DO ARQUIVO
#--------------------------------------------------------------------------
def Gerar_Problema_Grafo_P(arq):
    grafo = {}
    with open(arq,"r") as f:
        for dados in f:
            dados = dados.strip()
            dados = dados.split(",")
            aux1 = []
            for i in range (1,len(dados),2):
                aux=[]
                aux.append(dados[i])
                aux.append(int(dados[i+1]))
                aux1.append(aux)
            grafo[dados[0]] = aux1
        
    return grafo
#-----------------------------------------------------------------------------
# GERA GRID ALEATÓRIO
#-----------------------------------------------------------------------------
def Gera_Problema_Grid_Ale_P(nx,ny,qtd):
    mapa = np.zeros((nx,ny),int)
    
    k = 0
    while k<qtd:
        i = rd.randrange(0,nx)
        j = rd.randrange(0,ny)
        if mapa[i][j]==0:
            mapa[i][j] = 9
            k+=1
    return mapa,nx,ny
#-----------------------------------------------------------------------------
# GERA O GRID DE ARQUIVO TEXTO
#-----------------------------------------------------------------------------
def Gera_Problema_Grid_Fixo_P(arquivo):
    file = open(arquivo)
    mapa = []
    for line in file:
        aux_str = line.strip("\n")
        aux_str = aux_str.split(",")
        aux_int = [int(x) for x in aux_str]
        mapa.append(aux_int)
    nx = len(mapa)
    ny = len(mapa[0])
    return mapa,nx,ny
