# coding=utf-8
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider
from bokeh.plotting import figure

from scipy.integrate import odeint

# Constants
sigma = 10
rho = 28
beta = 8.0 / 3
theta = 3 * np.pi / 4
initial = (-10, -7, 35)
colors = ["#C6DBEF", "#9ECAE1", "#6BAED6", "#4292C6", "#2171B5", "#08519C", "#08306B", ]


def lorenz(xyz, t):
    x, y, z = xyz
    x_dot = sigma * (y - x)
    y_dot = x * rho - x * z - y
    z_dot = x * y - beta * z
    return [x_dot, y_dot, z_dot]


def update_data(attrname, old, new):
    # Get the current slider values
    t = np.arange(0, time.value, 0.005)
    print "updating", attrname, old, new, np.max(t)
    # Generate the new curve
    x, y, z, xprime = solve_lorenz(lorenz, initial, t)
    source.data = dict(x=x, y=y, z=z, xprime=xprime)


def solve_lorenz(lorenz, initial_cond, t):
    solution = odeint(lorenz, initial, t)
    x = solution[:, 0]
    y = solution[:, 1]
    z = solution[:, 2]
    xprime = np.cos(theta) * x - np.sin(theta) * y
    return x, y, z, xprime


# Set up data
t = np.arange(0, 100, 0.005)
x, y, z, xprime = solve_lorenz(lorenz, initial, t)
source = ColumnDataSource(data=dict(z=z, xprime=xprime))

# Plot
p = figure(title="Lorenz Interactive Plot")
p.multi_line('xprime','z',source=source, line_width=1.5, line_alpha=0.8, line_color=colors)
#p.multi_line(np.array_split(xprime, 7), np.array_split(z, 7), line_color=colors, line_alpha=0.8, line_width=1.5)

# Widgets
time = Slider(start=0, end=1000, value=100, step=.005, title="Time")

# Callbacks
time.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(time)

curdoc().add_root(row(inputs, p, width=800))
curdoc().title = "Interactive Chaos Plot"
