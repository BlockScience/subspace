import numpy as np
from scipy.stats import norm, poisson  # type: ignore

from subspace_model.types import (
    StochasticFunction,
    SubspaceModelParams,
    SubspaceModelState,
)


def DEFAULT_ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    g = state['block_utilization'] if state['block_utilization'] else 0
    scale_factor = 100
    s_min = 0.1 * scale_factor   # Governance set parameter
    C_max = 2 * scale_factor   # Governance set parameter
    a = 1 * scale_factor
    c = 1
    F = state['storage_fee_volume']
    s_max = max(C_max - F, 0)
    b = (s_min - s_max) / (np.tanh(c))
    s = a + b * np.tanh(-c * g)

    block_reward = (
        s * state['delta_blocks']
    )   # XXX: Assumes that state does not change over the extrapolation period

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
