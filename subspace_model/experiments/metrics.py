"""
Metrics that requires the full trajectory dataset in order to be computable
"""
from typing import List

import numpy as np
import pandas as pd

from subspace_model.types import *


def window_volatility(_s: pd.Series) -> pd.Series:
    s = _s.dropna()
    std_s = s.rolling(7).std()
    s_new = (std_s - std_s.mean()) / std_s.std()
    return s_new


def profit1(sim_df: pd.DataFrame) -> pd.DataFrame:
    sim_df = sim_df.set_index('days_passed')
    # Identify the balance columns
    balance_columns = [c for c in sim_df.columns if 'balance' in c]

    # Calculate the difference for each group
    profit1 = (
        sim_df[balance_columns]
        .groupby([sim_df['label'], sim_df['environmental_label']])
        .apply(lambda g: g.diff())
    )

    # Reset the index to flatten the DataFrame
    profit1 = profit1.fillna(0).add_prefix('profit1_')

    return profit1


def average_profit1(sim_df: pd.DataFrame) -> pd.DataFrame:
    # Set the desired multi-level index
    sim_df = sim_df.set_index(['label', 'environmental_label', 'days_passed'])

    # Identify the balance columns
    balance_columns = [c for c in sim_df.columns if 'balance' in c]

    # Calculate the difference and then the mean for each group
    average_profit1 = (
        sim_df[balance_columns]
        .groupby(level=['label', 'environmental_label'])
        .apply(lambda g: g.diff().mean())
    ).add_prefix('average_profit1_')
    return average_profit1
