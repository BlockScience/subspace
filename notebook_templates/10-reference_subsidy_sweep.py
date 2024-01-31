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

# %% [markdown] papermill={"duration": 0.006216, "end_time": "2024-01-31T00:37:29.330007", "exception": false, "start_time": "2024-01-31T00:37:29.323791", "status": "completed"}
# # Subspace Digital Twin, Initial Conditions Run
#
# *Shawn Anderson, January 2024*
#
# In this notebook, we examine medianl behavior over the first 90 days.

# %% [markdown] papermill={"duration": 0.004427, "end_time": "2024-01-31T00:37:29.342035", "exception": false, "start_time": "2024-01-31T00:37:29.337608", "status": "completed"}
# ## Part 1. Dependences & Set-up

# %% [markdown] papermill={"duration": 0.002372, "end_time": "2024-01-31T00:37:29.347022", "exception": false, "start_time": "2024-01-31T00:37:29.344650", "status": "completed"}
# Autoreload modules while developing.

# %% papermill={"duration": 1.402484, "end_time": "2024-01-31T00:37:30.751861", "exception": false, "start_time": "2024-01-31T00:37:29.349377", "status": "completed"}
# %load_ext autoreload
# %autoreload 2

import sys
sys.path.append('../')

import numpy as np
import pandas as pd
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

import hvplot.pandas
hvplot.extension('bokeh')

from bokeh.models import HoverTool
import holoviews as hv

from bokeh.palettes import Turbo256, Category20

from subspace_model.util import g

# %% [markdown] papermill={"duration": 0.007342, "end_time": "2024-01-31T00:37:30.762917", "exception": false, "start_time": "2024-01-31T00:37:30.755575", "status": "completed"}
# ## Part 2. Load Simulation Data

# %% [markdown] papermill={"duration": 0.003634, "end_time": "2024-01-31T00:37:30.771089", "exception": false, "start_time": "2024-01-31T00:37:30.767455", "status": "completed"}
# Load the simulation results data.

# %% papermill={"duration": 0.01675, "end_time": "2024-01-31T00:37:30.791167", "exception": false, "start_time": "2024-01-31T00:37:30.774417", "status": "completed"}
sim_df = pd.read_pickle(
    "../data/simulations/reference_subsidy_sweep-2024-01-30_11-07-21.pkl.gz"
).drop(['timestep', 'simulation', 'subset', 'timestep_in_days', 'block_time_in_seconds', 'delta_days', 'delta_blocks'], axis=1)

# %% papermill={"duration": 0.043776, "end_time": "2024-01-31T00:37:30.838477", "exception": false, "start_time": "2024-01-31T00:37:30.794701", "status": "completed"}
sim_df.head(5)

# %% [markdown] papermill={"duration": 0.003682, "end_time": "2024-01-31T00:37:30.848336", "exception": false, "start_time": "2024-01-31T00:37:30.844654", "status": "completed"}
# Simulation Runs.

# %% papermill={"duration": 0.01825, "end_time": "2024-01-31T00:37:30.870234", "exception": false, "start_time": "2024-01-31T00:37:30.851984", "status": "completed"}
sim_df.groupby(['run', 'label', 'environmental_label']).size().reset_index(name='Days').head()

# %% [markdown] papermill={"duration": 0.004013, "end_time": "2024-01-31T00:37:30.879600", "exception": false, "start_time": "2024-01-31T00:37:30.875587", "status": "completed"}
# ### Coloring Metrics
# Use a constant mapping from columns to colors

# %% papermill={"duration": 0.132155, "end_time": "2024-01-31T00:37:31.015368", "exception": false, "start_time": "2024-01-31T00:37:30.883213", "status": "completed"}
color_palette = Category20
# columns_to_color = sorted(list(set(sim_df.columns) - {'environmental_label', 'label', 'run', 'blocks_passed', 'days_passed'}))
columns_to_color = sim_df.columns
if color_palette == Turbo256:
    column_colors = dict(zip(columns_to_color, [color_palette[int(i)] for i in np.linspace(0,len(color_palette)-1, len(columns_to_color))]))

