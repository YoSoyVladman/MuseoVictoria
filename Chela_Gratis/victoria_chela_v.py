import re, sys, signal, os, time, datetime
import serial
### Instalar Requets
import requests
import json
import pygame

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"


BITRATE = 9600

SCR_SIZE = 320, 240
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RECT = [0, 0, 320, 240]


pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(SCR_SIZE)
background = pygame.Surface(screen.get_size())
background = background.convert()


def inicio():
    background.fill(WHITE)

    font = pygame.font.Font(None, 50)
    text = font.render("MUSEO VICTORIA", 1,BLACK)
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text,(10,100))

    screen.blit(background, (0, 0))
    pygame.display.flip()

def espera():
    background.fill(BLACK)

    font = pygame.font.Font(None, 50)
    text = font.render("MUSEO VICTORIA", 1,WHITE)
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, (10,100))

    screen.blit(background, (0, 0))
    pygame.display.flip()

def entregado():
    background.fill(BLUE)

    font = pygame.font.Font(None, 45)
    text = font.render("CHELA ENTREGADA", 1,WHITE)
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, (10,100))
    screen.blit(background, (0, 0))
    pygame.display.flip()

def permitido():
    background.fill(GREEN)

    font = pygame.font.Font(None,50)
    text = font.render("CHELA GRATIS", 1,WHITE)
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, (30,100))
    screen.blit(background, (0, 0))
    pygame.display.flip()

def nopermitido(text):
    background.fill(RED)
    font = pygame.font.Font(None, 50)
    text = font.render(text, 1,WHITE)
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, (10,100))
    screen.blit(background, (0, 0))
    pygame.display.flip()


#URL = 'http://10.0.1.100:8080/api/visitors/'
URL = 'http://10.1.8.170:9000/api/visitors/'

if __name__ == '__main__':
  ser = serial.Serial('/dev/ttyUSB0', BITRATE)
  rfidPattern = re.compile(b'[\W_]+')
  try:
    ser.flushInput()
    ser.flushOutput()
  except Exception, e:
    print "error open serial port: " + str(e)
    inicio()
    pass



  try:

      if ser.isOpen():
        inicio()
        while True:
           #pygame.draw.rect(screen,WHITE,RECT)
          line = ser.readline()
          last_received = line.strip()
          match = rfidPattern.sub('', last_received)
          print match
          cadena = URL + 'edad/' +match
          try:
              r = requests.get(cadena)
              json = r.json()
              print json
              edad = json.get('edad')
              chela = json.get('chelaFree')

              if edad == 'True':
                if not chela:
                  print 'Permitido'
                  permitido()
                  c = requests.post(URL + 'free/' + match + '/true')
                  #time.sleep(2)
                  #pygame.draw.rect(screen,BLACK,RECT)
                else:
                  print 'Entregada'
                  entregado()
              else:
    	      if(r.status_code == requests.codes.ok):
    		n = "MENOR DE EDAD"
                  	nopermitido(n)
    	      else:
                  	error = "NO ENCONTRADO"
                  	print 'Error'
                  	nopermitido(error)

          except requests.ConnectionError as e:
              inicio()
              pass
          except requests.HTTPError as e:
              inicio()
              pass
          except requests.ConnectTimeout as e:
              inicio()
              pass
          except requests.ReadTimeout as e:
              inicio()
              pass
          except requests.Timeout as e:
              inicio()
              pass


          #time.sleep(10)
          #espera()
          pygame.display.update()
          time.sleep(2)
          espera()
          #pygame.draw.rect(screen,BLACK,RECT)

  except serial.serialutil.SerialException:
      inicio()
      pass
