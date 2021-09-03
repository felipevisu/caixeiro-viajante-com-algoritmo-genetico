import math

# Pontos passados no arquivo
class Point():
    # Método construtor da classe
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Calcula a distância entre dois pontos
    def distancia(self, ponto2):
        return math.sqrt(math.pow(self.x - ponto2.x, 2) + math.pow(self.y - ponto2.y, 2))

arq = open('z-instancia.txt', 'r')
texto = arq.readlines()
numero_de_cidades = int(texto[0])

lista_cordenadas = []
adjacencias = []

for i in range(1, len(texto)):
    x, y = texto[i].split()
    lista_cordenadas.append(Point(int(x), int(y)))

for i in range(numero_de_cidades):
    adjacencias.append([0] * numero_de_cidades)

for i in range(0, len(lista_cordenadas)):
    for j in range(i+1, len(lista_cordenadas)):
        dist = lista_cordenadas[i].distancia(lista_cordenadas[j])
        adjacencias[i][j] = dist
        adjacencias[j][i] = dist
