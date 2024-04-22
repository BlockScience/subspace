import pandas as pd
import pytest as pt

from subspace_model.experiments.experiment import psuu
from subspace_model.psuu import timestep_tensor_to_trajectory_tensor


@pt.fixture(scope="module", params=[(100, 50, 1), (1000, 2, 1)])
def sim_df(request) -> pd.DataFrame:
    (SIMULATION_DAYS, N_SWEEP_SAMPLES, SAMPLES) = request.param
    return psuu(SIMULATION_DAYS=SIMULATION_DAYS, 
                TIMESTEP_IN_DAYS=1,
                SAMPLES=SAMPLES,
                N_SWEEP_SAMPLES=N_SWEEP_SAMPLES,
                SWEEPS_PER_PROCESS=1,
                PROCESSES=1,
                PARALLELIZE=False,
                USE_JOBLIB=False,
                RETURN_SIM_DF=True)


def test_run(sim_df):
    
    df = sim_df.query('timestep > 0')
    assert df.isnull().sum().sum() == 0

def test_kpi_values(sim_df):
    agg_df = timestep_tensor_to_trajectory_tensor(sim_df)

    # Per-Trajectory Co-Domain Tests
    for i, row in agg_df.iterrows():
        assert row['mean_relative_community_owned_supply'].mean() > 0.01
        assert row['mean_farmer_subsidy_factor'].mean() > 0
        assert row['mean_proposing_rewards_per_newly_pledged_space'].mean() > 0
        assert row['mean_proposer_reward_minus_voter_reward'].mean() > 0
        assert row['cumm_rewards_before_1yr'].mean() > 0
        assert row['abs_sum_storage_fees_per_sum_compute_fees'].mean() > 0
        assert row['cumm_rewards'].mean() > 0

    # Aggregate Co-Domain Tests
    assert agg_df['mean_relative_community_owned_supply'].mean() > 0.01
    assert agg_df['mean_farmer_subsidy_factor'].mean() > 0
    assert agg_df['mean_proposing_rewards_per_newly_pledged_space'].mean() > 0
    assert agg_df['mean_proposer_reward_minus_voter_reward'].mean() > 0
    assert agg_df['cumm_rewards_before_1yr'].mean() > 0
    assert agg_df['abs_sum_storage_fees_per_sum_compute_fees'].mean() > 0
    assert agg_df['cumm_rewards'].mean() > 0


