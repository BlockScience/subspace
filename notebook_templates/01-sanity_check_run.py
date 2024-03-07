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

# %% [markdown] editable=true papermill={"duration": 0.016379, "end_time": "2024-03-07T18:33:01.399138", "exception": false, "start_time": "2024-03-07T18:33:01.382759", "status": "completed"} slideshow={"slide_type": ""}
# # Subspace Digital Twin, Sanity Checking Run
#
# *Danilo Lessa Bernardineli, November 2023*
#
# On this notebook, we do an sanity checking run (which is a single run) so that basic metrics and KPIs
# for the simulation are computed.
#
# ## Part 1. Dependences & Set-up

# %% [markdown] papermill={"duration": 0.003512, "end_time": "2024-03-07T18:33:01.409577", "exception": false, "start_time": "2024-03-07T18:33:01.406065", "status": "completed"}
# Autoreload modules while developing.

# %% papermill={"duration": 0.023483, "end_time": "2024-03-07T18:33:01.436101", "exception": false, "start_time": "2024-03-07T18:33:01.412618", "status": "completed"}
# %load_ext autoreload
# %autoreload 2

# %% papermill={"duration": 1.752804, "end_time": "2024-03-07T18:33:03.192528", "exception": false, "start_time": "2024-03-07T18:33:01.439724", "status": "completed"}
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

# %% editable=true papermill={"duration": 0.028012, "end_time": "2024-03-07T18:33:03.228295", "exception": false, "start_time": "2024-03-07T18:33:03.200283", "status": "completed"} slideshow={"slide_type": ""} tags=["parameters"]
try:
    import ipynbname
    nb_name = ipynbname.name()
except:
    pass

# %% papermill={"duration": 0.016698, "end_time": "2024-03-07T18:33:03.250145", "exception": false, "start_time": "2024-03-07T18:33:03.233447", "status": "completed"} tags=["injected-parameters"]
# Parameters
nb_name = "01-sanity_check_run"


# %% [markdown] papermill={"duration": 0.010901, "end_time": "2024-03-07T18:33:03.265988", "exception": false, "start_time": "2024-03-07T18:33:03.255087", "status": "completed"}
# ## Part 2. Load Simulation Data

# %% papermill={"duration": 0.015428, "end_time": "2024-03-07T18:33:03.287428", "exception": false, "start_time": "2024-03-07T18:33:03.272000", "status": "completed"}
from glob import glob

# %% papermill={"duration": 0.019857, "end_time": "2024-03-07T18:33:03.311768", "exception": false, "start_time": "2024-03-07T18:33:03.291911", "status": "completed"}
newest_data = sorted(glob("../data/simulations/sanity_check_run*"))[-1]

# %% papermill={"duration": 0.015725, "end_time": "2024-03-07T18:33:03.332112", "exception": false, "start_time": "2024-03-07T18:33:03.316387", "status": "completed"}
sim_df = pd.read_pickle(newest_data)

# %% papermill={"duration": 0.037289, "end_time": "2024-03-07T18:33:03.373985", "exception": false, "start_time": "2024-03-07T18:33:03.336696", "status": "completed"}
sim_df.head(5)

# %% papermill={"duration": 0.023154, "end_time": "2024-03-07T18:33:03.402802", "exception": false, "start_time": "2024-03-07T18:33:03.379648", "status": "completed"}
sim_df.groupby(['run', 'label', 'environmental_label']).size().reset_index(name='Days')

# %% [markdown] papermill={"duration": 0.004652, "end_time": "2024-03-07T18:33:03.412270", "exception": false, "start_time": "2024-03-07T18:33:03.407618", "status": "completed"}
# ## Part 3. Visualizations
#
# On this section, we'll visualize some base metrics on the simulations results

# %% papermill={"duration": 0.026903, "end_time": "2024-03-07T18:33:03.443928", "exception": false, "start_time": "2024-03-07T18:33:03.417025", "status": "completed"}
from subspace_model.experiments.charts import ssc_metrics, aggregate_staking_pool_share_composition, ssc_stock_composition, total_fee_volume_per_day, environmental_processes, blockchain_size, block_utilization
from subspace_model.util import g, get_hex_colors_from_matplotlib_cmap, hv_save

