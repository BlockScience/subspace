from scipy.stats import norm, poisson  # type: ignore
import numpy as np

from subspace_model.types import (
    StochasticFunction,
    SubspaceModelParams,
    SubspaceModelState,
)


def DEFAULT_ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    g = state["block_utilization"] if state["block_utilization"] else 0

    s_min = 1000
    s_c = 10000
    B_max = 610
    C_max = 1000
    P = 37000
    F = (s_c / P) * (B_max * g)
    s_max = max(C_max - F, 0)

    a = 1000
    c = 1
    b = (s_min - s_max) / (np.tanh(c))
    s = a + b * np.tanh(-c * g)

    return s


def MOCK_ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state["reward_issuance_balance"] * 0.01  # HACK


def MOCK_ISSUANCE_FUNCTION_2(params: SubspaceModelParams, state: SubspaceModelState):
    return state["reward_issuance_balance"] / 5 * 365  # HACK


def DEFAULT_SLASH_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state["staking_pool_balance"] * 0.001  # HACK


def NORMAL_GENERATOR(mu: float, sigma: float) -> StochasticFunction:
    return lambda p, s: norm.rvs(mu, sigma)


def POISSON_GENERATOR(mu: float) -> StochasticFunction:
    return lambda p, s: poisson.rvs(mu)


def POSITIVE_INTEGER(generator: StochasticFunction) -> StochasticFunction:
    return lambda p, s: max(0, int(generator(p, s)))


def MAGNITUDE(generator: StochasticFunction) -> StochasticFunction:
    return lambda p, s: min(1, max(0, generator(p, s)))