if color_palette == Category20:
    column_colors = {col: Category20[20][i%20] for i, col in enumerate(columns_to_color)}


sim_df.count().to_frame().T.hvplot.bar(y=columns_to_color, color=[column_colors[c] for c in columns_to_color], rot=90, width=1400, height=500, title='Column Color Map', fontscale=1.4, yaxis=None)


# %% papermill={"duration": 0.022351, "end_time": "2024-01-31T00:37:31.041750", "exception": false, "start_time": "2024-01-31T00:37:31.019399", "status": "completed"}
def snake_to_title(s):
    """Utility function used for printing chart titles and labels as Title Case.
    Example:
    snake_to_caps('snake_case')
    >>> 'Snake Case'
    """
    
    return ' '.join(word.capitalize() for word in s.split('_'))

def fan_chart_quantile_median(df, column='circulating_supply', median_only=False):
    """Combine an area chart of min-max and a line chart of median for a series."""

    # min, max, median
    fan_df = df.groupby('days_passed')[column].agg(['min', 'max', 'median'])

    opts = dict(width=1200, height=500, title=f'{snake_to_title(column)} Fan Chart', ylabel=f'{column}_min_max_median')

    # Median curve
    hover = HoverTool(tooltips=[(f'{snake_to_title(column)} Median', '@median{0,0.00}')])
    median_chart = fan_df.hvplot(x='days_passed', y='median', alpha=1, line_width=4, label=f'{snake_to_title(column)} Median', tools=[hover], color=column_colors[column]).opts(**opts)
    if median_only:
        return median_chart

    # min-max band
    hover = HoverTool(tooltips=[(f'{snake_to_title(column)} Days Passed', '$x{0,0}')])
    bands_chart = fan_df.hvplot.area(x='days_passed', y='min', y2='max', legend='top_left', alpha=0.4, tools=[hover], ylim=(0,None), color=column_colors[column]).opts(**opts)

    # Composition
    chart = bands_chart * median_chart
    return chart


def fan_chart_quantile(df, column='circulating_supply', median_only=False):
    """Combine an area chart of min-max and a line chart of quantile for a series."""

    # 25%, 50%, 75%
    fan_df = df.groupby('days_passed')[column].quantile([0.25, 0.5, 0.75]).unstack().rename(columns={0.50:'median', 0.25:'0.25',0.75:'0.75'})

    # return fan_df

    opts = dict(width=1200, height=500, title=f'{snake_to_title(column)} Quantile Fan Chart', ylabel=f'{column}_quantile')

    # Quantile curve
    hover = HoverTool(tooltips=[(f'{snake_to_title(column)} Median', '@median{0,0.00}')])
    quatile_chart = fan_df.hvplot(x='days_passed', y='median', alpha=1, line_width=4, label=f'{snake_to_title(column)} Quantile', tools=[hover], color=column_colors[column]).opts(**opts)
    if median_only:
        return quatile_chart

    # min-max band
    hover = HoverTool(tooltips=[(f'{snake_to_title(column)} Days Passed', '$x{0,0}')])
    bands_chart = fan_df.hvplot.area(x='days_passed', y='0.25', y2='0.75', legend='top_left', alpha=0.4, tools=[hover], ylim=(0,None), color=column_colors[column]).opts(**opts)

    # Composition
    chart = bands_chart * quatile_chart
    return chart



# %% [markdown] papermill={"duration": 0.003877, "end_time": "2024-01-31T00:37:31.049879", "exception": false, "start_time": "2024-01-31T00:37:31.046002", "status": "completed"}
# ### KPIs

# %% papermill={"duration": 0.01453, "end_time": "2024-01-31T00:37:31.068276", "exception": false, "start_time": "2024-01-31T00:37:31.053746", "status": "completed"}
sim_df['issuance'] = sim_df['block_reward'] + sim_df['reference_subsidy']

sim_df['fees'] = sim_df['compute_fee_volume'] + sim_df['storage_fee_volume']

