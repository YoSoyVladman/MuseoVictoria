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



def white_background():
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def entregado():
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(RED)
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
    exit()

  if ser.isOpen():
    while True:
      #pygame.draw.rect(screen,WHITE,RECT)
      white_background()
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
              pygame.draw.rect(screen,GREEN,RECT)
              c = requests.post(URL + 'free/' + match + '/true')
              #time.sleep(2)
              #pygame.draw.rect(screen,BLACK,RECT)
            else:
              print 'Entregada'
              entregado()
          else:
            print 'No Permitido'
            pygame.draw.rect(screen,RED,RECT)

      except requests.ConnectionError as e:
          pass
      except requests.HTTPError as e:
          pass
      except requests.ConnectTimeout as e:
          pass
      except requests.ReadTimeout as e:
          pass
      except requests.Timeout as e:
          pass


      pygame.display.update()
      #time.sleep(2)
      #pygame.draw.rect(screen,BLACK,RECT)
