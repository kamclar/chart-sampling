"""
Interactive Statistical Sampling Explorer
Visualize how sample size affects statistical significance
"""

from scipy import stats
from math import sqrt
import numpy as np
from statistics import mean, stdev
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Div, Span, Legend
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.plotting import figure
from bokeh.palettes import Spectral6, Category10

# ============== CONFIGURATION ==============
COLORS = {
    'bars': ['#6C5B7B', '#C06C84', '#F67280', '#F8B195', '#355C7D'],
    'ttest': '#2ECC71',
    'mww': '#E74C3C', 
    'ranks': '#F39C12',
    'population_mean': '#1ABC9C',
    'background': '#F8F9FA',
    'error_bars': '#2C3E50'
}

# ============== DATA SETUP ==============
# Normal distribution population
mu, sigma = 2, 1
population = np.random.normal(mu, sigma, 1000)

# Initial sample size
initial_n = 5
N_array = [initial_n] * 5

# Initialize arrays
mean_array = []
sem_array = []
samples = []
x_err, y_err = [], []
x_bar, y_bar = [], []

for i in range(5):
    sampling = np.random.choice(population, N_array[i])
    samples.append(sampling)
    sample_mean = mean(sampling)
    sample_sem = stdev(sampling) / sqrt(N_array[i])
    
    mean_array.append(sample_mean)
    sem_array.append(sample_sem)
    x_bar.append(i + 1)
    y_bar.append(sample_mean)
    x_err.append([i + 1, i + 1])
    y_err.append([sample_mean - sample_sem, sample_mean + sample_sem])

# Calculate significance
def calc_significance(samples):
    signif_ttest = []
    signif_mww = []
    signif_ranks = []
    p_values = []
    
    for j in range(4):
        _, p_ttest = stats.ttest_ind(samples[j], samples[4])
        _, p_mww = stats.mannwhitneyu(samples[j], samples[4], alternative='two-sided')
        _, p_ranks = stats.ranksums(samples[j], samples[4])
        
        p_values.append({'ttest': p_ttest, 'mww': p_mww, 'ranks': p_ranks})
        
        signif_ttest.append(max(y_bar) + 0.5 if p_ttest < 0.05 else -10)
        signif_mww.append(max(y_bar) + 0.8 if p_mww < 0.05 else -10)
        signif_ranks.append(max(y_bar) + 1.1 if p_ranks < 0.05 else -10)
    
    return signif_ttest, signif_mww, signif_ranks, p_values

signif_ttest, signif_mww, signif_ranks, p_values = calc_significance(samples)

# ============== DATA SOURCES ==============
source_bars = ColumnDataSource(data=dict(
    x=x_bar, 
    y=y_bar, 
    colors=COLORS['bars']
))
source_err = ColumnDataSource(data=dict(x=x_err, y=y_err))
source_ttest = ColumnDataSource(data=dict(x=[1, 2, 3, 4], y=signif_ttest))
source_mww = ColumnDataSource(data=dict(x=[1, 2, 3, 4], y=signif_mww))
source_ranks = ColumnDataSource(data=dict(x=[1, 2, 3, 4], y=signif_ranks))

# ============== PLOT SETUP ==============
plot = figure(
    height=500, 
    width=600, 
    title="📊 Sampling from Normal Distribution (μ=2, σ=1)",
    tools="crosshair,pan,reset,save,wheel_zoom,box_zoom",
    x_range=[0.3, 5.7], 
    y_range=[-0.5, 6],
    x_axis_label="Sample Group",
    y_axis_label="Sample Mean ± SEM"
)

# Style the plot
plot.title.text_font_size = "16px"
plot.title.text_font_style = "bold"
plot.xaxis.axis_label_text_font_style = "bold"
plot.yaxis.axis_label_text_font_style = "bold"
plot.background_fill_color = "#FAFAFA"
plot.border_fill_color = "#FFFFFF"
plot.outline_line_color = "#E0E0E0"
plot.grid.grid_line_color = "#E8E8E8"
plot.grid.grid_line_alpha = 0.8

# Draw bars
bars = plot.vbar(
    x='x', 
    top='y', 
    source=source_bars, 
    width=0.6, 
    bottom=0, 
    color='colors',
    alpha=0.85,
    line_color='white',
    line_width=2
)

# Draw error bars
error_bars = plot.multi_line(
    'x', 'y', 
    source=source_err,
    line_width=3, 
    line_color=COLORS['error_bars'],
    line_cap='round'
)

