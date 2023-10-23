from subspace_model.types import *
from cadCAD_tools.types import Signal, VariableUpdate
from typing import Callable

def generic_policy(_1, _2, _3, _4) -> dict:
    """Function to generate pass through policy

    Args:
        _1
        _2
        _3
        _4

    Returns:
        dict: Empty dictionary
    """
    return {}


def replace_suf(variable: str, default_value=0.0) -> Callable:
    """Creates replacing function for state update from string

    Args:
        variable (str): The variable name that is updated

    Returns:
        function: A function that continues the state across a substep
    """
    return lambda _1, _2, _3, state, signal: (variable, signal.get(variable, default_value))


def add_suf(variable: str, default_value=0.0) -> Callable:
    """Creates replacing function for state update from string

    Args:
        variable (str): The variable name that is updated

    Returns:
        function: A function that continues the state across a substep
    """
    return lambda _1, _2, _3, state, signal: (variable, signal.get(variable, default_value) + state[variable])

## Time Tracking ##

def p_evolve_time(params: SubspaceModelParams, 
                  _2, _3, _4) -> Signal:
    return {'delta_days': params['timestep_in_days']}

def s_days_passed(_1, _2, _3, 
                  state: SubspaceModelState, 
                  signal: Signal) -> VariableUpdate:
    return {'days_passed': signal['delta_days'] + state['days_passed']}

## Farmer Rewards ##

def p_fund_reward(_1, _2, _3, state: SubspaceModelState) -> Signal:
    reward = state['issuance_balance'] * 0.01 # TODO
    return {'block_reward': reward, 'issuance_balance': -reward}

def p_issuance_reward(_1, _2, _3, state: SubspaceModelState) ->  Signal:
    reward = state['fund'] * 0.01 # TODO
    return {'block_reward': reward, 'issuance_balance': -reward}


def p_split_reward(params: SubspaceModelParams, _2, state: SubspaceModelState, _4) ->  Signal:
    reward = state['block_reward']
    reward_to_fund = reward * params['reward_proposer_share'] * params['fund_tax_on_proposer_reward']
    reward_to_farmers = reward - reward_to_fund
    return {'farmers_balance': reward_to_farmers, 'fund_balance': reward_to_fund}

## Operator Rewards

def p_operator_reward(_1, _2, _3, _4) ->  Signal:
    return {}