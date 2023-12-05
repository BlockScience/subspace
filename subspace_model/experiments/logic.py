from scipy.stats import norm, poisson  # type: ignore

from subspace_model.types import SubspaceModelParams, SubspaceModelState


def DEFAULT_ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state['reward_issuance_balance'] * 0.01   # HACK


def ISSUANCE_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state['reward_issuance_balance'] * 0.01   # HACK


def DEFAULT_SLASH_FUNCTION(params: SubspaceModelParams, state: SubspaceModelState):
    return state['staking_pool_balance'] * 0.001   # HACK


def NORMAL(params: SubspaceModelParams, state: SubspaceModelState, key: str):
    normal_params = params['stochastic_params'][key]
    deterministic = normal_params['deterministic']
    mu = normal_params['mu']
    sigma = normal_params['sigma']
    if deterministic or params['deterministic']:
        return mu
    return norm.rvs(mu, sigma)


def POISSON(params: SubspaceModelParams, state: SubspaceModelState, key: str):
    poisson_params = params['stochastic_params'][key]
    mu = poisson_params['mu']
    if poisson_params['deterministic'] or params['deterministic']:
        return mu
    return poisson.rvs(mu)
