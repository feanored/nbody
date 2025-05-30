# -*- coding: utf-8 -*-
from __future__ import division

from vetor import Vetor

class Particula:
    """Classe Partícula"""

    def __init__(self, lbl, r = (0, 0, 0), v = (0, 0, 0), mass = 1, color=None, material=None):
        '''(Particula, str, 3-tuple, 3-tuple, float) -> None
        O padrão é uma "partícula" na posição origem
        '''
        self.label = lbl
        # vetor posição
        self.r = Vetor(r)
        # vetor velocidade
        self.v = Vetor(v)
        # massa
        self.m = mass
        # vetor momentum
        self.p = self.v.multiply(self.m)
        # vetor posição auxiliar
        self.r_ = Vetor(r)
        # cor
        self.cor = color
        # material
        self.material = material

    def __str__(self):
        '''(Particula) -> str'''
        txt = "%s, %s, %s, %.14f"%(
              self.label, self.r, self.v, self.m)
        return txt

    def __eq__(self, other):
        return self.label == other.label

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.p > other.p

    def __lt__(self, other):
        return self.p < other.p

    def gravity(self, other, G):
        '''(Particula, Particula) -> Vetor
        Retorna o vetor força gravitacional em self causada por other
        g = G * m1 * m2 / r^2 * r (r é o vetor posicao)
        '''
        # vetor posição
        r = other.r - self.r
        # intensidade da força
        f = G * self.m * other.m / r.modulo3()
        # retorna vetor força
        return r.multiply(f)
