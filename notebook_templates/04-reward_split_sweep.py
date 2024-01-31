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

# %% [markdown] papermill={"duration": 0.002357, "end_time": "2024-01-31T00:36:57.336348", "exception": false, "start_time": "2024-01-31T00:36:57.333991", "status": "completed"}
# # Escrow Inclusion Sweep Run Experiment
#
# *Danilo Lessa Bernardineli, Shawn Anderson November 2023*
#
# In this notebook, we run an escrow inclusion sweep run that compares two parameter sets. 

# %% [markdown] papermill={"duration": 0.001519, "end_time": "2024-01-31T00:36:57.345118", "exception": false, "start_time": "2024-01-31T00:36:57.343599", "status": "completed"}
# ## Part 1. Dependences & Set-up

# %% papermill={"duration": 0.700512, "end_time": "2024-01-31T00:36:58.047376", "exception": false, "start_time": "2024-01-31T00:36:57.346864", "status": "completed"}
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

pio.renderers.default = "png" # For GitHub rendering

# %% [markdown] papermill={"duration": 0.007544, "end_time": "2024-01-31T00:36:58.056190", "exception": false, "start_time": "2024-01-31T00:36:58.048646", "status": "completed"}
# ## Part 2. Load Simulation Data

# %% papermill={"duration": 0.010236, "end_time": "2024-01-31T00:36:58.067839", "exception": false, "start_time": "2024-01-31T00:36:58.057603", "status": "completed"}
sim_df = pd.read_pickle(
    "../data/simulations/reward_split_sweep-2024-01-02_10-17-33.pkl.gz"
)

# %% papermill={"duration": 0.014895, "end_time": "2024-01-31T00:36:58.084163", "exception": false, "start_time": "2024-01-31T00:36:58.069268", "status": "completed"}
sim_df.head()

# %% papermill={"duration": 0.007347, "end_time": "2024-01-31T00:36:58.092708", "exception": false, "start_time": "2024-01-31T00:36:58.085361", "status": "completed"}
sim_df.groupby(['run', 'label', 'environmental_label']).size().reset_index(name='Counts')

# %% [markdown] papermill={"duration": 0.001149, "end_time": "2024-01-31T00:36:58.095061", "exception": false, "start_time": "2024-01-31T00:36:58.093912", "status": "completed"}
# ## Part 3. Visualizations
#
# On this section, we'll visualize some base metrics on the simulations results

# %% papermill={"duration": 0.005577, "end_time": "2024-01-31T00:36:58.101758", "exception": false, "start_time": "2024-01-31T00:36:58.096181", "status": "completed"}
sim_df = sim_df.set_index(['label', 'run', 'days_passed'])

# %% papermill={"duration": 0.087739, "end_time": "2024-01-31T00:36:58.190985", "exception": false, "start_time": "2024-01-31T00:36:58.103246", "status": "completed"}
sns.lineplot(sim_df, x='days_passed', y='circulating_supply', hue='label')

# %% papermill={"duration": 0.086972, "end_time": "2024-01-31T00:36:58.279698", "exception": false, "start_time": "2024-01-31T00:36:58.192726", "status": "completed"}
sns.lineplot(sim_df, x='days_passed', y='operator_pool_shares', hue='label')

# %% papermill={"duration": 0.084971, "end_time": "2024-01-31T00:36:58.366778", "exception": false, "start_time": "2024-01-31T00:36:58.281807", "status": "completed"}
sns.lineplot(sim_df, x='days_passed', y='nominator_pool_shares', hue='label')

# %% papermill={"duration": 0.091186, "end_time": "2024-01-31T00:36:58.461250", "exception": false, "start_time": "2024-01-31T00:36:58.370064", "status": "completed"}
sns.lineplot(sim_df, x='days_passed', y='block_utilization', hue='label')

# %% papermill={"duration": 0.085981, "end_time": "2024-01-31T00:36:58.550837", "exception": false, "start_time": "2024-01-31T00:36:58.464856", "status": "completed"}
from subspace_model.experiments.metrics import *


lst = []
for i, g_df in sim_df.groupby('run'):
    s = window_volatility(g_df.circulating_supply.diff()).reset_index()
    lst.append(s)

df = pd.concat(lst).dropna()
sns.lineplot(df, x='days_passed', y='circulating_supply', hue='label')

# %% papermill={"duration": 0.002904, "end_time": "2024-01-31T00:36:58.556684", "exception": false, "start_time": "2024-01-31T00:36:58.553780", "status": "completed"}
