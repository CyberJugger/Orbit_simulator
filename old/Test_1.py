import pygame
import numpy as np
import Test_2 as ob  # Importa il modulo contenente il metodo di Heun

# init
pygame.init()
screen = pygame.display.set_mode([500, 500])
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Times New Roman', 20)

# Costante gravitazionale modificata per visualizzazione
G = 0.00001
running = True

def o_t(r: tuple):  # o_t sta per origin translator
    return r + (250, 250)

class Planet:
    istant_vel = np.array([0, 0])

    def __init__(self, mass: int, radius: int, color: tuple, r_i: list, v0: list):
        super(Planet, self).__init__()
        self.m = mass
        self.r = radius
        self.color = color
        self.init_position = np.abs(np.array(r_i))
        self.init_vel = np.array(v0)
        self.init_ang_vel = np.divide(self.init_vel, self.init_position)
        self.position = np.array(r_i)

    def draw_planet(self):
        pygame.draw.circle(screen, self.color, self.position, self.r)

    def update(self, r_n: tuple):
        self.position = r_n

    def process_values(self, t, r1, theta1, r2, theta2):
        self.update(((r1/1e11) * np.cos(theta1), (r1/1e11) * np.sin(theta1)))

# Inizializzo i pianeti
terra = Planet(5000000, 10, (51, 153, 255), [300, 300], [0, 0])
sole = Planet(100000000, 10, (255, 51, 153), [255, 255], [0, 0])
y0 = [terra.init_position[0], 0, 0, terra.init_ang_vel[0], sole.init_position[0], 0, 0, sole.init_ang_vel[0]]

initialization_time = pygame.time.get_ticks()
last_time = initialization_time

# Parametri della simulazione
T = 31.536e6
N = int(2 * 31.536e6)
dt = T / N

while running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time) / 1000.0  # Converti dt in secondi
    last_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    white = (255, 255, 255)
    coord_ons = my_font.render(f"X:{terra.position[0]} Y:{terra.position[1]}", True, white)
    fps = my_font.render(str(clock.get_fps()), True, white)
    vel = my_font.render(f"Vel: x:{terra.istant_vel[0]}, y: {terra.istant_vel[1]}", True, white)
    screen.blit(coord_ons, (0, 0))
    screen.blit(fps, (0, 20))
    screen.blit(vel, (170, 20))

    ob.metodo_heun_bid(current_time, y0, 1, dt, terra.process_values)
    terra.draw_planet()
    sole.draw_planet()

    pygame.display.update()

pygame.quit()
