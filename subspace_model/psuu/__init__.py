from subspace_model.types import *
import pandas as pd


GOVERNANCE_SURFACE_PARAMS = [
    'component_1_initial_period_start',
    'component_1_initial_period_duration',
    'component_1_max_reference_subsidy',
    'component_1_max_cumulative_subsidy',
    'component_2_initial_period_start',
    'component_2_initial_period_duration',
    'component_2_max_reference_subsidy',
    'component_2_max_cumulative_subsidy',
    'reward_proposer_share',
    'weight_to_fee']


def timestep_tensor_to_trajectory_tensor(sim_df: pd.DataFrame) -> pd.DataFrame:
    i = 0
    sim_df[f'component_{i+1}_initial_period_start'] = sim_df.reference_subsidy_components.map(
        lambda x: x[i].initial_period_start)
    sim_df[f'component_{i+1}_initial_period_duration'] = sim_df.reference_subsidy_components.map(
        lambda x: x[i].initial_period_duration)
    sim_df[f'component_{i+1}_max_cumulative_subsidy'] = sim_df.reference_subsidy_components.map(
        lambda x: x[i].max_cumulative_subsidy)
    sim_df[f'component_{i+1}_max_reference_subsidy'] = sim_df.reference_subsidy_components.map(
        lambda x: x[i].max_reference_subsidy)

    i = 1
    sim_df[f'component_{i+1}_initial_period_start'] = sim_df.reference_subsidy_components.map(
        lambda x: x[i].initial_period_start)
    sim_df[f'component_{i+1}_initial_period_duration'] = sim_df.reference_subsidy_components.map(
        lambda x: x[i].initial_period_duration)
    sim_df[f'component_{i+1}_max_cumulative_subsidy'] = sim_df.reference_subsidy_components.map(
        lambda x: x[i].max_cumulative_subsidy)
    sim_df[f'component_{i+1}_max_reference_subsidy'] = sim_df.reference_subsidy_components.map(
        lambda x: x[i].max_reference_subsidy)

    from subspace_model.params import GOVERNANCE_SURFACE
    governance_surface_params = (set(GOVERNANCE_SURFACE.keys()) | {
                                 c for c in sim_df.columns if 'component' in c}) - {'reference_subsidy_components'}

    trajectory_id_columns = ['simulation', 'subset', 'run']
    agg_columns = trajectory_id_columns + list(governance_surface_params)

    from subspace_model.psuu.kpis import KPI_functions

    kpi_dfs = []
    threshold_dfs = []
    for kpi, (kpi_f, kpi_t) in KPI_functions.items():
        kpi_s = sim_df.groupby(agg_columns).apply(kpi_f, include_groups=False)
        kpi_s.name = kpi
        kpi_dfs.append(kpi_s)

    all_kpi_df = pd.concat(kpi_dfs, axis=1)
    return all_kpi_df
