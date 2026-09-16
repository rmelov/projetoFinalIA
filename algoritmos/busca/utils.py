import numpy as np  
import random as rd
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
