import pygame
import random
import Gravitacija
import numpy as np
import math


def vektor_hitrosti(coords1, coords2):
    dx = coords2[0] - coords1[0]
    dy = coords2[1] - coords1[1]
    l = math.sqrt(dx**2 + dy**2)
    kot = math.atan2(dy, dx)
    v1 = (dx, dy)
    v2 = (dy, -dx)
    v3 = (-dy, dx)
    # t1 = 3/4 v1 + v2
    # t2 = 3/4 v1 + v3
    t1 = (coords2[0] + 1/6*dy + 3/4*dx, coords2[1] - 1/6*dx + 3/4*dy)
    t2 = (coords2[0] - 1/6*dy + 3/4*dx, coords2[1] + 1/6*dx + 3/4*dy)


    return l/10, kot

def preslikava(x, y):

    x = int(universe_screen.mx + (universe_screen.dx + x) * universe_screen.magnification)
    y = int(universe_screen.my + (universe_screen.dy + y) * universe_screen.magnification)
    return (x, y)

width, height = 900, 500
key1 = False
while not key1:
    print("Nakjučna postavitev?(y\\n)")
    input1 = input()
    if input1 == "y":
        nakljucna_razporeditev = True
        print("Vpišite število delcev")
        n_delcev = int(input())
        key1 = True
    elif input1 == "n":
        nakljucna_razporeditev = False 
        print("Vpišite ime datoteke")
        datoteka = input()
        key1 = True
    else:
        print("Error")

class UniverseScreen:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.dx, self.dy = 0, 0
        self.mx, self.my = 0, 0
        self.magnification = 1.0
        
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

universe_screen = UniverseScreen(width, height)

pygame.display.set_caption('Gravitacija')


screen = pygame.display.set_mode((width, height))

env = Gravitacija.Okolje(width, height)
env.barva = (0,0,0)
env.addFunctions(["premik", "združi", "miška", "odboj"])

def radij(masa):
    return  2*masa**(1/2)

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
        particle_masa = int(sez[0])
        particle_size = radij(particle_masa)
        particle_x = int(sez[1])
        particle_y = int(sez[2])
        particle_v = float(sez[3])
        particle_kot = np.pi*float(sez[4])


        env.dodaj_delec(masa=particle_masa, size=particle_size, x = particle_x, y = particle_y, 
                        v = particle_v, kot = particle_kot, barva = (255,255,255))

clock = pygame.time.Clock()
izbrani = None
running = True
paused = True
lokacija = False
hitrost = False
masa = False
start = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_miš = pygame.mouse.get_pos()[0]
            y_miš = pygame.mouse.get_pos()[1]
            x_miš = (x_miš - universe_screen.mx)/universe_screen.magnification - universe_screen.dx
            y_miš = (y_miš - universe_screen.my)/universe_screen.magnification - universe_screen.dy
            izbrani = env.najdi_delec(x_miš, y_miš)
        elif event.type == pygame.MOUSEBUTTONUP:
            izbrani = None
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
            elif event.key == pygame.K_SPACE:
                paused = not paused
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
                
    
    screen.fill(env.barva)


    if izbrani:
        x_miš = pygame.mouse.get_pos()[0]
        y_miš = pygame.mouse.get_pos()[1]
        x_miš = (x_miš - universe_screen.mx)/universe_screen.magnification - universe_screen.dx
        y_miš = (y_miš - universe_screen.my)/universe_screen.magnification - universe_screen.dy
        if paused:
            if lokacija:
                izbrani.x = x_miš
                izbrani.y = y_miš
            elif hitrost:
                izbrani.v, izbrani.kot = vektor_hitrosti([x_miš, y_miš], [izbrani.x, izbrani.y])
            elif masa:
                
                izbrani.masa = math.dist([izbrani.x, izbrani.y], [x_miš, y_miš])
                

                izbrani.size = radij(izbrani.masa)
        else: 
            izbrani.miška(x_miš, y_miš)
    
    
    if not paused:    
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

        """if p.size < 2:
            pygame.draw.circle(screen, p.barva, (x, y, 2, 2), size = 2)
        else:"""
        pygame.draw.circle(screen, p.barva, (x, y), size, 0)
        
        #vektor hitrosti
        if paused:
            end_pos = (x + 10*p.v*math.cos(p.kot), y + 10*p.v*math.sin(p.kot))
            pygame.draw.line(screen, color = (0,255,0), width = 2, start_pos = (x, y), end_pos = end_pos)
        
    
    particles_to_remove = set(particles_to_remove)
    for p in particles_to_remove:
        env.delci.remove(p)

    pygame.display.flip()
    clock.tick(80)


