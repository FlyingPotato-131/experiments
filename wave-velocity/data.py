import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d as interp
from numpy.polynomial import Polynomial as poly
#from numpy.polynomial import polynomial as P
from math import log

def read(filename):
    with open(filename) as f:
        lines = f.readlines()

    duration = float(lines[2].split()[2])
    samples = np.asarray(lines[4:], dtype=int)
    
    return samples, duration, len(samples)

files = os.listdir(".")

clbr = re.compile('test')
nums = re.compile('\d+')
wave = re.compile('wave')

calfiles = []
datafiles = []

for i in range(len(files)):
    if(not clbr.search(files[i]) and nums.search(files[i]) and wave.search(files[i])):
        calfiles.append(files[i])
    elif(nums.search(files[i]) and wave.search(files[i])):
        datafiles.append(files[i])

calpoints = [[int(nums.search(calfiles[i]).group()) for i in range(len(calfiles))], [np.average(read(calfiles[i])[0]) for i in range(len(calfiles))]]

#print(calpoints)

#plt.plot(calpoints[0], calpoints[1])

#plt.plot(np.asarray(calpoints[0]), np.asarray(calpoints[1]))

Vh = interp(calpoints[0], calpoints[1], kind="cubic")
#Vh = poly.fit(calpoints[0], calpoints[1], 100)
h = np.linspace(20, 120, num=100, endpoint=True)

#print(Vh)

fig, ax = plt.subplots()

plt.yticks(np.arange(0, 255, step=10))
plt.ylabel("Значение на АЦП, число [0, 255]")

plt.xticks(np.arange(0, 130, step=10))
plt.xlabel("Уровень воды, мм")

plt.minorticks_on()
plt.grid(True, "major", "both", color = "#888888")
plt.grid(True, "minor", "both", linestyle = '--')
plt.title("Зависимость значения на АЦП от уровня воды")

ax.plot(calpoints[0], calpoints[1], "ro", label = "Измерения") 
ax.plot(h, Vh(h), "-", label = "Интерполяция")
ax.plot(h, 2.4/(0.017+0.465/h), "g-", label = "Оценка теоретической зависимости")
ax.legend()
#plt.show()
plt.savefig("clbr-graph.svg")

raw = [read(i) for i in datafiles]
data = [raw[i][0] for i in range(len(raw))]
time = [raw[i][1] for i in range(len(raw))]
length = [raw[i][2] for i in range(len(raw))]

velocity = []
height = []
#print(time)

for i in range(len(data) - 0):
    Vt = interp(np.linspace(0, length[i], num = length[i]), data[i], kind = "cubic")
    Vt2 = poly.fit(np.linspace(0, length[i], num = length[i]), data[i], 100)
    t  = np.linspace(0, length[i], num = 1000, endpoint = True)

    height.append(float(nums.search(datafiles[i]).group()))

#    zero = 0

#    for f in calfiles:
#        if nums.search(f).group() == nums.search(datafiles[i]).group():
#            zero = np.average(read(f)[0])
#    print(zero)

#    print(Vt2)
    
    fig, ax = plt.subplots()

    plt.yticks(np.arange(0, 255, step=10))
    plt.ylabel("Значение на АЦП, число [0, 255]")

    plt.xticks(np.arange(0, length[i], step = length[i] / time[i] * 2), np.arange(0, time[i], step = 2))
    plt.xlabel("Время, с")

    plt.title("Глубина от времени, {} мм".format(height[i]))

    plt.minorticks_on()
    plt.grid(True, "major", "both", color = "#888888")
    plt.grid(True, "minor", "both", linestyle = '--')
    
    ax.plot(data[i], "r.")
#    ax.plot(t, Vt(t), "-")
    ax.plot(t, Vt2(t), "g-")
#    ax.plot()

#    fig, ax = plt.subplots()

#    plt.ylabel("Производная")

#    plt.xticks(np.arange(0, length[i], step = length[i] / time[i] * 2), np.arange(0, time[i], step = 2))
#    plt.xlabel("Время, с")

#    plt.minorticks_on()
#    plt.grid(True, "major", "both", color = "#888888")
#    plt.grid(True, "minor", "both", linestyle = '--')
    
    deriv = Vt2.deriv(1)
    tau = 0
    delta = 0
    
    for num in range(length[i]):
        if abs(deriv(num)) < 0.01:
            delta += 1
        if abs(deriv(num)) > 0.01 and delta <= 5:
            delta = 0
        if abs(deriv(num)) > 0.01 and delta > 5:
            tau = num
            break

    for num in range(length[i] - 10):
        if abs(Vt2(num + 10) - Vt2(tau)) > 1:
            tau = num
            break

#    print(10 * tau / length[i])
    velocity.append(0.143 * length[i] / tau)
    ax.plot(np.linspace(tau, tau, num = 10), np.linspace(min(data[i]), max(data[i]), num = 10), "--")

    plt.savefig("depth-graph-{}mm.svg".format(height[i]))
#    ax.plot(t, deriv(t))

#print(height)
#print(velocity)

lnheight = []
lnvelocity = []

fig, ax = plt.subplots()
#ax.plot(height[0:3], velocity[0:3], "o")
for i in range(4):
    lnheight.append(log(height[i]))
    lnvelocity.append(log(velocity[i]))

line = poly.fit(lnheight[:3], lnvelocity[:3], 1)
t = np.linspace(min(lnheight), max(lnheight), num = 2, endpoint = True)

k = line(1) - line(0)

with open("coeff.txt", "w") as out:
    out.write(str(k))
#print(k)

#plt.yticks(np.arange(min(lnvelocity), max(lnvelocity), step = (max(lnvelocity) - min(lnvelocity)) / 10))
plt.ylabel("Скорость")
#plt.xticks(np.arange(min(lnheight), max(lnheight), step = (max(lnheight) - min(lnheight)) / 10))
plt.xlabel("Глубина")
plt.title("Логарифмическая зависимость скорости от глубины")

ax.plot(lnheight[:3], lnvelocity[:3], "o")
ax.plot(t, line(t))

plt.savefig("log-vel-height.svg")
#print(velocity)
#plt.show()

#print(calfiles)
#print(datafiles)

#print(calpoints)
