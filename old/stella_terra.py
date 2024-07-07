import numpy as np

def print_values(t, y, z):
    print(f"t = {t}, y = {y}, z = {z}")

def process_values(t, y, z):
    # Questa funzione utilizza i valori di t, y e z per descrivere il movimento dei punti in tempo reale
    # Qui puoi implementare la logica che desideri per elaborare i valori
    print_values(t, y, z)

def metodo_heunBid(t0, y0, z0, f1, f2, g1, g2, N, dt, process_values):
    y = np.zeros(2)
    z = np.zeros(2)
    t = t0
    y[0] = y0[0]
    y[1] = y0[1]
    z[0] = z0[0]
    z[1] = z0[1]

    for n in range(N):
        tn = t
        y1_euler = y[0] + dt * f2(tn, y[0], y[1], z[0])
        y2_euler = y[1] + dt * f1(tn, y[0], y[1])
        z1_euler = z[0] + dt * g2(tn, z[0], z[1], y[0])
        z2_euler = z[1] + dt * g1(tn, z[0], z[1])
        y_next = np.zeros(2)
        z_next = np.zeros(2)
        y_next[0] = y[0] + (dt/2) * (f1(tn, y[0], y[1]) + f1(tn, y1_euler, y2_euler))
        y_next[1] = y[1] + (dt/2) * (f2(tn, y[0], y[1], z[0]) + f2(tn, y1_euler, y2_euler, z[0]))
        z_next[0] = z[0] + (dt/2) * (g1(tn, z[0], z[1]) + g1(tn, z1_euler, z2_euler))
        z_next[1] = z[1] + (dt/2) * (g2(tn, z[0], z[1], y[0]) + g2(tn, z1_euler, z2_euler, y[0]))
        t += dt

        # Pass the current values to the process_values function
        """potrei sostiturire questa chiamata con uno yield
           e ottenere così una funzione chiamabile come modulo
        """
        yield t, y_next, z_next
        #process_values(t, y_next, z_next)

        # Update y and z for the next iteration
        y = y_next
        z = z_next

# Parametri e condizioni iniziali
"""
G = 6.6743e-11
m2 = 1.98847e30
m1 = 5.97219e24
t0 = 0
v0 = 30290
r0 = 1.471e11
omega = v0 / r0
c1 = (r0 ** 2) * omega
c2 = 0
"""
#definisco delle condizioni iniaziali per un problema fittizio in cui ci potrebbe essere collasso
G = 6.6743e-11
m2 = 1000
m1 = 5000
t0 = 0
v0 = 4
r0 = 10.5
v1 = 2
r1 = 10
omega = v0 / r0
omega2 = v1 / r1
c1 = (r0 ** 2) * omega
c2 = (r1 ** 2) * omega2

# Condizioni iniziali
y0 = [r0, 0]
z0 = [r1, 0]  # La stella inizia al centro

# Funzioni differenziali
f1 = lambda t, y1, y2: y2
f2 = lambda t, y1, y2, z1: (-G * m2 / ((abs(y1 - z1)) ** 2)) + (c1 ** 2) / ((y1 ** 3))
g1 = lambda t, z1, z2: z2
g2 = lambda t, z1, z2, y1: (+G * m1 / ((abs(y1 - z1)) ** 2)) + (c2 ** 2) / ((z1 ** 3)) #ho possibilità di 0/0
#g2 = lambda t, z1, z2, y1: (+G * m1 / ((abs(y1 - z1)) ** 2))

T = 31.536e6
N = int(2 * 31.536e6)
dt = T / N

# Esegui il metodo di Heun e processa i valori in tempo reale
for t,y,z in  metodo_heunBid(t0, y0, z0, f1, f2, g1, g2, N, dt, process_values):
    a1 = (c1 )/(y[0] ** 2)
    a2 = (c2 )/(z[0] ** 2) 
    print(f"t: {t}, r1, a1: {y};{a1}, z: {z};{a2}") 
