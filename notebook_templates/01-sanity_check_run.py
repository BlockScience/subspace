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

# %% [markdown] papermill={"duration": 0.008902, "end_time": "2024-02-07T16:44:04.133063", "exception": false, "start_time": "2024-02-07T16:44:04.124161", "status": "completed"}
# # Subspace Digital Twin, Sanity Checking Run
#
# *Danilo Lessa Bernardineli, November 2023*
#
# On this notebook, we do an sanity checking run (which is a single run) so that basic metrics and KPIs
# for the simulation are computed.
#
# ## Part 1. Dependences & Set-up

# %% [markdown] papermill={"duration": 0.002157, "end_time": "2024-02-07T16:44:04.142857", "exception": false, "start_time": "2024-02-07T16:44:04.140700", "status": "completed"}
# Autoreload modules while developing.

# %% papermill={"duration": 0.012407, "end_time": "2024-02-07T16:44:04.157323", "exception": false, "start_time": "2024-02-07T16:44:04.144916", "status": "completed"}
# %load_ext autoreload
# %autoreload 2

# %% papermill={"duration": 1.617145, "end_time": "2024-02-07T16:44:05.777150", "exception": false, "start_time": "2024-02-07T16:44:04.160005", "status": "completed"}
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

# %% [markdown] papermill={"duration": 0.008039, "end_time": "2024-02-07T16:44:05.788903", "exception": false, "start_time": "2024-02-07T16:44:05.780864", "status": "completed"}
# ## Part 2. Load Simulation Data

# %% papermill={"duration": 0.015822, "end_time": "2024-02-07T16:44:05.808058", "exception": false, "start_time": "2024-02-07T16:44:05.792236", "status": "completed"}
from glob import glob

# %% papermill={"duration": 0.013861, "end_time": "2024-02-07T16:44:05.825403", "exception": false, "start_time": "2024-02-07T16:44:05.811542", "status": "completed"}
newest_data = sorted(glob("../data/simulations/sanity_check_run*"))[-1]

# %% papermill={"duration": 0.014588, "end_time": "2024-02-07T16:44:05.843415", "exception": false, "start_time": "2024-02-07T16:44:05.828827", "status": "completed"}
sim_df = pd.read_pickle(newest_data)

# %% papermill={"duration": 0.029827, "end_time": "2024-02-07T16:44:05.876754", "exception": false, "start_time": "2024-02-07T16:44:05.846927", "status": "completed"}
sim_df.head(5)

# %% papermill={"duration": 0.02377, "end_time": "2024-02-07T16:44:05.904287", "exception": false, "start_time": "2024-02-07T16:44:05.880517", "status": "completed"}
sim_df.groupby(['run', 'label', 'environmental_label']).size().reset_index(name='Days')

# %% [markdown] papermill={"duration": 0.004293, "end_time": "2024-02-07T16:44:05.916233", "exception": false, "start_time": "2024-02-07T16:44:05.911940", "status": "completed"}
# ## Part 3. Visualizations
#
# On this section, we'll visualize some base metrics on the simulations results

# %% papermill={"duration": 0.017524, "end_time": "2024-02-07T16:44:05.937482", "exception": false, "start_time": "2024-02-07T16:44:05.919958", "status": "completed"}
from subspace_model.experiments.charts import ssc_metrics, aggregate_staking_pool_share_composition, ssc_stock_composition, total_fee_volume_per_day, environmental_processes, blockchain_size, block_utilization
from subspace_model.util import g, get_hex_colors_from_matplotlib_cmap

# %% papermill={"duration": 0.44999, "end_time": "2024-02-07T16:44:06.391675", "exception": false, "start_time": "2024-02-07T16:44:05.941685", "status": "completed"}
ssc_metrics_chart = ssc_metrics(sim_df, experiment='sanity-check')
g(ssc_metrics_chart)

# %% papermill={"duration": 0.158256, "end_time": "2024-02-07T16:44:06.557184", "exception": false, "start_time": "2024-02-07T16:44:06.398928", "status": "completed"}
aggregate_staking_pool_share_composition_chart = aggregate_staking_pool_share_composition(sim_df, experiment='sanity-check')
g(aggregate_staking_pool_share_composition_chart)

# %% papermill={"duration": 0.164463, "end_time": "2024-02-07T16:44:06.726805", "exception": false, "start_time": "2024-02-07T16:44:06.562342", "status": "completed"}
ssc_stock_composition_chart = ssc_stock_composition(sim_df, experiment='sanity-check')
g(ssc_stock_composition_chart)

