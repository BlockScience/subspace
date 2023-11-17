"""
Metrics that requires the full trajectory dataset in order to be computable
"""
from subspace_model.types import *
import pandas as pd
import numpy as np

def window_volatility(_s: pd.Series) -> pd.Series:
    s = _s.dropna()
    std_s = s.rolling(7).std()
    s_new = (std_s - std_s.mean()) / std_s.std()
    return s_new