import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import os

USA13 = [
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
]


def gerar_populacao(tamanho, num_cidades):
    populacao = []
    for _ in range(tamanho):
        rota = list(range(num_cidades))
        random.shuffle(rota)
        populacao.append(rota)
    return populacao

def fitness(rota):
    distancia = 0
    for i in range(len(rota) - 1):
        distancia += USA13[rota[i]][rota[i + 1]]
    distancia += USA13[rota[-1]][rota[0]]
    return 1 / distancia

def selecao(populacao, torneio):
    selecionados = random.sample(populacao, torneio)
    return max(selecionados, key=fitness).copy()

def aplicar_crossover(pai1, pai2, taxa_crossover=0.9):
    if random.random() > taxa_crossover:
        return pai1.copy(), pai2.copy()
    tamanho = len(pai1)
    a, b = sorted(random.sample(range(tamanho), 2))
    filho1 = [-1] * tamanho
    filho2 = [-1] * tamanho
    filho1[a:b+1] = pai1[a:b+1]
    filho2[a:b+1] = pai2[a:b+1]

    def preencher(filho, outro):
        posicao = (b + 1) % tamanho
        for gene in outro:
            if gene not in filho:
                filho[posicao] = gene
                posicao = (posicao + 1) % tamanho
        return filho

    filho1 = preencher(filho1, pai2)
    filho2 = preencher(filho2, pai1)
    return filho1, filho2

def aplicar_mutacao(individuo, taxa_mutacao):
    individuo = individuo.copy()
    for i in range(len(individuo)):
        if random.random() < taxa_mutacao:
            j = random.randint(0, len(individuo) - 1)
            individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

def nova_geracao(populacao, mutacao, elitismo, torneio, tamanho_populacao):
    populacao_ordenada = sorted(populacao, key=fitness, reverse=True)
    nova_pop = populacao_ordenada[:elitismo]
    while len(nova_pop) < tamanho_populacao:
        pai1 = selecao(populacao, torneio)
        pai2 = selecao(populacao, torneio)
        filho1, filho2 = aplicar_crossover(pai1, pai2)
        filho1 = aplicar_mutacao(filho1, mutacao)
        filho2 = aplicar_mutacao(filho2, mutacao)
        nova_pop.extend([filho1, filho2])
    return nova_pop[:tamanho_populacao]


def executar_experimento(nome_exp, valores, param_nome, geracoes=400, execucoes=30):
    num_cidades = len(USA13)
    diretorio = os.path.join("graficos", nome_exp)
    os.makedirs(diretorio, exist_ok=True)

    resultados_boxplot = []
    historicos_por_config = {}

    tamanho_populacao_base = 50
    mutacao_base = 0.05
    elitismo_base = 5
    torneio_base = 3

    for valor in valores:
        melhores_execucoes = []
        historicos = []

        for _ in range(execucoes):
            
            tamanho_populacao = tamanho_populacao_base
            mutacao = mutacao_base
            elitismo = elitismo_base
            torneio = torneio_base

            if param_nome == "tamanho_populacao":
                tamanho_populacao = valor
            elif param_nome == "mutacao":
                mutacao = valor
            elif param_nome == "elitismo":
                elitismo = int(tamanho_populacao_base * valor)
            elif param_nome == "torneio":
                torneio = valor

            populacao = gerar_populacao(tamanho_populacao, num_cidades)
            melhor_dist = float("inf")
            historico = []

            for _ in range(geracoes):
                populacao = nova_geracao(populacao, mutacao, elitismo, torneio, tamanho_populacao)
                melhor = max(populacao, key=fitness)
                dist = 1 / fitness(melhor)
                historico.append(dist)
                if dist < melhor_dist:
                    melhor_dist = dist

            melhores_execucoes.append(melhor_dist)
            historicos.append(historico)

        resultados_boxplot.append(melhores_execucoes)
        historicos_por_config[valor] = np.mean(historicos, axis=0)

        
        plt.figure(figsize=(8, 4))
        plt.plot(np.mean(historicos, axis=0), label=f"{param_nome} = {valor}")
        plt.xlabel("Geração")
        plt.ylabel("Melhor distância (média)")
        plt.title(f"Convergência - {nome_exp} ({param_nome}={valor})")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(diretorio, f"convergencia_{param_nome}_{valor}.png"), dpi=300)
        plt.close()

    
    plt.figure(figsize=(8, 5))
    plt.boxplot(resultados_boxplot, patch_artist=True)
    plt.xticks(range(1, len(valores) + 1), valores)
    plt.xlabel(param_nome)
    plt.ylabel("Melhor distância")
    plt.title(f"Boxplot Comparativo - {nome_exp}")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(diretorio, f"boxplot_{nome_exp}.png"), dpi=300)
    plt.close()


tamanho_populacao_exp_1 = [20, 50, 100]
executar_experimento("experimento_1", tamanho_populacao_exp_1, "tamanho_populacao")

mutacao_exp_2 = [0.01, 0.05, 0.10, 0.20]
executar_experimento("experimento_2", mutacao_exp_2, "mutacao")

torneio_exp_3 = [2, 3, 5, 7]
executar_experimento("experimento_3", torneio_exp_3, "torneio")

elitismo_exp_4 = [0.0, 0.01, 0.05, 0.10]
executar_experimento("experimento_4", elitismo_exp_4, "elitismo")