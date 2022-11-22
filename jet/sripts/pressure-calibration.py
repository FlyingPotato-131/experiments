import numpy as np
import matplotlib.pyplot as plt

def read(filename):
    with open(filename) as f:
        lines = f.readlines()

    steps = int(lines[2].split()[2])
    measures = np.asarray(lines[4:], dtype=int)

    return measures, steps, len(measures)


measures, steps, length = read("jet-data-cal-pressure-2022-11-17-17.54.33.txt")
p0 = np.mean(measures)

measures, steps, length = read("jet-data-cal-pressure-2022-11-17-17.58.58.txt")
p65 = np.mean(measures)


x = [0, 65]
y = [p0, p65]
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
ax.scatter(x, y, label = "измерения")
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax.plot(x, p(x), label = "P = " + str(round((1/p.coef[0]), 3)) + "*N - " + str(round((p.coef[1]/p.coef[0]), 2)) + " [Па]", color = 'green')

ax.set_title("Калибровочный график зависимости показаний АЦП от давления", fontsize = 20)
ax.set_xlabel("Давление [Па]", fontsize = 15)
ax.set_ylabel("Отсчёта АЦП", fontsize = 15)
ax.minorticks_on()
ax.grid(which='both')

ax.legend(fontsize=15)
fig.savefig("pressure-calibration.png")

plt.show()