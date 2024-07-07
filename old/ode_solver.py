import numpy as np
import matplotlib.pyplot as plt

def print_values(t, y):
    print(f"t = {t}, y = {y}")

def metodo_heunBid(t0, y0, f1, f2, N, dt):
    y = np.zeros((N+1, 2))
    t = np.zeros(N+1)
    t[0] = t0
    y[0, 0] = y0[0]
    y[0, 1] = y0[1]

    for n in range(N):
        tn = t[n]
        y1_euler = y[n, 0] + dt * f2(tn, y[n, 0], y[n, 1])
        y2_euler = y[n, 1] + dt * f1(tn, y[n, 0], y[n, 1])
        y[n+1, 0] = y[n, 0] + (dt/2) * (f1(tn, y[n, 0], y[n, 1]) + f1(tn, y1_euler, y2_euler))
        y[n+1, 1] = y[n, 1] + (dt/2) * (f2(tn, y[n, 0], y[n, 1]) + f2(tn, y1_euler, y2_euler))
        t[n+1] = t[n] + dt

        # Print the values at each step
        print_values(t[n+1], y[n+1])

    return t, y

# Parametri e condizioni iniziali
G = 6.6743e-11
m2 = 1.98847e30
t0 = 0
v0 = 30290
r0 = 1.471e11
omega = v0 / r0
c = (r0 ** 2) * omega
m1 = 5.97219e24

# Il cuore del sistema differenziale
y0 = [r0, 0]
f1 = lambda t, y1, y2: y2
f2 = lambda t, y1, y2: (-G * m2 / (y1 ** 2)) + (c ** 2) / (y1 ** 3)

T = 31.536e6
N = int(31.536e6)
dt = T / N

t, yheun = metodo_heunBid(t0, y0, f1, f2, N, dt)

# Grafico della soluzione
plt.plot(t, yheun[:, 0], '-', linewidth=2)
plt.xlabel('Time t (iterations)')
plt.ylabel('Solution y1')
plt.title('Distanza Terra dal Sole')
plt.legend(['Heun method'], loc='northeast')
plt.show()
