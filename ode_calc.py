import numpy as np

# Costante gravitazionale e masse
G = 6.6743e-11
m1 = 5.97219e24
m2 = 1.98847e30
m1 = 10e6 # Massa del primo corpo (es. Terra)
m2 = 10e10 
# Funzioni differenziali
def f_r1(r1, v1, r2, omega1):
    return (-G * m2 / (np.abs(r1 - r2)) ** 2) + r1 * omega1 ** 2

def f_theta1(r1, v1, omega1):
    return -2 * v1 * omega1 / r1

def f_r2(r2, v2, r1, omega2):
    return (+G * m1 / (np.abs(r2 - r1)) ** 2) + r2 * omega2 ** 2

def f_theta2(r2, v2, omega2):
    return -2 * v2 * omega2 / r2

# Metodo di Heun per il sistema di equazioni differenziali, singolo passo
def metodo_heun_bid_step(y, dt):
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

    return np.array([r1_next, v1_next, theta1_next, omega1_next, r2_next, v2_next, theta2_next, omega2_next])
