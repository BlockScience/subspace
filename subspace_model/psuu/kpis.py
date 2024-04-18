from subspace_model.psuu.types import *
from subspace_model.types import *
import subspace_model.metrics as m
import numpy as np
from pandera.typing import DataFrame
from typing import Optional
## KPIs

def per_timestep_average_relative_community_owned_supply(df: DataFrame) -> KPI:
    return (df.community_owned_supply / df.total_supply).mean()


def mean_farmer_subsidy_factor(df: DataFrame) -> KPI:
    """
    Farmer Subsidy Factor = Cummulative Rewards / Cummulative Farmer Revenue
    Where Revenue = Cummulative Farmer Inflows (Rewards + Storage Fees + Compute Fees)
    """
    farmer_revenue = (df.cumm_rewards + df.cumm_storage_fees_to_farmers + df.cumm_compute_fees_to_farmers)
    farmer_subsidy_factor = df.cumm_rewards / farmer_revenue
    return farmer_subsidy_factor.mean()

def mean_proposing_rewards_per_newly_pledged_space(df: DataFrame) -> KPI:
    """
    M(t) = Rewards to Proposers(t) / New Pledged Space(t)
    """
    return (df['reward_to_voters'] / df['total_space_pledged'].diff()).mean()

def mean_proposer_reward_minus_voter_reward(df: DataFrame) -> KPI:
    return (df['reward_to_proposer'] - df['reward_to_voters']).mean()

def cumm_rewards_before_1yr(df: DataFrame) -> KPI:
    return df.query("days_passed < 366").block_reward.sum()


def abs_sum_storage_fees_per_sum_compute_fees(df: TrajectoryDataFrame) -> KPI:
    """
    M(t) = Storage Fee Volume(t) / Compute Fee Volume(t)
    """
    return df.storage_fee_volume.sum() / (df.storage_fee_volume.sum() + df.compute_fee_volume.sum())

def cumm_rewards(df: TrajectoryDataFrame) -> KPI:
    return df.block_reward.sum()


## PSuU KPI Dict

KPI_functions: dict[str, TrajectoryKPIandThreshold] = {
    'mean_relative_community_owned_supply': TrajectoryKPIandThreshold(per_timestep_average_relative_community_owned_supply, "larger_than_median"),
    'mean_farmer_subsidy_factor': TrajectoryKPIandThreshold(mean_farmer_subsidy_factor, "smaller_than_median"),
    'mean_proposing_rewards_per_newly_pledged_space': TrajectoryKPIandThreshold(mean_proposing_rewards_per_newly_pledged_space, "larger_than_median"),
    'mean_proposer_reward_minus_voter_reward': TrajectoryKPIandThreshold(mean_proposer_reward_minus_voter_reward, "larger_than_median"),
    'cumm_rewards_before_1yr': TrajectoryKPIandThreshold(cumm_rewards_before_1yr, "larger_than_median"),
    'abs_sum_storage_fees_per_sum_compute_fees': TrajectoryKPIandThreshold(abs_sum_storage_fees_per_sum_compute_fees, "smaller_than_median"),
    'cumm_rewards': TrajectoryKPIandThreshold(cumm_rewards, "smaller_than_median")
}



