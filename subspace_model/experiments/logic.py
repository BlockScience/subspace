import numpy as np
from scipy.stats import norm, poisson  # type: ignore

from subspace_model.const import BLOCKS_PER_MONTH, BLOCKS_PER_YEAR, DAY_TO_SECONDS
from subspace_model.metrics import (
    earned_minus_burned_supply,
    earned_supply,
    issued_supply,
    total_supply,
)
from subspace_model.types import (
    StochasticFunction,
    SubspaceModelParams,
    SubspaceModelState,
)


def DEFAULT_ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    # Extract necessary values from the state
    a = state['reference_subsidy']
    F = state['storage_fee_volume']
    g = state['block_utilization']

    # Fixed parameters. These can be tuned as needed.
    c = params['issuance_function_constant']
    d = 1

    # Calculate b
    b = (a - max(a - F, 0)) / math.tanh(c)

    # Calculate s(g)
    s_g = a + b * math.tanh(-c * (g - d))

    # Ensure block_reward is non-negative
    block_reward = max(s_g, 0)

    return block_reward


def MOCK_ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state['reward_issuance_balance'] * 0.01  # HACK


def MOCK_ISSUANCE_FUNCTION_2(params: SubspaceModelParams, state: SubspaceModelState):
    return state['reward_issuance_balance'] / 5 * 365  # HACK


def DEFAULT_SLASH_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state['staking_pool_balance'] * 0.001  # HACK


def NORMAL_GENERATOR(mu: float, sigma: float) -> StochasticFunction:
    return lambda p, s: norm.rvs(mu, sigma)


def POISSON_GENERATOR(mu: float) -> StochasticFunction:
    return lambda p, s: poisson.rvs(mu)


def POSITIVE_INTEGER(generator: StochasticFunction) -> StochasticFunction:
    return lambda p, s: max(0, int(generator(p, s)))


def MAGNITUDE(generator: StochasticFunction) -> StochasticFunction:
    return lambda p, s: min(1, max(0, generator(p, s)))


SUPPLY_ISSUED = issued_supply

SUPPLY_EARNED = earned_supply

SUPPLY_EARNED_MINUS_BURNED = earned_minus_burned_supply

SUPPLY_TOTAL = total_supply


import math
from dataclasses import dataclass


@dataclass
class SubsidyComponent:
    initial_period_start: float    # τ_{0, i}
    initial_period_end: float      # τ_{1, i}
    max_cumulative_subsidy: float  # Ω_i
    max_reference_subsidy: float   # α_i

    def __call__(self, t: float) -> float:
        """Allow the instance to be called as a function to calculate the subsidy."""
        return self.calculate_subsidy(t)

    def calculate_subsidy(self, t: float) -> float:
        """Calculate S(t) the subsidy for a given time."""
        if t < self.initial_period_start:
            return 0
        elif self.initial_period_start <= t <= self.initial_period_end:
            already_distributed = self.max_reference_subsidy * (
                t - self.initial_period_start
            )
            if already_distributed >= self.max_cumulative_subsidy:
                return 0
            elif (
                already_distributed + self.max_reference_subsidy
                > self.max_cumulative_subsidy
            ):
                return self.max_cumulative_subsidy - already_distributed
            else:
                return self.max_reference_subsidy
        else:
            return self.calculate_exponential_subsidy(t)

    def calculate_exponential_subsidy(self, t: float) -> float:
        """Calculate S_e(t) the exponential subsidy for a given time."""
        K = self.max_total_subsidy_during_exponential_period
        if K > 0:
            return self.max_reference_subsidy * math.exp(
                -self.max_reference_subsidy / max(1, K * (t - self.initial_period_end))
            )
        else:
            return 0

    @property
    def max_total_subsidy_during_exponential_period(self) -> float:
        """Calculate K the maximum total subsidy during the exponential period."""
        return self.max_cumulative_subsidy - self.max_reference_subsidy * (
            self.initial_period_end - self.initial_period_start
        )

    @property
    def halving_period(self) -> float:
        """Calculate L the halving period for the component rewards."""
        K = self.max_total_subsidy_during_exponential_period
        return K * math.log(2) / self.max_reference_subsidy


REFERENCE_SUBSIDY_CONSTANT_SINGLE_COMPONENT = [
    SubsidyComponent(0, 2 * BLOCKS_PER_YEAR, 10_000, 10_000 / (2 * BLOCKS_PER_YEAR)),
]
REFERENCE_SUBSIDY_HYBRID_SINGLE_COMPONENT = [
    SubsidyComponent(0, BLOCKS_PER_MONTH, 10_000, 1_000 / BLOCKS_PER_MONTH),
]
REFERENCE_SUBSIDY_HYBRID_TWO_COMPONENTS = [
    SubsidyComponent(0, BLOCKS_PER_MONTH, 5_000, 1_000 / BLOCKS_PER_MONTH),
    SubsidyComponent(
        6 * BLOCKS_PER_MONTH, 7 * BLOCKS_PER_MONTH, 5_000, 1_000 / BLOCKS_PER_MONTH
    ),
]

DEFAULT_REFERENCE_SUBSIDY_COMPONENTS = REFERENCE_SUBSIDY_CONSTANT_SINGLE_COMPONENT


def TRANSACTION_COUNT_PER_DAY_FUNCTION_CONSTANT_UTILIZATION_50(
    params: SubspaceModelParams, state: SubspaceModelState
) -> float:
    average_transaction_size = state['average_transaction_size']
    max_size = (
        params['max_block_size'] * DAY_TO_SECONDS * params['block_time_in_seconds']
    )

    # Hold a constant utilization rate of 0.5
    transaction_count = 0.5 * max_size / average_transaction_size

    return transaction_count


def TRANSACTION_COUNT_PER_DAY_FUNCTION_GROWING_UTILIZATION_TWO_YEARS(
    params: SubspaceModelParams, state: SubspaceModelState
) -> float:

    days_passed = state['days_passed']
    average_transaction_size = state['average_transaction_size']
    max_size = (
        params['max_block_size'] * DAY_TO_SECONDS * params['block_time_in_seconds']
    )

    utilization = min(days_passed / (2 * 365), 1)

    # Grow utilization rate from 0 to 1 over 2 years
    transaction_count = utilization * max_size / average_transaction_size

    return transaction_count


def WEEKLY_VARYING(params: SubspaceModelParams, state: SubspaceModelState):
    return 2 + np.sin(2 * np.pi * state['days_passed'] / 7)
