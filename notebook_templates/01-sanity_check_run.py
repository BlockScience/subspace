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

# %% [markdown] papermill={"duration": 0.007647, "end_time": "2024-03-07T16:48:42.989298", "exception": false, "start_time": "2024-03-07T16:48:42.981651", "status": "completed"}
# # Subspace Digital Twin, Sanity Checking Run
#
# *Danilo Lessa Bernardineli, November 2023*
#
# On this notebook, we do an sanity checking run (which is a single run) so that basic metrics and KPIs
# for the simulation are computed.
#
# ## Part 1. Dependences & Set-up

# %% [markdown] papermill={"duration": 0.008249, "end_time": "2024-03-07T16:48:43.004765", "exception": false, "start_time": "2024-03-07T16:48:42.996516", "status": "completed"}
# Autoreload modules while developing.

# %% papermill={"duration": 0.011567, "end_time": "2024-03-07T16:48:43.018773", "exception": false, "start_time": "2024-03-07T16:48:43.007206", "status": "completed"}
# %load_ext autoreload
# %autoreload 2

# %% papermill={"duration": 1.645201, "end_time": "2024-03-07T16:48:44.667349", "exception": false, "start_time": "2024-03-07T16:48:43.022148", "status": "completed"}
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

# %% [markdown] papermill={"duration": 0.003818, "end_time": "2024-03-07T16:48:44.675072", "exception": false, "start_time": "2024-03-07T16:48:44.671254", "status": "completed"}
# ## Part 2. Load Simulation Data

# %% papermill={"duration": 0.015189, "end_time": "2024-03-07T16:48:44.693864", "exception": false, "start_time": "2024-03-07T16:48:44.678675", "status": "completed"}
from glob import glob

# %% papermill={"duration": 0.014441, "end_time": "2024-03-07T16:48:44.712127", "exception": false, "start_time": "2024-03-07T16:48:44.697686", "status": "completed"}
newest_data = sorted(glob("../data/simulations/sanity_check_run*"))[-1]

# %% papermill={"duration": 0.018162, "end_time": "2024-03-07T16:48:44.733983", "exception": false, "start_time": "2024-03-07T16:48:44.715821", "status": "completed"}
sim_df = pd.read_pickle(newest_data)

# %% papermill={"duration": 0.03505, "end_time": "2024-03-07T16:48:44.772804", "exception": false, "start_time": "2024-03-07T16:48:44.737754", "status": "completed"}
sim_df.head(5)

# %% papermill={"duration": 0.024858, "end_time": "2024-03-07T16:48:44.801768", "exception": false, "start_time": "2024-03-07T16:48:44.776910", "status": "completed"}
sim_df.groupby(['run', 'label', 'environmental_label']).size().reset_index(name='Days')

# %% [markdown] papermill={"duration": 0.006271, "end_time": "2024-03-07T16:48:44.817095", "exception": false, "start_time": "2024-03-07T16:48:44.810824", "status": "completed"}
# ## Part 3. Visualizations
#
# On this section, we'll visualize some base metrics on the simulations results

# %% papermill={"duration": 0.017396, "end_time": "2024-03-07T16:48:44.838488", "exception": false, "start_time": "2024-03-07T16:48:44.821092", "status": "completed"}
from subspace_model.experiments.charts import ssc_metrics, aggregate_staking_pool_share_composition, ssc_stock_composition, total_fee_volume_per_day, environmental_processes, blockchain_size, block_utilization
from subspace_model.util import g, get_hex_colors_from_matplotlib_cmap

# %% papermill={"duration": 0.620351, "end_time": "2024-03-07T16:48:45.462749", "exception": false, "start_time": "2024-03-07T16:48:44.842398", "status": "completed"}
ssc_metrics_chart = ssc_metrics(sim_df, experiment='sanity-check')
g(ssc_metrics_chart)

# %% papermill={"duration": 0.085697, "end_time": "2024-03-07T16:48:45.561714", "exception": false, "start_time": "2024-03-07T16:48:45.476017", "status": "completed"}
aggregate_staking_pool_share_composition_chart = aggregate_staking_pool_share_composition(sim_df, experiment='sanity-check')
g(aggregate_staking_pool_share_composition_chart)

# %% papermill={"duration": 0.226888, "end_time": "2024-03-07T16:48:45.793972", "exception": false, "start_time": "2024-03-07T16:48:45.567084", "status": "completed"}
ssc_stock_composition_chart = ssc_stock_composition(sim_df, experiment='sanity-check')
g(ssc_stock_composition_chart)

