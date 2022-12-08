
import numpy as np
import matplotlib.pyplot as plt


u1 = 0.99 * 28.97 + 0.01 * 18.01
u2 = 0.94 * 28.97 + 0.01 * 18.01 + 0.05 * 44.01
print(u1, u2)

x = [0, 5]
y = [(1000*1.399620225025242*8.31*295.75/u1)**0.5, (1000*1.3922728425900492*8.31*295.75/u2)**0.5]
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
#ax.scatter(x, y, label = "измерения")
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax.plot(x, p(x), label = "k = " + str(f'{(p.coef[0]/100):.1e}') + " * C [м/c]", color = "orange")

ax.set_title("Зависимость скорости звука от концентрации углекислого газа", fontsize = 20)
ax.set_ylabel("Скорость звука [м/с]", fontsize = 15)
ax.set_xlabel("Концентрация СО2 [%]", fontsize = 15)
ax.minorticks_on()
ax.grid(which='both')

ax.legend(fontsize=15)
fig.savefig("distance-calibration.png")

plt.show()