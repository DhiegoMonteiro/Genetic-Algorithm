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

def verificar_rota(cidades,rota):
    
    for cidade in rota:
        if cidade > 12:
            raise ValueError("Cidade inválida encontrada na rota")
    
    if len(rota) != len(cidades) + 1:
        raise ValueError("A rota deve passar por todas as cidades e voltar a cidade inicial")
    
    if rota[0] != rota[-1]:
        raise ValueError("A rota deve começar e terminar na mesma cidade")
    
    if len(set(rota[:-1])) != len(cidades):
        raise ValueError("A rota só pode visitar cada cidade exatamente uma vez")
    
    
    
    
def calcular_distancia_total(cidades, rota):
    
    verificar_rota(cidades, rota)
    
    distancia_total = 0
    
    for i in range(len(rota) - 1):
        origem = rota[i]
        destino = rota[i + 1]
        distancia_total += cidades[origem][destino]
    
    
    return distancia_total

tamanho_populacao = 50
geracoes = 400
mutacao = 0.05
elitismo = 5
torneio = 3
execucoes = 30

def gerar_populacao(tamanho_populacao, numero_cidades):
    populacao = []
    for _ in range(tamanho_populacao):
        rota = list(range(numero_cidades))
        random.shuffle(rota)
        populacao.append(rota)
    return populacao

def fitness(rota):
    distancia = 0
    for i in range(len(rota) - 1):
        distancia += USA13[rota[i]][rota[i + 1]]
    distancia += USA13[rota[-1]][rota[0]]
    return 1 / distancia

def selecao(populacao):
    
    selecionados = random.sample(populacao, torneio)
    melhor_individuo = max(selecionados, key=fitness)
    
    return melhor_individuo.copy()



def aplicar_crossover(pai1, pai2, taxa_crossover=0.9):
    """
    Aplica crossover com probabilidade definida pela taxa
    """
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

def aplicar_mutacao(individuo, mutacao):
    individuo = individuo.copy()
    for i in range(len(individuo)):
        if random.random() < mutacao:
            j = random.randint(0, len(individuo) - 1)
            individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

def nova_geracao(populacao):
    populacao_ordenada = sorted(populacao, key=fitness, reverse=True)
    nova_populacao = populacao_ordenada[:elitismo]
    
    while len(nova_populacao) < tamanho_populacao:
        pai1 = selecao(populacao)
        pai2 = selecao(populacao)
        filho1, filho2 = aplicar_crossover(pai1, pai2)
        filho1 = aplicar_mutacao(filho1, mutacao)
        filho2 = aplicar_mutacao(filho2, mutacao)
        nova_populacao.extend([filho1, filho2])
    
    return nova_populacao[:tamanho_populacao]

num_cidades = len(USA13)
melhores_execucoes = []
for i in range(execucoes):
    
    populacao = gerar_populacao(tamanho_populacao, num_cidades)
    melhor_distancia = float('inf')
    melhor_rota = None
    historico = []

    for j in range(geracoes):
        populacao = nova_geracao(populacao)
        melhor = max(populacao, key=fitness) 
        distancia = 1 / fitness(melhor)
        historico.append(distancia)     
        if distancia < melhor_distancia:
            melhor_distancia = distancia
            melhor_rota = melhor.copy()
        
    melhores_execucoes.append(melhor_distancia)
    print(f"Execução {i+1}: melhor distância = {melhor_distancia:.2f}")
    
print("\nMelhor rota encontrada:", melhor_rota + [melhor_rota[0]])
print("Distância total:", melhor_distancia)

media_resultados = np.mean(melhores_execucoes)
desvio_resultados = np.std(melhores_execucoes)

print(f"\nMédia das melhores distâncias em {execucoes} execuções: {media_resultados:.2f}")
print(f"Desvio padrão das melhores distâncias: {desvio_resultados:.2f}")

diretorio_base = os.path.dirname(os.path.abspath(__file__))

graficos = os.path.join(diretorio_base, "graficos")
os.makedirs(graficos, exist_ok=True)


plt.figure(figsize=(10, 5))
plt.plot(historico, color="blue", linewidth=2)
plt.title("Convergência do Algoritmo Genético - TSP")
plt.xlabel("Geração")
plt.ylabel("Distância")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(f"{graficos}/convergencia_AG_TSP.png", dpi=300)
plt.close()

plt.figure(figsize=(6, 6))
plt.boxplot(melhores_execucoes, vert=True, patch_artist=True,
            boxprops=dict(facecolor="lightblue", color="blue"),
            medianprops=dict(color="red", linewidth=2))
plt.title(f"Distribuição das Melhores Distâncias ({execucoes} execuções)")
plt.ylabel("Distância Total")
plt.grid(True, axis='y', linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(f"{graficos}/boxplot_resultados_TSP.png", dpi=300)
plt.close()
