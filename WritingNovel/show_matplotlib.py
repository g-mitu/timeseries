import matplotlib.pyplot as plt
import numpy as np  # 导入包

t1 = np.arange(0.0, 4.0, 0.1)
t2 = np.arange(0.0, 4.0, 0.05)  # 准备一些数据

fig = plt.figure()  # 准备好这张纸，并把句柄传给fig
ax1 = fig.add_subplot(211)  # 使用句柄fig添加一个子图
line1, = plt.plot(t1, np.sin(2 * np.pi * t1), '--*')  # 绘图，将句柄返给line1
plt.title('sine function demo')
plt.xlabel('time(s)')
plt.ylabel('votage(mV)')
plt.xlim([0.0, 5.0])
plt.ylim([-1.2, 1.2])
plt.grid('on')

plt.setp(line1, lw=2, c='g')  # 通过setp函数，设置句柄为line1的线的属性，c是color的简写
line1.set_antialiased(False)  # 通过line1句柄的set_*属性设置line1的属性
plt.text(4, 0, '$\mu=100,\\sigma=15$')  # 添加text，注意，它能接受LaTeX哟！

ax2 = fig.add_subplot(212)
plt.plot(t2, np.exp(-t2), ':r')

plt.plot(t2, np.cos(2 * np.pi * t2), '--b')

plt.xlabel('time')
plt.ylabel('amplitude')
plt.show()

## sample 2
"""
==================
ggplot style sheet
==================

This example demonstrates the "ggplot" style, which adjusts the style to
emulate ggplot_ (a popular plotting package for R_).

These settings were shamelessly stolen from [1]_ (with permission).

.. [1] http://www.huyng.com/posts/sane-color-scheme-for-matplotlib/

.. _ggplot: http://ggplot2.org/
.. _R: https://www.r-project.org/

"""
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

fig, axes = plt.subplots(ncols=2, nrows=2)
ax1, ax2, ax3, ax4 = axes.ravel()

# scatter plot (Note: `plt.scatter` doesn't use default colors)
x, y = np.random.normal(size=(2, 200))
ax1.plot(x, y, 'o')

# sinusoidal lines with colors from default color cycle
L = 2*np.pi
x = np.linspace(0, L)
ncolors = len(plt.rcParams['axes.prop_cycle'])
shift = np.linspace(0, L, ncolors, endpoint=False)
for s in shift:
    ax2.plot(x, np.sin(x + s), '-')
ax2.margins(0)

# bar graphs
x = np.arange(5)
y1, y2 = np.random.randint(1, 25, size=(2, 5))
width = 0.25
ax3.bar(x, y1, width)
ax3.bar(x + width, y2, width,
        color=list(plt.rcParams['axes.prop_cycle'])[2]['color'])
ax3.set_xticks(x + width)
ax3.set_xticklabels(['a', 'b', 'c', 'd', 'e'])

# circles with colors from default color cycle
for i, color in enumerate(plt.rcParams['axes.prop_cycle']):
    xy = np.random.normal(size=2)
    ax4.add_patch(plt.Circle(xy, radius=0.3, color=color['color']))
ax4.axis('equal')
ax4.margins(0)

plt.show()