fees_and_issuance = ['compute_fee_volume','storage_fee_volume', 'fees', 'block_reward', 'reference_subsidy', 'issuance']

# %% papermill={"duration": 0.014772, "end_time": "2024-01-31T00:37:31.086966", "exception": false, "start_time": "2024-01-31T00:37:31.072194", "status": "completed"}
# Compute Fees and Storage Fees

# The dynamics of storage fees vs issuance. Who will dominate at the beginning, storage fees or issues rewards? Note that this is a metric.
# Another metrics of interest, general revenue per timestep, farmers, proposers, voters, and data blocks
# revenue = proposer_reward + storage_fees. For data blocks and voters you only have rewards not fees. Farmers is the sum of those three.
# The above topics are what has been discussed and therefor are higher priority than the stocks. 

# %% papermill={"duration": 0.124681, "end_time": "2024-01-31T00:37:31.215460", "exception": false, "start_time": "2024-01-31T00:37:31.090779", "status": "completed"}
color_palette = Category20
# columns_to_color = sorted(list(set(sim_df.columns) - {'environmental_label', 'label', 'run', 'blocks_passed', 'days_passed'}))
columns_to_color = sim_df.columns
if color_palette == Turbo256:
    column_colors = dict(zip(columns_to_color, [color_palette[int(i)] for i in np.linspace(0,len(color_palette)-1, len(columns_to_color))]))

if color_palette == Category20:
    column_colors = {col: Category20[20][i%20] for i, col in enumerate(columns_to_color)}


sim_df.count().to_frame().T.hvplot.bar(y=columns_to_color, color=[column_colors[c] for c in columns_to_color], rot=90, width=1400, height=500, title='Column Color Map', fontscale=1.4, yaxis=None)

# %% [markdown] papermill={"duration": 0.007487, "end_time": "2024-01-31T00:37:31.230512", "exception": false, "start_time": "2024-01-31T00:37:31.223025", "status": "completed"}
# ### Balances and Supplies

# %% papermill={"duration": 0.015998, "end_time": "2024-01-31T00:37:31.251164", "exception": false, "start_time": "2024-01-31T00:37:31.235166", "status": "completed"}
system_balances = ['other_issuance_balance', 'reward_issuance_balance']
agent_balances = [
    'farmers_balance',
    'operators_balance',
    'nominators_balance',
    'holders_balance',
]
agent_pool_balances = ['staking_pool_balance']
protocol_treasury_balances = ['fund_balance']
other_balances = list(set([c for c in sim_df.columns if 'balance' in c]) - set(system_balances + agent_balances + agent_pool_balances + protocol_treasury_balances) )
supply_columns = list({c for c in sim_df.columns if 'supply' in c} - {'max_credit_supply', 'issued_supply', 'total_supply'})
balance_columns = list(set([c for c in sim_df.columns if 'balance' in c]) - set(system_balances))

# %% papermill={"duration": 0.014246, "end_time": "2024-01-31T00:37:31.270740", "exception": false, "start_time": "2024-01-31T00:37:31.256494", "status": "completed"}
system_balances

# %% papermill={"duration": 0.013729, "end_time": "2024-01-31T00:37:31.288512", "exception": false, "start_time": "2024-01-31T00:37:31.274783", "status": "completed"}
agent_balances

# %% papermill={"duration": 0.014164, "end_time": "2024-01-31T00:37:31.306725", "exception": false, "start_time": "2024-01-31T00:37:31.292561", "status": "completed"}
agent_pool_balances

# %% papermill={"duration": 0.013745, "end_time": "2024-01-31T00:37:31.325191", "exception": false, "start_time": "2024-01-31T00:37:31.311446", "status": "completed"}
protocol_treasury_balances

# %% papermill={"duration": 0.014175, "end_time": "2024-01-31T00:37:31.343747", "exception": false, "start_time": "2024-01-31T00:37:31.329572", "status": "completed"}
other_balances

# %% papermill={"duration": 0.013757, "end_time": "2024-01-31T00:37:31.361847", "exception": false, "start_time": "2024-01-31T00:37:31.348090", "status": "completed"}
supply_columns

