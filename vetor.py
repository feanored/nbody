# -*- coding: utf-8 -*-
from __future__ import division

from numpy import sqrt

class Vetor:
    """Classe Vetor, representa um vetor do R^3"""

    def __init__(self, u=(0, 0, 0)):
        self.x = u[0]
        self.y = u[1]
        self.z = u[2]

    def __str__(self):
        txt = "%.14f, %.14f, %.14f"%(self.x, self.y, self.z)
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
        return self.x*self.x + self.y*self.y + self.z*self.z

    def modulo3(self):
        mod3 = self.modulo2()
        return sqrt(mod3*mod3*mod3)

    def modulo(self):
        return sqrt(self.modulo2())

    def unit(self):
        return self.multiply(1/self.modulo())

    def distancia(self, other):
        '''(Vetor, Vetor) -> float
        Recebe referências `self` e `other` a objetos vetor e
        retorna a distância euclidiana entre os pontos representados
        por `self` e `other`.'''
        d = self - other
        return d.modulo()

    def distancia2(self, other):
        '''(Vetor, Vetor) -> float
        Recebe referências `self` e `other` a objetos vetor e
        retorna a distância quadrática euclidiana entre os pontos representados
        por `self` e `other`.'''
        d = self - other
        return d.modulo2()
