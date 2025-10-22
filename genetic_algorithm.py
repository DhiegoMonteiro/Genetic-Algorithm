import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import knapsack
import pandas as pd
import os

dimensao = 20
tamanho_populacao = 50
geracoes = 500
mutacao = 0.02
elitismo = 2
torneio = 3
execucoes = 30

def gerar_populacao(tamanho_populacao, dimensao):
    populacao = []
    for i in range (tamanho_populacao):
        individuo = [random.randint(0,1) for j in range(dimensao)]
        populacao.append(individuo)
        
    return populacao

def fitness(selecionado):
    valor_total, peso_total, valido = knapsack.knapsack(selecionado, dim=dimensao)

    if not valido:
        return 0

    return valor_total
    

def selecao(populacao):
    selecionados = random.sample(populacao, torneio)
    fitness_values = []
    for individuo in selecionados:
        fitness_values.append(fitness(individuo))

    melhor_indice = np.argmax(fitness_values)
    melhor_individuo = selecionados[melhor_indice]
    
    return melhor_individuo



def aplicar_crossover(tipo_crossover, pai1, pai2, taxa_crossover=0.8):
    """
    Aplica crossover com probabilidade definida pela taxa
    """
    if tipo_crossover == "um ponto":
        if random.random() < taxa_crossover:
            # Aplica crossover (exemplo: crossover de um ponto)
            ponto = random.randint(1, len(pai1) - 1)
            filho1 = pai1[:ponto] + pai2[ponto:]
            filho2 = pai2[:ponto] + pai1[ponto:]
            
        else:
            # Sem crossover - retorna cópias dos pais
            return pai1.copy(), pai2.copy()
    
    elif tipo_crossover == "dois pontos":
        ponto1 = random.randint(1, len(pai1) - 2)
        ponto2 = random.randint(ponto1 + 1, len(pai1) - 1)
        filho1 = pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]
        filho2 = pai2[:ponto1] + pai1[ponto1:ponto2] + pai2[ponto2:]
        
    
    
    elif tipo_crossover == "uniforme":
        filho1, filho2 = [], []
        for i in range(len(pai1)):
            if random.random() < 0.5:
                filho1.append(pai1[i])
                filho2.append(pai2[i])
            else:
                filho1.append(pai2[i])
                filho2.append(pai1[i])
    else:
        raise ValueError("Tipo de crossover inválido, por favor, escolha entre um ponto, dois pontos e uniforme")
    
    return filho1, filho2

def aplicar_mutacao(individuo, mutacao):
    for i in range(len(individuo)):
        if random.random() < mutacao:
            individuo[i] = 1 - individuo[i]  
    return individuo

tipos_crossover = ["um ponto", "dois pontos", "uniforme"]
resultados = {}
convergencia_media = {}

for tipo in tipos_crossover:
    resultados[tipo] = []
    convergencias = []

    print(f"\n=== Executando 30 vezes: Crossover {tipo} ===")
    for execucao in range(execucoes):
        populacao = gerar_populacao(tamanho_populacao, dimensao)
        melhores_por_geracao = []

        for g in range(geracoes):
            nova_populacao = []

            
            populacao = sorted(populacao, key=fitness, reverse=True)
            elites = populacao[:elitismo]
            nova_populacao.extend(copy.deepcopy(elites))

            
            while len(nova_populacao) < tamanho_populacao:
                pai1 = selecao(populacao)
                pai2 = selecao(populacao)
                filho1, filho2 = aplicar_crossover(tipo, pai1, pai2, taxa_crossover=0.8)
                filho1 = aplicar_mutacao(filho1, mutacao)
                filho2 = aplicar_mutacao(filho2, mutacao)
                nova_populacao.extend([filho1, filho2])

            populacao = nova_populacao[:tamanho_populacao]
            melhores_por_geracao.append(fitness(populacao[0]))

        
        melhor_individuo = max(populacao, key=fitness)
        resultados[tipo].append(fitness(melhor_individuo))
        convergencias.append(melhores_por_geracao)

    
    convergencia_media[tipo] = np.mean(convergencias, axis=0)

print("\n=== Estatísticas finais ===")
for tipo in tipos_crossover:
    media = np.mean(resultados[tipo])
    desvio = np.std(resultados[tipo])
    print(f"{tipo}: Média = {media:.2f}, Desvio Padrão = {desvio:.2f}")

os.makedirs('./graficos', exist_ok=True)

plt.figure(figsize=(10,6))
for tipo in tipos_crossover:
    plt.plot(convergencia_media[tipo], label=tipo)
plt.xlabel("Geração")
plt.ylabel("Melhor Fitness Médio")
plt.title("Convergência média das 3 configurações de GA - Knapsack 20D")
plt.legend()
plt.grid(True)
plt.savefig('./graficos/convergencia_GA.png', dpi=300)
plt.show()

hill_tradicional_fitness = pd.read_csv('./fitness/hillclimbing.txt', header=None).values.flatten()
hill_estocastico_fitness = pd.read_csv('./fitness/stocastichillclimbing.txt', header=None).values.flatten()

dados_boxplot = [
    resultados["um ponto"],
    resultados["dois pontos"],
    resultados["uniforme"],
    hill_tradicional_fitness,
    hill_estocastico_fitness
]

labels = [
    "GA - Um ponto",
    "GA - Dois pontos",
    "GA - Uniforme",
    "Hill Climbing Tradicional",
    "Hill Climbing Estocástico"
]

plt.figure(figsize=(12,6))
plt.boxplot(dados_boxplot, labels=labels)
plt.ylabel("Melhor Fitness")
plt.title("Comparação das 5 configurações: GA e Hill Climbing (30 execuções)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('./graficos/boxplot_comparativo.png', dpi=300)
plt.show()