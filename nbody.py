# -*- coding: utf-8 -*-
from __future__ import division
from visual import *
from math import pi, sqrt, ceil
from sys import argv
from random import triangular as next_rand
from datetime import datetime as time

from vetor import Vetor
from particula import Particula

###############################################################################

# constantes (unidades solares)
R, V, M = 100, 1.5, 70 # [UA, UA / Ano, Massa Solar]

# densidade de estrelas t�picas com 1 raio solar
RHO = (5/8) * M / 0.004652 # [Massa Solar / UA]

# raio de relaxamento
EPS = R/40 # [UA]

# passagem de tempo (anos)
dt = 1/12

###############################################################################

class Nbody:
    """Classe Nbody"""

    def __init__(self, pts=[]):
        '''(Nbody, list of Particula) -> None
        Recebe uma lista de particulas
        '''
        self.n = len(pts)
        self.bodies = pts
        self.pontos = {}
        if self.n > 0:
            self.make_stars()
        # FLAGS
        self.trail = False
        self.center = False
        self.verbose = False
        self.pause = False

    def __str__(self):
        '''(NBody) -> str'''
        txt  = '   Label   |   Posi��o (x, y, z)   |'
        txt += '   Velocidade (x, y, z)   |   Massa \n'
        for i in range(74): txt += '-'
        txt += '\n'
        for body in self.bodies:
            txt += str(body)+"\n"
        return txt

    def set_bodies(self, pts):
        self.n = len(pts)
        self.bodies = pts
        self.make_stars()

    def make_stars(self):
        for body in self.bodies:
            v = vector(body.r.x, body.r.y, body.r.z)
            r = 15 * (body.m * 3. / RHO / 4. / (pi**2))**(1/3)
            s = sphere(pos=v, radius=r, make_trail=self.trail, retain=100,
                color=(next_rand(0, 1), next_rand(0, 1), next_rand(0, 1)))
            self.pontos[body.label] = s

    def key_input(self, ev):
        '''(Nbody, event) -> None
        Trigger para eventos do teclado
        '''
        if ev.key == "t":
            self.set_trail()
        elif ev.key == "c":
            self.center = not self.center
        elif ev.key == "i":
            scene.range -= vector(EPS*5)
        elif ev.key == "o":
            scene.range += vector(EPS*5)
        elif ev.key == "p":
            self.pause = True
            while self.pause:
                scene.waitfor("keydown")
        elif ev.key == "r":
            self.pause = False


    def mouse(self, ev):
        '''(Nbody, event) -> None
        Trigger para clicks do mouse
        '''
        scene.center = ev.pos

    def set_trail(self):
        '''(Nbody) -> None
        Ativa ou desativa tra�o das �rbitas
        '''
        self.trail = not self.trail
        for p in self.pontos:
            self.pontos[p].make_trail = self.trail

    def mass_center(self):
        '''(Nbody) -> 3-tuple, float
        Retorna a posi��o do centro de massa e massa total
        '''
        s, m = Vetor(), 0
        for body in self.bodies:
            s += body.r.multiply(body.m)
            m += body.m
        c = s.multiply(1/m)
        return c.to_list(), m

    def atualiza_anim(self, t):
        '''(Nbody, float) -> None
        Atualiza visualiza��o do sistema
        '''
        # taxa por segundo de atualiza��es
        rate(120)

        print("::ATUALIZA��O - %d Corpos - (%.2f anos)::"%(self.n, t))
        if self.verbose:
            print(self)

        # atualiza posi��o das bolinhas
        for i in range(self.n):
            body = self.bodies[i]
            v = vector(body.r.x, body.r.y, body.r.z)
            self.pontos[body.label].pos = v

        # centraliza a visualiza��o no centro de massa
        if self.center:
            scene.center, m = self.mass_center()

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
                        r = 15 * (m * 3. / RHO / 4. / (pi**2))**(1/3)

                        # colis�o inel�stica
                        p = self.bodies[i].p + self.bodies[j].p
                        v = p.multiply(1/m)

                        # obt�m qual dos 2 tem momento maior
                        a, b = i, j
                        if self.bodies[j] > self.bodies[i]:
                            a, b = j, i

                        # atualiza o de momento maior
                        self.bodies[a].m = m
                        self.bodies[a].v = v
                        self.bodies[a].p = p
                        self.pontos[self.bodies[a].label].radius = r

                        # exclui o outro
                        self.pontos[self.bodies[b].label].visible = False
                        del self.pontos[self.bodies[b].label]
                        self.bodies.pop(b)
                        has = True
                j += 1
            i += 1
        self.n = len(self.bodies)

    def integracao(self, tempo):
        '''(Nbody, float) -> None
        Realiza integra��o num�rica da for�a gravitacional em Nbody
        '''
        t = 0
        while t < tempo and self.n > 1:
            for i in range(self.n):
                body = self.bodies[i]

                # somatoria de for�as devido �s demais part�culas
                f_res = Vetor()
                for j in range(self.n):
                    if i != j:
                        f_res += body.gravity(self.bodies[j])
                
                # calculando impulso nesse corpo
                dp = f_res.multiply(dt)
                
                # calculando velocidade atual
                body.p = body.p + dp
                body.v = body.p.multiply(1/body.m)
                
                # calculando posicao atual (na pos auxiliar)
                body.r_ = body.r + body.v.multiply(dt)

            # atualiza posi��es das part�culas
            for body in self.bodies:
                body.r = body.r_

            # trata as colis�es
            self.colisoes()

            t += dt
            # atualiza anima��o
            self.atualiza_anim(t)

    def registra(self):
        '''(Nbody) -> None
        Registra estado final em arquivo de texto
        '''
        tt = time.now()
        tt = "%02d%02d%02d"%(tt.hour, tt.minute, tt.second)
        nome = "regs/nbody-%d-#%s.txt"%(self.n, tt)
        arq = open(nome, "w")
        arq.write(self.__str__())
        arq.close()

    def carrega(self, nome):
        '''(Nbody, str) -> list
        L� estado inicial de arquivo de texto
        '''
        arq = open("regs/"+nome+".txt", "r")
        c = 0
        pts = []
        for linha in arq:
            c += 1
            if c < 3: continue
            dados = linha.split(", ")
            r = (float(dados[1]), float(dados[2]), float(dados[3]))
            v = (float(dados[4]), float(dados[5]), float(dados[6]))
            m = float(dados[7])
            p = Particula(dados[0], r, v, m)
            pts.append(p)
        arq.close()
        return pts

