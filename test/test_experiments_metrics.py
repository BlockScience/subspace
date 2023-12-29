import pandas as pd
import pytest

from subspace_model.experiments.experiment import sanity_check_run
from subspace_model.experiments.metrics import (
    profit1_mean,
    profit1_trajectory,
    window_volatility,
)


# Define the fixture
@pytest.fixture(scope='module')
def sim_df_sanity_check():
    return sanity_check_run(SIMULATION_DAYS=70, TIMESTEP_IN_DAYS=1, SAMPLES=1)


def test_window_volatility_circulating_supply(sim_df_sanity_check):
    sim_df = sim_df_sanity_check

    runs = sim_df.set_index(['label', 'run', 'days_passed']).groupby('run')
    lst = []
    for i, g_df in runs:
        s = window_volatility(g_df['circulating_supply'].diff()).reset_index()
        lst.append(s)

    result_df = pd.concat(lst).dropna()

    return result_df


def test_window_volatility_circulating_supply_apply(sim_df_sanity_check):
    sim_df = sim_df_sanity_check

    runs = sim_df.set_index(['label', 'run', 'days_passed']).groupby('run')
    result_df = runs.apply(
        lambda g: window_volatility(g['circulating_supply'].diff()).T.reset_index()
    )

    # Debug: Check the result immediately after apply
    result_df = result_df.reset_index(drop=True)
    result_df = result_df.dropna()

    return result_df


def test_window_volatility_methods(sim_df_sanity_check):
    result_1 = test_window_volatility_circulating_supply(sim_df_sanity_check)
    result_2 = test_window_volatility_circulating_supply_apply(sim_df_sanity_check)
    pd.testing.assert_frame_equal(result_1, result_2, check_dtype=True)


def test_profit1_trajectory(sim_df_sanity_check):
    result = profit1_trajectory(sim_df_sanity_check)
    return result


def test_profit1_mean(sim_df_sanity_check):
    result = profit1_mean(sim_df_sanity_check)
    return result
