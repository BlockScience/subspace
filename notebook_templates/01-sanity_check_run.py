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

# %% [markdown] papermill={"duration": 0.003544, "end_time": "2024-01-31T00:36:28.997437", "exception": false, "start_time": "2024-01-31T00:36:28.993893", "status": "completed"}
# # Subspace Digital Twin, Sanity Checking Run
#
# *Danilo Lessa Bernardineli, November 2023*
#
# On this notebook, we do an sanity checking run (which is a single run) so that basic metrics and KPIs
# for the simulation are computed.
#
# ## Part 1. Dependences & Set-up

# %% [markdown] papermill={"duration": 0.002039, "end_time": "2024-01-31T00:36:29.001806", "exception": false, "start_time": "2024-01-31T00:36:28.999767", "status": "completed"}
# Autoreload modules while developing.

# %% papermill={"duration": 0.011406, "end_time": "2024-01-31T00:36:29.015209", "exception": false, "start_time": "2024-01-31T00:36:29.003803", "status": "completed"}
# %load_ext autoreload
# %autoreload 2

# %% papermill={"duration": 1.676402, "end_time": "2024-01-31T00:36:30.694002", "exception": false, "start_time": "2024-01-31T00:36:29.017600", "status": "completed"}
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
import panel as pn
import seaborn as sns
import hvplot.pandas
import holoviews as hv
hvplot.extension('plotly')
hv.extension('plotly')

import warnings
warnings.filterwarnings('ignore')

pio.renderers.default = "png" # For GitHub rendering

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

# %% [markdown] papermill={"duration": 0.003715, "end_time": "2024-01-31T00:36:30.701474", "exception": false, "start_time": "2024-01-31T00:36:30.697759", "status": "completed"}
# ## Part 2. Load Simulation Data

# %% papermill={"duration": 0.017591, "end_time": "2024-01-31T00:36:30.722648", "exception": false, "start_time": "2024-01-31T00:36:30.705057", "status": "completed"}
sim_df = pd.read_pickle(
    "../data/simulations/sanity_check_run-2024-01-02_10-16-07.pkl.gz"
)

# %% papermill={"duration": 0.031944, "end_time": "2024-01-31T00:36:30.758318", "exception": false, "start_time": "2024-01-31T00:36:30.726374", "status": "completed"}
sim_df.head(5)

# %% papermill={"duration": 0.019862, "end_time": "2024-01-31T00:36:30.782102", "exception": false, "start_time": "2024-01-31T00:36:30.762240", "status": "completed"}
sim_df.groupby(['run', 'label', 'environmental_label']).size().reset_index(name='Days')

# %% [markdown] papermill={"duration": 0.004726, "end_time": "2024-01-31T00:36:30.790621", "exception": false, "start_time": "2024-01-31T00:36:30.785895", "status": "completed"}
# ## Part 3. Visualizations
#
# On this section, we'll visualize some base metrics on the simulations results

# %% papermill={"duration": 0.035954, "end_time": "2024-01-31T00:36:30.830540", "exception": false, "start_time": "2024-01-31T00:36:30.794586", "status": "completed"}
from subspace_model.experiments.charts import ssc_metrics, aggregate_staking_pool_share_composition, ssc_stock_composition, total_fee_volume_per_day, environmental_processes, blockchain_size, block_utilization
from subspace_model.util import g, get_hex_colors_from_matplotlib_cmap

# %% papermill={"duration": 0.43764, "end_time": "2024-01-31T00:36:31.272097", "exception": false, "start_time": "2024-01-31T00:36:30.834457", "status": "completed"}
ssc_metrics_chart = ssc_metrics(sim_df, experiment='sanity-check')
g(ssc_metrics_chart)

# %% papermill={"duration": 0.092613, "end_time": "2024-01-31T00:36:31.369135", "exception": false, "start_time": "2024-01-31T00:36:31.276522", "status": "completed"}
aggregate_staking_pool_share_composition_chart = aggregate_staking_pool_share_composition(sim_df, experiment='sanity-check')
g(aggregate_staking_pool_share_composition_chart)

# %% papermill={"duration": 0.266346, "end_time": "2024-01-31T00:36:31.640514", "exception": false, "start_time": "2024-01-31T00:36:31.374168", "status": "completed"}
ssc_stock_composition_chart = ssc_stock_composition(sim_df, experiment='sanity-check')
g(ssc_stock_composition_chart)

# %% papermill={"duration": 0.084804, "end_time": "2024-01-31T00:36:31.731474", "exception": false, "start_time": "2024-01-31T00:36:31.646670", "status": "completed"}
total_fee_volume_per_day_chart = total_fee_volume_per_day(sim_df, experiment='sanity-check')
g(total_fee_volume_per_day_chart)

# %% papermill={"duration": 0.14691, "end_time": "2024-01-31T00:36:31.884705", "exception": false, "start_time": "2024-01-31T00:36:31.737795", "status": "completed"}
environmental_processes_chart = environmental_processes(sim_df, experiment='sanity-check')
g(environmental_processes_chart)

