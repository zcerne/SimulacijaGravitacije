import pygame
import random
import Gravitacija
import numpy as np
import math
import re
import time

pygame.init()

width, height = 1000, 600
def vektor_hitrosti(coords1, coords2):
    dx = coords2[0] - coords1[0]
    dy = coords2[1] - coords1[1]
    l = math.sqrt(dx**2 + dy**2)
    kot = math.atan2(dy, dx)
    t1 = (coords2[0] + 1/6*dy + 3/4*dx, coords2[1] - 1/6*dx + 3/4*dy)
    t2 = (coords2[0] - 1/6*dy + 3/4*dx, coords2[1] + 1/6*dx + 3/4*dy)

    return l/10, kot

def preslikava(x, y):

    x = int(universe_screen.mx + (universe_screen.dx + x) * universe_screen.magnification)
    y = int(universe_screen.my + (universe_screen.dy + y) * universe_screen.magnification)
    
    return (x, y)

def zagon():
    key1 = False
    while not key1:
        print("Nakjučna postavitev?(y\\n)")
        input1 = input() 
        if input1 == "y":
            nakljucna_razporeditev = True
            print("Vpišite število delcev")
            n_delcev = input()
            try:
                n_delcev = int(n_delcev)
            except:
                print("Prosim vnesite celo število.")
            if type(n_delcev) == int:
                razporedi(nakljucna_razporeditev, n_delcev)
                key1 = True
        elif input1 == "n":
            print("Vpišite ime datoteke")
            datoteka = input()
            try:
                razporedi(nakljucna_razporeditev = False, datoteka = datoteka)
            except:
                print("Datoteka ni najdena. Poskusite ponovno.")
                continue
            key1 = True
        else:
            print("Neveljaven odgovor. Poskusi z y ali n.")

def message_to_screen(msg, color, coords, size):
    font = pygame.font.SysFont(None, size) # 25 - velikost
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, coords)

def shrani_zacetni_pogoj(delci, datoteka):
    dat = open(datoteka, "w")
    for delec in delci:
        masa = delec.masa
        x = delec.x
        y = delec.y
        v = delec.v
        kot = delec.kot
        print(str(masa) + "," +  str(int(x)) + "," + str(int(y)) + "," + str(v) + "," + str(kot / np.pi), file = dat)

def najdi(x_mis, y_mis):
    x_mis, y_mis = preslikava(x_mis, y_mis)
    
    if math.dist((x_mis, y_mis), universe_screen.g_coords) < 10:
        universe_screen.najdi_g = True
    elif math.dist((x_mis, y_mis), universe_screen.info_gumb) < 20:
        universe_screen.info = not universe_screen.info
        universe_screen.paused = True
    elif abs(x_mis - universe_screen.back_gumb[0]) < 30 and abs(y_mis - universe_screen.back_gumb[1]) < 15:
        env.delci = []
        universe_screen.reset()
        universe_screen.prikaz_vrednosti = True
        universe_screen.paused = True
        universe_screen.zagon = True


def premik_g(x_mis):
    universe_screen.g_coords[0] = preslikava(x_mis, 0)[0]
    if universe_screen.g_coords[0] < universe_screen.g_os1[0]:
        universe_screen.g_coords[0] = universe_screen.g_os1[0]
    elif universe_screen.g_coords[0] > universe_screen.g_os2[0]:
        universe_screen.g_coords[0] = universe_screen.g_os2[0]

    env.G = universe_screen.max_G*(1 - (universe_screen.g_os2[0] - universe_screen.g_coords[0])/(universe_screen.g_os2[0] - universe_screen.g_os1[0]))

#def info_screen():


def radij(masa):
    return  2*masa**(1/2)

