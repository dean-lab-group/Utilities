# coding=utf-8
import numpy as np
from bokeh.plotting import figure
from scipy.integrate import odeint
#from matplotlib.pylab import *
#from mpl_toolkits.mplot3d import axes3d
#import matplotlib.pyplot as plt
#from matplotlib import cm
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Slider


sigma = 10
rho = 28
beta = 8.0 / 3
theta = 3 * np.pi / 4

def exact_solvable(xyz, t):
    x, y, z = xyz
    x_dot = 0
    y_dot = 0
    z_dot = 0

def lorenz(xyz, t):
    x, y, z = xyz
    x_dot = sigma * (y - x)
    y_dot = x * rho - x * z - y
    z_dot = x * y - beta * z
    return [x_dot, y_dot, z_dot]


initial = (-10, -7, 35)
#t = np.arange(0, 100, 0.006)
t = np.arange(0, 100, 0.005)

solution = odeint(lorenz, initial, t)

x = solution[:, 0]
y = solution[:, 1]
z = solution[:, 2]
xprime = np.cos(theta) * x - np.sin(theta) * y

print np.sum(np.sqrt(x**2 + y**2 + z**2))

# fig = figure()
# ax = axes3d.Axes3D(fig)
# ax.plot(x, y, z)
# show(fig)


colors = ["#C6DBEF", "#9ECAE1", "#6BAED6", "#4292C6", "#2171B5", "#08519C", "#08306B", ]

p = figure(title="lorenz example")
p.multi_line(np.array_split(xprime, 7), np.array_split(z, 7), line_color=colors, line_alpha=0.8, line_width=1.5)
slider = Slider(start=0, end=1000, value=100, step=.005, title="Time")

show(widgetbox(slider))
output_file("lorenz.html", title="lorenz.py example")
show(p)  # open a browser