# %% papermill={"duration": 0.100228, "end_time": "2024-01-31T00:36:31.991822", "exception": false, "start_time": "2024-01-31T00:36:31.891594", "status": "completed"}
blockchain_size_chart = blockchain_size(sim_df, experiment='sanity-check')
g(blockchain_size_chart)

# %% papermill={"duration": 0.059772, "end_time": "2024-01-31T00:36:32.059108", "exception": false, "start_time": "2024-01-31T00:36:31.999336", "status": "completed"}
block_utilization_chart = block_utilization(sim_df, experiment='sanity-check')
g(block_utilization_chart)

# %% [markdown] papermill={"duration": 0.007747, "end_time": "2024-01-31T00:36:32.074815", "exception": false, "start_time": "2024-01-31T00:36:32.067068", "status": "completed"}
# ## Part 4. Scoped KPIs

# %% papermill={"duration": 0.020527, "end_time": "2024-01-31T00:36:32.103507", "exception": false, "start_time": "2024-01-31T00:36:32.082980", "status": "completed"}
from subspace_model.experiments.charts import non_negative_profits, negative_profits, holomap_selector_curve, holomap_selector_box, holomap_selector_box, circulating_supply_volatility, weekly_rewards_to_nominators, weekly_issuance_rate, cumulative_issuance_rate

# %% [markdown] papermill={"duration": 0.007459, "end_time": "2024-01-31T00:36:32.118638", "exception": false, "start_time": "2024-01-31T00:36:32.111179", "status": "completed"}
# Timestep analysis

# %% [markdown] papermill={"duration": 0.007364, "end_time": "2024-01-31T00:36:32.133435", "exception": false, "start_time": "2024-01-31T00:36:32.126071", "status": "completed"}
# ### Profit 1 (Inflows[t] - Outflows[t])

# %% papermill={"duration": 0.027026, "end_time": "2024-01-31T00:36:32.167851", "exception": false, "start_time": "2024-01-31T00:36:32.140825", "status": "completed"}
from subspace_model.experiments.metrics import profit1_timestep
profit1_timestep_df = profit1_timestep(sim_df)
profit1_timestep_df.head()

# %% papermill={"duration": 0.100596, "end_time": "2024-01-31T00:36:32.277887", "exception": false, "start_time": "2024-01-31T00:36:32.177291", "status": "completed"}
non_negative_profits_chart = non_negative_profits(profit1_timestep_df)
g(non_negative_profits_chart)

# %% papermill={"duration": 0.152675, "end_time": "2024-01-31T00:36:32.438912", "exception": false, "start_time": "2024-01-31T00:36:32.286237", "status": "completed"}
negative_profits_chart = negative_profits(profit1_timestep_df)
g(negative_profits_chart)

# %% [markdown] papermill={"duration": 0.008863, "end_time": "2024-01-31T00:36:32.456959", "exception": false, "start_time": "2024-01-31T00:36:32.448096", "status": "completed"}
# Holomap Selector over Profits

# %% papermill={"duration": 0.213225, "end_time": "2024-01-31T00:36:32.679063", "exception": false, "start_time": "2024-01-31T00:36:32.465838", "status": "completed"}
profit1_holomap_curve = holomap_selector_curve(profit1_timestep_df)
g(profit1_holomap_curve)

# %% [markdown] papermill={"duration": 0.009518, "end_time": "2024-01-31T00:36:32.698972", "exception": false, "start_time": "2024-01-31T00:36:32.689454", "status": "completed"}
# Grid Layout

# %% papermill={"duration": 0.371387, "end_time": "2024-01-31T00:36:33.080088", "exception": false, "start_time": "2024-01-31T00:36:32.708701", "status": "completed"}
profit1_grid_layout_curve = hv.NdLayout(hv.GridSpace(profit1_holomap_curve)).cols(5)
g(profit1_grid_layout_curve)

# %% [markdown] papermill={"duration": 0.01382, "end_time": "2024-01-31T00:36:33.108694", "exception": false, "start_time": "2024-01-31T00:36:33.094874", "status": "completed"}
# Trajectory Analysis

# %% papermill={"duration": 0.160142, "end_time": "2024-01-31T00:36:33.282382", "exception": false, "start_time": "2024-01-31T00:36:33.122240", "status": "completed"}
profit1_holomap_box = holomap_selector_box(profit1_timestep_df)
g(profit1_holomap_box)

# %% papermill={"duration": 0.267681, "end_time": "2024-01-31T00:36:33.564170", "exception": false, "start_time": "2024-01-31T00:36:33.296489", "status": "completed"}
profit1_grid_layout_box = hv.NdLayout(hv.GridSpace(profit1_holomap_box)).cols(5)
g(profit1_grid_layout_box)

