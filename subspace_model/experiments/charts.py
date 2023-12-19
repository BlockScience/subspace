import matplotlib.pyplot as plt
import pandas as pd
import plotly
import plotly.express as px
import seaborn as sns

from subspace_model.trajectory_metrics import window_volatility


def ab_circulating_supply(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    fig = px.line(
        sim_df,
        x='days_passed',
        y='circulating_supply',
        title=f'{experiment} - AB Test Circulating Supply',
    )
    return fig


def ab_operator_pool_shares(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    fig = px.line(
        sim_df,
        x='days_passed',
        y='operator_pool_shares',
        title=f'{experiment} - AB Test Operator Pool Shares',
    )
    return fig


def ab_nominator_pool_shares(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    fig = px.line(
        sim_df,
        x='days_passed',
        y='nominator_pool_shares',
        title=f'{experiment} - AB Test Nominator Pool Shares',
    )
    return fig


def ab_block_utilization(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    fig = px.line(
        sim_df,
        x='days_passed',
        y='block_utilization',
        title=f'{experiment} - AB Test Block Utilization',
    )
    return fig


def ab_circulating_supply_volatility(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    lst = []
    for i, g_df in sim_df.set_index(['label', 'run', 'days_passed']).groupby('run'):
        s = window_volatility(g_df.circulating_supply.diff()).reset_index()
        lst.append(s)

    sim_df = pd.concat(lst).dropna()
    fig = px.line(
        sim_df,
        x='days_passed',
        y='circulating_supply',
        title=f'{experiment} - AB Test Windowed Volatility of Circulating Supply',
    )
    return fig