# %% papermill={"duration": 0.118695, "end_time": "2024-03-07T16:48:45.918864", "exception": false, "start_time": "2024-03-07T16:48:45.800169", "status": "completed"}
total_fee_volume_per_day_chart = total_fee_volume_per_day(sim_df, experiment='sanity-check')
g(total_fee_volume_per_day_chart)

# %% papermill={"duration": 0.125721, "end_time": "2024-03-07T16:48:46.051175", "exception": false, "start_time": "2024-03-07T16:48:45.925454", "status": "completed"}
environmental_processes_chart = environmental_processes(sim_df, experiment='sanity-check')
g(environmental_processes_chart)

# %% papermill={"duration": 0.087316, "end_time": "2024-03-07T16:48:46.145534", "exception": false, "start_time": "2024-03-07T16:48:46.058218", "status": "completed"}
blockchain_size_chart = blockchain_size(sim_df, experiment='sanity-check')
g(blockchain_size_chart)

# %% papermill={"duration": 0.05781, "end_time": "2024-03-07T16:48:46.211171", "exception": false, "start_time": "2024-03-07T16:48:46.153361", "status": "completed"}
block_utilization_chart = block_utilization(sim_df, experiment='sanity-check')
g(block_utilization_chart)

# %% [markdown] papermill={"duration": 0.008447, "end_time": "2024-03-07T16:48:46.228292", "exception": false, "start_time": "2024-03-07T16:48:46.219845", "status": "completed"}
# ## Part 4. Scoped KPIs

# %% papermill={"duration": 0.019641, "end_time": "2024-03-07T16:48:46.270656", "exception": false, "start_time": "2024-03-07T16:48:46.251015", "status": "completed"}
from subspace_model.experiments.charts import non_negative_profits, negative_profits, holomap_selector_curve, holomap_selector_box, holomap_selector_box, circulating_supply_volatility, weekly_rewards_to_nominators, weekly_issuance_rate, cumulative_issuance_rate

# %% [markdown] papermill={"duration": 0.008133, "end_time": "2024-03-07T16:48:46.286755", "exception": false, "start_time": "2024-03-07T16:48:46.278622", "status": "completed"}
# Timestep analysis

# %% [markdown] papermill={"duration": 0.007624, "end_time": "2024-03-07T16:48:46.302055", "exception": false, "start_time": "2024-03-07T16:48:46.294431", "status": "completed"}
# ### Profit 1 (Inflows[t] - Outflows[t])

# %% papermill={"duration": 0.036064, "end_time": "2024-03-07T16:48:46.345810", "exception": false, "start_time": "2024-03-07T16:48:46.309746", "status": "completed"}
from subspace_model.experiments.metrics import profit1_timestep
profit1_timestep_df = profit1_timestep(sim_df)
profit1_timestep_df.head()

# %% papermill={"duration": 0.146023, "end_time": "2024-03-07T16:48:46.503102", "exception": false, "start_time": "2024-03-07T16:48:46.357079", "status": "completed"}
non_negative_profits_chart = non_negative_profits(profit1_timestep_df)
g(non_negative_profits_chart)

# %% papermill={"duration": 0.063775, "end_time": "2024-03-07T16:48:46.575708", "exception": false, "start_time": "2024-03-07T16:48:46.511933", "status": "completed"}
negative_profits_chart = negative_profits(profit1_timestep_df)
g(negative_profits_chart)

# %% [markdown] papermill={"duration": 0.009094, "end_time": "2024-03-07T16:48:46.594291", "exception": false, "start_time": "2024-03-07T16:48:46.585197", "status": "completed"}
# Holomap Selector over Profits

# %% papermill={"duration": 0.202108, "end_time": "2024-03-07T16:48:46.805486", "exception": false, "start_time": "2024-03-07T16:48:46.603378", "status": "completed"}
profit1_holomap_curve = holomap_selector_curve(profit1_timestep_df)
g(profit1_holomap_curve)

# %% [markdown] papermill={"duration": 0.009591, "end_time": "2024-03-07T16:48:46.825145", "exception": false, "start_time": "2024-03-07T16:48:46.815554", "status": "completed"}
# Grid Layout

# %% papermill={"duration": 0.313743, "end_time": "2024-03-07T16:48:47.148711", "exception": false, "start_time": "2024-03-07T16:48:46.834968", "status": "completed"}
profit1_grid_layout_curve = hv.NdLayout(hv.GridSpace(profit1_holomap_curve)).cols(5)
g(profit1_grid_layout_curve)

