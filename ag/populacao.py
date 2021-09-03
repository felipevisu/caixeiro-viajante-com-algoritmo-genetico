from random import random
from individuo import Individuo

class Populacao():
    # Método construtor da classe
    def __init__(self, num_cidades, tamanho_populacao, adjacencias):
        self.num_cidades = num_cidades
        self.adjacencias = adjacencias # matriz de distâncias entre as cidades
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.melhor_solucao = 0
        self.valor_roleta = 0 # utilizado na seleção do pai
        self.lista_solucoes = []
        self.lista_solucoes_medias = []
        self.numero_geracoes = 0

    # Método para imprimir a classe
    def __str__(self):
        return('Melhor da geração %s\nNota: %s\nCromossomo: %s\n'
            % (self.populacao[self.tamanho_populacao-1].geracao,
               self.populacao[self.tamanho_populacao-1].nota_avaliacao,
               self.populacao[self.tamanho_populacao-1].cromossomo)
        )

    # Cria os indivíduos e adiciona a lista de população
    def criaIndividuos(self):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(self.num_cidades, self.adjacencias))
        self.melhor_solucao = self.populacao[self.tamanho_populacao-1]

    # Ordena os indivíduos do pior para o melhor
    # Esta ordenação será utilizada no método de seleção dos pais
    def ordena(self):
        self.populacao = sorted(
            self.populacao,
            key = lambda populacao: populacao.nota_avaliacao,
            reverse = True
        )

    # Atualiza o melhor indivíduo
    def melhorIndividuo(self, individuo):
        if individuo.nota_avaliacao < self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    # Método da roleta para seleção dos pais
    def selecionaPai(self):
        valor = self.valor_roleta
        valor = random() * valor
        pai = self.tamanho_populacao
        soma = 0
        while pai >=0 and soma < valor:
            soma = soma + pai
            pai = pai-2
        return pai

    # Executa o algoritmo genético em todas suas etapas
    def resolver(self, taxa_mutacao, max_geracoes, ax):
        # Gera o valor para a função de seleção
        for i in range(self.tamanho_populacao):
            self.valor_roleta += i

        # Cria a primeira geração
        self.criaIndividuos()

        # Avalia a primeira geração
        for individuo in self.populacao:
            individuo.avaliacao()

        # Ordena os indivíduos
        self.ordena()

        print(self)

        for i in range(self.tamanho_populacao):
            ax.plot(0,self.populacao[i].nota_avaliacao, 'o')

        # Repete o processo conforme o número de gerações expecificado
        for geracao in range(max_geracoes):
            nova_populacao = []

            # Gera uma nova população
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.selecionaPai()
                pai2 = self.selecionaPai()
                filhos = self.populacao[pai1].crossoverOPX(self.populacao[pai2])
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            # Avalia a nova geração
            self.populacao = list(nova_populacao)
            for individuo in self.populacao:
                individuo.avaliacao()

            for i in range(self.tamanho_populacao):
                ax.plot(geracao,self.populacao[i].nota_avaliacao + random()%0.6 - 0.3, 'o')

            # Ordena
            self.ordena()

            # Atualiza o melhor indivíduo
            melhor = self.populacao[self.tamanho_populacao-1]
            self.melhorIndividuo(melhor)

            self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
            print(self)

            self.lista_solucoes_medias.append(self.populacao[int(self.num_cidades/2)].nota_avaliacao)


        # Imprime o melhor resultado final
        self.numero_geracoes = geracao
        print('--------------\n')
        print('Melhor solução geral')
        print('Geração: %s\nNota: %s\nCromossomo: %s'
            % (self.melhor_solucao.geracao, self.melhor_solucao.nota_avaliacao, self.melhor_solucao.cromossomo)
        )
        return self.melhor_solucao.nota_avaliacao
