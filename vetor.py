# -*- coding: utf-8 -*-

from math import sqrt

class Vetor:
    """Classe Vetor, representa um vetor do R^3"""

    def __init__(self, u=(0, 0, 0)):
        self.x = u[0]
        self.y = u[1]
        self.z = u[2]

    def __str__(self):
        txt = "(%.2f, %.2f, %.2f)"%(self.x, self.y, self.z)
        return txt

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z)

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        soma = Vetor()
        soma.x = self.x + other.x
        soma.y = self.y + other.y
        soma.z = self.z + other.z
        return soma

    def to_list(self):
        return [self.x, self.y, self.z]

    def multiply(self, real):
        novo = Vetor()
        novo.x = self.x * real
        novo.y = self.y * real
        novo.z = self.z * real
        return novo

    def __sub__(self, other):
        return self + other.multiply(-1)

    def modulo2(self):
        return self.x**2 + self.y**2 + self.z**2

    def modulo(self):
        return sqrt(self.modulo2())

    def distancia(self, other):
        '''(Vetor, Vetor) -> float
        Recebe referências `self` e `other` a objetos vetor e
        retorna a distância euclidiana entre os pontos representados
        por `self` e `other`.'''
        return (self - other).modulo()

    def distancia2(self, other):
        '''(Vetor, Vetor) -> float
        Recebe referências `self` e `other` a objetos vetor e
        retorna a distância quadrática euclidiana entre os pontos representados
        por `self` e `other`.'''
        return (self - other).modulo2()