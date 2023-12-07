from scipy.stats import norm, poisson  # type: ignore

from subspace_model.types import (
    StochasticFunction,
    SubspaceModelParams,
    SubspaceModelState,
)


def DEFAULT_ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state['reward_issuance_balance'] * 0.01   # HACK


def ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state['reward_issuance_balance'] * 0.01   # HACK


def DEFAULT_SLASH_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state['staking_pool_balance'] * 0.001   # HACK


def NORMAL_GENERATOR(mu: float, sigma: float) -> StochasticFunction:
    return lambda p, s: norm.rvs(mu, sigma)


def POISSON_GENERATOR(mu: float) -> StochasticFunction:
    return lambda p, s: poisson.rvs(mu)


def POSITIVE_INTEGER(generator: StochasticFunction) -> StochasticFunction:
    return lambda p, s: max(0, int(generator(p, s)))


def MAGNITUDE(generator: StochasticFunction) -> StochasticFunction:
    return lambda p, s: min(1, max(0, generator(p, s)))
