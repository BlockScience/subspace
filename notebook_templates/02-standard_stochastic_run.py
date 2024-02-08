# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: subspace
#     language: python
#     name: subspace
# ---

# %% [markdown] papermill={"duration": 0.002328, "end_time": "2024-01-31T00:36:41.081247", "exception": false, "start_time": "2024-01-31T00:36:41.078919", "status": "completed"}
# # Subspace Digital Twin, Standard Stochastic Run
#
# *Danilo Lessa Bernardineli, November 2023*

# %% [markdown] papermill={"duration": 0.002204, "end_time": "2024-01-31T00:36:41.090901", "exception": false, "start_time": "2024-01-31T00:36:41.088697", "status": "completed"}
# ## Part 1. Dependences & Set-up

# %% papermill={"duration": 1.545462, "end_time": "2024-01-31T00:36:42.637816", "exception": false, "start_time": "2024-01-31T00:36:41.092354", "status": "completed"}
import sys
sys.path.append('../')
import pandas as pd
import hvplot.pandas
import holoviews as hv
hvplot.extension('plotly')

import plotly.io as pio
pio.renderers.default = "png" # For GitHub rendering

import numpy as np

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

# %% [markdown] papermill={"duration": 0.00727, "end_time": "2024-01-31T00:36:42.647774", "exception": false, "start_time": "2024-01-31T00:36:42.640504", "status": "completed"}
# ## Part 2. Load Simulation Data

# %% papermill={"duration": 0.014345, "end_time": "2024-01-31T00:36:42.665011", "exception": false, "start_time": "2024-01-31T00:36:42.650666", "status": "completed"}
# from subspace_model.experiment import standard_stochastic_run
# sim_df = standard_stochastic_run()

# Load simulation results from terminal ran experiment
sim_df = pd.read_pickle(
    "../data/simulations/standard_stochastic_run-2024-01-02_12-04-38.pkl.gz"
)

# %% papermill={"duration": 0.018446, "end_time": "2024-01-31T00:36:42.685898", "exception": false, "start_time": "2024-01-31T00:36:42.667452", "status": "completed"}
sim_df.head()

# %% papermill={"duration": 0.008744, "end_time": "2024-01-31T00:36:42.697140", "exception": false, "start_time": "2024-01-31T00:36:42.688396", "status": "completed"}
sim_df.groupby(['run', 'label', 'environmental_label']).size().reset_index(name='Days')

# %% [markdown] papermill={"duration": 0.002495, "end_time": "2024-01-31T00:36:42.702175", "exception": false, "start_time": "2024-01-31T00:36:42.699680", "status": "completed"}
# ## Part 3. Visualizations
#
# On this section, we'll visualize some base metrics on the simulations results

# %% papermill={"duration": 0.006988, "end_time": "2024-01-31T00:36:42.711716", "exception": false, "start_time": "2024-01-31T00:36:42.704728", "status": "completed"}
runs = [run for _, run in sim_df.groupby('run')]

# %% papermill={"duration": 0.01873, "end_time": "2024-01-31T00:36:42.732944", "exception": false, "start_time": "2024-01-31T00:36:42.714214", "status": "completed"}
runs[0].head()

# %% papermill={"duration": 0.016365, "end_time": "2024-01-31T00:36:42.752171", "exception": false, "start_time": "2024-01-31T00:36:42.735806", "status": "completed"}
runs[1].head()

# %% papermill={"duration": 0.369738, "end_time": "2024-01-31T00:36:43.124985", "exception": false, "start_time": "2024-01-31T00:36:42.755247", "status": "completed"}
circulating_supply_fan_df = sim_df.groupby('days_passed')['circulating_supply'].agg(['min', 'max', 'mean'])
chart = circulating_supply_fan_df.hvplot.area(x='days_passed', y='min', y2='max', title='Circulating Supply Fan Chart', width=1200, height=500, ylabel='circulating_supply_min_max_mean') * circulating_supply_fan_df.hvplot(x='days_passed', y='mean')
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.136083, "end_time": "2024-01-31T00:36:43.267396", "exception": false, "start_time": "2024-01-31T00:36:43.131313", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='circulating_supply', by=['label', 'run'], title='Circulating Supply', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.114286, "end_time": "2024-01-31T00:36:43.386157", "exception": false, "start_time": "2024-01-31T00:36:43.271871", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='issued_supply', by=['label', 'run'], title='Issued Supply', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.117901, "end_time": "2024-01-31T00:36:43.509155", "exception": false, "start_time": "2024-01-31T00:36:43.391254", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='operator_pool_shares', by=['label', 'run'], title='Operator Pool Shares', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.114416, "end_time": "2024-01-31T00:36:43.629647", "exception": false, "start_time": "2024-01-31T00:36:43.515231", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='nominator_pool_shares', by=['label', 'run'], title='Nominator Pool Shares', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.131401, "end_time": "2024-01-31T00:36:43.768022", "exception": false, "start_time": "2024-01-31T00:36:43.636621", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='storage_fee_volume', by=['label', 'run'], title='Storage Fee Volume', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.138724, "end_time": "2024-01-31T00:36:43.914777", "exception": false, "start_time": "2024-01-31T00:36:43.776053", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='compute_fee_volume', by=['label', 'run'], title='Compute Fee Volume', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.114267, "end_time": "2024-01-31T00:36:44.038493", "exception": false, "start_time": "2024-01-31T00:36:43.924226", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='average_base_fee', by=['label', 'run'], title='Average Base Fee', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.134968, "end_time": "2024-01-31T00:36:44.184474", "exception": false, "start_time": "2024-01-31T00:36:44.049506", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='average_compute_weight_per_tx', by=['label', 'run'], title='Average Compute Weight Per Tx', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.111043, "end_time": "2024-01-31T00:36:44.326324", "exception": false, "start_time": "2024-01-31T00:36:44.215281", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='history_size', by=['label', 'run'], title='History Size', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.13704, "end_time": "2024-01-31T00:36:44.476267", "exception": false, "start_time": "2024-01-31T00:36:44.339227", "status": "completed"}
chart = sim_df.set_index(['days_passed', 'label', 'run']).space_pledged.diff().to_frame().query('days_passed > 0').hvplot.line(x='days_passed', y='space_pledged', by=['label', 'run'], title='Space Pledged', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.148937, "end_time": "2024-01-31T00:36:44.639825", "exception": false, "start_time": "2024-01-31T00:36:44.490888", "status": "completed"}
chart = sim_df.hvplot.line(x='days_passed', y='block_utilization', by=['label', 'run'], title='Block Utilization', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.06626, "end_time": "2024-01-31T00:36:44.722943", "exception": false, "start_time": "2024-01-31T00:36:44.656683", "status": "completed"}
from subspace_model.experiments.metrics import *


lst = []
for i, g_df in sim_df.set_index(['days_passed', 'label', 'run']).groupby('run'):
    s = window_volatility(g_df.circulating_supply.diff()).reset_index()
    lst.append(s)

df = pd.concat(lst).dropna()

# %% papermill={"duration": 0.192032, "end_time": "2024-01-31T00:36:44.931884", "exception": false, "start_time": "2024-01-31T00:36:44.739852", "status": "completed"}
chart = df.hvplot.line(x='days_passed', y='circulating_supply', by=['label', 'run'], title='Windowed Volatility of Circulating Supply', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))
