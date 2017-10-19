# -*- coding: utf-8 -*-

from math import sqrt

# coordenadas canônicas
X, Y, Z = 0, 1, 2

# constante G em S.I.
G = -6.67408E-11

class Particula():
  """Classe Partícula (em Unidades S.I.)"""

  def __init__(self, lbl, pos = [0, 0, 0], vel = [0, 0, 0], mass = 1):
    '''(Particula, str, list[3], list[3], float) -> None
    O padrão é a "partícula" da posição origem'''
    self.pos = pos[:]
    self.vel = vel
    self.pos_ = pos # aux para cálculos
    self.mass = mass
    self.label = lbl

  def __str__(self):
    '''(Particula) -> str'''
    txt = "%s: pos = (%.2f, %.2f, %.2f), vel=(%.2f, %.2f, %.2f)\n"%(
          self.label, self.x(), self.y(), self.z(), self.vx(), self.vy(), self.vz())
    return txt
  
  def x(self):
    return self.pos[X]

  def y(self):
    return self.pos[Y]

  def z(self):
    return self.pos[Z]

  def x_(self):
    return self.pos_[X]

  def y_(self):
    return self.pos_[Y]

  def z_(self):
    return self.pos_[Z]

  def set_x(self, x):
    self.pos[X] = x

  def set_y(self, y):
    self.pos[Y] = y

  def set_z(self, z):
    self.pos[Z] = z

  def set_x_(self, x):
    self.pos_[X] = x

  def set_y_(self, y):
    self.pos_[Y] = y

  def set_z_(self, z):
    self.pos_[Z] = z

  def vx(self):
    return self.vel[X]

  def vy(self):
    return self.vel[Y]

  def vz(self):
    return self.vel[Z]

  def set_vx(self, vx):
    self.vel[X] = vx

  def set_vy(self, vy):
    self.vel[Y] = vy

  def set_vz(self, vz):
    self.vel[Z] = vz

  def m(self):
    return self.mass

  def distancia(self, other):
    '''(Particula, Particula) -> int ou float
    Recebe referências `self` e `other` a objetos Particula e
    retorna a distância euclidiana entre os pontos representados
    por `self` e `other`.'''
    return sqrt(self.distancia2(other))

  def distancia2(self, other):
    '''(Particula, Particula) -> int ou float
    Recebe referências `self` e `other` a objetos Particula e
    retorna a distância quadrática euclidiana entre os pontos representados
    por `self` e `other`.'''
    return (self.x() - other.x())**2 + (self.y() - other.y())**2 + (self.z() - other.z())**2

  def pos_modulo(self):
    '''(Particula) -> float
    Retorna modulo do vetor posição da partícula (à origem)'''
    origem = Particula()
    return self.distancia(origem)

  def pos_unit(self, other):
    '''(Particula) -> list(3)
    Retorna vetor posicao unitária que aponta de other para self'''
    modulo = self.distancia(other)
    r = self.pos_vector(other)
    r[X] /= modulo
    r[Y] /= modulo
    r[Z] /= modulo
    return r

  def pos_vector(self, other):
    '''(Posicao)
    Retorna vetor posicao que aponta de other para self'''
    r = [0, 0, 0]
    r[X] = self.x() - other.x()
    r[Y] = self.y() - other.y()
    r[Z] = self.z() - other.z()
    return r

  def gravity(self, other):
    '''(Particula, Particula) -> list(3)
    Retorna o vetor aceleração gravitacional em self causada por other
    g = G * m1 * m2 / r^2 * r (r é o vetor posicao)'''
    f = G * (self.m() * other.m() / self.distancia2(other))
    r = self.pos_vector(other)
    g = [0, 0, 0]
    g[X] = f*r[X]
    g[Y] = f*r[Y]
    g[Z] = f*r[Z]
    return g
