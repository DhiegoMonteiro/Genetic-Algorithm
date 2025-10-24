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

rota1 = [0, 2 , 3, 5 , 6, 4, 1, 9, 7, 8, 11, 10, 12, 0]
rota2 = [2, 5, 9, 11, 1, 0, 7, 8, 6, 4, 10, 3, 12, 2]
rota3 = [7, 0, 2, 3, 9, 5, 10, 11, 12, 4, 6, 8, 1, 7]
rota4 = [4, 1, 11, 9, 2, 3, 5, 10, 0, 7, 8, 6, 12, 4]
rota5 = [6, 4, 5, 9, 0, 7, 8, 1, 2, 3, 10, 11, 12, 6]
rota7 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
rota8 = [0, 2, 3, 5, 6, 4, 1, 9, 7, 8, 11, 10, 12]
rota9 = [0, 1, 2, 3, 4, 5, 6, 1, 8, 9, 10, 11, 12, 0]
rotas = [rota4, rota3, rota1, rota2, rota7, rota8, rota5, rota9]

for rota in rotas: 
    try:
        distancia_total = calcular_distancia_total(USA13, rota)
        print(f"{rota} é válida. Distância total = {distancia_total}  \n" )
    except ValueError as erro:
        print(f"Rota {rota} é inválida: {erro} \n")