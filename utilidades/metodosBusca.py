METODOS_DISPONIVEIS = [
    {
        "id": "profundidade",
        "nome": "Profundidade",
        "ponderado": False,
    },
    {
        "id": "prof_limitada",
        "nome": "Profundidade Limitada",
        "ponderado": False,
    },
    {
        "id": "aprofundamento_iterativo",
        "nome": "Aprofundamento Iterativo",
        "ponderado": False,
    },
    {
        "id": "amplitude",
        "nome": "Amplitude",
        "ponderado": False,
    },
    {
        "id": "bidirecional",
        "nome": "Bidirecional",
        "ponderado": False,
    },
    {
        "id": "custo_uniforme",
        "nome": "Custo Uniforme",
        "ponderado": True,
    },
    {
        "id": "greedy",
        "nome": "Greedy",
        "ponderado": True,
    },
    {
        "id": "a_estrela",
        "nome": "A-Estrela",
        "ponderado": True,
    },
    {
        "id": "aia_estrela",
        "nome": "AIA-Estrela",
        "ponderado": True,
    },
]

METODO_IDS = [metodo["id"] for metodo in METODOS_DISPONIVEIS]