# %% papermill={"duration": 0.610961, "end_time": "2024-03-07T18:33:04.059758", "exception": false, "start_time": "2024-03-07T18:33:03.448797", "status": "completed"}
ssc_metrics_chart = ssc_metrics(sim_df, experiment='sanity-check')
g(ssc_metrics_chart)

# %% editable=true papermill={"duration": 0.123231, "end_time": "2024-03-07T18:33:04.191476", "exception": false, "start_time": "2024-03-07T18:33:04.068245", "status": "completed"} slideshow={"slide_type": ""}
hv_save(ssc_metrics_chart, 'ssc_metrics_chart', nb_name)

# %% papermill={"duration": 0.108412, "end_time": "2024-03-07T18:33:04.305521", "exception": false, "start_time": "2024-03-07T18:33:04.197109", "status": "completed"}
aggregate_staking_pool_share_composition_chart = aggregate_staking_pool_share_composition(sim_df, experiment='sanity-check')
g(aggregate_staking_pool_share_composition_chart)

# %% editable=true papermill={"duration": 0.072879, "end_time": "2024-03-07T18:33:04.384433", "exception": false, "start_time": "2024-03-07T18:33:04.311554", "status": "completed"} slideshow={"slide_type": ""}
hv_save(aggregate_staking_pool_share_composition_chart, 'aggregate_staking_pool_share_composition_chart', nb_name)

# %% papermill={"duration": 0.261085, "end_time": "2024-03-07T18:33:04.652278", "exception": false, "start_time": "2024-03-07T18:33:04.391193", "status": "completed"}
ssc_stock_composition_chart = ssc_stock_composition(sim_df, experiment='sanity-check')
g(ssc_stock_composition_chart)

# %% editable=true papermill={"duration": 0.122566, "end_time": "2024-03-07T18:33:04.803315", "exception": false, "start_time": "2024-03-07T18:33:04.680749", "status": "completed"} slideshow={"slide_type": ""}
hv_save(ssc_stock_composition_chart, 'ssc_stock_composition_chart', nb_name)

# %% papermill={"duration": 0.138484, "end_time": "2024-03-07T18:33:04.949309", "exception": false, "start_time": "2024-03-07T18:33:04.810825", "status": "completed"}
total_fee_volume_per_day_chart = total_fee_volume_per_day(sim_df, experiment='sanity-check')
g(total_fee_volume_per_day_chart)

# %% editable=true papermill={"duration": 0.082517, "end_time": "2024-03-07T18:33:05.042665", "exception": false, "start_time": "2024-03-07T18:33:04.960148", "status": "completed"} slideshow={"slide_type": ""}
hv_save(total_fee_volume_per_day_chart, 'total_fee_volume_per_day_chart', nb_name)

# %% papermill={"duration": 0.146708, "end_time": "2024-03-07T18:33:05.197518", "exception": false, "start_time": "2024-03-07T18:33:05.050810", "status": "completed"}
environmental_processes_chart = environmental_processes(sim_df, experiment='sanity-check')
g(environmental_processes_chart)

# %% editable=true papermill={"duration": 0.089838, "end_time": "2024-03-07T18:33:05.295463", "exception": false, "start_time": "2024-03-07T18:33:05.205625", "status": "completed"} slideshow={"slide_type": ""}
hv_save(environmental_processes_chart, 'environmental_processes_chart', nb_name)

# %% papermill={"duration": 0.135679, "end_time": "2024-03-07T18:33:05.444956", "exception": false, "start_time": "2024-03-07T18:33:05.309277", "status": "completed"}
blockchain_size_chart = blockchain_size(sim_df, experiment='sanity-check')
g(blockchain_size_chart)

# %% editable=true papermill={"duration": 0.073665, "end_time": "2024-03-07T18:33:05.530391", "exception": false, "start_time": "2024-03-07T18:33:05.456726", "status": "completed"} slideshow={"slide_type": ""}
hv_save(blockchain_size_chart, 'blockchain_size_chart', nb_name)

# %% papermill={"duration": 0.085578, "end_time": "2024-03-07T18:33:05.624630", "exception": false, "start_time": "2024-03-07T18:33:05.539052", "status": "completed"}
block_utilization_chart = block_utilization(sim_df, experiment='sanity-check')
g(block_utilization_chart)

