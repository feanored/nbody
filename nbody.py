# -*- coding: utf-8 -*-
from __future__ import print_function, division
from random import triangular as next_rand
from datetime import datetime as time
from six.moves import input
from numpy import sqrt
from visual import *
from sys import argv
from math import pi

from vetor import Vetor
from particula import Particula

###############################################################################

# constantes (unidades solares)
R, V, M = 100, 1.5, 70 # [UA, UA / Ano, Massa Solar]

# densidade tipica de estrelas com 1 raio solar
RHO = (5/8) * M / 0.004652 # [Massa Solar / UA]

# raio de relaxamento
EPS = R/40 # [UA]

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

        # atributos de estado
        self.center = 0
        self.trail = False
        self.verbose = False
        self.pause = False

        # G em S.I. : -6.67408E-11
        # G em unidades solares
        self.G = 1

        # passagem de tempo (anos)
        self._dt = 1/120
        self.dt = self._dt


    def __str__(self):
        '''(NBody) -> str'''
        txt  = '   Label   |   Posicao (x, y, z)   |'
        txt += '   Velocidade (x, y, z)   |   Massa \n'
        txt += '-' * 74
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

            if body.cor is None:
                body.cor = (next_rand(0, 1), next_rand(0, 1), next_rand(0, 1))
            if body.material is None:
                body.material = materials.marble
            
            s = sphere(pos=v, radius=r, make_trail=self.trail, 
                retain=100, color=body.cor, material=body.material)
            self.pontos[body.label] = s

    def key_input(self, ev):
        '''(Nbody, event) -> None
        Trigger para eventos do teclado
        '''
        if ev.key == "o":
            self.set_trail()
        
        elif ev.key == "c":
            if self.center == 1:
                self.center = 0
            else:
                self.center = 1
            print("Center: ", self.center)
        
        elif ev.key == "C":
            if self.center == 2:
                self.center = 0
            else:
                self.center = 2
            print("Center: ", self.center)
        
        elif ev.key == "v":
            self.verbose = True
        
        elif ev.key == "V":
            print(self)
        
        elif ev.key == "Z":
            scene.range -= vector(EPS*5)
        
        elif ev.key == "z":
            scene.range += vector(EPS*5)
        
        elif ev.key == "p":
            self.pause = True
            while self.pause:
                scene.waitfor("keydown")
        
        elif ev.key == "r":
            self.pause = False
        
        elif ev.key == "g":
            self.G -= 0.1
            print("G: ", self.G)
        
        elif ev.key == "G":
            self.G += 0.1
            print("G: ", self.G)
        
        elif ev.key == "t":
            self.dt -= self._dt
            if self.dt <= self._dt: 
                self.dt = self._dt
            print("dt: ", self.dt)
        
        elif ev.key == "T":
            self.dt += self._dt
            print("dt: ", self.dt)


    def mouse(self, ev):
        '''(Nbody, event) -> None
        Trigger para clicks do mouse
        '''
        scene.center = ev.pos

    def set_trail(self):
        '''(Nbody) -> None
        Ativa ou desativa traco das orbitas
        '''
        self.trail = not self.trail
        for p in self.pontos:
            self.pontos[p].make_trail = self.trail

    def mass_center(self):
        '''(Nbody) -> 3-tuple
        Retorna a posicao do centro de massa
        '''
        s, m = Vetor(), 0
        for body in self.bodies:
            s += body.r.multiply(body.m)
            m += body.m
        c = s.multiply(1/m)
        return c.to_list()

    def star_center(self):
        '''(Nbody) -> 3-tuple
        Retorna a posicao do corpo de maior massa
        '''
        s, m = Vetor(), 0
        for body in self.bodies:
            if body.m > m:
                m = body.m
                s = body.r
        return s.to_list()

    def atualiza_anim(self, t):
        '''(Nbody, float) -> None
        Atualiza visualizacao do sistema
        '''
        # taxa por segundo de atualizacoes
        rate(120)

        if self.verbose:
            print("::%d Corpos - (%.2f anos)::"%(self.n, t))
            self.verbose = False

        # atualiza posicao das bolinhas
        for i in range(self.n):
            body = self.bodies[i]
            v = vector(body.r.x, body.r.y, body.r.z)
            self.pontos[body.label].pos = v

        # centraliza a visualizacao
        if self.center == 1:
            scene.center = self.mass_center() # centro de massa
        elif self.center == 2:
            scene.center = self.star_center() # corpo de maior massa

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

                        # colisao inelastica
                        p = self.bodies[i].p + self.bodies[j].p
                        v = p.multiply(1/m)

                        # obtem qual das 2 tem o maior momento
                        a, b = i, j
                        if self.bodies[j] > self.bodies[i]:
                            a, b = j, i

                        # atualiza a de maior momento
                        self.bodies[a].m = m
                        self.bodies[a].v = v
                        self.bodies[a].p = p
                        self.pontos[self.bodies[a].label].radius = r

                        # exclui a outra
                        self.pontos[self.bodies[b].label].visible = False
                        del self.pontos[self.bodies[b].label]
                        self.bodies.pop(b)
                        has = True
                j += 1
            i += 1
        self.n = len(self.bodies)

    def integracao(self, tempo):
        '''(Nbody, float) -> None
        Realiza integracao numerica da forca gravitacional em Nbody
        '''
        t = 0
        while t < tempo and self.n > 1:
            for i in range(self.n):
                body = self.bodies[i]

                # somatoria de forcas devido as demais particulas
                f_res = Vetor()
                for j in range(self.n):
                    if i != j:
                        f_res += body.gravity(self.bodies[j], self.G)
                
                # calculando impulso nesse corpo
                dp = f_res.multiply(self.dt)
                
                # calculando velocidade atual
                body.p = body.p + dp
                body.v = body.p.multiply(1/body.m)
                
                # calculando posicao atual (na pos auxiliar)
                body.r_ = body.r + body.v.multiply(self.dt)

            # atualiza posicoes das particulas
            for body in self.bodies:
                body.r = body.r_

            # trata as colisoes
            self.colisoes()

            t += self.dt
            # atualiza animacao
            self.atualiza_anim(t)

    def registra(self):
        '''(Nbody) -> None
        Registra estado final em arquivo de texto
        '''
        t = time.now()
        t = "%02d%02d%d-%02d%02d"%(t.day, t.month, t.year, t.hour, t.minute)
        nome = r"./regs/nbody-%02d#%s.txt"%(self.n, t)
        arq = open(nome, "w+")
        arq.write(self.__str__())
        arq.close()

    def carrega(self, nome):
        '''(Nbody, str) -> list
        Le estado inicial de arquivo de texto
        '''
        arq = open("regs/nbody-"+nome+".txt", "r")
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

    # configuracoes da tela
    scene.title = "# feanored-NBody #"
    scene.background = (0.2, 0.2, 0.2)
    scene.autoscale = 1
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
    
    # parametros
    if len(argv) > 1:
        print(argv[1])
        if "t" in argv[1]:
            corpos.trail = True
        if "c" in argv[1]:
            corpos.center = True

    op = ""
    while op == "" or not op in "lsgx":
        txt  = "O que deseja?\n"
        txt += " [S]imular o Sistema Solar\n"
        txt += " [L]er estado inicial de arquivo\n"
        txt += " [G]erar particulas aleatorias\n"
        txt += " [X] Sair do programa\n"
        print(txt)
        op = input("Digite opcao: ")

    # Sair do programa
    if op == "x":
        return

    # Sistema Solar
    elif op == "s":
        global EPS
        EPS = 0.2
        scene.range = 20
        scene.forward = vector(0, -1, 0)
        corpos.center = True
        corpos.trail = True
        pts = []
        # Velocidade circular v0 = sqrt(GM/R)
        pts.append(Particula("Sol", (0, 0, 0), (0, 0, 0), 1, color.yellow, materials.emissive))
        pts.append(Particula("Jupiter", (5.5, 0, 0), (0, 0, sqrt(corpos.G/5.5)), 1E-3, color.cyan))
        pts.append(Particula("Saturno", (10, 0, 0), (0, 0, sqrt(corpos.G/10)), 3E-4, color.orange))
        pts.append(Particula("Terra", (1, 0, 0), (0, 0, sqrt(corpos.G)), 3.003E-6, color.blue))
        pts.append(Particula("Marte", (1.4, 0, 0), (0, 0, sqrt(corpos.G/1.4)), 3.2e-7, color.red))
    
    # Ler particulas de arquivo
    elif op == "l":
        nome = input("Digite nome do arquivo com estado inicial: [nbody-] ")
        pts = corpos.carrega(nome)
        if len(pts) < 1:
            print("Arquivo invalido!")
            return

    # pontos aleatorios
    elif op == "g":
        pts = []
        N = 0
        while N < 2:
            N = input("Qtde de particulas [20]: ")
            if N == "":
                N = 20
            else:
                N = int(N)
            if N < 2:
                print("Minimo de 2 particulas!")
        for i in range(N):
            ''' 
            Gera N particulas aleatorias
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
            Objeto Particula
            '''
            p = Particula(lbl, (x, y, z), (vx, vy, vz), m)
            pts.append(p)

    # tempo para integracao em anos
    T = input("Insira o tempo de integracao (em anos) [2500]: ")
    if T == "":
        T = 2500
    else:
        T = float(T)
    if T < 1:
        print("Tempo invalido!")
        return

    # insere as particulas
    corpos.set_bodies(pts)

    # aumenta tamanho dos planetas
    if op == "s":
        corpos.pontos["Terra"].retain = 77
        corpos.pontos["Marte"].retain = 126
        corpos.pontos["Jupiter"].retain = 970
        corpos.pontos["Saturno"].retain = 2365
        for p in corpos.pontos:
            if p == "Sol": continue
            corpos.pontos[p].radius *= 10

    # centraliza visualizacao 
    scene.center = corpos.mass_center()

    # registra eventos
    scene.bind('keydown', corpos.key_input)
    scene.bind('click', corpos.mouse)

    # pausa no início
    corpos.pause = True
    scene.waitfor("keydown")

    # liga a forca da gravidade
    corpos.integracao(T)

    # salva estado final em arquivo de texto
    corpos.registra()

    print("\n::Fim::")

###############################################################################

if __name__ == "__main__":
    main()