import numpy as np
import matplotlib.pyplot as plt

"""
Riceve in input tutti i dati del problema che vogliamo simulare
e controlla che l'orbita sia simulabile e fino a che valore di T
il programma principale dovrà allora far uscire un banner a schermo
in cui avvisa che l'orbita può essere simulata fino a un certo T
"""

# Parametri
G = 6.67430e-11  # Costante gravitazionale in m^3 kg^-1 s^-2
m1 = 1000 # Massa del primo corpo (Terra) in kg
m2 = 10e10  # Massa del secondo corpo (Sole) in kg

# Condizioni iniziali
r1_0 = 200  # Raggio iniziale del primo corpo (Terra) in m
v1_0 = 0  # Velocità iniziale radiale del primo corpo in m/s
theta1_0 = 0  # Angolo iniziale del primo corpo in rad
omega1_0 = 0.15 / r1_0  # Velocità angolare iniziale del primo corpo in rad/s

r2_0 = 0.000001  # Raggio iniziale del secondo corpo (Sole) in m (inizialmente al centro)
v2_0 = 0  # Velocità iniziale radiale del secondo corpo in m/s
theta2_0 = 0  # Angolo iniziale del secondo corpo in rad
omega2_0 = 0.000001 / r2_0  # Velocità angolare iniziale del secondo corpo in rad/s

# Funzioni differenziali
def f_r1(r1, v1, r2, omega1):
    return (-G * m2 / (np.abs(r1 - r2)) ** 2) + r1 * omega1 ** 2

def f_theta1(r1, v1, omega1):
    return -2 * v1 * omega1 / r1

def f_r2(r2, v2, r1, omega2):
    return (G * m1 / (np.abs(r2 - r1)) ** 2) + r2 * omega2 ** 2

def f_theta2(r2, v2, omega2):
    return -2 * v2 * omega2 / r2

# Metodo di Heun per il sistema di equazioni differenziali
def metodo_heun_bid(t0, y0, N, dt, process_values):
    t = t0
    y = np.array(y0)

    for n in range(N):
        print(t)
        print(dt)
        r1, v1, theta1, omega1, r2, v2, theta2, omega2 = y

        # Predizione con metodo di Eulero
        r1_euler = r1 + dt * v1
        v1_euler = v1 + dt * f_r1(r1, v1, r2, omega1)
        theta1_euler = theta1 + dt * omega1
        omega1_euler = omega1 + dt * f_theta1(r1, v1, omega1)

        r2_euler = r2 + dt * v2
        v2_euler = v2 + dt * f_r2(r2, v2, r1, omega2)
        theta2_euler = theta2 + dt * omega2
        omega2_euler = omega2 + dt * f_theta2(r2, v2, omega2)

        # Correzione con metodo di Heun
        r1_next = r1 + (dt / 2) * (v1 + v1_euler)
        v1_next = v1 + (dt / 2) * (f_r1(r1, v1, r2, omega1) + f_r1(r1_euler, v1_euler, r2_euler, omega1_euler))
        theta1_next = theta1 + (dt / 2) * (omega1 + omega1_euler)
        omega1_next = omega1 + (dt / 2) * (f_theta1(r1, v1, omega1) + f_theta1(r1_euler, v1_euler, omega1_euler))

        r2_next = r2 + (dt / 2) * (v2 + v2_euler)
        v2_next = v2 + (dt / 2) * (f_r2(r2, v2, r1, omega2) + f_r2(r2_euler, v2_euler, r1_euler, omega2_euler))
        theta2_next = theta2 + (dt / 2) * (omega2 + omega2_euler)
        omega2_next = omega2 + (dt / 2) * (f_theta2(r2, v2, omega2) + f_theta2(r2_euler, v2_euler, omega2_euler))

        t += dt
        y = np.array([r1_next, v1_next, theta1_next, omega1_next, r2_next, v2_next, theta2_next, omega2_next])

        # Pass the current values to the process_values function
        process_values(t, r1_next, theta1_next, r2_next, theta2_next)

# Liste per i dati
times = []
r1_values = []
theta1_values = []
r2_values = []
theta2_values = []

def process_values(t, r1, theta1, r2, theta2):
    times.append(t)
    r1_values.append(r1)
    theta1_values.append(theta1)
    r2_values.append(r2)
    theta2_values.append(theta2)

# Parametri della simulazione
T = 15000  # Un anno in secondi
N = 30000  # Numero di passi temporali
dt = T / N

# Condizioni iniziali nel formato richiesto
y0 = [r1_0, v1_0, theta1_0, omega1_0, r2_0, v2_0, theta2_0, omega2_0]

# Esegui la simulazione
metodo_heun_bid(0, y0, N, dt, process_values)

# Plotta i risultati
plt.figure(figsize=(14, 7))

# Raggio
plt.subplot(2, 1, 1)
plt.plot(times, r1_values, label='r1 (Terra)')
plt.plot(times, r2_values, label='r2 (Sole)')
plt.xlabel('Tempo (s)')
plt.ylabel('Raggio (m)')
plt.title('Raggio nel tempo')
plt.legend()

# Angolo
plt.subplot(2, 1, 2)
plt.plot(times, theta1_values, label='theta1 (Terra)')
plt.plot(times, theta2_values, label='theta2 (Sole)')
plt.xlabel('Tempo (s)')
plt.ylabel('Angolo (rad)')
plt.title('Angolo nel tempo')
plt.legend()

plt.tight_layout()
plt.show()