# %% papermill={"duration": 0.114232, "end_time": "2024-02-07T16:44:06.847110", "exception": false, "start_time": "2024-02-07T16:44:06.732878", "status": "completed"}
total_fee_volume_per_day_chart = total_fee_volume_per_day(sim_df, experiment='sanity-check')
g(total_fee_volume_per_day_chart)

# %% papermill={"duration": 0.12224, "end_time": "2024-02-07T16:44:06.975894", "exception": false, "start_time": "2024-02-07T16:44:06.853654", "status": "completed"}
environmental_processes_chart = environmental_processes(sim_df, experiment='sanity-check')
g(environmental_processes_chart)

# %% papermill={"duration": 0.085645, "end_time": "2024-02-07T16:44:07.068484", "exception": false, "start_time": "2024-02-07T16:44:06.982839", "status": "completed"}
blockchain_size_chart = blockchain_size(sim_df, experiment='sanity-check')
g(blockchain_size_chart)

# %% papermill={"duration": 0.058107, "end_time": "2024-02-07T16:44:07.134015", "exception": false, "start_time": "2024-02-07T16:44:07.075908", "status": "completed"}
block_utilization_chart = block_utilization(sim_df, experiment='sanity-check')
g(block_utilization_chart)

# %% [markdown] papermill={"duration": 0.007784, "end_time": "2024-02-07T16:44:07.149701", "exception": false, "start_time": "2024-02-07T16:44:07.141917", "status": "completed"}
# ## Part 4. Scoped KPIs

# %% papermill={"duration": 0.019224, "end_time": "2024-02-07T16:44:07.176450", "exception": false, "start_time": "2024-02-07T16:44:07.157226", "status": "completed"}
from subspace_model.experiments.charts import non_negative_profits, negative_profits, holomap_selector_curve, holomap_selector_box, holomap_selector_box, circulating_supply_volatility, weekly_rewards_to_nominators, weekly_issuance_rate, cumulative_issuance_rate

# %% [markdown] papermill={"duration": 0.007506, "end_time": "2024-02-07T16:44:07.191739", "exception": false, "start_time": "2024-02-07T16:44:07.184233", "status": "completed"}
# Timestep analysis

# %% [markdown] papermill={"duration": 0.007488, "end_time": "2024-02-07T16:44:07.206799", "exception": false, "start_time": "2024-02-07T16:44:07.199311", "status": "completed"}
# ### Profit 1 (Inflows[t] - Outflows[t])

# %% papermill={"duration": 0.025565, "end_time": "2024-02-07T16:44:07.240020", "exception": false, "start_time": "2024-02-07T16:44:07.214455", "status": "completed"}
from subspace_model.experiments.metrics import profit1_timestep
profit1_timestep_df = profit1_timestep(sim_df)
profit1_timestep_df.head()

# %% papermill={"duration": 0.143937, "end_time": "2024-02-07T16:44:07.391800", "exception": false, "start_time": "2024-02-07T16:44:07.247863", "status": "completed"}
non_negative_profits_chart = non_negative_profits(profit1_timestep_df)
g(non_negative_profits_chart)

# %% papermill={"duration": 0.057839, "end_time": "2024-02-07T16:44:07.458355", "exception": false, "start_time": "2024-02-07T16:44:07.400516", "status": "completed"}
negative_profits_chart = negative_profits(profit1_timestep_df)
g(negative_profits_chart)

# %% [markdown] papermill={"duration": 0.008852, "end_time": "2024-02-07T16:44:07.492137", "exception": false, "start_time": "2024-02-07T16:44:07.483285", "status": "completed"}
# Holomap Selector over Profits

# %% papermill={"duration": 0.196798, "end_time": "2024-02-07T16:44:07.697803", "exception": false, "start_time": "2024-02-07T16:44:07.501005", "status": "completed"}
profit1_holomap_curve = holomap_selector_curve(profit1_timestep_df)
g(profit1_holomap_curve)

# %% [markdown] papermill={"duration": 0.009876, "end_time": "2024-02-07T16:44:07.718281", "exception": false, "start_time": "2024-02-07T16:44:07.708405", "status": "completed"}
# Grid Layout

# %% papermill={"duration": 0.293399, "end_time": "2024-02-07T16:44:08.021090", "exception": false, "start_time": "2024-02-07T16:44:07.727691", "status": "completed"}
profit1_grid_layout_curve = hv.NdLayout(hv.GridSpace(profit1_holomap_curve)).cols(5)
g(profit1_grid_layout_curve)

