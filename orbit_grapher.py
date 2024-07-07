import pygame
import random as rand
import numpy as np
import ode_calc as ob

#init
pygame.init()
screen = pygame.display.set_mode([1000, 1000])
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Times New Roman', 20)

# Run until the user asks to quit
#G = float(6.67e-11)
running = True
toggle_text = True
def o_t(r: tuple): #o_t sta per origin translator
    r = r + (250,250)
    return r

def compute_cinematics(pianeta1,pianeta2, y):
    #print(y)
    pianeta1.compute_cinematics(y[2], y[0])
    pianeta2.compute_cinematics(y[6], y[4])

class Planet:    
    
    istant_vel = np.array([0,0])
    
    def __init__(self, mass: int, radius: int, color: tuple, r_i, coord_i, v0):
        super(Planet, self).__init__()
        self.m = mass
        self.r = radius
        self.color = color
        self.init_position = r_i
        self.init_vel = v0
        self.init_ang_vel = np.divide(self.init_vel,self.init_position)
        self.position = np.array(coord_i)
        #self.angle = np.atan(self.position[1]/self.position[0])
        # definisco una classe contenente tutte le info necessarie sul pianeta
    
    def draw_planet(self):
        pygame.draw.circle(screen, self.color, self.position, self.r)
        #definiso un metodo per disegnare automaticamente un pianeta

    def update(self, r_n: tuple):
        self.position = r_n

    #definisce una cinematica basilare ma senza alcuna dinamica dietro
    def compute_cinematics(self, angle,r):        
        #ricorda di applicare un fattore di scala
        #le coordinate calcoalte sono rispetto a 0, queste sono traslate a 500,500
        self.new_position = (500 + (r)*np.cos(angle), 500 + (r)*np.sin(angle))
        self.update(self.new_position)

    #semplice funzione dinamica (f: forza, t: tempo)

G = 6.6743e-11  # Costante gravitazionale
m1 = 1000 # Massa del primo corpo (es. Terra)
m2 = 10e10  # Massa del secondo corpo (es. Sole)
r1 = 200
v0 = 0.15

#inizializzo i pianeti
terra = Planet(m1, 10, (51, 153, 255), r1, (r1,0),v0)
sole = Planet(m2, 10, (255, 51, 153), 1.41421e-5,(0.00001, 0.00001), 0.0000001)
y0 = [terra.init_position, 0, 0, terra.init_ang_vel, sole.init_position, 0, 0, sole.init_ang_vel]

current_state = y0

T = 31.536e6
N = int(31.536e6)

initialization_time = pygame.time.get_ticks() #mi da un offset da togliere, è il tempo necessario per arrivare al loop
last_time = 0
t_s = 0 #è il tempo della simulazione

while running:
    clock.tick(500)
    #screen.fill((0,0,0))
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks() - initialization_time
    dt = 0.5  # Converti dt in secondi
    t_s = t_s + dt

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #devo aggiungere qualcosa che aumenti o diminuisca la velocità
    if keys[pygame.K_t]:
        if toggle_text == True:
                toggle_text = False
                terra.r = 1
                sole.r = 1
                screen.fill((0,0,0))
        else:
            toggle_text = True
            terra.r = 10
            sole.r = 10
 

    # le righe sotto si occupano di stampare il testo a schermo
    white = (255,255,255)
    #coord_ons = my_font.render(f"X:{terra.position[0]} Y:{terra.position[1]}", True, white)
    fps= my_font.render(f"fps: {str(int(clock.get_fps()))}", True, white)
    #vel = my_font.render(f"Vel: x:{terra.istant_vel[0]}, y: {terra.istant_vel[1]}", True, white)
    time = my_font.render(f"tr: {current_time/1000}", True, white)
    time_s = my_font.render(f"ts: {t_s}", True, white)
    if toggle_text == True:
        screen.fill((0,0,0))
        #screen.blit(coord_ons, (0,0))
        screen.blit(fps, (0,0))
        screen.blit(time, (100,0))
        screen.blit(time_s, (2, 20))

    new_state = ob.metodo_heun_bid_step(current_state, dt)
    current_state = new_state
    compute_cinematics(terra,sole, current_state)
    
    terra.draw_planet()
    sole.draw_planet()
    #print(f"sole: {sole.position}, terra:{terra.position}")

    pygame.display.update()

# Done! Time to quit.
pygame.quit()