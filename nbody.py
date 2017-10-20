# -*- coding: utf-8 -*-

from visual import *
from math import pi
from sys import argv
from random import uniform as next_rand
from datetime import datetime as time
from vetor import Vetor
from particula import Particula

# constantes (unidades solares)
R, V, M = 200, 1.5, 1.4 # [UA, UA / Ano, Massa Solar]

# densidade de estrelas típicas com 1 raio solar
RHO = (5./8) * M / 0.004652 # [Massa Solar / UA]

# raio de relaxamento
EPS = 5 # [UA]

# passagem de tempo (anos)
dt = 1./12

class Nbody:
    """Classe Nbody"""

    def __init__(self, pts):
        '''(Nbody, list of Particula) -> None
        Recebe uma lista de particulas'''
        self.trail = False
        self.n = len(pts)
        self.bodies = pts
        self.pontos = []
        for body in self.bodies:
            v = vector(body.r.x, body.r.y, body.r.z)
            r = 15 * (body.m * 3. / RHO / 4. / (pi**2))**(1./3)
            s = sphere(pos=v, radius=r, make_trail=self.trail, retain=100,
                color=(next_rand(0, 1), next_rand(0, 1), next_rand(0, 1)))
            self.pontos.append(s)
        scene.bind('keydown', self.key_input)

    def __str__(self):
        '''(NBody) -> str'''
        txt = ""
        for body in self.bodies:
            txt += str(body)+"\n"
        return txt

    def mass_center(self):
        '''(Nbody) -> 3-tuple, float
        Retorna a posição do centro de massa e massa total
        '''
        p, m = Vetor(), 0
        for body in self.bodies:
            p += body.p
            m += body.m
        c = p.multiply(1./m)
        return c.to_list(), m

    def atualiza_anim(self, t):
        '''(Nbody, float) -> None
        Atualiza visualização do sistema
        '''
        # taxa por segundo de atualizações
        rate(30)

        print("::ATUALIZAÇÃO - %d Corpos - (%.2f anos)::"%(self.n, t))
        print(self)

        # atualiza posição das bolinhas
        for i in range(self.n):
            body = self.bodies[i]
            v = vector(body.r.x, body.r.y, body.r.z)
            self.pontos[i].pos = v

        # centraliza a visualização no centro de massa
        scene.center, m = self.mass_center()

    def key_input(self, ev):
        '''(Nbody, event) -> None
        Trigger para eventos do teclado
        '''
        if ev.key == "t":
            self.set_trail()

    def set_trail(self):
        '''(Nbody) -> None
        Ativa ou desativa traço das órbitas
        '''
        self.trail = not self.trail
        for p in self.pontos:
            p.make_trail = self.trail

    def colisoes(self):
        '''(Nbody) -> None
        Verifica se houve colisao, agregando as particulas
        '''
        i, has = 0, False
        while i < len(self.bodies) and not has:
            j = 1
            while j < len(self.bodies) and not has:
                if self.bodies[i] != self.bodies[j]:
                    dist = self.bodies[i].r.distancia(self.bodies[j].r)
                    if dist < EPS:
                        # calcula novos raio e massa
                        m = self.bodies[i].m + self.bodies[j].m
                        r = 15 * (m * 3. / RHO / 4. / (pi**2))**(1./3)

                        # colisão inelástica
                        p = self.bodies[i].p + self.bodies[j].p
                        v = p.multiply(1./m)

                        # obtém qual dos 2 tem momento maior
                        a, b = i, j
                        if self.bodies[j] > self.bodies[i]:
                            a, b = j, i

                        # atualiza o de momento maior
                        self.bodies[a].m = m
                        self.bodies[a].v = v
                        self.bodies[a].p = p
                        self.pontos[a].radius = r

                        # exclui o outro
                        self.bodies.pop(b)
                        self.pontos[b].visible = False
                        self.pontos.pop(b)
                        has = True
                j += 1
            i += 1
        self.n = len(self.bodies)

    def integracao(self, tempo):
        '''(Nbody, float) -> None
        Realiza integração numérica da força gravitacional em Nbody
        '''
        t = 0
        while t < tempo:
            for i in range(self.n):
                body = self.bodies[i]

                # somatoria de forças devido às demais partículas
                f_res = Vetor()
                for j in range(self.n):
                    if i != j:
                        f_res += body.gravity(self.bodies[j])
                
                # calculando impulso nesse corpo
                dp = f_res.multiply(dt)
                
                # calculando velocidade atual
                body.v += dp.multiply(1./body.m)
                body.p = body.v.multiply(body.m)
                
                # calculando posicao atual (na pos auxiliar)
                body.r_ = body.r + body.v.multiply(dt)

            # atualiza posições das partículas
            for body in self.bodies:
                body.r = body.r_

            # trata as colisões
            self.colisoes()

            t += dt
            # atualiza animação
            self.atualiza_anim(t)

    def registra(self):
        '''(Nbody) -> None
        Registra estado final em arquivo de texto
        '''
        nome = "regs/nbody-%d-%s.txt"%(self.n, str(time.now()))
        arq = open(nome, "w")
        arq.write(str(self))
        arq.close()

###############################################################################

def main():
    
    # configuracões da tela
    scene.background = (0.6, 0.6, 0.6)
    scene.width = 1366
    scene.height = 700
    scene.range = R

    # número de corpos
    N = 5
    if len(argv) > 1:
        N = int(argv[1])
    
    pts = []
    # pontos fixos
    pts.append(Particula("p_1", (0, -R/2, 0), (0.5, 0, 0), M*5))
    pts.append(Particula("p_2", (0, R/2, 0), (-1.2, 0, 0), M))

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
        m = next_rand(M/4, M)

        # objeto particula
        p = Particula(lbl, (x, y, z), (vx, vy, vz), m)
        pts.append(p)

    # inicia objeto Nbody
    corpos = Nbody(pts)

    # centraliza visualização 
    scene.center, ma = corpos.mass_center()

    # tempo Total (anos) (TEMPO DE COLAPSO GRAVITACIONAL)
    T = sqrt(3./32*pi*(R**3)/ma)
    print("Tempo de colapso: %f anos"%(T))

    # pausa, espera por enter ou click
    scene.waitfor('keydown click')

    # liga a força da gravidade
    corpos.integracao(T)

    # salva estado final em arquivo de texto
    corpos.registra()

    print("\n::Fim::")

if __name__ == "__main__":
    main()