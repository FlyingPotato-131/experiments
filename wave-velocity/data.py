import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d as interp
from numpy.polynomial import Polynomial as poly
#from numpy.polynomial import polynomial as P
from math import log

def read(filename): #считать данные из файла
    with open(filename) as f:
        lines = f.readlines()

    duration = float(lines[2].split()[2])
    samples = np.asarray(lines[4:], dtype=int)
    
    return samples, duration, len(samples)

files = os.listdir(".")

clbr = re.compile('test')
nums = re.compile('\d+')
wave = re.compile('wave') #регулярные выражения

calfiles = []
datafiles = []

for i in range(len(files)): #списки названий необходимых файлов
    if(not clbr.search(files[i]) and nums.search(files[i]) and wave.search(files[i])):
        calfiles.append(files[i])
    elif(nums.search(files[i]) and wave.search(files[i])):
        datafiles.append(files[i])

calpoints = [[int(nums.search(calfiles[i]).group()) for i in range(len(calfiles))], [np.average(read(calfiles[i])[0]) for i in range(len(calfiles))]]

Vh = interp(calpoints[0], calpoints[1], kind="cubic") #интерполяция данных
h = np.linspace(20, 120, num=100, endpoint=True)

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
ax.plot(h, 2.4/(0.017+0.465/h), "g-", label = "Оценка теоретической зависимости") #теоретическая зависимость
ax.legend()
plt.savefig("clbr-graph.svg") #график калибровки

raw = [read(i) for i in datafiles]
data = [raw[i][0] for i in range(len(raw))]
time = [raw[i][1] for i in range(len(raw))]
length = [raw[i][2] for i in range(len(raw))]

velocity = []
height = []

for i in range(len(data) - 0):
    Vt2 = poly.fit(np.linspace(0, length[i], num = length[i]), data[i], 100) #полиномиальная оценка зависимости глубины от времени
    t  = np.linspace(0, length[i], num = 1000, endpoint = True)

    height.append(float(nums.search(datafiles[i]).group()))
    
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
    ax.plot(t, Vt2(t), "g-")
    
    deriv = Vt2.deriv(1)
    tau = 0
    delta = 0
    
    for num in range(length[i]): # нахождение первого промежутка малой по модулю производной
        if abs(deriv(num)) < 0.01:
            delta += 1
        if abs(deriv(num)) > 0.01 and delta <= 5:
            delta = 0
        if abs(deriv(num)) > 0.01 and delta > 5:
            tau = num
            break

    for num in range(length[i] - 10): # нахождение точки начала волны
        if abs(Vt2(num + 10) - Vt2(tau)) > 1:
            tau = num
            break

    velocity.append(0.143 * length[i] / tau)
    ax.plot(np.linspace(tau, tau, num = 10), np.linspace(min(data[i]), max(data[i]), num = 10), "--")

    plt.savefig("depth-graph-{}mm.svg".format(height[i])) # построение графика

lnheight = []
lnvelocity = []

fig, ax = plt.subplots()

for i in range(4):
    lnheight.append(log(height[i]))
    lnvelocity.append(log(velocity[i]))

line = poly.fit(lnheight[:3], lnvelocity[:3], 1)
t = np.linspace(min(lnheight), max(lnheight), num = 2, endpoint = True)

k = line(1) - line(0)

with open("coeff.txt", "w") as out:
    out.write(str(k))

plt.ylabel("Скорость")
plt.xlabel("Глубина")
plt.title("Логарифмическая зависимость скорости от глубины")

ax.plot(lnheight[:3], lnvelocity[:3], "o")
ax.plot(t, line(t))

plt.savefig("log-vel-height.svg") # построение логарифмической зависимости скорости от глубины
