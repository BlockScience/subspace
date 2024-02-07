import holoviews as hv
import hvplot.pandas
import matplotlib.pyplot as plt
import pandas as pd
import plotly
import plotly.express as px
import seaborn as sns

from subspace_model.experiments.metrics import window_volatility
from subspace_model.util import get_hex_colors_from_matplotlib_cmap


def ab_circulating_supply(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    fig = px.line(
        sim_df,
        x="days_passed",
        y="circulating_supply",
        title=f"{experiment} - AB Test Circulating Supply",
    )
    return fig


def ab_operator_pool_shares(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    fig = px.line(
        sim_df,
        x="days_passed",
        y="operator_pool_shares",
        title=f"{experiment} - AB Test Operator Pool Shares",
    )
    return fig


def ab_nominator_pool_shares(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    fig = px.line(
        sim_df,
        x="days_passed",
        y="nominator_pool_shares",
        title=f"{experiment} - AB Test Nominator Pool Shares",
    )
    return fig


def ab_block_utilization(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    """
    Returns a plotly figure. Show in jupyter with pio.show(fig)
    """
    chart = sim_df.hvplot.line(
        x="days_passed",
        y="block_utilization",
        by=["environmental_label", "label"],
        title=f"{experiment} - AB Test Block Utilization",
        height=500,
        width=1400,
    )
    fig = plotly.graph_objects.Figure(hv.render(chart, backend="plotly"))
    return fig


def ab_circulating_supply_volatility(
    sim_df: pd.DataFrame, experiment: str
) -> plotly.graph_objects.Figure:
    lst = []
    for i, g_df in sim_df.set_index(["label", "run", "days_passed"]).groupby("run"):
        s = window_volatility(g_df.circulating_supply.diff()).reset_index()
        lst.append(s)

    sim_df = pd.concat(lst).dropna()
    fig = px.line(
        sim_df,
        x="days_passed",
        y="circulating_supply",
        title=f"{experiment} - AB Test Windowed Volatility of Circulating Supply",
    )
    return fig


def ssc_metrics(sim_df: pd.DataFrame, experiment: str) -> hv.core.overlay.NdOverlay:
    # Ensure numeric types for plotly
    for col in sim_df.columns:
        if "supply" in col or col == "sum_of_stocks":
            sim_df[col] = pd.to_numeric(sim_df[col], errors="coerce")
    chart = sim_df.hvplot(
        x="days_passed",
        y=[col for col in sim_df.columns if "supply" in col or col == "sum_of_stocks"],
        title="SSC Metrics",
        logy=True,
        ylabel="SSC Value",
        width=1000,
        height=500,
    )

    return chart


def aggregate_staking_pool_share_composition(
    sim_df: pd.DataFrame, experiment: str
) -> hv.core.overlay.NdOverlay:
    chart = sim_df.hvplot(
        x="days_passed",
        y=[el for el in sim_df.columns if "shares" in el],
        title="Aggregate Staking Pool share composition",
        logy=True,
        ylabel="SSC Value",
        width=1000,
        height=500,
    )

    return chart


def ssc_stock_composition(
    sim_df: pd.DataFrame, experiment: str
) -> hv.core.overlay.NdOverlay:
    chart = sim_df.hvplot(
        x="days_passed",
        y=[c for c in sim_df.columns if "_balance" in c],
        title="SSC Stock Composition",
        logy=True,
        ylabel="SSC Value",
        width=1000,
        height=500,
    )
    return chart


def total_fee_volume_per_day(
    sim_df: pd.DataFrame, experiment: str
) -> hv.core.overlay.NdOverlay:
    chart = sim_df.hvplot(
        x="days_passed",
        y=[el for el in sim_df.columns if "volume" in el],
        title="Total Fee Volume per Day",
        logy=True,
        width=1000,
        height=500,
    )
    return chart


def environmental_processes(
    sim_df: pd.DataFrame, experiment: str
) -> hv.core.overlay.NdOverlay:
    # Columns of Interest
    columns = [el for el in sim_df.columns if "average" in el]

    # Get hex colors
    colors = get_hex_colors_from_matplotlib_cmap(n=len(columns), cmap_name="tab10")

    chart = sim_df.hvplot.line(
        x="days_passed",
        y=[el for el in sim_df.columns if "average" in el],
        logy=True,
        color=colors,
        by="variable",
        width=1000,
        height=500,
        title="Environmental Processes",
    )

    return chart


def blockchain_size(sim_df: pd.DataFrame, experiment: str) -> hv.core.overlay.NdOverlay:
    chart = sim_df.hvplot.line(
        x="days_passed",
        y=["blockchain_history_size", "total_space_pledged"],
        logy=True,
        width=1000,
        height=500,
        title="Blockchain Size",
        ylabel="Bytes",
    )
    return chart


def block_utilization(sim_df: pd.DataFrame, experiment: str) -> hv.element.chart.Curve:
    chart = sim_df.hvplot.line(
        x="days_passed",
        y=["block_utilization"],
        width=1000,
        height=500,
        title="Block Utilization",
    )
    return chart


def non_negative_profits(
    profit1_timestep_df: pd.DataFrame,
) -> hv.core.overlay.NdOverlay:
    chart = (
        profit1_timestep_df.loc[:, (profit1_timestep_df >= 0).all()]
        .reset_index()
        .hvplot.line(
            x="days_passed",
            logy=True,
            width=1000,
            height=500,
            title="Non Negative Profits",
        )
    )
    return chart


def negative_profits(profit1_timestep_df: pd.DataFrame) -> hv.element.chart.Curve:
    chart = (
        profit1_timestep_df.loc[:, (profit1_timestep_df < 0).any()]
        .reset_index()
        .hvplot.line(
            x="days_passed", logy=True, width=1000, height=500, title="Negative Profits"
        )
    )
    return chart


def holomap_selector_curve(
    profit1_timestep_df: pd.DataFrame,
) -> hv.core.overlay.NdOverlay:
    curve_dict = {
        column: profit1_timestep_df.reset_index()
        .groupby(["label", "environmental_label", "days_passed"])
        .mean()
        .reset_index()
        .hvplot.line(
            y=column,
            by=["label", "environmental_label"],
            x="days_passed",
            width=1000,
            height=500,
        )
        .opts(title=column)
        for column in profit1_timestep_df.columns
    }
    holomap = hv.HoloMap(curve_dict)
    return holomap


def holomap_selector_box(
    profit1_timestep_df: pd.DataFrame,
) -> hv.core.overlay.NdOverlay:
    def plot_quantile(df, column):
        plot = (
            df.reset_index()
            .groupby(["label", "environmental_label", "days_passed"])
            .mean()
            .reset_index()
            .hvplot.box(y=column, by=["label", "environmental_label"])
            .opts(title=column)
        )
        return plot

    curve_dict = {
        column: plot_quantile(profit1_timestep_df, column)
        for column in profit1_timestep_df.columns
    }
    holomap = hv.HoloMap(curve_dict)
    return holomap


def circulating_supply_volatility(
    sim_df: pd.DataFrame, experiment: str
) -> hv.core.overlay.NdOverlay:
    s = window_volatility(
        sim_df.set_index("days_passed").circulating_supply.diff()
    ).reset_index()

    chart = s.hvplot.line(
        x="days_passed",
        y="circulating_supply",
        title="Circulating Supply Volatility (z-score on weekly standard deviation)",
        width=1000,
        height=500,
    )

    return chart


def weekly_rewards_to_nominators(
    sim_df: pd.DataFrame, experiment: str
) -> hv.core.overlay.NdOverlay:
    n_days = 7
    fig_df = sim_df.set_index("days_passed")
    s = (
        fig_df.rewards_to_nominators.rolling(n_days).sum()
        / fig_df.circulating_supply.rolling(n_days).mean()
    )
    chart = s.hvplot.line(
        title="Weekly Rewards to Nominators (% of Circ Supply per day)",
        ylabel="Weekly Rewards to Nominators (% of Circulating Supply)",
        height=500,
        width=1000,
        yformatter="%.2f%%",
    )

    return chart


def weekly_issuance_rate(
    sim_df: pd.DataFrame, experiment: str
) -> hv.core.overlay.NdOverlay:
    n = 7
    fig_df = sim_df.set_index("days_passed")
    s = fig_df.reward_issuance_balance.diff() * -1.0
    s /= fig_df.max_credit_supply
    s = s.rolling(n).sum()[n - 1 :: n]
    chart = s.hvplot(
        x="days_passed",
        y="reward_issuance_balance",
        title="Weekly Reward Issuance Rate",
        ylabel="% of Max Credit Supply ",
        yformatter="%.8f%%",
        height=500,
        width=1000,
    )
    return chart


def cumulative_issuance_rate(
    sim_df: pd.DataFrame, experiment: str
) -> hv.core.overlay.NdOverlay:
    n = 7
    fig_df = sim_df.set_index("days_passed")
    s = fig_df.reward_issuance_balance.diff() * -1.0
    s /= fig_df.max_credit_supply
    s = s.cumsum()

    chart = s.hvplot(
        x="days_passed",
        y="reward_issuance_balance",
        title="Cumulative Reward Issuance Rate",
        ylabel="% of Max Credit Supply ",
        yformatter="%.8f%%",
        height=500,
        width=1000,
    )
    return chart


# def default_metrics(sim_df: pd.DataFrame, experiment: str) -> plotly.graph_objects.Figure:
