
import numpy as np
import matplotlib.pyplot as plt


ref_voltage = 3.3
period = 0.002 #sampling period in ms
data_size = 4990
length = 1158

data = []
data.append(np.loadtxt('data_01.txt', dtype = int)[:data_size] * (ref_voltage / 4095))
data.append(np.loadtxt('data_11.txt', dtype = int)[:data_size] * (ref_voltage / 4095))

duration = period * data_size
t = np.arange(0, duration, period)

t_0 = np.argmax(data[0]) * period
t_1 = np.argmax(data[1]) * period
sound_speed = length / (t_1 - t_0)


data = []
data.append(np.loadtxt('data_01-l.txt', dtype = int)[:data_size] * (ref_voltage / 4095))
data.append(np.loadtxt('data_11-l.txt', dtype = int)[:data_size] * (ref_voltage / 4095))

t_0 = np.argmax(data[0]) * period
t_1 = np.argmax(data[1]) * period
sound_speed_l = length / (t_1 - t_0)

u1 = 0.99 * 28.97 + 0.01 * 18.01
u2 = 0.94 * 28.97 + 0.01 * 18.01 + 0.05 * 44.01

x = [0, 5]
x1 = [0, 6]
y = [(1000*1.399620225025242*8.31*295.75/u1)**0.5, (1000*1.3922728425900492*8.31*295.75/u2)**0.5]
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)

z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax.plot(x1, p(x1), label = "Аналитическая зависимость", color = "orange")
k = p.coef[0]
b = p.coef[1]


ax.set_title("Зависимость скорости звука от концентрации углекислого газа", fontsize = 20)
ax.set_ylabel("Скорость звука [м/с]", fontsize = 15)
ax.set_xlabel("Концентрация СО2 [%]", fontsize = 15)
ax.minorticks_on()
ax.grid(which='both')

C1 = (sound_speed-b)/k; C2 = (sound_speed_l-b)/k

ax.scatter(C1, sound_speed, label = "Значения в воздухе: " + str(f'{(sound_speed):3.1f}') + " [м/с], " + str(f'{(C1):3.1f}') + " [%]")
ax.scatter(C2, sound_speed_l, label = "Значения в выдохе: " + str(f'{(sound_speed_l):3.1f}') + " [м/с], " + str(f'{(C2):3.1f}') + " [%]")

ax.legend(fontsize=15)
fig.savefig("distance-calibration.png")

plt.show()