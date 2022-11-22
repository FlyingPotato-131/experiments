import numpy as np
import matplotlib.pyplot as plt

def read(filename):
    with open(filename) as f:
        lines = f.readlines()

    steps = int(lines[2].split()[2])
    measures = np.asarray(lines[4:], dtype=int)

    return measures, steps, len(measures)


measures, steps, length = read("jet-data-cal-motor-2022-11-17-17.30.39.txt")
dist = measures[2]


x = [0, steps]
y = [0, dist/10]
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
ax.scatter(x, y, label = "измерения")
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax.plot(x, p(x), label = "X = " + str(f'{(p.coef[0]/100):.1e}') + " * step [м]", color = "orange")

ax.set_title("Калибровочный график зависимости перемещения трубки Пито от шага двигателя", fontsize = 20)
ax.set_xlabel("Количетво шагов", fontsize = 15)
ax.set_ylabel("Перемещение трубки Пито [см]", fontsize = 15)
ax.minorticks_on()
ax.grid(which='both')

ax.legend(fontsize=15)
fig.savefig("distance-calibration.png")

plt.show()