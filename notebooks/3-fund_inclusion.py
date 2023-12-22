# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
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

# %% [markdown]
# # Escrow Inclusion Sweep Run Experiment
#
# *Danilo Lessa Bernardineli, Shawn Anderson November 2023*
#
# In this notebook, we run an escrow inclusion sweep run that compares two parameter sets. 
#
#
# ## Part 1. Running the Simulation

# %%
sim_df = pd.read_pickle(
    "../data/simulations/fund_inclusion-2023-12-21_21-35-29.pkl.gz"
)

# %%
sim_df.head()

# %%
sns.lineplot(sim_df, x='days_passed', y='circulating_supply', hue='label').set(title='AB Test Circulating Supply')

# %%
sns.lineplot(sim_df, x='days_passed', y='operator_pool_shares', hue='label').set(title='AB Test Operator Pool Shares')

# %%
sns.lineplot(sim_df, x='days_passed', y='nominator_pool_shares', hue='label').set(title='AB Test Nominator Pool Shares')

# %%
sns.lineplot(sim_df, x='days_passed', y='block_utilization', hue='label').set(title='AB Test Block Utilization')

# %%
from subspace_model.trajectory_metrics import *


lst = []
for i, g_df in sim_df.set_index(['label', 'run', 'days_passed']).groupby('run'):
    s = window_volatility(g_df.circulating_supply.diff()).reset_index()
    lst.append(s)

df = pd.concat(lst).dropna()
sns.lineplot(df, x='days_passed', y='circulating_supply', hue='label').set(title='AB Test Windowed Volatility of Circulating Supply')