# %% [markdown] papermill={"duration": 0.013914, "end_time": "2024-03-07T16:48:47.177527", "exception": false, "start_time": "2024-03-07T16:48:47.163613", "status": "completed"}
# Trajectory Analysis

# %% papermill={"duration": 0.154288, "end_time": "2024-03-07T16:48:47.346141", "exception": false, "start_time": "2024-03-07T16:48:47.191853", "status": "completed"}
profit1_holomap_box = holomap_selector_box(profit1_timestep_df)
g(profit1_holomap_box)

# %% papermill={"duration": 0.210015, "end_time": "2024-03-07T16:48:47.571993", "exception": false, "start_time": "2024-03-07T16:48:47.361978", "status": "completed"}
profit1_grid_layout_box = hv.NdLayout(hv.GridSpace(profit1_holomap_box)).cols(5)
g(profit1_grid_layout_box)

# %% papermill={"duration": 0.066722, "end_time": "2024-03-07T16:48:47.655090", "exception": false, "start_time": "2024-03-07T16:48:47.588368", "status": "completed"}
circulating_supply_volatility_chart = circulating_supply_volatility(sim_df, experiment='sanity-check')
g(circulating_supply_volatility_chart)

# %% papermill={"duration": 0.067681, "end_time": "2024-03-07T16:48:47.739550", "exception": false, "start_time": "2024-03-07T16:48:47.671869", "status": "completed"}
weekly_rewards_to_nominators_chart = weekly_rewards_to_nominators(sim_df, experiment='sanity-check')
g(weekly_rewards_to_nominators_chart)

# %% papermill={"duration": 0.07085, "end_time": "2024-03-07T16:48:47.827576", "exception": false, "start_time": "2024-03-07T16:48:47.756726", "status": "completed"}
weekly_issuance_rate_chart = weekly_issuance_rate(sim_df, experiment='sanity-check')
g(weekly_issuance_rate_chart)

# %% papermill={"duration": 0.069916, "end_time": "2024-03-07T16:48:47.914896", "exception": false, "start_time": "2024-03-07T16:48:47.844980", "status": "completed"}
cumulative_issuance_rate_chart = cumulative_issuance_rate(sim_df, experiment='sanity-check')
g(cumulative_issuance_rate_chart)

# %% [markdown] papermill={"duration": 0.018245, "end_time": "2024-03-07T16:48:47.951044", "exception": false, "start_time": "2024-03-07T16:48:47.932799", "status": "completed"}
# ### Generating Layouts

# %% papermill={"duration": 0.061617, "end_time": "2024-03-07T16:48:48.031409", "exception": false, "start_time": "2024-03-07T16:48:47.969792", "status": "completed"}
hv.extension('bokeh')

# %% papermill={"duration": 0.821702, "end_time": "2024-03-07T16:48:48.871630", "exception": false, "start_time": "2024-03-07T16:48:48.049928", "status": "completed"}
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

# %% papermill={"duration": 1.102225, "end_time": "2024-03-07T16:48:49.994783", "exception": false, "start_time": "2024-03-07T16:48:48.892558", "status": "completed"}
charts2 = [ 
    profit1_grid_layout_curve,
    profit1_grid_layout_box,
]

layout2 = hv.Layout(charts2).opts(shared_axes=False).cols(1) 
# hv.save(layout2, 'metrics2.png', fmt='png')
layout2

# %% [markdown] papermill={"duration": 0.024514, "end_time": "2024-03-07T16:48:50.041290", "exception": false, "start_time": "2024-03-07T16:48:50.016776", "status": "completed"}
# ### Normalized Perspectives

# %% papermill={"duration": 0.042255, "end_time": "2024-03-07T16:48:50.106783", "exception": false, "start_time": "2024-03-07T16:48:50.064528", "status": "completed"}
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

# %% papermill={"duration": 0.705871, "end_time": "2024-03-07T16:48:50.836576", "exception": false, "start_time": "2024-03-07T16:48:50.130705", "status": "completed"}
df_normalized_chart = df_normalized.hvplot.line(x='days_passed', by=['label', 'environmental_label'], title="Normalized Numeric Outcomes", width=2000, height=1000, line_width=2, ylim=(0,1))
# hv.save(df_normalized_chart, 'df_normalized_chart.png', fmt='png')
df_normalized_chart

# %% papermill={"duration": 0.023692, "end_time": "2024-03-07T16:48:50.885882", "exception": false, "start_time": "2024-03-07T16:48:50.862190", "status": "completed"}
