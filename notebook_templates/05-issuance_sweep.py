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

# %% [markdown] papermill={"duration": 0.002048, "end_time": "2024-01-31T00:36:48.951304", "exception": false, "start_time": "2024-01-31T00:36:48.949256", "status": "completed"}
# # Issuance Sweep Run Experiment
#
# *Danilo Lessa Bernardineli, Shawn Anderson November 2023*
#
# In this notebook, we run an issuance sweep run that compares two parameter sets. 

# %% [markdown] papermill={"duration": 0.002766, "end_time": "2024-01-31T00:36:48.961944", "exception": false, "start_time": "2024-01-31T00:36:48.959178", "status": "completed"}
# ## Part 1. Dependences & Set-up

# %% papermill={"duration": 1.731603, "end_time": "2024-01-31T00:36:50.695841", "exception": false, "start_time": "2024-01-31T00:36:48.964238", "status": "completed"}
import sys
sys.path.append('../')

import os

import numpy as np
import pandas as pd


import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter
import seaborn as sns

import holoviews as hv
import hvplot.pandas
hvplot.extension('plotly')

pio.renderers.default = "png" # For GitHub rendering

# %% [markdown] papermill={"duration": 0.007511, "end_time": "2024-01-31T00:36:50.705880", "exception": false, "start_time": "2024-01-31T00:36:50.698369", "status": "completed"}
# ## Part 2. Load Simulation Data

# %% papermill={"duration": 0.009916, "end_time": "2024-01-31T00:36:50.717887", "exception": false, "start_time": "2024-01-31T00:36:50.707971", "status": "completed"}
sim_df = pd.read_pickle("../data/simulations/issuance_sweep-2024-01-02_12-27-12.pkl.gz")

# %% papermill={"duration": 0.013708, "end_time": "2024-01-31T00:36:50.733654", "exception": false, "start_time": "2024-01-31T00:36:50.719946", "status": "completed"}
sim_df.head()

# %% papermill={"duration": 0.008513, "end_time": "2024-01-31T00:36:50.744446", "exception": false, "start_time": "2024-01-31T00:36:50.735933", "status": "completed"}
sim_df.groupby(['run', 'label', 'environmental_label']).size().reset_index(name='Counts')

# %% papermill={"duration": 0.007081, "end_time": "2024-01-31T00:36:50.753872", "exception": false, "start_time": "2024-01-31T00:36:50.746791", "status": "completed"}
sim_df = sim_df.set_index(['label', 'run', 'days_passed'])

# %% papermill={"duration": 0.011455, "end_time": "2024-01-31T00:36:50.767545", "exception": false, "start_time": "2024-01-31T00:36:50.756090", "status": "completed"}
sim_df['block_reward'].groupby('label').describe()

# %% papermill={"duration": 0.011478, "end_time": "2024-01-31T00:36:50.781565", "exception": false, "start_time": "2024-01-31T00:36:50.770087", "status": "completed"}
sim_df['block_utilization'].groupby('label').describe()

# %% papermill={"duration": 0.908654, "end_time": "2024-01-31T00:36:51.693605", "exception": false, "start_time": "2024-01-31T00:36:50.784951", "status": "completed"}
fig = px.line(
    sim_df,
    x=sim_df.index.get_level_values('days_passed'),
    y="circulating_supply",
    title="AB Test Circulating Supply",
    color=sim_df.index.get_level_values('label'),
    labels={
        "circulating_supply": "Circulating Supply",
        "x": "Days Passed",
        "color": "Label"
    }
)
fig.update_layout(width=1200, height=500)
fig.show()

# %% papermill={"duration": 0.07083, "end_time": "2024-01-31T00:36:51.767785", "exception": false, "start_time": "2024-01-31T00:36:51.696955", "status": "completed"}
# box plot
fig = px.box(
    sim_df,
    x=sim_df.index.get_level_values('label'),
    y="circulating_supply",)
fig.update_layout(width=1000, height=500)
fig.show()

# %% papermill={"duration": 0.554479, "end_time": "2024-01-31T00:36:52.325709", "exception": false, "start_time": "2024-01-31T00:36:51.771230", "status": "completed"}
# sns.lineplot(sim_df, x="days_passed", y="operator_pool_shares", hue="label").set(
#     title="AB Test Operator Pool Shares"
# )
fig = px.line(
    sim_df,
    x=sim_df.index.get_level_values("days_passed"),
    y="operator_pool_shares",
    title="AB Test Operator Pool Shares",
    color=sim_df.index.get_level_values("label"),
    labels={
        "operator_pool_shares": "Operator Pool Shares",
        "x": "Days Passed",
        "color": "Label",
    },
)
fig.update_layout(width=1200, height=500)
fig.show()

# %% papermill={"duration": 0.591141, "end_time": "2024-01-31T00:36:52.921124", "exception": false, "start_time": "2024-01-31T00:36:52.329983", "status": "completed"}
fig = px.line(
    sim_df,
    x=sim_df.index.get_level_values("days_passed"),
    y="nominator_pool_shares",
    title="AB Test Nominator Pool Shares",
    color=sim_df.index.get_level_values("label"),
    labels={
        "nominator_pool_shares": "Nominator Pool Shares",
        "x": "Days Passed",
        "color": "Label",
    },
)
fig.update_layout(width=1200, height=500)
fig.show()

# %% papermill={"duration": 0.045777, "end_time": "2024-01-31T00:36:52.971721", "exception": false, "start_time": "2024-01-31T00:36:52.925944", "status": "completed"}
from subspace_model.experiments.metrics import *


lst = []
for i, g_df in sim_df.groupby('run'):
    s = window_volatility(g_df.circulating_supply.diff()).reset_index()
    lst.append(s)

df = pd.concat(lst).dropna()

# %% papermill={"duration": 0.092595, "end_time": "2024-01-31T00:36:53.068983", "exception": false, "start_time": "2024-01-31T00:36:52.976388", "status": "completed"}
chart = df.hvplot.line(x='days_passed', y='circulating_supply', by=['label', 'run'], title='Windowed Volatility of Circulating Supply', width=1200, height=500)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.005014, "end_time": "2024-01-31T00:36:53.079225", "exception": false, "start_time": "2024-01-31T00:36:53.074211", "status": "completed"}
