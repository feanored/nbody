# -*- coding: utf-8 -*-

from visual import *
from sys import argv
from particula import Particula
from random import triangular as next_rand

class Nbody:
    def __init__(self, pts):
        '''(Nbody, list of Particula) -> None
        Recebe uma lista de particulas'''
        self.n = len(pts)
        self.bodies = pts
        self.pontos = []
        for body in self.bodies:
            v = vector(body.x(),body.y(),body.z())
            s = sphere(pos=v, radius=7, make_trail=True,
                color=(next_rand(0, 1), next_rand(0, 1), next_rand(0, 1)))
            self.pontos.append(s)

    def __str__(self):
        '''(NBody) -> str'''
        txt = ""
        for body in self.bodies:
            txt += str(body)
        return txt

    def mass_center(self):
        '''(Nbody) -> 3-tuple
        Retorna a posição do centro de massa
        '''
        m, ma = [0, 0, 0], 0
        for body in self.bodies:
            m = [m[0]+body.m()*body.x(), 
            m[1]+body.m()*body.y(),
            m[2]+body.m()*body.z()]
            ma += body.m()
        return (m[0]/ma, m[1]/ma, m[2]/ma)

    def atualiza_anim(self, t):
        '''(Nbody, float) -> None
        Atualiza visualização do sistema
        '''
        # taxa por segundo de atualizações
        rate(50)

        print("::ATUALIZAÇÃO (%.0f)s::"%(t))
        print(self)

        # atualiza posição das bolinhas
        for i in range(self.n):
            body = self.bodies[i]
            v = vector(body.x(),body.y(),body.z())
            self.pontos[i].pos = v

        # centraliza a visualização no centro de massa
        scene.center = self.mass_center()

    def integracao(self, tempo=100):
        '''(Nbody, int) -> None
        Realiza integração numérica da força gravitacional em Nbody
        '''
        t = 0
        while t < tempo:
            for i in range(self.n):
                body = self.bodies[i]

                # somatoria de forças devido às demais partículas
                soma_f = [0, 0, 0]
                for j in range(self.n):
                    if i != j:
                        soma_f = soma_v(soma_f, body.gravity(self.bodies[j]))
                
                # calculando impulso nesse corpo
                px, py, pz = mult_v(soma_f, dt)
                
                # calculando velocidade atual
                vx = body.vx() + (px / body.m())
                vy = body.vy() + (py / body.m())
                vz = body.vz() + (pz / body.m())
                body.set_vx(vx)
                body.set_vy(vy)
                body.set_vz(vz)
                
                # calculando posicao atual (na pos auxiliar)
                x = body.x() + body.vx() * dt
                y = body.y() + body.vy() * dt
                z = body.z() + body.vz() * dt
                body.set_x_(x)
                body.set_y_(y)
                body.set_z_(z)

            # atualiza posições das partículas
            for body in self.bodies:
                body.set_x(body.x_())
                body.set_y(body.y_())
                body.set_z(body.z_())

            t += dt
            # atualiza animação
            self.atualiza_anim(t)

###############################################################################

def soma_v(a, b):
    s = []
    for i in range(len(a)):
        s.append(a[i] + b[i])
    return s

def mult_v(a, m):
    p = ()
    for i in range(len(a)):
        p += (a[i]*m, )
    return p

###############################################################################

# constantes
R, V, M = 200, 1, 1E10

# configuracões da tela
scene.background = (0.6, 0.6, 0.6)
scene.width = 800
scene.height = 600
scene.range = 3*R

# passagem de tempo (s)
dt = 1

# tempo Total (s)
T = 1E4

# número de corpos
N = 5
if len(argv) > 1:
    N = int(argv[1])

def main():
    
    pts = []
    # pontos fixos
    pts.append(Particula("p_1", [0, -R/2, 0], [sqrt(M/R/1E6/80), 0, 0], M*80))
    pts.append(Particula("p_2", [0, R/2, 0], [-sqrt(M/R/1E6), 0, 0], M))

    # pontos aleatórios
    for i in range(len(pts), N):
        # cria N particulas com distribuição simétrica
        lbl = "p_%d"%(i+1)
        x = next_rand(-R, R)
        y = next_rand(-R, R)
        z = next_rand(-R, R)
        vx = next_rand(-V, V)
        vy = next_rand(-V, V)
        vz = next_rand(-V, V)
        m = next_rand(M/100, M)

        # objeto particula
        p = Particula(lbl, [x, y, z], [vx, vy, vz], m)
        pts.append(p)

    # inicia objeto Nbody
    corpos = Nbody(pts)

    # centraliza visualização 
    scene.center = corpos.mass_center()

    # pausa, espera por click
    scene.mouse.getclick() 

    # liga a força da gravidade
    corpos.integracao(T)

    print("\n::Fim::")

if __name__ == "__main__":
    main()