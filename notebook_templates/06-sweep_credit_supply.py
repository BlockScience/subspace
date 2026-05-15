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

# %% [markdown] papermill={"duration": 0.003559, "end_time": "2024-01-31T00:37:00.407878", "exception": false, "start_time": "2024-01-31T00:37:00.404319", "status": "completed"}
# Autoreload modules while developing.

# %% papermill={"duration": 0.012794, "end_time": "2024-01-31T00:37:00.428772", "exception": false, "start_time": "2024-01-31T00:37:00.415978", "status": "completed"}
# %load_ext autoreload
# %autoreload 2

# %% [markdown] papermill={"duration": 0.002361, "end_time": "2024-01-31T00:37:00.433592", "exception": false, "start_time": "2024-01-31T00:37:00.431231", "status": "completed"}
# # Subspace Digital Twin, Sweep Credit Supply
#
# * Shawn Anderson, December 2023*
#
# In this notebook, we explore a test sweep over three credit supply definitions. These are: supply_issued, supply_earned, and supply_earned_minus_burned.

# %% papermill={"duration": 1.650665, "end_time": "2024-01-31T00:37:02.086657", "exception": false, "start_time": "2024-01-31T00:37:00.435992", "status": "completed"}
import pandas as pd
import hvplot.pandas
import plotly.io as pio
from holoviews import opts
import holoviews as hv
import plotly.express as px
hvplot.extension('plotly')
pio.renderers.default = "png" # For GitHub rendering

import sys
sys.path.append('../')

from subspace_model.experiments.charts import ab_block_utilization

# %% [markdown] papermill={"duration": 0.008251, "end_time": "2024-01-31T00:37:02.098605", "exception": false, "start_time": "2024-01-31T00:37:02.090354", "status": "completed"}
# ### Part 1. Load Data:  Sweep-Credit-Supply

# %% [markdown] papermill={"duration": 0.003533, "end_time": "2024-01-31T00:37:02.105686", "exception": false, "start_time": "2024-01-31T00:37:02.102153", "status": "completed"}
# Load simulation data and set index to `days_passed`, backfill (for initial timesteps) and replace nan with 0.

# %% papermill={"duration": 0.032844, "end_time": "2024-01-31T00:37:02.141933", "exception": false, "start_time": "2024-01-31T00:37:02.109089", "status": "completed"}
df = pd.read_pickle('../data/simulations/sweep_credit_supply-2023-12-21_22-37-37.pkl.gz').set_index('days_passed').bfill().fillna(0)
df.head()

# %% papermill={"duration": 0.015682, "end_time": "2024-01-31T00:37:02.161396", "exception": false, "start_time": "2024-01-31T00:37:02.145714", "status": "completed"}
df.shape

# %% [markdown] papermill={"duration": 0.003629, "end_time": "2024-01-31T00:37:02.168763", "exception": false, "start_time": "2024-01-31T00:37:02.165134", "status": "completed"}
# ### AB Test Block Utilization

# %% papermill={"duration": 0.466071, "end_time": "2024-01-31T00:37:02.638535", "exception": false, "start_time": "2024-01-31T00:37:02.172464", "status": "completed"}
fig = ab_block_utilization(df.reset_index(), experiment='Sweep Credit Supply')
pio.show(fig)

# %% papermill={"duration": 0.062185, "end_time": "2024-01-31T00:37:02.707705", "exception": false, "start_time": "2024-01-31T00:37:02.645520", "status": "completed"}
fig.write_image('test.png')

# %% papermill={"duration": 0.133901, "end_time": "2024-01-31T00:37:02.846185", "exception": false, "start_time": "2024-01-31T00:37:02.712284", "status": "completed"}
chart = df.hvplot.line(x='days_passed', y='circulating_supply', by=['environmental_label','label'], title='Circulating Supply', height=500, width=1400)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.134467, "end_time": "2024-01-31T00:37:02.986172", "exception": false, "start_time": "2024-01-31T00:37:02.851705", "status": "completed"}
chart = df.hvplot.line(x='days_passed', y='operator_pool_shares', by=['environmental_label','label'], title='Operator Pool Share', height=500, width=1400)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.131796, "end_time": "2024-01-31T00:37:03.124255", "exception": false, "start_time": "2024-01-31T00:37:02.992459", "status": "completed"}
chart = df.hvplot.line(x='days_passed', y='nominator_pool_shares', by=['environmental_label','label'], title='Nominator Pool Share', height=500, width=1400)
pio.show(hv.render(chart, backend='plotly'))

# %% [markdown] papermill={"duration": 0.008279, "end_time": "2024-01-31T00:37:03.141731", "exception": false, "start_time": "2024-01-31T00:37:03.133452", "status": "completed"}
# Create a normalized version of the simulation data for exploring the results. This will allow us to see all stocks in the range of 0-1.

