from glob import glob
from typing import Callable, Dict, List, Tuple, Union

import diskcache as dc
import pandas as pd

cache = dc.Cache('./s3-cache/')

def get_psuu_dataset_from_s3(
        location: str='s3://subspace-simulations/psuu_run-2024-04-24T21:42:42Z/trajectory_tensor.pkl.gz',
        use_cache=True
        )->pd.DataFrame:
    if use_cache and (location in cache):
        print("Loading data from local cache...")
        df = cache[location]
    else:
        print("Loading data from S3 and caching...")
        df = pd.read_pickle(location, compression='gzip')
        cache[location] = df

    if 'index' in df.columns:
        df = df.drop(columns=['index'])

    return df




def get_utility_tensor_from_trajectory_tensor(agg_df: pd.DataFrame, KPI_functions: dict, GOVERNANCE_SURFACE_PARAMS: dict) -> pd.DataFrame:
# Type alias for a Criterion function
    Criterion = Callable[[float, pd.Series], bool]

    def evaluate(x: pd.Series, data: pd.DataFrame, success_criteria: Union[str, Criterion]) -> pd.Series:
        col_name = x.name  # Assuming col_name comes from the Series name
        if isinstance(success_criteria, str):
            if success_criteria == 'smaller_than_median':
                y = data.loc[:, col_name] < data.loc[:, col_name].median()
            elif success_criteria == 'larger_than_median':
                y = data.loc[:, col_name] > data.loc[:, col_name].median()
            else:
                raise Exception('Criteria not specified')
        else:
            y = data[col_name].map(lambda z: success_criteria(z, data[col_name]))
        return y

    utility_dfs: List[pd.DataFrame] = []
    for kpi, (kpi_f, threshold_f) in KPI_functions.items():
        kpi_df = agg_df.reset_index()[[kpi]]
        utility_df = kpi_df.apply(lambda x: evaluate(x, agg_df.reset_index(), threshold_f))
        utility_df.name = kpi
        utility_dfs.append(utility_df)

    utility_df: pd.DataFrame = pd.concat(utility_dfs, axis=1).astype(int)
    utility_df.index = agg_df.reset_index().set_index(GOVERNANCE_SURFACE_PARAMS+['simulation', 'subset', 'run']).index
    utility_df.reset_index(drop=True)
    return utility_df
