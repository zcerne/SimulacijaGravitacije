import pygame
import random
import Gravitacija
import numpy as np

pygame.display.set_caption('Gravitacija')

širina, višina = 700, 400
screen = pygame.display.set_mode((širina, višina))

env = Gravitacija.Okolje(širina, višina)
env.barva = (0,0,0)
env.addFunctions(["premik", "združi", "miška"])

def radij(masa):
    return  masa**0.5

for p in range(2):
    particle_masa = random.randint(1,4)
    particle_size = radij(particle_masa)
    env.dodaj_delec(masa=particle_masa, size=particle_size, v=0, barva=(255,255,255))

izbrani = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            izbrani = env.najdi_delec(*pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            izbrani = None

    if izbrani:
        izbrani.miška(*pygame.mouse.get_pos())
    
    
    env.update()
    screen.fill(env.barva)

    particles_to_remove = []
    for p in env.delci:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.size = radij(p.masa)
            del p.__dict__['collide_with']

        if p.size < 2:
            pygame.draw.rect(screen, p.barva, (int(p.x), int(p.y), 2, 2))
        else:
            pygame.draw.circle(screen, p.barva, (int(p.x), int(p.y)), int(p.size), 0)
        
    for p in particles_to_remove:
        env.delci.remove(p)

    pygame.display.flip()



