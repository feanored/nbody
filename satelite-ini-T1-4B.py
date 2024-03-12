# -*- coding: cp1252 -*-
# programa satelite-ini.py
# declaracoes iniciais:
from __future__ import print_function, division
from visual import *
scene.width = 1400
scene.height = 980

# CONSTANTES 
G = 6.7e-11
mTerra = 6e24
msatelite = 15e3

# Objetos e cond. iniciais 
Terra = sphere(pos=vector(0,0,0), radius=6.4e6, material=materials.earth) 
satelite = sphere(pos=vector(2.1e7, 0,0), radius=2e6, color=color.yellow, material=materials.emissive) # cria um satélite amarelo

# Obs. O raio do satélite é enorme para facilitar sua visualização na tela 
# vsatelite = vector(0,1.9e3,0) # velocidade inicial do satélite 
vsatelite = vector(0,5.02e3,0) # velocidade inicial do satélite
psatelite = msatelite * vsatelite 

 
# Vetores ilustrativos e outros parâmetros da visualização 
scene.autoscale = 1  # mantém a escala da janela fixa (não atualiza automaticamente) 
parr = arrow(color=color.green,shaftwidth=1e6) # seta para representar o momento 
escalap=0.25 # fator de escala para a seta do momento 
Farr = arrow(color=color.red,shaftwidth=1e6) # seta para representar a força 
escalaF=1e3 # fator de escala para a seta da força 
trajetoria=curve(color=color.yellow) # curva para representar a trajetória 

# parametros de simulação
deltat = 60
t_tot = 3e7

# início 
t = 0 

# inicia pausado
scene.mouse.getclick()

trajetoria.append(pos=satelite.pos) # ponto inicial da trajetória 
sinal=1. # vai servir para contar meias voltas 
contador=0 # número de meias voltas
# -------------------------------------------------------- 

while t < t_tot:
	rate(300) # frequência do loop na simulação

#-----------------------------inicio da sua programação
# NÃO ALTERE A INDENTAÇÃO (1 TAB) 
# RESPETITE O USO DE MAIÚSCULAS E MINÚSCULAS
 
	r =  satelite.pos - Terra.pos # Posição do satélite em relação à Terra
	rmag = mag(r) # Módulo de r
	rhat = r / rmag # vetor unitário de r
	FTerra = G * mTerra * msatelite / (rmag*rmag) # atração gravitacional da Terra sobre o satélite
	Fnet = - FTerra * rhat # Força resultante sobre o satélite
	
	print('Fnet=', Fnet)
	
	psatelite = psatelite + (Fnet * deltat) # atualização do momento do satélite
	satelite.pos = satelite.pos + (psatelite/msatelite) * deltat # atualização da posição do satélite
#
#-----------------------------fim da sua programação    
    
	trajetoria.append(pos=satelite.pos) # acrescenta o trecho na trajetória
	parr.pos=satelite.pos # posiciona a seta do momento no satélite
	Farr.pos=satelite.pos # posiciona a seta da forca no satélite
	parr.axis=psatelite*escalap # define o tamanho e orientação da seta do momento com um fator de escala
	Farr.axis=Fnet*escalaF  # define o tamanho e orientação da seta da força com um fator de escala
    
#verifica se o satélite colidiu com a terra:
	if rmag < Terra.radius: 
		break
#------------------------------------------
#código para contar o número de meias-voltas=
#número de vezes que a coordenada y do satélite troca de sinal:
	if sinal*satelite.pos.y < 0:
		sinal=-sinal
		contador=contador+1
		
	#limita a execução a N períodos completos (N*2 meias voltas)	
	N = 10	
	if contador == N*2:
		print('O periodo e: ', 2*t/N / 3600, ' horas')
		break
		
	t = t+deltat # faz o tempo passar
