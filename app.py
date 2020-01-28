from flask import Flask, render_template
''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''

from scipy import stats
from math import sqrt
import numpy as np
from statistics import mean, stdev
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from bokeh.models import Span


# Set up data
global s



# normal distribution
mu, sigma = 2, 1 # mean and standard deviation
s = np.random.normal(mu, sigma, 1000)

n = 2

N_array = []
for i in range(5):
    N_array.append(n)

mean_array = []
sem_array = []
samples = []
x, y = [], []
x_bar, y_bar = [], []
t_tests = []
for i in range(5):
    sampling = np.random.choice(s, N_array[i])
    samples.append(sampling)
    mean_array.append(mean(sampling))
    sem_array.append(stdev(sampling)/sqrt(N_array[i]))
    x_bar.append(i+1)
    y_bar.append(mean_array[i])
    x.append([i + 1, i + 1])
    y.append([mean_array[i], mean_array[i] + sem_array[i]])

signif = []
signif_mww = []
for i in range(4):
    _, res = stats.ttest_ind(samples[i], samples[4])
    _, res_mww = stats.mannwhitneyu(samples[i], samples[4])
    t_tests.append(res)
    if res < 0.05:
        signif.append(3.5)
    else:
        signif.append(-1)
    if res_mww < 0.05:
        signif_mww.append(4.5)
    else:
        signif_mww.append(-1)


source = ColumnDataSource(data=dict(x=x, y=y))
source_bars = ColumnDataSource(data=dict(x=x_bar, y=y_bar))
source_signif = ColumnDataSource(data=dict(x=[1, 2, 3, 4], y=signif))
source_signif_mww = ColumnDataSource(data=dict(x=[1, 2, 3, 4], y=signif_mww))
print(x)
print(y)


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="Sampling from one population with normal distribution",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 6], y_range=[0, max(s)])

# plots
plot.multi_line('x', 'y', source=source,
               line_dash='solid', line_width=2, line_color='black')
plot.vbar(x='x', top='y', source=source_bars, width=0.5, bottom=0, color="#CAB2D6")
plot.circle('x', 'y', source=source_signif, size=10, color='navy', alpha=0.5)
plot.circle('x', 'y', source=source_signif_mww, size=10, color='red', alpha=0.5)
hline = Span(location=mean(s), dimension='width', line_color='black', line_width=1)

plot.renderers.extend([hline])


# Set up widgets
text = TextInput(title="title", value='number of samples')
no_samples = []
for i in range(5):
    no_samples.append(Slider(title="measurements " + str(i+1), value=3, start=2, end=100, step=1))

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):
    global s
    # Get the current slider values
    for i in range(5):
        if N_array[i] != no_samples[i].value:
            sampling = np.random.choice(s, no_samples[i].value)
            samples[i] = sampling
            mean_array[i] = (mean(sampling))
            sem_array[i] = (stdev(sampling)/sqrt(N_array[i]))
            N_array[i] = no_samples[i].value

            x[i] = ([i + 1, i + 1])
            y[i] = ([mean_array[i], mean_array[i] + sem_array[i]])
            x_bar[i] = (i + 1)
            y_bar[i] = (mean_array[i])

            if i < 4:
                _, res = stats.ttest_ind(samples[i], samples[4])
                _, res_mww = stats.mannwhitneyu(samples[i], samples[4])
                t_tests[i] = res
                if res < 0.05:
                    signif[i] = 3.5
                else:
                    signif[i] = -1
                if res_mww < 0.05:
                    signif_mww[i] = 4.5
                    print(res_mww)
                else:
                    signif_mww[i] = -1

            source.data = dict(x=x, y=y)
            source_bars.data = dict(x=x_bar, y=y_bar)
            source_signif.data = dict(x=[1, 2, 3, 4], y=signif)
            source_signif_mww.data = dict(x=[1, 2, 3, 4], y=signif_mww)


for w in no_samples:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, no_samples[0], no_samples[1], no_samples[2], no_samples[3], no_samples[4])

curdoc().clear()
curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Random Sampling"
