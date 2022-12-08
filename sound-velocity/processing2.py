from matplotlib import pyplot as plt
import numpy
from textwrap import wrap
import matplotlib.ticker as ticker

def fun_graz(v2): # для выдыхаемого воздуха, все аналогично
    r=8.31446
    t=298.15

    x_noa=0.99964
    m_noa=0.02897
    c_p_noa=1.0036
    c_v_noa=0.7166

    m_y=0.04401
    c_p_y=0.838
    c_v_y=0.649

    m_h=0.01801
    c_p_h=1.863
    c_v_h=1.403

    n=1-(1*3170)/(101375)
    k1=n*(m_y-m_noa)*c_p_y
    k2=n*(m_y-m_noa)*c_v_y
    k3=n*(m_y-m_noa)
    a=x_noa*n*m_noa*c_p_noa + (1-n)*m_h*c_p_h
    b=x_noa*n*m_noa*c_v_noa + (1-n)*m_h*c_v_h
    c=x_noa*n*m_noa + (1-n)*m_h

    # print(n)
    # print(a, b, c)

    e1=v2*k2*k3
    e2=v2*(k2*c+k3*b)-k1*r*t
    e3=v2*b*c-a*r*t
    # print(e1, e2, e3)

    d = e2 ** 2 - 4 * e1 * e3
    x = (-e2 + d ** 0.5) / (2 * e1)
    if x>=0.035 and x<=0.045:
        print(x)
        print(v2**0.5)
    return x

x1 = fun_graz(339.79)
x2 = fun_graz(343.01)
print (x1, x2)

#график чистого воздуха
mas_x_chis=[i/10 for i in range(3350, 3469)]

#график грязного воздуха
mas_x_graz=[i/10 for i in range(3430, 3481)]
mas_y_graz=[fun_graz(i**2) for i in mas_x_graz]


fig, ax=plt.subplots()
ax.grid(which='major', color = 'k')
ax.minorticks_on()
ax.grid(which='minor', color = 'gray', linestyle = ':')
# ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
# #  Устанавливаем интервал вспомогательных делений:
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.4))
#
# #  Тоже самое проделываем с делениями на оси "y":
# ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))


ax.plot([i*100 for i in mas_y_graz], mas_x_graz, label = 'выдыхаемый')
#установка двух точек, найденных по найденной скорости и концентрации,
#полученной подстановкой этой скорости в уравнение
ax.scatter(0.0009130754671489064*100, 339.79, c='purple')
ax.scatter(0.040463144573048414*100, 343.01, c='red')

ax.legend(shadow = False, loc = 'right', fontsize = 10)
ax.set_xlabel("содержание углекислого газа, %")
ax.set_ylabel("скорость звука, м/с")
plt.show()