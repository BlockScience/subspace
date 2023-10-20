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


def replace_suf(variable: str) -> Callable:
    """Creates replacing function for state update from string

    Args:
        variable (str): The variable name that is updated

    Returns:
        function: A function that continues the state across a substep
    """
    return lambda _1, _2, _3, state, signal: (variable, signal[variable])


def add_suf(variable: str) -> Callable:
    """Creates replacing function for state update from string

    Args:
        variable (str): The variable name that is updated

    Returns:
        function: A function that continues the state across a substep
    """
    return lambda _1, _2, _3, state, signal: (variable, signal[variable] + state[variable])

## Time Tracking ##

def p_evolve_time(params: SubspaceModelParams, 
                  _2, _3, _4) -> Signal:
    return {'delta_days': params['timestep_in_days']}

def s_days_passed(_1, _2, _3, 
                  state: SubspaceModelState, 
                  signal: Signal) -> VariableUpdate:
    return {'days_passed': signal['delta_days'] + state['days_passed']}

## Farmer Rewards ##

def p_fund_reward(_1, _2, _3, _4) -> Signal:
    return {}

def p_issuance_reward(_1, _2, _3, _4) ->  Signal:
    {}