###############################################################################

def main():
    print("\n# feanored-NBody #\n")
    # configurac�es da tela
    scene.title = "# feanored-NBody #"
    scene.background = (0, 0, 0)
    scene.lights = []
    distant_light(direction=(0,R,0), color=color.white)
    distant_light(direction=(0,-R,0), color=color.white)
    distant_light(direction=(R,0,0), color=color.white)
    distant_light(direction=(-R,0,0), color=color.white)
    distant_light(direction=(0,0,R), color=color.white)
    distant_light(direction=(0,0,-R), color=color.white)
    scene.width = 1366
    scene.height = 768
    scene.range = R*2

    # inicia objeto Nbody
    corpos = Nbody()
    
    # par�metros
    if len(argv) > 1:
        if "t" in argv[1]:
            corpos.trail = True
        if "c" in argv[1]:
            corpos.center = True
        if "v" in argv[1]:
            corpos.verbose = True

    op = ""
    while op == "" or not op in "lsg":
        txt  = "O que deseja?\n"
        txt += " [S]imular o Sistema Solar\n"
        txt += " [L]er estado inicial de arquivo\n"
        txt += " [G]erar part�culas aleat�rias\n"
        print(txt)
        op = raw_input("Digite op��o: ")

    # Sistema Solar
    if op == "s":
        global EPS
        EPS = 0.2
        scene.range = 20
        scene.forward = vector(0, -1, 0)
        corpos.center = True
        corpos.trail = True
        pts = []
        # Velocidade circular v0 = sqrt(GM/R)
        pts.append(Particula("Sol", (0, 0, 0), (0, 0, 0), 1))
        pts.append(Particula("Jupiter", (5.5, 0, 0), (0, 0, sqrt(1/5.5)), 1E-3))
        pts.append(Particula("Saturno", (10, 0, 0), (0, 0, sqrt(1/10)), 3E-4))
        pts.append(Particula("Terra", (1, 0, 0), (0, 0, 1), 3.003E-6))
        pts.append(Particula("Marte", (1.4, 0, 0), (0, 0, sqrt(1/1.4)), 3.2e-7))
    
    # Ler part�culas de arquivo
    elif op == "l":
        nome = raw_input("Digite nome do arquivo com estado inicial: ")
        pts = corpos.carrega(nome)
        if len(pts) < 1:
            print("Arquivo inv�lido!")
            return

    # pontos aleat�rios
    elif op == "g":
        pts = []
        N = ""
        while N == "":
            N = raw_input("Qtde de part�culas: ")
        N = int(N)
        if N < 2:
            print("O m�nimo de part�culas � 2!")
            return
        for i in range(N):
            ''' 
            Gera N particulas com distribui��o triangular
            '''
            lbl = "p_%d"%(i+1)
            x = next_rand(-R, R)
            y = next_rand(-R, R)
            z = next_rand(-R, R)
            vx = next_rand(-V, V)
            vy = next_rand(-V, V)
            vz = next_rand(-V, V)
            m = next_rand(0.7, M)
            '''
            Objeto Part�cula
            '''
            p = Particula(lbl, (x, y, z), (vx, vy, vz), m)
            pts.append(p)

    # tempo para integra��o em anos
    T = raw_input("Insira o tempo de integra��o (em anos) [2500]: ")
    if T == "":
        T = 2500
    else:
        T = float(T)
    if T < 1:
        print("Tempo inv�lido!")
        return

    # insere as part�culas
    corpos.set_bodies(pts)

    # aumenta tamanho dos planetas
    if op == "s":
        corpos.pontos["Terra"].retain = 77
        corpos.pontos["Marte"].retain = 126
        corpos.pontos["Jupiter"].retain = 970
        corpos.pontos["Saturno"].retain = 2365
        for p in corpos.pontos:
            if p == "Sol": continue
            corpo = corpos.pontos[p]
            corpo.radius = corpo.radius*5

    # centraliza visualiza��o 
    scene.center, ma = corpos.mass_center()

    # pausa, espera por tecla ou click
    ev = scene.waitfor('keydown click')    

    # registra eventos
    scene.bind('keydown', corpos.key_input)
    scene.bind('click', corpos.mouse)

    # liga a for�a da gravidade
    corpos.integracao(T)

    # salva estado final em arquivo de texto
    corpos.registra()

    print("\n::Fim::")

###############################################################################

if __name__ == "__main__":
    main()