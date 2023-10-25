from subspace_model.types import *
from cadCAD_tools.types import Signal, VariableUpdate
from typing import Callable
from scipy.stats import poisson, norm
from subspace_model.metrics import *
from random import randint

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
    """
    """
    return {'delta_days': params['timestep_in_days']}

def s_days_passed(_1, _2, _3, 
                  state: SubspaceModelState, 
                  signal: Signal) -> VariableUpdate:
    """
    """
    return {'days_passed': signal['delta_days'] + state['days_passed']}

## Farmer Rewards ##

def p_fund_reward(_1, _2, _3, state: SubspaceModelState) -> Signal:
    """
    """
    reward = state['issuance_balance'] * 0.01 # TODO: put correct form
    return {'block_reward': reward, 'issuance_balance': -reward}

def p_issuance_reward(_1, _2, _3, state: SubspaceModelState) ->  Signal:
    """
    """
    reward = state['fund'] * 0.01 # TODO: put correct form
    return {'block_reward': reward, 'issuance_balance': -reward}


def p_split_reward(params: SubspaceModelParams, _2, state: SubspaceModelState, _4) ->  Signal:
    """
    """
    reward = state['block_reward']
    reward_to_fund = reward * params['reward_proposer_share'] * params['fund_tax_on_proposer_reward']
    reward_to_farmers = reward - reward_to_fund
    return {'farmers_balance': reward_to_farmers, 'fund_balance': reward_to_fund}

## Operator Rewards

def p_operator_reward(_1, _2, _3, _4) ->  Signal:
    """
    """
    # TODO: implement
    return {}


## Environmental processes

def p_commit_sectors(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    new_sectors = randint(0, 3) # TODO: make an more nuanced model
    new_bytes = new_sectors * params['sector_size_in_bytes']
    return {'commit_size_in_bytes': new_bytes}

def p_archive(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    timestep_in_seconds = params['timestep_in_days'] * (24 * 60 * 60)
    archival_count =  timestep_in_seconds / (params['block_time_in_seconds'] * params['archival_duration_in_blocks'])
    new_bytes = archival_count * params['archive_size_in_bytes']
    return {'commit_size_in_bytes': new_bytes}

def s_average_base_fee(_1, _2, _3, _4, _5) -> VariableUpdate:
    """
    Roughly inspired by ETH
    """
    return ('average_base_fee', max(norm.rvs(35, 5), 0))

def s_average_priority_fee(_1, _2, _3, _4, _5) -> VariableUpdate:
    """
    Roughly inspired by ETH
    """
    return ('average_priority_fee', max(norm.rvs(5, 5), 0))

def s_average_compute_units(_1, _2, _3, _4, _5) -> VariableUpdate:
    """
    Roughly inspired by https://coinmetrics.io/the-ethereum-gas-report/
    """
    return ('average_compute_units', max(norm(50_000, 20_000), 5_000))

def s_transaction_count(_1, _2, _3, _4, _5) -> VariableUpdate:
    """
    Arbitrary assumption
    """
    return ('transaction_count', max(poisson(1),0))

## Compute & Operator Fees
def p_storage_fees(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    """
    total_issued_credit_supply = issued_supply(state['token_distribution'])
    total_space_pledged = state['commit_size_in_bytes']
    blockchain_size = state['history_size_in_bytes']

    storage_fee_in_credits_per_bytes = total_issued_credit_supply / (total_space_pledged - blockchain_size)
    transaction_bytes = state['transaction_count_per_timestep'] * state['average_transaction_size']
    total_storage_fees = storage_fee_in_credits_per_bytes * transaction_bytes

    fees_to_fund = params['fund_tax_on_storage_fees'] * total_storage_fees
    fees_to_farmers = total_storage_fees - fees_to_fund

    return {'farmers_balance': fees_to_farmers,
            'fund_balance': fees_to_fund}


def p_compute_fees(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    """
    compute_units = state['average_compute_fees'] * state['transaction_count_per_timestep']
    base_fees = state['average_base_fee'] * compute_units
    priority_fees = state['average_priority_fee'] * compute_units

    fees_to_farmers = priority_fees * params['farmer_tax_on_compute_priority_fees']
    fees_to_pool = base_fees + (priority_fees - fees_to_farmers)
    # TODO distribute fees to farmers / nominators according to shares
    fees_to_nominators = fees_to_pool / 2 # HACK: temporary assumption
    fees_to_operators = fees_to_pool - fees_to_nominators # HACK: temporary assumption
    return {'farmers_balance': fees_to_farmers,
             'nominators_balance': fees_to_nominators,
             'operators_balance': fees_to_operators}


### User Behavioral Processes

def p_staking(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
return {'operators_balance': None,
        'staking_pool_balance': None,
        'nominators_balance': None}


def p_transfers(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    """
    return {'operators_balance': None, 
            'holders_balance': None, 
            'nominators_balance': None, 
            'farmers_balance': None} 