def razporedi(nakljucna_razporeditev, n_delcev = None, datoteka = None):
    if nakljucna_razporeditev:
        for p in range(n_delcev):
            particle_masa = random.randint(1,4)
            particle_size = radij(particle_masa)
            env.dodaj_delec(masa=particle_masa, size=particle_size, barva=(255,255,255))
    else:
        podatki = open(datoteka, "r")
        vrstice = podatki.readlines()
        for x in vrstice:
            sez = x.split(",")
            particle_masa = float(sez[0])
            particle_size = radij(particle_masa)
            particle_x = int(sez[1])
            particle_y = int(sez[2])
            particle_v = float(sez[3])
            particle_kot = np.pi*float(sez[4])


            env.dodaj_delec(masa=particle_masa, size=particle_size, x = particle_x, y = particle_y, 
                            v = particle_v, kot = particle_kot, barva = (255,255,255))

#test test
class UniverseScreen:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.dx, self.dy = 0, 0
        self.mx, self.my = 0, 0
        self.magnification = 1.0
        
        self.running = True
        self.paused = True

        self.prikaz_vrednosti = True

        self.max_G = 30
        self.najdi_g = False
        self.g_os1 = (20, height - 20)
        self.g_os2 = (200, height - 20)
        
        self.g_coords = [(1/30 - 1)*(180) + 200, height - 25]

        self.info_gumb = (width - 15, height - 15)
        self.info = False

        self.zagon = True
        self.back_gumb = [width - 30, 15]
        
    def scroll(self, dx=0, dy=0):
        self.dx += dx * width / (self.magnification*10)
        self.dy += dy * height / (self.magnification*10)
        
    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1-self.magnification) * self.width/2
        self.my = (1-self.magnification) * self.height/2
        
    def reset(self):
        self.dx, self.dy = 0, 0
        self.mx, self.my = 0, 0
        self.magnification = 1.0

    def info_screen(self):
        while self.info:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    universe_screen.info = False
                    env.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x_miš = pygame.mouse.get_pos()[0]
                    y_miš = pygame.mouse.get_pos()[1]
                    najdi(x_miš, y_miš)

                screen.fill((255, 255, 255))
                message_to_screen("Info", (0,0,0), [width/2, 20], 30)
                info = open("info.txt", "r", encoding = "utf-8")
                info_lines = info.readlines()
                for i, line in enumerate(info_lines):
                    line = line.strip()
                    message_to_screen(line, (0,0,0), [10, 30*i + 50], 30)
                
                pygame.draw.rect(screen, color = (0,0,0), rect = (universe_screen.info_gumb[0] - 15, universe_screen.info_gumb[1] - 15 , 30, 30), width = 2)
                message_to_screen("X", (0,0,0), [universe_screen.info_gumb[0] - 2, universe_screen.info_gumb[1] - 7], 25)
                clock.tick(15)
                pygame.display.flip()
        
    def zacetni_zaslon(self):
        st = ""
        kluc = 0
        while self.zagon:
            screen.fill((0,0,0))
            event = pygame.event.poll()
            keys = pygame.key.get_pressed()
            
            if kluc == 0:
                message_to_screen("Za naključno postavitev pritisnite \"y\".", (255, 255, 255), [width/5, height/2 - 40], 40)
                message_to_screen("Za vnos podatkov iz datoteke pritisnite \"n\".", (255, 255, 255), [width/5, height/2], 40)
            elif kluc == 1:
                message_to_screen("Vpišite število delcev in pritisnite enter: " + st, (255, 255, 255), [width/5, height/2 - 40], 40)
            elif kluc == 2:
                message_to_screen("Vpišite ime datoteke: " + st, (255, 255, 255), [width/3,height/2], 40)
            if event.type == pygame.QUIT:
                self.zagon = False
                universe_screen.running = False

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if kluc == 0:
                    if key == "y":
                        kluc = 1
                        key = ""
                    elif key == "n":
                        kluc = 2
                        key = ""
                
                if kluc == 1: 
                    if len(key) == 1:
                        st += key
                    elif key == "backspace":
                        st = st[:-1]
                    elif key == "return":
                        je_stevilo = re.match(r'^([\s\d]+)$', st)
                        if je_stevilo != None:
                            n_delcev = int(st)
                            if n_delcev < 300:
                                razporedi(nakljucna_razporeditev = True, n_delcev = n_delcev, datoteka = None)
                                shrani_zacetni_pogoj(env.delci, datoteka = "zacetno_stanje.txt")
                                self.zagon = False
                            else:
                                screen.fill((0,0,0))
                                message_to_screen("Poskusite manj od 300", (255, 255, 255), [width/3,height/2], 40)
                                st = ""
                                pygame.display.flip()
                                time.sleep(2)
                        else:
                            screen.fill((0,0,0))
                            message_to_screen("Poskusite s številom", (255, 255, 255), [width/3,height/2], 40)
                            st = ""
                            pygame.display.flip()
                            time.sleep(2)
                if kluc == 2:
                    if len(key) == 1:
                        st += key
                    elif key == "backspace":
                        st = st[:-1]
                    elif key == "return":
                        try:
                            razporedi(nakljucna_razporeditev = False, datoteka = st)
                            shrani_zacetni_pogoj(env.delci, datoteka = "zacetno_stanje.txt")
                        except:
                            screen.fill((0,0,0))
                            message_to_screen("Datoteka ni najdena", (255, 255, 255), [width/3,height/2], 40)
                            st = ""
                            pygame.display.flip()
                            time.sleep(2)
                            continue
                        self.zagon = False

            pygame.display.flip()

