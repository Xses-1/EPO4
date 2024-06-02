from module4 import KITTmodel
from PID import PID
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Button, Slider

positionx = 1.0
positiony = 1.0
currentAngle = 90.0

waittime = 100
movetime = 1900
t = np.linspace(0,10,2000)
Setpointsx = np.concatenate([np.zeros(waittime), [positionx] * movetime])
Setpointsy = np.concatenate([np.zeros(waittime), [positiony] * movetime])

def TestPIDIntegration(kp, ki, kd):
    Pid = PID()
    Pid.AngleKp = kp
    Pid.AngleKd = kd
    Pid.AngleKi = ki
    KITT = KITTmodel()

    z = [0]
    F = 0.0
    phi = 0.0

    x = [0.0]
    y = [0.0]
    angle = [90.0]
    Phis = [0]
    Thetas = [0]

    for i in range(1,len(t)):
        dt = t[i] - t[i-1]

        position_Vector, Theta = KITT.update(phi,F,dt)

        x.append(position_Vector[0][0])
        y.append(position_Vector[1][0])


        F,phi = Pid.Update(Setpointsx[i], Setpointsy[i], x[-1], y[-1], Theta, dt)
        #print(Pid.angle , '  ', phi)

        Phis.append(phi)
        Thetas.append(Theta)

    return x , y , Phis, Thetas

fig,ax = plt.subplots(2,2)


init_kp = 1
init_ki = 0
init_kd = 0


fig, ax = plt.subplots(2,2)
fig.subplots_adjust(bottom=0.2, left = 0.1, top = 0.98, right = 0.99)

line1, = ax[0][0].plot(TestPIDIntegration(init_kp, init_ki, init_kd)[0], TestPIDIntegration(init_kp, init_ki, init_kd)[1], lw=2, label = 'car position')
line11, = ax[0][0].plot(Setpointsy, Setpointsx, label = 'car setpoint')
ax[0][0].set_xlabel('X [m]')
ax[0][0].set_ylabel('Y [m]')
ax[0][0].set_ylim(-2,2)
ax[0][0].set_xlim(-2,2)
ax[0][0].legend(loc = 'upper right')

line2, = ax[0][1].plot(t, TestPIDIntegration(init_kp, init_ki, init_kd)[2], lw=2, label = 'wheel Angle')
line22 = ax[0][1].set_ylabel('wheel angle [Deg]')
ax[0][1].set_ylim(-35,35)
ax[0][1].set_xlabel('time [s]')
ax[0][1].legend()


line3, = ax[1][0].plot(t, TestPIDIntegration(init_kp, init_ki, init_kd)[3], lw=2, label = 'Thetas')
line33, = ax[1][0].plot(t,(np.concatenate([[0.0] * waittime, [45.0] * movetime])), label = 'theta setpoint')
ax[1][0].set_ylabel('Theta [deg]')
ax[1][0].set_xlabel('time [s]')
ax[1][0].set_ylim(-1,180)
ax[1][0].legend(loc = 'upper right')

line4, = ax[1][1].plot(t, TestPIDIntegration(init_kp, init_ki, init_kd)[0], lw=2, label = 'x position')
line44, = ax[1][1].plot(t,Setpointsx, label = 'x setpoint')
ax[1][1].set_ylabel('x position [m]')
ax[1][1].set_xlabel('time [s]')
ax[1][1].set_ylim(-2,2)
ax[1][1].legend(loc = 'upper right')


axKp = fig.add_axes([0.05, 0.1, 0.25, 0.03])
Kp_slider = Slider(
    ax=axKp,
    label='Kp',
    valmin=-5,
    valmax=5,
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
    print('update')
    x, y, phis, Thetas = TestPIDIntegration(Kp_slider.val,ki_slider.val ,Kd_slider.val)
    line1.set_xdata(x)
    line1.set_ydata(y)

    line2.set_ydata(phis)
    line3.set_ydata(Thetas)
    line4.set_ydata(x)
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