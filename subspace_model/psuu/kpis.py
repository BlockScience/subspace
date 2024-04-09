from subspace_model.psuu.types import *
from subspace_model.types import *
import subspace_model.metrics as m
import numpy as np
from pandera.typing import DataFrame

## KPIs

def per_timestep_average_relative_community_owned_supply(df: DataFrame) -> KPI:
    return (df.community_owned_supply / df.total_supply).mean()


def mean_farmer_subsidy_factor(df: DataFrame) -> KPI:
    pass

def mean_proposing_rewards_per_newly_pledged_space(df: DataFrame) -> KPI:
    pass

def mean_proposer_reward_minus_voter_reward(df: DataFrame) -> KPI:
    return (df['reward_to_proposer'] - df['reward_to_voters']).mean()

def cumm_rewards_before_1yr(df: DataFrame) -> KPI:
    return df.query("days_passed < 366").block_reward.sum()


def abs_sum_storage_fees_per_sum_compute_fees(df: TrajectoryDataFrame) -> KPI:
    pass

def cumm_rewards(df: TrajectoryDataFrame) -> KPI:
    return df.block_reward.sum()

## Thresholds

def larger_than_median_across_trajectories(kpi: KPI, kpi_list: list[KPI]) -> Optional[bool]:
    kpi_median = np.median(kpi_list)
    if kpi > kpi_median:
        return True
    elif kpi < kpi_median:
        return False
    else:
        return None
    

def smaller_than_median_across_trajectories(kpi: KPI, kpi_list: list[KPI]) -> Optional[bool]:
    kpi_median = np.median(kpi_list)
    if kpi < kpi_median:
        return True
    elif kpi > kpi_median:
        return False
    else:
        return None

## PSuU KPI Dict

KPI_functions: dict[str, TrajectoryKPIandThreshold] = {
    'mean_relative_community_owned_supply': TrajectoryKPIandThreshold(per_timestep_average_relative_community_owned_supply, larger_than_median_across_trajectories),
    'mean_farmer_subsidy_factor': TrajectoryKPIandThreshold(mean_farmer_subsidy_factor, smaller_than_median_across_trajectories),
    'mean_proposing_rewards_per_newly_pledged_space': TrajectoryKPIandThreshold(mean_proposing_rewards_per_newly_pledged_space, larger_than_median_across_trajectories),
    'mean_proposer_reward_minus_voter_reward': TrajectoryKPIandThreshold(mean_proposer_reward_minus_voter_reward, larger_than_median_across_trajectories),
    'cumm_rewards_before_1yr': TrajectoryKPIandThreshold(cumm_rewards_before_1yr, larger_than_median_across_trajectories),
    'abs_sum_storage_fees_per_sum_compute_fees': TrajectoryKPIandThreshold(abs_sum_storage_fees_per_sum_compute_fees, smaller_than_median_across_trajectories),
    'cumm_rewards': TrajectoryKPIandThreshold(cumm_rewards, smaller_than_median_across_trajectories)
}