universe_screen = UniverseScreen(width, height)

env = Gravitacija.Okolje(width, height)
env.barva = (0,0,0)
env.addFunctions(["premik", "miška", "združi"])

#zagon()

pygame.display.set_caption('Gravitacija')
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

izbrani = None
doloci_g = False
lokacija = False
hitrost = False
masa = False
start = 0

universe_screen.zacetni_zaslon()

while universe_screen.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            universe_screen.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_miš = pygame.mouse.get_pos()[0]
            y_miš = pygame.mouse.get_pos()[1]
            x_miš = (x_miš - universe_screen.mx)/universe_screen.magnification - universe_screen.dx
            y_miš = (y_miš - universe_screen.my)/universe_screen.magnification - universe_screen.dy
            izbrani = env.najdi_delec(x_miš, y_miš)
            najdi(x_miš, y_miš)
        
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if izbrani:
                    env.delci.remove(izbrani)
                    izbrani = None
                else:
                    env.dodaj_delec(x = x_miš, y = y_miš, masa = 4, size = 4, barva=(255,255,255))

        elif event.type == pygame.MOUSEBUTTONUP:
            izbrani = None
            universe_screen.najdi_g = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                universe_screen.scroll(dx=1)
            elif event.key == pygame.K_RIGHT:
                universe_screen.scroll(dx=-1)
            elif event.key == pygame.K_UP:
                universe_screen.scroll(dy=1)
            elif event.key == pygame.K_DOWN:
                universe_screen.scroll(dy=-1)
            elif event.key == pygame.K_KP_PLUS:
                universe_screen.zoom(2)
            elif event.key == pygame.K_KP_MINUS:
                universe_screen.zoom(0.5)
            elif event.key == pygame.K_r:
                universe_screen.reset()
                env.delci = []
                razporedi(nakljucna_razporeditev = False, datoteka = "zacetno_stanje.txt")
                universe_screen.paused = True
                start = 0
            elif event.key == pygame.K_SPACE:
                universe_screen.paused = not universe_screen.paused
                if start == 0:
                    shrani_zacetni_pogoj(env.delci, datoteka = "zacetno_stanje.txt")
                    start = 1
            elif event.key == pygame.K_s:
                shrani_zacetni_pogoj(env.delci, datoteka = "saved.txt")
            elif event.key == pygame.K_l:
                lokacija = True
                hitrost = False
                masa = False
            elif event.key == pygame.K_v:
                hitrost = True
                lokacija = False
                masa = False
            elif event.key == pygame.K_m:
                masa = True
                hitrost = False
                lokacija = False
            elif event.key == pygame.K_d:
                universe_screen.prikaz_vrednosti = not universe_screen.prikaz_vrednosti
                

    if universe_screen.info:
        universe_screen.info_screen()
    if universe_screen.zagon:
        universe_screen.zacetni_zaslon()

    
    screen.fill(env.barva)
    
    if izbrani or universe_screen.najdi_g:
        x_miš = pygame.mouse.get_pos()[0]
        y_miš = pygame.mouse.get_pos()[1]
        x_miš = (x_miš - universe_screen.mx)/universe_screen.magnification - universe_screen.dx
        y_miš = (y_miš - universe_screen.my)/universe_screen.magnification - universe_screen.dy
        if universe_screen.najdi_g:
            premik_g(x_miš)
        elif universe_screen.paused:
            if lokacija:
                izbrani.x = x_miš
                izbrani.y = y_miš
            elif hitrost:
                izbrani.v, izbrani.kot = vektor_hitrosti([x_miš, y_miš], [izbrani.x, izbrani.y])
            elif masa:
                if [izbrani.x, izbrani.y] == [x_miš, y_miš]:
                    izbrani.masa = 0
                else:
                    izbrani.masa = 2*math.dist([izbrani.x, izbrani.y], [x_miš, y_miš])

                izbrani.size = radij(izbrani.masa)
        else: 
            izbrani.miška(x_miš, y_miš)
    
    if not universe_screen.paused and env.delci:
        env.update()

    particles_to_remove = []
    for p in env.delci:
        if 'collide_with' in p.__dict__:
            
            particles_to_remove.append(p.collide_with)
            p.size = radij(p.masa)
            del p.__dict__['collide_with']
        
        x = int(universe_screen.mx + (universe_screen.dx + p.x) * universe_screen.magnification)
        y = int(universe_screen.my + (universe_screen.dy + p.y) * universe_screen.magnification)
        size = int(p.size * universe_screen.magnification)

        if p.size < 1:
            pygame.draw.circle(screen, p.barva, (x, y, 2, 2), radius = 1)
        else:
            pygame.draw.circle(screen, p.barva, (x, y), size)
        
        #vektor hitrosti
        if universe_screen.paused:
            end_pos = (x + 10 * p.v * math.cos(p.kot), y + 10 * p.v * math.sin(p.kot))
            pygame.draw.line(screen, color = (0,255,0), width = 2, start_pos = (x, y), end_pos = end_pos)

        if universe_screen.prikaz_vrednosti:
            message_to_screen("m = " + str(int(p.masa)), (240, 0, 0), [x, y], 15)
            message_to_screen("v = " + str(round(p.v, 2)), (240, 0, 0), [x, y + 9], 15)
    
    if universe_screen.paused:
        if lokacija:
            message_to_screen("Določite koordinate", (255, 255, 255), [10, 10], 30)
        elif masa:
            message_to_screen("Določite mase", (255, 255, 255), [10, 10], 30)
        elif hitrost:
            message_to_screen("Določite hitrosti", (255, 255, 255), [10, 10], 30)

    
    
    pygame.draw.line(screen, color = (0,255,255), width = 2, start_pos = universe_screen.g_os1, end_pos = universe_screen.g_os2)
    pygame.draw.rect(screen, color = (0,255,255), rect = (universe_screen.g_coords[0], universe_screen.g_coords[1], 10, 10))
    message_to_screen("G = " + str(round(env.G, 1)), (0,255,255), [universe_screen.g_coords[0], universe_screen.g_coords[1] + 10], 15)
    
    pygame.draw.rect(screen, color = (255,255,255), rect = (universe_screen.info_gumb[0] - 15, universe_screen.info_gumb[1] - 15 , 30, 30), width = 2)
    message_to_screen("i", (255,255,255), [universe_screen.info_gumb[0] - 2, universe_screen.info_gumb[1] - 7], 25)

    pygame.draw.rect(screen, color = (255,255,255), rect = (universe_screen.back_gumb[0] - 30, universe_screen.back_gumb[1] - 15, 60, 30), width = 2)
    message_to_screen("back", (255,255,255), [universe_screen.back_gumb[0] - 15, universe_screen.back_gumb[1] - 7], 25)
    #pygame.draw.circle(screen, (255,255,255), universe_screen.back_gumb, 10)
    particles_to_remove = set(particles_to_remove)
    for p in particles_to_remove:
        env.delci.remove(p)

    pygame.display.flip()
    clock.tick(80)