# %% editable=true papermill={"duration": 0.055654, "end_time": "2024-03-07T18:33:05.690007", "exception": false, "start_time": "2024-03-07T18:33:05.634353", "status": "completed"} slideshow={"slide_type": ""}
hv_save(block_utilization_chart, 'block_utilization_chart', nb_name)

# %% [markdown] papermill={"duration": 0.008966, "end_time": "2024-03-07T18:33:05.708027", "exception": false, "start_time": "2024-03-07T18:33:05.699061", "status": "completed"}
# ## Part 4. Scoped KPIs

# %% papermill={"duration": 0.0222, "end_time": "2024-03-07T18:33:05.741462", "exception": false, "start_time": "2024-03-07T18:33:05.719262", "status": "completed"}
from subspace_model.experiments.charts import non_negative_profits, negative_profits, holomap_selector_curve, holomap_selector_box, holomap_selector_box, circulating_supply_volatility, weekly_rewards_to_nominators, weekly_issuance_rate, cumulative_issuance_rate

# %% [markdown] papermill={"duration": 0.024214, "end_time": "2024-03-07T18:33:05.774852", "exception": false, "start_time": "2024-03-07T18:33:05.750638", "status": "completed"}
# Timestep analysis

# %% [markdown] papermill={"duration": 0.010028, "end_time": "2024-03-07T18:33:05.795708", "exception": false, "start_time": "2024-03-07T18:33:05.785680", "status": "completed"}
# ### Profit 1 (Inflows[t] - Outflows[t])

# %% papermill={"duration": 0.027726, "end_time": "2024-03-07T18:33:05.833827", "exception": false, "start_time": "2024-03-07T18:33:05.806101", "status": "completed"}
from subspace_model.experiments.metrics import profit1_timestep
profit1_timestep_df = profit1_timestep(sim_df)
profit1_timestep_df.head()

# %% papermill={"duration": 0.162586, "end_time": "2024-03-07T18:33:06.007559", "exception": false, "start_time": "2024-03-07T18:33:05.844973", "status": "completed"}
non_negative_profits_chart = non_negative_profits(profit1_timestep_df)
g(non_negative_profits_chart)

# %% editable=true papermill={"duration": 0.104273, "end_time": "2024-03-07T18:33:06.131364", "exception": false, "start_time": "2024-03-07T18:33:06.027091", "status": "completed"} slideshow={"slide_type": ""}
hv_save(non_negative_profits_chart, 'non_negative_profits_chart', nb_name)

# %% [markdown] papermill={"duration": 0.009821, "end_time": "2024-03-07T18:33:06.152785", "exception": false, "start_time": "2024-03-07T18:33:06.142964", "status": "completed"}
# Holomap Selector over Profits

# %% papermill={"duration": 0.2314, "end_time": "2024-03-07T18:33:06.394053", "exception": false, "start_time": "2024-03-07T18:33:06.162653", "status": "completed"}
profit1_holomap_curve = holomap_selector_curve(profit1_timestep_df)
g(profit1_holomap_curve)

# %% [markdown] papermill={"duration": 0.010043, "end_time": "2024-03-07T18:33:06.414484", "exception": false, "start_time": "2024-03-07T18:33:06.404441", "status": "completed"}
# Grid Layout

# %% editable=true papermill={"duration": 0.06558, "end_time": "2024-03-07T18:33:06.491207", "exception": false, "start_time": "2024-03-07T18:33:06.425627", "status": "completed"} slideshow={"slide_type": ""}
hv_save(profit1_holomap_curve, 'profit1_holomap_curve', nb_name)

# %% papermill={"duration": 0.39843, "end_time": "2024-03-07T18:33:06.900518", "exception": false, "start_time": "2024-03-07T18:33:06.502088", "status": "completed"}
profit1_grid_layout_curve = hv.NdLayout(hv.GridSpace(profit1_holomap_curve)).cols(5)
g(profit1_grid_layout_curve)

# %% [markdown] papermill={"duration": 0.01824, "end_time": "2024-03-07T18:33:06.934318", "exception": false, "start_time": "2024-03-07T18:33:06.916078", "status": "completed"}
# Trajectory Analysis