# %% papermill={"duration": 0.014413, "end_time": "2024-01-31T00:37:31.380437", "exception": false, "start_time": "2024-01-31T00:37:31.366024", "status": "completed"}
balance_columns

# %% papermill={"duration": 0.014648, "end_time": "2024-01-31T00:37:31.399373", "exception": false, "start_time": "2024-01-31T00:37:31.384725", "status": "completed"}
balance_columns

# %% papermill={"duration": 0.014591, "end_time": "2024-01-31T00:37:31.418581", "exception": false, "start_time": "2024-01-31T00:37:31.403990", "status": "completed"}
supply_columns

# %% papermill={"duration": 0.014276, "end_time": "2024-01-31T00:37:31.437217", "exception": false, "start_time": "2024-01-31T00:37:31.422941", "status": "completed"}
fees_and_issuance

# %% papermill={"duration": 0.013831, "end_time": "2024-01-31T00:37:31.455649", "exception": false, "start_time": "2024-01-31T00:37:31.441818", "status": "completed"}
# balance_columns = fees_and_issuance
# balance_columns = supply_columns

# %% papermill={"duration": 0.018626, "end_time": "2024-01-31T00:37:31.478722", "exception": false, "start_time": "2024-01-31T00:37:31.460096", "status": "completed"}
box_df = sim_df.set_index(['days_passed', 'label'])[balance_columns]
box_df

# %% papermill={"duration": 0.020693, "end_time": "2024-01-31T00:37:31.504000", "exception": false, "start_time": "2024-01-31T00:37:31.483307", "status": "completed"}
describe_df = box_df.describe().drop('count')
describe_df

# %% papermill={"duration": 0.030261, "end_time": "2024-01-31T00:37:31.538895", "exception": false, "start_time": "2024-01-31T00:37:31.508634", "status": "completed"}
describe_labels_df = box_df.groupby('label').apply(lambda label: label.describe().drop('count'))
describe_labels_df

# %% papermill={"duration": 0.043875, "end_time": "2024-01-31T00:37:31.587778", "exception": false, "start_time": "2024-01-31T00:37:31.543903", "status": "completed"}
describe_difference_df = pd.DataFrame(describe_labels_df.values - pd.concat([describe_df for i in range(sim_df['label'].nunique())]).values, columns=describe_labels_df.columns, index=describe_labels_df.index)
df = describe_difference_df

def log_scale(val, max_abs_log):
    """ Apply logarithmic scaling to a value. """
    if val == 0:
        return 0
    else:
        return np.sign(val) * np.log(abs(val) + 1) / max_abs_log

def color_scale(val):
    max_abs_val = df.abs().max().max()
    max_abs_log = np.log(max_abs_val + 1)

    scaled_val = log_scale(val, max_abs_log)

    if scaled_val < 0:
        intensity = int(255 * (1 + scaled_val))  # More negative, more red
        return f'background-color: rgb(255, {intensity}, {intensity})'
    elif scaled_val > 0:
        intensity = int(255 * (1 - scaled_val))  # More positive, more green
        return f'background-color: rgb({intensity}, 255, {intensity})'
    else:
        return 'background-color: rgb(255, 255, 255)'

header_styles = [{
    'selector': f'th.col_heading.level0.col{i}',
    'props': [('background-color', column_colors.get(col))]
} for i, col in enumerate(df.columns)]

df.columns.name = 'balance'

describe_difference_df_styled = df.style.map(color_scale).set_table_styles(header_styles)
describe_difference_df_styled

# %% papermill={"duration": 0.694678, "end_time": "2024-01-31T00:37:32.287748", "exception": false, "start_time": "2024-01-31T00:37:31.593070", "status": "completed"}
box_df_melted = box_df.reset_index().drop('days_passed',axis=1).melt(id_vars=['label'])

violin_list = [label.hvplot.violin(y='value', by='variable', c='variable', legend='top_left', width=1200, height=500, title=f'SSC Balances {name}', cmap=column_colors, ylim=(0,box_df.max().max()*0.75)) for name, label in box_df_melted.groupby('label')]

