from genetic_algorithm.person import  Person


class Dna(object):
    def __init__(self, quantity_of_persons: int):
        self.quantity_of_persons = quantity_of_persons
        self.genes = []
        self.fitness = 0
        self.fill_genes()

    def fill_genes(self):
        """
        Preencher o Dna com várias pessoas
        :return:
        """
        for i in range(self.quantity_of_persons):
            person = Person('Some random name...')
            self.genes.append(person)

#Passar quantidade de pessoas e com base nessa informação, definir o size do grupo
#divir as pessos em grupos, se for qtd_pessoas par Ok, se não distribuir o resto nos grupos