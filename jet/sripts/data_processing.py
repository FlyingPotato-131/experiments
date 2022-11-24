import os
import re
import numpy as np
import matplotlib.pyplot as plt


def read(filename): #считать данные из файла
    with open(filename) as f:
        lines = f.readlines()

    steps = int(lines[2].split()[2])
    measures = np.asarray(lines[4:], dtype=int)

    return measures, steps, len(measures)


def get_velocity(value):
    pres = 0.16 * value - 157.9
    if (pres) < 0: pres = 0
    vel = (2*pres)**0.5 - 3
    if vel < 0: vel = 0
    return vel


files = os.listdir(".")

clbr = re.compile('cal')
nums = re.compile('\d+')  # регулярные выражения
jet  = re.compile('jet')

datafiles = []
consumption = []

for i in range(len(files)):  # списки названий необходимых файлов
    if (not clbr.search(files[i]) and jet.search(files[i]) and nums.search(files[i])):
        datafiles.append(files[i])

datafiles = sorted(datafiles)
print(datafiles)

fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
ax.set_title("Скорость потока воздуха в сечении затопленной струи", fontsize = 20)
ax.set_xlabel("Положение трубки Пито относительно центра струи [мм]", fontsize = 15)
ax.set_ylabel("Скорость воздуха [м/с]", fontsize = 15)
ax.minorticks_on()
ax.set_xlim([-30, 30])
ax.grid(which='both')

for i in range(len(datafiles)):
    vel = []; x = []
    measures, steps, length = read(datafiles[i])
    replace = np.argmax(measures)

    for j in range(length):
        velocity = get_velocity(measures[j])
        dist = steps / length * 0.055
        vel.append(velocity)
        x.append((j - replace) * dist)

    z = np.polyfit(x, vel, 8)
    p = np.poly1d(z)
    replace = np.argmax(p(x))
    x = []
    for j in range(length):
        x.append((j - replace) * steps / length * 0.055)

    Q = 0
    for j in range(length - 1):
        Q += 3.14 * (abs(x[j]) * vel[j] + abs(x[j + 1]) * vel[j + 1]) * dist / 1000
    consumption.append(Q)
    ax.plot(x, vel, label= "Q (" + str(10*i) + " мм) = " + str(round(Q, 2)) + " [г/с]")

with open("consumption.txt", 'w') as f:
    for item in consumption:
        f.write(str(round(item, 2)) + " ")

ax.legend(fontsize=15)
fig.savefig("velocity-outgo.png")
plt.show()
