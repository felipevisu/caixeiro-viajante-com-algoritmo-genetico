from random import random, randint, sample
import matriz

class Individuo():
    # Método construtor da classe
    def __init__(self, num_cidades, adjacencias, geracao=0):
        self.num_cidades = num_cidades
        self.adjacencias = adjacencias
        self.nota_avaliacao = 0
        self.geracao = geracao
        self.cromossomo = []

        while len(self.cromossomo) != num_cidades-1:
            cidade = randint(1, num_cidades-1)
            if cidade not in self.cromossomo:
                self.cromossomo.append(cidade)

    # Método para imprimir a classe
    def __str__(self):
        return('Geração: %s\nNota: %s\nCromossomo: %s\n' %
            (self.geracao, self.nota_avaliacao, self.cromossomo)
        )

    # Função de avaliação onde a nota é composta pela distância percorrida
    def avaliacao(self):
        nota = 0
        nota = matriz.adjacencias[0][self.cromossomo[0]]
        for i in range(len(self.cromossomo)-1):
            nota = nota + self.adjacencias[self.cromossomo[i]][self.cromossomo[i+1]]
        nota = nota + matriz.adjacencias[self.cromossomo[len(self.cromossomo)-1]][0]
        self.nota_avaliacao = nota
        return nota

    # Função de cruzamento 1
    def crossoverPMX(self, outro_individuo):
        pai1 = self.cromossomo
        pai2 = outro_individuo.cromossomo

        tamanho = len(pai1)
        p1, p2 = [0]*tamanho, [0]*tamanho
        for i in range(tamanho):
            p1[pai1[i]-1] = i+1
            p2[pai2[i]-1] = i+1

        cxPonto1 = randint(0, tamanho)
        cxPonto2 = randint(0, tamanho - 1)
        if cxPonto2 >= cxPonto1:
            cxPonto2 += 1
        else:
            cxPonto1, cxPonto2 = cxPonto2, cxPonto1

        for i in range(cxPonto1, cxPonto2):
            temp1 = pai1[i]-1
            temp2 = pai2[i]-1
            pai1[i], pai1[p1[temp2]-1] = temp2+1, temp1+1
            pai2[i], pai2[p2[temp1]-1] = temp1+1, temp2+1

            p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
            p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

        filhos = [
            Individuo(self.num_cidades, self.adjacencias, self.geracao + 1),
            Individuo(self.num_cidades, self.adjacencias,self.geracao + 1)
        ]

        filhos[0].cromossomo = p1
        filhos[1].cromossomo = p2
        return filhos

    # Função de cruzamento 2
    def crossoverOPX(self, outro_individuo):
        pai1 = self.cromossomo
        pai2 = outro_individuo.cromossomo

        tamanho = len(pai1)
        corte = int(tamanho/2)

        utilizados = [False]*(tamanho+1)
        filho1 = []

        for i in range(0, corte):
            filho1.append(pai1[i])
            utilizados[pai1[i]] = True
        for i in range(corte, tamanho):
            if not utilizados[pai2[i]]:
                filho1.append(pai2[i])
                utilizados[pai2[i]] = True
        for i in range(1, tamanho+1):
            if not utilizados[i]:
                filho1.append(i)

        utilizados = [False]*(tamanho+1)
        filho2 = []

        for i in range(0, corte):
            filho2.append(pai2[i])
            utilizados[pai2[i]] = True
        for i in range(corte, tamanho):
            if not utilizados[pai1[i]]:
                filho2.append(pai1[i])
                utilizados[pai1[i]] = True
        for i in range(1, tamanho+1):
            if not utilizados[i]:
                filho2.append(i)

        filhos = [
            Individuo(self.num_cidades, self.adjacencias, self.geracao + 1),
            Individuo(self.num_cidades, self.adjacencias, self.geracao + 1)
        ]

        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos

    # Função de cruzamento 3
    def crossoverOBX(self, outro_individuo):
        ind1 = self.cromossomo
        ind2 = outro_individuo.cromossomo
        size = len(ind1)
        a, b = sample(range(size), 2)
        if a > b:
            a, b = b, a

        holes1, holes2 = [True]*size, [True]*size
        for i in range(size):
            if i < a or i > b:
                holes1[ind2[i]-1] = False
                holes2[ind1[i]-1] = False

        temp1, temp2 = ind1, ind2
        k1 , k2 = b + 1, b + 1
        for i in range(size):
            if not holes1[temp1[(i + b + 1) % size]-1]:
                ind1[k1 % size] = temp1[(i + b + 1) % size]
                k1 += 1

            if not holes2[temp2[(i + b + 1) % size]-1]:
                ind2[k2 % size] = temp2[(i + b + 1) % size]
                k2 += 1

        for i in range(a, b + 1):
            ind1[i], ind2[i] = ind2[i], ind1[i]

        filhos = [
            Individuo(self.num_cidades, self.adjacencias, self.geracao + 1),
            Individuo(self.num_cidades, self.adjacencias, self.geracao + 1)
        ]

        filhos[0].cromossomo = ind1
        filhos[1].cromossomo = ind2
        return filhos

    # Função de mutação com o método da roleta
    def mutacao(self, taxa_mutacao):
        copia = self.cromossomo.copy()
        valor_anterior = self.avaliacao()

        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                p1 = randint(0, len(self.cromossomo)-1)
                p2 = randint(0, len(self.cromossomo)-1)
                self.cromossomo[p1], self.cromossomo[p2] = self.cromossomo[p2], self.cromossomo[p1]

        if(self.avaliacao() > valor_anterior):
            self.cromossomo = copia.copy()

        return self