# %% editable=true papermill={"duration": 0.305886, "end_time": "2024-03-07T18:33:07.255191", "exception": false, "start_time": "2024-03-07T18:33:06.949305", "status": "completed"} slideshow={"slide_type": ""}
hv_save(profit1_grid_layout_curve, 'profit1_grid_layout_curve', nb_name)

# %% papermill={"duration": 0.162836, "end_time": "2024-03-07T18:33:07.452275", "exception": false, "start_time": "2024-03-07T18:33:07.289439", "status": "completed"}
profit1_holomap_box = holomap_selector_box(profit1_timestep_df)
g(profit1_holomap_box)

# %% editable=true papermill={"duration": 0.059315, "end_time": "2024-03-07T18:33:07.527323", "exception": false, "start_time": "2024-03-07T18:33:07.468008", "status": "completed"} slideshow={"slide_type": ""}
hv_save(profit1_holomap_box, 'profit1_holomap_box', nb_name)

# %% papermill={"duration": 0.233608, "end_time": "2024-03-07T18:33:07.776328", "exception": false, "start_time": "2024-03-07T18:33:07.542720", "status": "completed"}
profit1_grid_layout_box = hv.NdLayout(hv.GridSpace(profit1_holomap_box)).cols(5)
g(profit1_grid_layout_box)

# %% editable=true papermill={"duration": 0.245949, "end_time": "2024-03-07T18:33:08.040008", "exception": false, "start_time": "2024-03-07T18:33:07.794059", "status": "completed"} slideshow={"slide_type": ""}
hv_save(profit1_grid_layout_box, 'profit1_grid_layout_box', nb_name)

# %% papermill={"duration": 0.081153, "end_time": "2024-03-07T18:33:08.149119", "exception": false, "start_time": "2024-03-07T18:33:08.067966", "status": "completed"}
circulating_supply_volatility_chart = circulating_supply_volatility(sim_df, experiment='sanity-check')
g(circulating_supply_volatility_chart)

# %% editable=true papermill={"duration": 0.060404, "end_time": "2024-03-07T18:33:08.226888", "exception": false, "start_time": "2024-03-07T18:33:08.166484", "status": "completed"} slideshow={"slide_type": ""}
hv_save(circulating_supply_volatility_chart, 'circulating_supply_volatility_chart', nb_name)

# %% papermill={"duration": 0.078061, "end_time": "2024-03-07T18:33:08.322776", "exception": false, "start_time": "2024-03-07T18:33:08.244715", "status": "completed"}
weekly_rewards_to_nominators_chart = weekly_rewards_to_nominators(sim_df, experiment='sanity-check')
g(weekly_rewards_to_nominators_chart)

# %% editable=true papermill={"duration": 0.068777, "end_time": "2024-03-07T18:33:08.412809", "exception": false, "start_time": "2024-03-07T18:33:08.344032", "status": "completed"} slideshow={"slide_type": ""}
hv_save(weekly_rewards_to_nominators_chart, 'weekly_rewards_to_nominators_chart', nb_name)

# %% papermill={"duration": 0.077295, "end_time": "2024-03-07T18:33:08.516635", "exception": false, "start_time": "2024-03-07T18:33:08.439340", "status": "completed"}
weekly_issuance_rate_chart = weekly_issuance_rate(sim_df, experiment='sanity-check')
g(weekly_issuance_rate_chart)

# %% editable=true papermill={"duration": 0.064362, "end_time": "2024-03-07T18:33:08.599420", "exception": false, "start_time": "2024-03-07T18:33:08.535058", "status": "completed"} slideshow={"slide_type": ""}
hv_save(weekly_issuance_rate_chart, 'weekly_issuance_rate_chart', nb_name)

# %% papermill={"duration": 0.10505, "end_time": "2024-03-07T18:33:08.733737", "exception": false, "start_time": "2024-03-07T18:33:08.628687", "status": "completed"}
cumulative_issuance_rate_chart = cumulative_issuance_rate(sim_df, experiment='sanity-check')
g(cumulative_issuance_rate_chart)

