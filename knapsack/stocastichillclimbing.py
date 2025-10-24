import copy
import random
import os
import knapsack
def gerar_vizinhos_knapsack(solucao, n_vizinhos=10):
    """
    Gera vizinhos para o problema knapsack
    Estratégia: flip de um bit aleatório

    Args:
        solucao: solução binária atual
        n_vizinhos: número de vizinhos

    Returns:
        list: lista de vizinhos
    """
    vizinhos = []
    n_itens = len(solucao)

    # Gerar vizinhos por flip de bit
    sorted_pos = []
    for i in range(n_vizinhos):
        # Escolher posição aleatória para flip
        pos = random.randint(0, n_itens - 1)
        if pos in sorted_pos:
            continue

        vizinho = solucao.copy()
        vizinho[pos] = 1 - vizinho[pos]  # Flip do bit
        vizinhos.append(vizinho)
        sorted_pos.append(pos)

    return vizinhos

class HillClimbing:
    def __init__(self, funcao_fitness, gerar_vizinhos, maximizar=True):
        """
        Inicializa o algoritmo Hill Climbing

        Args:
            funcao_fitness: função que avalia soluções
            gerar_vizinhos: função que gera vizinhos de uma solução
            maximizar: True para maximização, False para minimização
        """
        self.funcao_fitness = funcao_fitness
        self.gerar_vizinhos = gerar_vizinhos
        self.maximizar = maximizar
        self.historico = []

    def executar(self, solucao_inicial, max_iteracoes=1000, verbose=False):
        """
        Executa o algoritmo Hill Climbing

        Args:
            solucao_inicial: solução inicial
            max_iteracoes: número máximo de iterações
            verbose: imprimir progresso

        Returns:
            tuple: (melhor_solucao, melhor_fitness, historico)
        """
        solucao_atual = copy.deepcopy(solucao_inicial)
        fitness_atual = self.funcao_fitness(solucao_atual)

        self.historico = [fitness_atual]
        iteracao = 0
        melhorias = 0

        if verbose:
            print(f"Iteração {iteracao}: Fitness = {fitness_atual:.4f}")

        while iteracao < max_iteracoes:
            iteracao += 1

            # Gerar vizinhos
            vizinhos = self.gerar_vizinhos(solucao_atual)

            # Avaliar vizinhos e encontrar o melhor
            melhor_vizinho = None
            melhor_fitness_vizinho = fitness_atual

            for vizinho in vizinhos:
                fitness_vizinho = self.funcao_fitness(vizinho)

                # Verificar se é melhor
                eh_melhor = (
                    fitness_vizinho > melhor_fitness_vizinho
                    if self.maximizar
                    else fitness_vizinho < melhor_fitness_vizinho
                )

                if eh_melhor:
                    melhor_vizinho = vizinho
                    melhor_fitness_vizinho = fitness_vizinho

            # Se encontrou vizinho melhor, move para ele
            if melhor_vizinho is not None:
                solucao_atual = copy.deepcopy(melhor_vizinho)
                fitness_atual = melhor_fitness_vizinho
                melhorias += 1

                if verbose:
                    print(f"Iteração {iteracao}: Fitness = {fitness_atual:.4f}")
            else:
                # Nenhum vizinho melhor encontrado - parar
                if verbose:
                    print(f"Convergiu na iteração {iteracao}")
                break

            self.historico.append(fitness_atual)

        if verbose:
            print(f"Melhorias realizadas: {melhorias}")
            print(f"Fitness final: {fitness_atual:.4f}")

        return solucao_atual, fitness_atual, self.historico

if __name__ == "__main__":
    DIM = 20
    MAX_ITERACOES = 200
    EXECUCOES = 30

    os.makedirs('./fitness', exist_ok=True)
    fitness_hc_esto = []

    for _ in range(EXECUCOES):
        solucao_inicial = [int(random.random() > 0.5) for _ in range(DIM)]
        hc = HillClimbing(
            funcao_fitness=lambda sol: knapsack.knapsack(sol, dim=DIM)[0],
            gerar_vizinhos=lambda s: [random.choice(gerar_vizinhos_knapsack(s))],
            maximizar=True
        )
        _, melhor_fitness, _ = hc.executar(solucao_inicial, max_iteracoes=MAX_ITERACOES)
        fitness_hc_esto.append(melhor_fitness)


    with open('./fitness/stocastichillclimbing.txt', "w") as f:
        for valor in fitness_hc_esto:
            f.write(f"{valor}\n")