# Draw significance markers
ttest_dots = plot.scatter(
    'x', 'y', 
    source=source_ttest, 
    size=15, 
    color=COLORS['ttest'], 
    alpha=0.9,
    marker='circle',
    legend_label="t-test (p<0.05)"
)

mww_dots = plot.scatter(
    'x', 'y', 
    source=source_mww, 
    size=15, 
    color=COLORS['mww'], 
    alpha=0.9,
    marker='square',
    legend_label="Mann-Whitney (p<0.05)"
)

ranks_dots = plot.scatter(
    'x', 'y', 
    source=source_ranks, 
    size=15, 
    color=COLORS['ranks'], 
    alpha=0.9,
    marker='triangle',
    legend_label="Wilcoxon (p<0.05)"
)

# Population mean line
hline = Span(
    location=mean(population), 
    dimension='width', 
    line_color=COLORS['population_mean'], 
    line_width=3,
    line_dash='dashed'
)
plot.renderers.extend([hline])

# Legend styling
plot.legend.location = "top_right"
plot.legend.background_fill_alpha = 0.8
plot.legend.border_line_color = "#CCCCCC"
plot.legend.label_text_font_size = "10px"

# ============== WIDGETS ==============
header = Div(text="""
    <h2 style="color: #2C3E50; margin: 0; font-family: Arial, sans-serif;">
        🔬 Statistical Sampling Explorer
    </h2>
    <p style="color: #7F8C8D; margin: 5px 0 15px 0; font-size: 14px;">
        Adjust sample sizes to see how they affect statistical tests.<br>
        <b>Markers appear</b> when groups 1-4 differ significantly from group 5.
    </p>
""", width=300)

sliders = []
for i in range(5):
    slider = Slider(
        title=f"🧪 Sample {i+1} size", 
        value=initial_n, 
        start=2, 
        end=100, 
        step=1,
        bar_color=COLORS['bars'][i]
    )
    sliders.append(slider)

info_div = Div(text="""
    <div style="background: #EBF5FB; padding: 10px; border-radius: 8px; margin-top: 15px; font-size: 12px;">
        <b>📈 Legend:</b><br>
        <span style="color: #1ABC9C;">━━</span> Population mean (μ=2)<br>
        <span style="color: #2C3E50;">┃</span> Error bars (±SEM)<br><br>
        <b>🎯 Significance (vs Sample 5):</b><br>
        <span style="color: #2ECC71;">●</span> t-test<br>
        <span style="color: #E74C3C;">■</span> Mann-Whitney U<br>
        <span style="color: #F39C12;">▲</span> Wilcoxon rank-sum
    </div>
""", width=300)

# ============== CALLBACKS ==============
def update_data(attrname, old, new):
    global samples, mean_array, sem_array, x_bar, y_bar, x_err, y_err
    
    for i in range(5):
        if N_array[i] != sliders[i].value:
            N_array[i] = sliders[i].value
            sampling = np.random.choice(population, N_array[i])
            samples[i] = sampling
            
            sample_mean = mean(sampling)
            sample_sem = stdev(sampling) / sqrt(N_array[i])
            
            mean_array[i] = sample_mean
            sem_array[i] = sample_sem
            x_bar[i] = i + 1
            y_bar[i] = sample_mean
            x_err[i] = [i + 1, i + 1]
            y_err[i] = [sample_mean - sample_sem, sample_mean + sample_sem]
    
    # Recalculate significance
    signif_ttest, signif_mww, signif_ranks, _ = calc_significance(samples)
    
    # Update all sources
    source_bars.data = dict(x=x_bar, y=y_bar, colors=COLORS['bars'])
    source_err.data = dict(x=x_err, y=y_err)
    source_ttest.data = dict(x=[1, 2, 3, 4], y=signif_ttest)
    source_mww.data = dict(x=[1, 2, 3, 4], y=signif_mww)
    source_ranks.data = dict(x=[1, 2, 3, 4], y=signif_ranks)

for slider in sliders:
    slider.on_change('value', update_data)

# ============== LAYOUT ==============
controls = column(
    header,
    *sliders,
    info_div,
    width=320
)

layout = row(controls, plot, sizing_mode="fixed")

curdoc().clear()
curdoc().add_root(layout)
curdoc().title = " Statistical Sampling Explorer"
