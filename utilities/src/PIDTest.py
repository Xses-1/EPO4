from module4 import KITTmodel
from EPO4.Inc.PID import PID
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Button, Slider

positionx = 0.0
positiony = 2.0
currentAngle = 90.0

t = np.linspace(0,40,2000)
Setpointsy = np.concatenate([np.zeros(100), [positiony] * 1900])

def TestPIDForce(kp,ki,kd):
    Pid = PID()
    Pid.ForceKp = kp
    Pid.ForceKd = kd
    Pid.ForceKi = ki
    KITT = KITTmodel()

    z = [0]
    F = 0
    for i in range(1,len(t)):
        dt = t[i] - t[i-1]

        v = KITT.velocity_state(F, dt)
        z.append(z[-1] + (v * dt))
        
        deltaP, deltaTheta = Pid.CalculateErrors(positionx, Setpointsy[i], positionx, z[-1], currentAngle)

        F = Pid.calculateForce(deltaP, dt)

    z = np.array(z)
    try:
        print(f'Rise Time: {t[(0.9<z) & (z < 1)][0]}')
    except IndexError:
        print("never reaches equilibrium")


    return z

init_kp = 1
init_ki = 0
init_kd = 0


fig, ax = plt.subplots()
line, = ax.plot(t, TestPIDForce(init_kp, init_ki, init_kd), lw=2)
line2  = ax.plot(t, Setpointsy)
ax.set_xlabel('Time [s]')
ax.set_ylabel('distance [m]')
ax.set_ylim(-0.5,2)
fig.subplots_adjust(bottom=0.2, left = 0.1, top = 0.98, right = 0.99)

axKp = fig.add_axes([0.05, 0.1, 0.25, 0.03])
Kp_slider = Slider(
    ax=axKp,
    label='Kp',
    valmin=0,
    valmax=30,
    valinit=init_kp,
)

axKi = fig.add_axes([0.4, 0.1, 0.25, 0.03])
ki_slider = Slider(
    ax=axKi,
    label='Ki',
    valmin=-1,
    valmax=1,
    valinit=init_ki,
)

axKd = fig.add_axes([0.7, 0.1, 0.25, 0.03])
Kd_slider = Slider(
    ax=axKd,
    label='Kd',
    valmin=-1,
    valmax=1,
    valinit=init_kd,
)

def update(val):
    line.set_ydata(TestPIDForce(Kp_slider.val, ki_slider.val, Kd_slider.val))
    fig.canvas.draw_idle()


Kp_slider.on_changed(update)
ki_slider.on_changed(update)
Kd_slider.on_changed(update)

resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    Kp_slider.reset()
    ki_slider.reset()
    Kd_slider.reset()
button.on_clicked(reset)

plt.show()