# %% papermill={"duration": 0.068109, "end_time": "2024-01-31T00:36:33.659068", "exception": false, "start_time": "2024-01-31T00:36:33.590959", "status": "completed"}
circulating_supply_volatility_chart = circulating_supply_volatility(sim_df, experiment='sanity-check')
g(circulating_supply_volatility_chart)

# %% papermill={"duration": 0.066629, "end_time": "2024-01-31T00:36:33.741555", "exception": false, "start_time": "2024-01-31T00:36:33.674926", "status": "completed"}
weekly_rewards_to_nominators_chart = weekly_rewards_to_nominators(sim_df, experiment='sanity-check')
g(weekly_rewards_to_nominators_chart)

# %% papermill={"duration": 0.067343, "end_time": "2024-01-31T00:36:33.826418", "exception": false, "start_time": "2024-01-31T00:36:33.759075", "status": "completed"}
weekly_issuance_rate_chart = weekly_issuance_rate(sim_df, experiment='sanity-check')
g(weekly_issuance_rate_chart)

# %% papermill={"duration": 0.070285, "end_time": "2024-01-31T00:36:33.914565", "exception": false, "start_time": "2024-01-31T00:36:33.844280", "status": "completed"}
cumulative_issuance_rate_chart = cumulative_issuance_rate(sim_df, experiment='sanity-check')
g(cumulative_issuance_rate_chart)

# %% [markdown] papermill={"duration": 0.017481, "end_time": "2024-01-31T00:36:33.949892", "exception": false, "start_time": "2024-01-31T00:36:33.932411", "status": "completed"}
# ### Generating Layouts

# %% papermill={"duration": 0.062673, "end_time": "2024-01-31T00:36:34.030116", "exception": false, "start_time": "2024-01-31T00:36:33.967443", "status": "completed"}
hv.extension('bokeh')

# %% papermill={"duration": 0.887127, "end_time": "2024-01-31T00:36:34.941449", "exception": false, "start_time": "2024-01-31T00:36:34.054322", "status": "completed"}
charts1 = [
    ssc_metrics_chart,
    aggregate_staking_pool_share_composition_chart, 
    ssc_stock_composition_chart,
    total_fee_volume_per_day_chart,
    environmental_processes_chart,
    blockchain_size_chart, 
    block_utilization_chart, 
    non_negative_profits_chart,
    negative_profits_chart,
    circulating_supply_volatility_chart,
    circulating_supply_volatility_chart,
    weekly_rewards_to_nominators_chart,
    weekly_issuance_rate_chart,
    cumulative_issuance_rate_chart,
]

layout1 = hv.Layout(charts1).opts(shared_axes=False).cols(3) 
# hv.save(layout1, 'metrics1.png', fmt='png')
layout1

# %% papermill={"duration": 1.177473, "end_time": "2024-01-31T00:36:36.147975", "exception": false, "start_time": "2024-01-31T00:36:34.970502", "status": "completed"}
charts2 = [ 
    profit1_grid_layout_curve,
    profit1_grid_layout_box,
]

layout2 = hv.Layout(charts2).opts(shared_axes=False).cols(1) 
# hv.save(layout2, 'metrics2.png', fmt='png')
layout2

# %% [markdown] papermill={"duration": 0.028741, "end_time": "2024-01-31T00:36:36.205270", "exception": false, "start_time": "2024-01-31T00:36:36.176529", "status": "completed"}
# ### Normalized Perspectives

# %% papermill={"duration": 0.047796, "end_time": "2024-01-31T00:36:36.281515", "exception": false, "start_time": "2024-01-31T00:36:36.233719", "status": "completed"}
df = sim_df.set_index('days_passed').bfill().fillna(0)

# Take numeric columns for normalizationn
df_numeric = df.select_dtypes(include=['number'])

# Create the normalized results
df_normalized = df_numeric / df_numeric.max()

# Add the label column back
df_normalized[['label', 'environmental_label']] = df[['label', 'environmental_label']]

# Drop unecessary columns
df_normalized = df_normalized.drop(['run', 'timestep', 'simulation', 'subset', 'timestep_in_days', 'block_time_in_seconds', 'sum_of_stocks', 'buffer_size'], axis=1)
df_normalized.shape

# %% papermill={"duration": 0.572244, "end_time": "2024-01-31T00:36:36.882893", "exception": false, "start_time": "2024-01-31T00:36:36.310649", "status": "completed"}
df_normalized_chart = df_normalized.hvplot.line(x='days_passed', by=['label', 'environmental_label'], title="Normalized Numeric Outcomes", width=2000, height=1000, line_width=2, ylim=(0,1))
# hv.save(df_normalized_chart, 'df_normalized_chart.png', fmt='png')
df_normalized_chart

# %% papermill={"duration": 0.036975, "end_time": "2024-01-31T00:36:36.958138", "exception": false, "start_time": "2024-01-31T00:36:36.921163", "status": "completed"}