# %% papermill={"duration": 0.02756, "end_time": "2024-01-31T00:37:03.178050", "exception": false, "start_time": "2024-01-31T00:37:03.150490", "status": "completed"}
# Take numeric columns for normalizationn
df_numeric = df.select_dtypes(include=['number'])

# Create the normalized results
df_normalized = df_numeric / df_numeric.max()

# Add the label column back
df_normalized[['label', 'environmental_label']] = df[['label', 'environmental_label']]

# Drop unecessary columns
df_normalized = df_normalized.drop(['run', 'timestep', 'simulation', 'subset', 'timestep_in_days', 'block_time_in_seconds', 'sum_of_stocks', 'buffer_size'], axis=1)
df_normalized.shape

# %% [markdown] papermill={"duration": 0.006754, "end_time": "2024-01-31T00:37:03.191707", "exception": false, "start_time": "2024-01-31T00:37:03.184953", "status": "completed"}
# Groupby Label

# %% papermill={"duration": 0.664736, "end_time": "2024-01-31T00:37:03.863219", "exception": false, "start_time": "2024-01-31T00:37:03.198483", "status": "completed"}
df_normalized.hvplot.line(x='days_passed', groupby='label', by='environmental_label')

# %% [markdown] papermill={"duration": 0.013354, "end_time": "2024-01-31T00:37:03.890737", "exception": false, "start_time": "2024-01-31T00:37:03.877383", "status": "completed"}
# Groupby Environmental Label

# %% papermill={"duration": 0.605244, "end_time": "2024-01-31T00:37:04.511034", "exception": false, "start_time": "2024-01-31T00:37:03.905790", "status": "completed"}
df_normalized.hvplot.line(x='days_passed', groupby='environmental_label', by='label')

# %% [markdown] papermill={"duration": 0.018205, "end_time": "2024-01-31T00:37:04.547546", "exception": false, "start_time": "2024-01-31T00:37:04.529341", "status": "completed"}
# Isolate columns that differ over the parameter sets.

# %% papermill={"duration": 0.03883, "end_time": "2024-01-31T00:37:04.604288", "exception": false, "start_time": "2024-01-31T00:37:04.565458", "status": "completed"}
# Group by 'days_past` to see if there is variation across labels per day
differing_values = df_normalized.groupby('days_passed').nunique()

# Take columns that have any day where values are varied across labels.
df_differing_columns = df_normalized[list(differing_values.columns[differing_values.gt(1).any()])].reset_index()
df_differing_columns.shape

# %% [markdown] papermill={"duration": 0.018938, "end_time": "2024-01-31T00:37:04.641673", "exception": false, "start_time": "2024-01-31T00:37:04.622735", "status": "completed"}
# Group by label. Each label represents a parameter set for AB testing.

# %% papermill={"duration": 0.414546, "end_time": "2024-01-31T00:37:05.088966", "exception": false, "start_time": "2024-01-31T00:37:04.674420", "status": "completed"}
chart = df_differing_columns.reset_index().hvplot(
    x="days_passed", 
    y=[col for col in df_differing_columns.columns if "supply" in col],
    width=1000, height=500, row='label',col='environmental_label', title='SSC Supply')

pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.032199, "end_time": "2024-01-31T00:37:05.139678", "exception": false, "start_time": "2024-01-31T00:37:05.107479", "status": "completed"}
labels = list(df_differing_columns['label'].unique())


# %% papermill={"duration": 0.032844, "end_time": "2024-01-31T00:37:05.191203", "exception": false, "start_time": "2024-01-31T00:37:05.158359", "status": "completed"}
labels

# %% papermill={"duration": 0.034253, "end_time": "2024-01-31T00:37:05.243832", "exception": false, "start_time": "2024-01-31T00:37:05.209579", "status": "completed"}
environmental_labels = list(df_differing_columns['environmental_label'].unique())
environmental_labels

# %% papermill={"duration": 0.406834, "end_time": "2024-01-31T00:37:05.669730", "exception": false, "start_time": "2024-01-31T00:37:05.262896", "status": "completed"}
chart = df_differing_columns.reset_index().hvplot(
    x="days_passed", 
    y=[col for col in df_differing_columns.columns if "shares" in col],
    width=1000, height=500, row='label',col='environmental_label', title='Pool Shares')

pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.793468, "end_time": "2024-01-31T00:37:06.483332", "exception": false, "start_time": "2024-01-31T00:37:05.689864", "status": "completed"}
chart = df_differing_columns.reset_index().hvplot(
    x="days_passed", 
    y=[col for col in df_differing_columns.columns if "_balance" in col],
    width=1000, height=500, row='label',col='environmental_label', title='Balances')

pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.311236, "end_time": "2024-01-31T00:37:06.815860", "exception": false, "start_time": "2024-01-31T00:37:06.504624", "status": "completed"}
chart = df_differing_columns.reset_index().hvplot(
    x="days_passed", 
    y=[col for col in df_differing_columns.columns if "volume" in col],
    width=1000, height=500, row='label',col='environmental_label', title='Compute and Storage Fee Volume')

pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 1.788468, "end_time": "2024-01-31T00:37:08.626615", "exception": false, "start_time": "2024-01-31T00:37:06.838147", "status": "completed"}
chart = df_differing_columns.hvplot(x='days_passed', row='label', col='environmental_label', height=1000, width=1400, ylim=(0,1))
pio.show(hv.render(chart, backend='plotly'))

# %% [markdown] papermill={"duration": 0.026889, "end_time": "2024-01-31T00:37:08.681257", "exception": false, "start_time": "2024-01-31T00:37:08.654368", "status": "completed"}
# Create a long form dataframe.

# %% papermill={"duration": 0.048779, "end_time": "2024-01-31T00:37:08.756015", "exception": false, "start_time": "2024-01-31T00:37:08.707236", "status": "completed"}
long_df = df_differing_columns.reset_index().melt(id_vars=['days_passed', 'label', 'environmental_label'], var_name='State', value_name='Value')
long_df

# %% papermill={"duration": 0.15, "end_time": "2024-01-31T00:37:08.932763", "exception": false, "start_time": "2024-01-31T00:37:08.782763", "status": "completed"}
chart = long_df.hvplot.line(
    x='days_passed', 
    y='Value', 
    by=['label', 'environmental_label'], 
    groupby='State',
)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.145412, "end_time": "2024-01-31T00:37:09.106061", "exception": false, "start_time": "2024-01-31T00:37:08.960649", "status": "completed"}
chart = long_df[long_df['State'].isin(['fund_balance', 'storage_fee_volume', 'block_reward'])].hvplot(x='days_passed', y='Value', groupby='State', by=['label', 'environmental_label'])
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.485485, "end_time": "2024-01-31T00:37:09.619141", "exception": false, "start_time": "2024-01-31T00:37:09.133656", "status": "completed"}
chart = long_df[long_df['State'].isin(['fund_balance', 'storage_fee_volume', 'block_reward'])].hvplot(x='days_passed', y='Value',  by=['environmental_label','label', 'State'], subplots=True)
pio.show(hv.render(chart, backend='plotly'))

# %% papermill={"duration": 0.047644, "end_time": "2024-01-31T00:37:09.700224", "exception": false, "start_time": "2024-01-31T00:37:09.652580", "status": "completed"}
y = ['circulating_supply', 'user_supply', 'issued_supply', 'staking_pool_balance', 'fund_balance', 'burnt_balance', 'reward_issuance_balance', 'farmers_balance', 'holders_balance', 'storage_fee_volume', 'space_pledged', 'history_size', 'replication_factor']

# %% papermill={"duration": 0.0513, "end_time": "2024-01-31T00:37:09.783580", "exception": false, "start_time": "2024-01-31T00:37:09.732280", "status": "completed"}
long_df[long_df['State'].isin(y)]

# %% papermill={"duration": 0.087587, "end_time": "2024-01-31T00:37:09.903475", "exception": false, "start_time": "2024-01-31T00:37:09.815888", "status": "completed"}
hvplot.extension('bokeh')
def plot_column(df: pd.DataFrame, column: str):
    df = df.reset_index().groupby(['environmental_label', 'label', 'days_passed']).mean().reset_index()
    chart = df.hvplot.line(y=column, by=['environmental_label', 'label'], x='days_passed', alpha=0.8, line_width=4, height=200, width=900)
    return chart


# %% papermill={"duration": 0.523797, "end_time": "2024-01-31T00:37:10.460053", "exception": false, "start_time": "2024-01-31T00:37:09.936256", "status": "completed"}
charts_dict = {column: plot_column(df_differing_columns, column) for column in df_differing_columns.columns}

# %% papermill={"duration": 3.663909, "end_time": "2024-01-31T00:37:14.161036", "exception": false, "start_time": "2024-01-31T00:37:10.497127", "status": "completed"}
holomap = hv.HoloMap(charts_dict)
grid = hv.GridSpace(holomap)
layout = hv.NdLayout(grid)
layout = layout.cols(2)
layout

# %% papermill={"duration": 1.203546, "end_time": "2024-01-31T00:37:15.429516", "exception": false, "start_time": "2024-01-31T00:37:14.225970", "status": "completed"}
pio.show(hv.render(layout, backend='plotly'))

# %% papermill={"duration": 0.076058, "end_time": "2024-01-31T00:37:15.579884", "exception": false, "start_time": "2024-01-31T00:37:15.503826", "status": "completed"}
