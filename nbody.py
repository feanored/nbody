# -*- coding: utf-8 -*-

from visual import *
from math import pi
from sys import argv
from particula import Particula
from random import uniform as next_rand
from datetime import datetime as time

# constantes (unidades solares)
R, V, M = 250, 1.5, 1.4 # [UA, UA / Ano, Massa Solar]

# densidade de estrelas típicas com 1 raio solar
RHO = (5./8) * M / 0.004652 # [Massa Solar / UA]

# raio de relaxamento
EPS = 5 # [UA]

# passagem de tempo (anos)
dt = 1./12

class Nbody:
    def __init__(self, pts):
        '''(Nbody, list of Particula) -> None
        Recebe uma lista de particulas'''
        self.trail = False
        self.n = len(pts)
        self.bodies = pts
        self.pontos = []
        for body in self.bodies:
            v = vector(body.x(),body.y(),body.z())
            r = 15 * (body.m() * 3. / RHO / 4. / (pi**2))**(1./3)
            s = sphere(pos=v, radius=r, make_trail=self.trail, retain=100,
                color=(next_rand(0, 1), next_rand(0, 1), next_rand(0, 1)))
            self.pontos.append(s)
        scene.bind('keydown', self.key_input)

    def __str__(self):
        '''(NBody) -> str'''
        txt = ""
        for body in self.bodies:
            txt += str(body)
        return txt

    def mass_center(self):
        '''(Nbody) -> 3-tuple, float
        Retorna a posição do centro de massa e massa total
        '''
        m, ma = [0, 0, 0], 0
        for body in self.bodies:
            m = [m[0]+body.m()*body.x(), 
            m[1]+body.m()*body.y(),
            m[2]+body.m()*body.z()]
            ma += body.m()
        return (m[0]/ma, m[1]/ma, m[2]/ma), ma

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
            v = vector(body.x(),body.y(),body.z())
            self.pontos[i].pos = v

        # centraliza a visualização no centro de massa
        scene.center, z = self.mass_center()

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
                if self.bodies[i].label != self.bodies[j].label:
                    dist = self.bodies[i].distancia(self.bodies[j])
                    if dist < EPS:
                        # calcula novos raio e massa
                        m = self.bodies[i].m()+self.bodies[j].m()
                        r = 15 * (m * 3. / RHO / 4. / (pi**2))**(1./3)
                        # colisão inelástica
                        mi = mult_v(self.bodies[i].vel, self.bodies[i].m())
                        mj = mult_v(self.bodies[j].vel, self.bodies[j].m())
                        mt = soma_v(mi, mj)
                        v = mult_v(mt, 1./m)
                        # atualiza um dos corpos
                        self.bodies[i].set_m(m)
                        self.bodies[i].vel = [v[0], v[1], v[2]]
                        self.pontos[i].radius = r
                        # exclui o outro
                        self.bodies.pop(j)
                        self.pontos[j].visible = False
                        self.pontos.pop(j)
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

def main():
    
    # configuracões da tela
    scene.background = (0.6, 0.6, 0.6)
    scene.width = 1366
    scene.height = 700
    scene.range = R*2./3

    # número de corpos
    N = 5
    if len(argv) > 1:
        N = int(argv[1])
    
    pts = []
    # pontos fixos
    #pts.append(Particula("p_1", [0, -R/2, 0], [0.5, 0, 0], M*5))
    #pts.append(Particula("p_2", [0, R/2, 0], [-1.2, 0, 0], M))

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
        p = Particula(lbl, [x, y, z], [vx, vy, vz], m)
        pts.append(p)

    # inicia objeto Nbody
    corpos = Nbody(pts)

    # centraliza visualização 
    scene.center, ma = corpos.mass_center()

    # tempo Total (anos) (TEMPO DE COLAPSO GRAVITACIONAL)
    T = sqrt(3./32*pi*(4./3*(pi**2)*(R**3))/ma)
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