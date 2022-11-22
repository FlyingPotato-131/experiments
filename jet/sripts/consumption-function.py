import matplotlib.pyplot as plt

with open("consumption.txt", 'r') as f:
    cons = list(map(float, f.read().split()))

fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
ax.set_title("Зависимость расхода воздуха от расстояния до сопла", fontsize = 20)
ax.set_xlabel("Расстояние от трубки Пито до сопла [мм]", fontsize = 15)
ax.set_ylabel("Расход воздуха [г/с]", fontsize = 15)
ax.minorticks_on()
ax.grid(which='both')

x = []

for i in range(len(cons)):
    x += [10*i]

ax.plot(x, cons, label = "func")

fig.savefig("consumption.png")
plt.show()