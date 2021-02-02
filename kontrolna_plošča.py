import pygame
import random
import Gravitacija
import numpy as np

width, height = 700, 400
#test test
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
env.addFunctions(["premik", "združi", "miška"])

def radij(masa):
    return  masa**(1/2)

for p in range(200):
    particle_masa = random.randint(1,4)
    particle_size = radij(particle_masa)
    env.dodaj_delec(masa=particle_masa, size=particle_size, v=0, barva=(255,255,255))

clock = pygame.time.Clock()
izbrani = None
running = True
paused = False

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
            elif event.key == pygame.K_KP_PLUS :
                universe_screen.zoom(2)
            elif event.key == pygame.K_KP_MINUS:
                universe_screen.zoom(0.5)
            elif event.key == pygame.K_r:
                universe_screen.reset()
            elif event.key == pygame.K_SPACE:
                paused = not paused

    if izbrani:
        x_miš = pygame.mouse.get_pos()[0]
        y_miš = pygame.mouse.get_pos()[1]
        x_miš = (x_miš - universe_screen.mx)/universe_screen.magnification - universe_screen.dx
        y_miš = (y_miš - universe_screen.my)/universe_screen.magnification - universe_screen.dy
        izbrani.miška(x_miš, y_miš)
    
    
    if not paused:    
        env.update()

    screen.fill(env.barva)

    particles_to_remove = []
    for p in env.delci:
        if 'collide_with' in p.__dict__:
            
            particles_to_remove.append(p.collide_with)
            p.size = radij(p.masa)
            del p.__dict__['collide_with']
        
        x = int(universe_screen.mx + (universe_screen.dx + p.x) * universe_screen.magnification)
        #x_miš = (pygame.mouse.get_pos()[0] - universe_screen.mx)/universe_screen.magnification - universe_screen.dx
        y = int(universe_screen.my + (universe_screen.dy + p.y) * universe_screen.magnification)
        size = int(p.size * universe_screen.magnification)

        if p.size < 2:
            pygame.draw.rect(screen, p.barva, (x, y, 2, 2))
        else:
            pygame.draw.circle(screen, p.barva, (x, y), size, 0)
    
    particles_to_remove = set(particles_to_remove)
    for p in particles_to_remove:
        env.delci.remove(p)

    pygame.display.flip()
    clock.tick(80)