# Combine plots into a single column layout
layout = hv.Layout(violin_list).cols(1)

layout

# %% papermill={"duration": 0.025703, "end_time": "2024-01-31T00:37:32.320057", "exception": false, "start_time": "2024-01-31T00:37:32.294354", "status": "completed"}
[label for name, label in box_df.reset_index().groupby('label')][0]

# %% papermill={"duration": 1.064872, "end_time": "2024-01-31T00:37:33.391532", "exception": false, "start_time": "2024-01-31T00:37:32.326660", "status": "completed"}
line_list = [hv.Overlay([fan_chart_quantile(label, column) for column in label.columns if column not in ['label', 'days_passed']]).opts(title=f'SSC Balances {name}', legend_opts={'location':'top_left'}) for name, label in box_df.reset_index().groupby('label')]
layout = hv.Layout(line_list).cols(1)
layout

# %% papermill={"duration": 0.812031, "end_time": "2024-01-31T00:37:34.213748", "exception": false, "start_time": "2024-01-31T00:37:33.401717", "status": "completed"}
violin_list = [variable.hvplot.violin(y='value', by='label', color=column_colors[name], width=1200, height=500, title=f'SSC Balances {name}', ylim=(0,variable.max()['value'].max()), ylabel=name) for name, variable in box_df_melted.groupby('variable')]

layout = hv.Layout(violin_list).cols(1).opts(shared_axes=False)

layout

# %% papermill={"duration": 0.513818, "end_time": "2024-01-31T00:37:34.740457", "exception": false, "start_time": "2024-01-31T00:37:34.226639", "status": "completed"}
line_list = [variable.hvplot.line(x='days_passed', by='label', y='value', title=name, legend='top_left', line_width=3).opts(legend_opts={'background_fill_color': column_colors[name], 'background_fill_alpha': 0.2}) for name, variable in box_df.reset_index().melt(id_vars=['label', 'days_passed']).groupby('variable')]

layout = hv.Layout(line_list).cols(2).opts(shared_axes=False)
layout

# %% [markdown] papermill={"duration": 0.01537, "end_time": "2024-01-31T00:37:34.771189", "exception": false, "start_time": "2024-01-31T00:37:34.755819", "status": "completed"}
# Definition (per timestep) storage_fees_per_rewards = state['storage_fee_volume'] / state['block_reward']
#
# We are interested in having the (95%, 50%, 5%) quantile distribution over that metric when taking windows of 1 week, 4 weeks and 12 weeks.

# %% papermill={"duration": 0.134439, "end_time": "2024-01-31T00:37:34.920649", "exception": false, "start_time": "2024-01-31T00:37:34.786210", "status": "completed"}
opts = dict(width=800, height=400)
charts = []
for weeks in [1,4,12]:
    sim_df['storage_fee_per_rewards_q1'] = sim_df['storage_fee_per_rewards'].rolling(7*weeks).quantile(0.05)
    sim_df['storage_fee_per_rewards_q2'] = sim_df['storage_fee_per_rewards'].rolling(7*weeks).quantile(0.50)
    sim_df['storage_fee_per_rewards_q3'] = sim_df['storage_fee_per_rewards'].rolling(7*weeks).quantile(0.95)
    
    fan = sim_df.hvplot.area(x='days_passed', y='storage_fee_per_rewards_q1', y2='storage_fee_per_rewards_q3', by='label', stacked=False, hover=False, legend='bottom_right')
    
    median = sim_df.hvplot.line(x='days_passed', y='storage_fee_per_rewards_q2', by='label', alpha=0.8, line_width=4, ylim=(0,None), title=f'Storage Fee Per Rewards 95% Quantile Rolling {weeks} weeks.', legend='bottom_right')
    chart = fan * median
    charts.append(chart.opts(**opts))

# %% papermill={"duration": 0.368155, "end_time": "2024-01-31T00:37:35.305892", "exception": false, "start_time": "2024-01-31T00:37:34.937737", "status": "completed"}
hv.Layout(charts).cols(3)
