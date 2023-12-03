#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import serial
import pygame
from pygame.locals import *
import sys
import time
import csv
import matplotlib.pyplot as plt

pygame.init()

L  = 360
xi = 60
yi = 70
xf = L + xi
yf = L + yi

espessura = 60

preto = (64,64,64)
branco = (245,245,245)
cinza = (150, 150, 150)
azul =  (30,144,255) #55,153,219
verde = (240,240,240)
verdesc = (80,80,80)
amarelo = (240, 224, 93)

fonte1 = pygame.font.SysFont("arial", 160, bold=True)
fonte2 = pygame.font.SysFont("arial", 50, bold=True)
fonte3 = pygame.font.SysFont("arial", 15, bold=True)

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height),pygame.DOUBLEBUF)
background = pygame.Surface(screen.get_size()).convert()
screen.fill(preto)

pygame.display.set_caption ('Anemômetro MPXV 5004')
clock = pygame.time.Clock()

tomadas = 0
vo = 0

teste = 1

if teste == 1:
    try:
        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            print("Linux")
        elif sys.platform.startswith('win'):
            ser = serial.Serial('COM3', 9600)
            print("Windows (eca!)")
        elif sys.platform.startswith('darwin'):
            ser = serial.Serial('/dev/tty.usbmodemxxxxxxx', 9600) # editar a parte "xxxxxxx" com o número da porta serial
            #ser = serial.Serial('/dev/tty.usbserial????', 9600)
            print("Mac OSX")
        else:
            print("Não foi possível abrir a porta serial")
            label = fonte2.render("Não foi possível abrir a porta serial",1,amarelo)
            screen.blit(label,(20,10))
            pygame.display.flip()
            time.sleep(3.0)
            sys.exit()
            
        time.sleep(1.0)
        print("foi")
        time.sleep(1.0)
        print("leu")
        sulfixo = int(time.time())
        csvFile = open(f'dados_{sulfixo}.csv', 'w')
        csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
        xo = 0
        x_graf = []
        dado_graf = []
    except:
        print("Não foi possível abrir a porta serial")
        label = fonte2.render("Não foi possível abrir a porta serial",1,amarelo)
        screen.blit(label,(20,10))
        pygame.display.flip()
        time.sleep(3.0)
        sys.exit()
        