# %% [markdown] papermill={"duration": 0.013708, "end_time": "2024-02-07T16:44:08.048903", "exception": false, "start_time": "2024-02-07T16:44:08.035195", "status": "completed"}
# Trajectory Analysis

# %% papermill={"duration": 0.146456, "end_time": "2024-02-07T16:44:08.209266", "exception": false, "start_time": "2024-02-07T16:44:08.062810", "status": "completed"}
profit1_holomap_box = holomap_selector_box(profit1_timestep_df)
g(profit1_holomap_box)

# %% papermill={"duration": 0.203635, "end_time": "2024-02-07T16:44:08.427934", "exception": false, "start_time": "2024-02-07T16:44:08.224299", "status": "completed"}
profit1_grid_layout_box = hv.NdLayout(hv.GridSpace(profit1_holomap_box)).cols(5)
g(profit1_grid_layout_box)

# %% papermill={"duration": 0.064414, "end_time": "2024-02-07T16:44:08.508596", "exception": false, "start_time": "2024-02-07T16:44:08.444182", "status": "completed"}
circulating_supply_volatility_chart = circulating_supply_volatility(sim_df, experiment='sanity-check')
g(circulating_supply_volatility_chart)

# %% papermill={"duration": 0.066856, "end_time": "2024-02-07T16:44:08.592083", "exception": false, "start_time": "2024-02-07T16:44:08.525227", "status": "completed"}
weekly_rewards_to_nominators_chart = weekly_rewards_to_nominators(sim_df, experiment='sanity-check')
g(weekly_rewards_to_nominators_chart)

# %% papermill={"duration": 0.069411, "end_time": "2024-02-07T16:44:08.681485", "exception": false, "start_time": "2024-02-07T16:44:08.612074", "status": "completed"}
weekly_issuance_rate_chart = weekly_issuance_rate(sim_df, experiment='sanity-check')
g(weekly_issuance_rate_chart)

# %% papermill={"duration": 0.070088, "end_time": "2024-02-07T16:44:08.770157", "exception": false, "start_time": "2024-02-07T16:44:08.700069", "status": "completed"}
cumulative_issuance_rate_chart = cumulative_issuance_rate(sim_df, experiment='sanity-check')
g(cumulative_issuance_rate_chart)

# %% [markdown] papermill={"duration": 0.017908, "end_time": "2024-02-07T16:44:08.806018", "exception": false, "start_time": "2024-02-07T16:44:08.788110", "status": "completed"}
# ### Generating Layouts

# %% papermill={"duration": 0.058889, "end_time": "2024-02-07T16:44:08.883098", "exception": false, "start_time": "2024-02-07T16:44:08.824209", "status": "completed"}
hv.extension('bokeh')

# %% papermill={"duration": 0.786785, "end_time": "2024-02-07T16:44:09.689393", "exception": false, "start_time": "2024-02-07T16:44:08.902608", "status": "completed"}
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

# %% papermill={"duration": 1.078602, "end_time": "2024-02-07T16:44:10.789214", "exception": false, "start_time": "2024-02-07T16:44:09.710612", "status": "completed"}
charts2 = [ 
    profit1_grid_layout_curve,
    profit1_grid_layout_box,
]

layout2 = hv.Layout(charts2).opts(shared_axes=False).cols(1) 
# hv.save(layout2, 'metrics2.png', fmt='png')
layout2

# %% [markdown] papermill={"duration": 0.021429, "end_time": "2024-02-07T16:44:10.833193", "exception": false, "start_time": "2024-02-07T16:44:10.811764", "status": "completed"}
# ### Normalized Perspectives

# %% papermill={"duration": 0.037852, "end_time": "2024-02-07T16:44:10.892455", "exception": false, "start_time": "2024-02-07T16:44:10.854603", "status": "completed"}
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

# %% papermill={"duration": 0.695777, "end_time": "2024-02-07T16:44:11.609773", "exception": false, "start_time": "2024-02-07T16:44:10.913996", "status": "completed"}
df_normalized_chart = df_normalized.hvplot.line(x='days_passed', by=['label', 'environmental_label'], title="Normalized Numeric Outcomes", width=2000, height=1000, line_width=2, ylim=(0,1))
# hv.save(df_normalized_chart, 'df_normalized_chart.png', fmt='png')
df_normalized_chart

# %% papermill={"duration": 0.023295, "end_time": "2024-02-07T16:44:11.656630", "exception": false, "start_time": "2024-02-07T16:44:11.633335", "status": "completed"}