# %% editable=true papermill={"duration": 0.06097, "end_time": "2024-03-07T18:33:08.817286", "exception": false, "start_time": "2024-03-07T18:33:08.756316", "status": "completed"} slideshow={"slide_type": ""}
hv_save(cumulative_issuance_rate_chart, 'cumulative_issuance_rate_chart', nb_name)

# %% [markdown] papermill={"duration": 0.020238, "end_time": "2024-03-07T18:33:08.858881", "exception": false, "start_time": "2024-03-07T18:33:08.838643", "status": "completed"}
# ### Generating Layouts

# %% papermill={"duration": 0.072745, "end_time": "2024-03-07T18:33:08.953211", "exception": false, "start_time": "2024-03-07T18:33:08.880466", "status": "completed"}
hv.extension('bokeh')

# %% editable=true papermill={"duration": 0.911893, "end_time": "2024-03-07T18:33:09.891989", "exception": false, "start_time": "2024-03-07T18:33:08.980096", "status": "completed"} slideshow={"slide_type": ""}
charts1 = [
    ssc_metrics_chart,
    aggregate_staking_pool_share_composition_chart, 
    ssc_stock_composition_chart,
    total_fee_volume_per_day_chart,
    environmental_processes_chart,
    blockchain_size_chart, 
    block_utilization_chart, 
    non_negative_profits_chart,
    circulating_supply_volatility_chart,
    circulating_supply_volatility_chart,
    weekly_rewards_to_nominators_chart,
    weekly_issuance_rate_chart,
    cumulative_issuance_rate_chart,
]

layout1 = hv.Layout(charts1).opts(shared_axes=False).cols(3) 
# hv.save(layout1, 'metrics1.png', fmt='png')
layout1

# %% editable=true papermill={"duration": 4.698207, "end_time": "2024-03-07T18:33:14.613743", "exception": false, "start_time": "2024-03-07T18:33:09.915536", "status": "completed"} slideshow={"slide_type": ""}
hv_save(layout1, 'layout1', nb_name)

# %% papermill={"duration": 1.201907, "end_time": "2024-03-07T18:33:15.845392", "exception": false, "start_time": "2024-03-07T18:33:14.643485", "status": "completed"}
charts2 = [ 
    profit1_grid_layout_curve,
    profit1_grid_layout_box,
]

layout2 = hv.Layout(charts2).opts(shared_axes=False).cols(1) 
# hv.save(layout2, 'metrics2.png', fmt='png')
layout2

# %% editable=true papermill={"duration": 3.873351, "end_time": "2024-03-07T18:33:19.754430", "exception": false, "start_time": "2024-03-07T18:33:15.881079", "status": "completed"} slideshow={"slide_type": ""}
hv_save(layout2, 'layout2', nb_name)

# %% [markdown] papermill={"duration": 0.025063, "end_time": "2024-03-07T18:33:19.807013", "exception": false, "start_time": "2024-03-07T18:33:19.781950", "status": "completed"}
# ### Normalized Perspectives

# %% papermill={"duration": 0.04414, "end_time": "2024-03-07T18:33:19.879121", "exception": false, "start_time": "2024-03-07T18:33:19.834981", "status": "completed"}
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

# %% papermill={"duration": 0.78463, "end_time": "2024-03-07T18:33:20.691757", "exception": false, "start_time": "2024-03-07T18:33:19.907127", "status": "completed"}
df_normalized_chart = df_normalized.hvplot.line(x='days_passed', by=['label', 'environmental_label'], title="Normalized Numeric Outcomes", width=2000, height=1000, line_width=2, ylim=(0,1))
# hv.save(df_normalized_chart, 'df_normalized_chart.png', fmt='png')
df_normalized_chart

# %% editable=true papermill={"duration": 2.863144, "end_time": "2024-03-07T18:33:23.589002", "exception": false, "start_time": "2024-03-07T18:33:20.725858", "status": "completed"} slideshow={"slide_type": ""}
hv_save(df_normalized_chart, 'df_normalized_chart', nb_name)

# %% editable=true papermill={"duration": 0.027164, "end_time": "2024-03-07T18:33:23.646637", "exception": false, "start_time": "2024-03-07T18:33:23.619473", "status": "completed"} slideshow={"slide_type": ""}