while True:
    clock.tick(20)
    screen.fill(preto)
    for event in pygame.event.get():
        if event.type == QUIT:
            if teste == 1:
                ser.close() 
                csvFile.close()
            print("Saindo....")
            pygame.quit()
            sys.exit()   # fim do programa.
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if teste == 1:
                    ser.close()   # fecha porta serial.
                    csvFile.close()
                print("Saindo....")
                pygame.quit()
                sys.exit()   # fim do programa.
            if event.key == K_z:
                if teste == 1:
                    ser.write(b'a')
                    linha = ser.readline()
                    vo = int(linha.strip())
                else:
                    pass
            if event.key == K_x:
                if teste == 1:
                    xo = xo + 1
                    x_graf.append(xo)
                    dado_graf.append(valor)
                    csvWriter.writerow([xo,todos])
                    #print dado_graf
                else:
                    pass
            if event.key == K_g:
                if teste == 1:
                    plt.plot(x_graf, dado_graf, 'b--o')
                    plt.xlabel('Tomada')
                    plt.ylabel('Pressão (Pa)')
                    plt.grid(True)
                    plt.show()
                else:
                    pass
            if event.key == K_p:
                if teste == 1:
                    teste = 0
                    label = fonte2.render("Pausado...",1,amarelo)
                    screen.blit(label,(20,10))
                else:
                    teste = 1
            if event.key == K_s:
                if teste == 1:
                    labelx = fonte2.render("Movimentando...",1,amarelo)
                    screen.blit(labelx,(20,10))
                    pygame.display.flip()
                    ser.write(b's')
                    movido = ""
                    tomadas += 1
                    while movido != b'ok':
                        movido = ser.readline().strip()
                        print(movido)
                else:
                    pass
            if event.key == K_d:
                if teste == 1:
                    label = fonte2.render("Movimentando...",1,amarelo)
                    screen.blit(label,(20,10))
                    pygame.display.flip()
                    ser.write(b'd')
                    movido = ""
                    if tomadas > 0: tomadas -=1
                    while movido != b'ok':
                        movido = ser.readline().strip()
                        print(movido)
                else:
                    pass
            if event.key == K_h:
                if teste == 1:
                    label = fonte2.render("Movimentando...",1,amarelo)
                    screen.blit(label,(20,10))
                    pygame.display.flip()
                    for i in range (0,tomadas):
                        ser.write(b'd')
                        movido = ""
                        while movido != b'ok':
                            movido = ser.readline().strip()
                            print(movido)
                    tomadas = 0
                else:
                    pass
            if event.key == K_n:
                if teste == 1:
                    csvFile.close()
                    sulfixo = int(time.time())
                    csvFile = open(f'dados_{sulfixo}.csv', 'w')
                    csvWriter = csv.writer(csvFile, delimiter=',', lineterminator='\n')
                    xo = 0
                    x_graf = []
                    dado_graf = []                    
                else:
                    pass


    if teste == 1:
        dados = 0
        intervalo = 200
        todos = []
        for i in range (1,intervalo+1):
            ser.write(b'a')
            time.sleep(0.01)
            linha = ser.readline()
            dados += float(linha.strip())
            todos.append(float(linha.strip())-vo)
            
        dados = dados/float(intervalo)
        valor = (float(dados)-vo)*(0.1875/1)
        val   = (valor/10)*(3.0/2)*math.pi
        #Trecho abaixo para ler o MPX2010
        #valor = ((float(linha.strip())-vo)*0.0078125)*20
        #valor = int(linha.strip())-vo
        #valor = 0.1293840*(float(linha.strip())-vo) - 0.0183951
        #val   = ((float(linha.strip())-vo)/100)*(3.0/2)*math.pi
        if valor < 0:
            valor = 0
            val   = 0
    else:
        curPos = pygame.mouse.get_pos()
        valor = (float(curPos[0])/screen_width)*(3.0/2)*math.pi
        val = valor
        
    pygame.draw.arc(screen,verdesc,(xi,yi,xf,yf),0,(3.0/2)*math.pi,espessura)
    pygame.draw.arc(screen,verdesc,(xi,yi-1,xf,yf),0,(3.0/2)*math.pi,espessura)
    pygame.draw.arc(screen,azul,(xi,yi,xf,yf),0,val,espessura)
    pygame.draw.arc(screen,azul,(xi,yi-1,xf,yf),0,val,espessura)
    #pygame.draw.arc(screen,azul,(xi-1,yi,xf,yf),0,valor,espessura)
    
    label = fonte1.render(str('{:5.1f}'.format(valor)),1,azul)
    #label = fonte1.render(str('{:04.1f}'.format(valor)),1,azul)
    screen.blit(label,(xi+(xf/2),yi+(yf/2)))

    label = fonte2.render("Pa",1,branco)
    #label = fonte2.render(" mV",1,azul)
    screen.blit(label,(xi+200+xf/2,yi+160+yf/2))
    
    label = fonte2.render(f"Tomada: {tomadas}", 1, branco)
    screen.blit(label, (200 + screen_width/2, screen_height - 60))
    
    h = 40
    
    label = fonte3.render("COMANDOS:", 1, cinza)
    screen.blit(label, (200 + screen_width/2, 10))
    
    label = fonte3.render("Tecle Z para zerar", 1, cinza)
    screen.blit(label, (200 + screen_width/2, h))

    h += 30
    label = fonte3.render("Tecle X para salvar dados", 1, cinza)
    screen.blit(label, (200 + screen_width/2, h))

    h += 30
    label = fonte3.render("Tecle S para mover para cima", 1, cinza)
    screen.blit(label, (200 + screen_width/2, h))

    h += 30
    label = fonte3.render("Tecle D para mover para baixo", 1, cinza)
    screen.blit(label, (200 + screen_width/2, h))

    h += 30
    label = fonte3.render("Tecle H para mover para posição inicial", 1, cinza)
    screen.blit(label, (200 + screen_width/2, h))
    
    h += 70
    label = fonte3.render("Tecle ESC para encerrar", 1, cinza)
    screen.blit(label, (200 + screen_width/2, h))

    #pygame.display.update()
    pygame.display.flip()
    time.sleep(0.1)

pygame.quit()
