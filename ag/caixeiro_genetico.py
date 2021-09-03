from populacao import Populacao
import matplotlib
import matplotlib.pyplot as plt
import matriz

if __name__ == '__main__':
    tamanho_populacao = 40
    taxa_mutacao = 0.1
    max_geracoes = 100

    matplotlib.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()

    ag = Populacao(matriz.numero_de_cidades, tamanho_populacao, matriz.adjacencias)
    resultado = ag.resolver(taxa_mutacao, max_geracoes, ax)

    plt.show()
