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
    return ('days_passed', signal['delta_days'] + state['days_passed'])

## Farmer Rewards ##

def p_fund_reward(_1, _2, _3, state: SubspaceModelState) -> Signal:
    """
    Farmer rewards that originates from the DSF.
    """
    dsf_share = state['dsf_relative_disbursal_per_day'] ** state['delta_days']
    reward = state['fund_balance'] * dsf_share
    return {'block_reward': reward, 'fund_balance': -reward}

def p_issuance_reward(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) ->  Signal:
    """
    Farmer rewards that originates from protocol issuance.
    """
    issuance_per_day = params['issuance_function'](state)
    reward = issuance_per_day * state['delta_days']

    # Make sure that the protocol has tokens to issue
    if reward > state['reward_issuance_balance']:
        reward = state['reward_issuance_balance']
    else:
        pass

    return {'block_reward': reward, 'reward_issuance_balance': -reward}


def p_split_reward(params: SubspaceModelParams, _2, _3,  state: SubspaceModelState) ->  Signal:
    """
    """
    reward = state['block_reward']
    reward_to_fund = reward * params['reward_proposer_share'] * params['fund_tax_on_proposer_reward']
    reward_to_farmers = reward - reward_to_fund
    return {'farmers_balance': reward_to_farmers, 'fund_balance': reward_to_fund}

## Operator Rewards

def p_operator_reward(_1, _2, _3, _4) ->  Signal:
    """
    Protocol issued rewards to Staked Operators.
    NOTE: Assumed to be zero.
    """
    reward = 0.0
    return {'other_issuance_balance': -reward, 'operators_balance': reward}


## Environmental processes

def p_commit_sectors(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    Decide amount of commited bytes to be added
    """
    new_sectors = int(max(norm.rvs(params['avg_new_sectors_per_day'], params['std_new_sectors_per_day']), 0))
    new_bytes = new_sectors * params['sector_size_in_bytes']
    return {'commit_size_in_bytes': new_bytes}

def p_archive(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    TODO: check if underlying assumptions are valid. 
    """
    timestep_in_seconds = params['timestep_in_days'] * (24 * 60 * 60)
    archival_count =  timestep_in_seconds / (params['block_time_in_seconds'] * params['archival_duration_in_blocks'])
    new_bytes = archival_count * params['archive_size_in_bytes'] 
    return {'commit_size_in_bytes': new_bytes}

def s_average_base_fee(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average base fee during an timestep through
    a Gaussian process.
    """
    return ('average_base_fee', max(norm.rvs(params['avg_base_fee'], params['std_base_fee']), params['min_base_fee']))

def s_average_priority_fee(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average priority fee during an timestep through
    a Gaussian process.
    """
    return ('average_priority_fee', max(norm.rvs(params['avg_priority_fee'], params['std_priority_fee']), 0))

def s_average_compute_units(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average compute units per transaction through a Gaussian process.
    """
    return ('average_compute_units', max(norm.rvs(params['avg_compute_units_per_tx'], params['std_compute_units_per_tx']), params['min_compute_units_per_tx']))

def s_average_transaction_size(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average transaction size through a Gaussian process.
    """
    return ('average_transaction_size', max(norm.rvs(params['avg_transaction_size'], params['std_transaction_size']), params['min_transaction_size']))

def s_transaction_count(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average transaction size through a Poisson process.
    """
    return ('transaction_count', max(poisson.rvs(params['avg_transaction_count']),0))

## Compute & Operator Fees
def p_storage_fees(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    """
    # Input
    total_issued_credit_supply = issued_supply(state)
    total_space_pledged = state['commit_size_in_bytes']
    blockchain_size = state['history_size_in_bytes']

    # Compute total storage fees during this timestep
    # TODO: use average storage fee rather than immediate storage fee instead
    storage_fee_in_credits_per_bytes = total_issued_credit_supply / (total_space_pledged - blockchain_size)
    transaction_bytes = state['transaction_count'] * state['average_transaction_size']
    total_storage_fees = storage_fee_in_credits_per_bytes * transaction_bytes

    # HACK: lack of holders balance is handled by capping the total fees paid
    eff_total_storage_fees = min(total_storage_fees, state['holders_balance'])

    # Fee distribution
    fees_to_fund = params['fund_tax_on_storage_fees'] * eff_total_storage_fees
    fees_to_farmers = eff_total_storage_fees - fees_to_fund
    

    return {'farmers_balance': fees_to_farmers,
            'fund_balance': fees_to_fund,
            'holders_balance': -eff_total_storage_fees,
            'storage_fee_volume': eff_total_storage_fees}


def p_compute_fees(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    """
    compute_units = state['average_compute_units'] * state['transaction_count']
    base_fees = state['average_base_fee'] * compute_units
    priority_fees = state['average_priority_fee'] * compute_units
    
     # HACK: lack of holders balance is handled by capping the total fees paid
    total_fees = base_fees + priority_fees
    eff_total_fees = min(total_fees, state['holders_balance'])
    eff_scale = eff_total_fees / total_fees

    eff_base_fees = base_fees * eff_scale
    eff_priority_fees = priority_fees * eff_scale

    fees_to_farmers = eff_priority_fees * params['compute_fees_to_farmers']
    fees_to_pool = eff_base_fees + (eff_priority_fees - fees_to_farmers)

    denominator = (state['operator_pool_shares'] + state['nominator_pool_shares'])
    if denominator == 0:
        denominator = 1/2
    nominators_share = state['nominator_pool_shares'] / denominator

    fees_to_nominators = fees_to_pool * nominators_share * (1 - params['compute_fees_tax_to_operators'])
    fees_to_operators = fees_to_pool - fees_to_nominators

    total_fees = fees_to_farmers + fees_to_nominators + fees_to_operators
    return {'farmers_balance': fees_to_farmers,
             'nominators_balance': fees_to_nominators,
             'operators_balance': fees_to_operators,
             'holders_balance': -eff_total_fees,
             'compute_fee_volume': eff_total_fees}

def p_slash(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    """

    slash_count = poisson.rvs(params['avg_slash_per_day'])
    slash_value = min(slash_count * params['slash_function'](state), state['operators_balance']) # TODO: check

    slash_to_fund = slash_value * params['slash_to_fund']
    slash_to_holders = slash_value * params['slash_to_holders']
    slash_to_burn = slash_value - (slash_to_fund + slash_to_holders)

    return {'operators_balance': -slash_value, 
            'fund_balance': slash_to_fund, 
            'holders_balance': slash_to_holders, 
            'burnt_balance': slash_to_burn} 

def p_unvest(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    Impl notes: 30% of total. 
    22% to be unvested with 24mo and 8% to be unvested with 48mo.
    25% total to be unlocked after 12mo and linearly afterwards.
    """

    # TODO: parametrize / generalize
    if state['days_passed'] < 365:
        allocated_tokens = 0.0
    elif state['days_passed'] >= 365:
        allocated_tokens = 0.30 * 0.25
        allocated_tokens += 0.22 * 0.75 * min((state['days_passed'] - 365) / (365 * 2), 1) # Investors
        allocated_tokens += 0.08 * 0.75 * min((state['days_passed'] - 365) / (4 * 365), 1) # Team
        allocated_tokens *= params['max_credit_supply']

    tokens_to_allocate = allocated_tokens - state['allocated_tokens']
    holders_balance = tokens_to_allocate
    other_issuance_balance = -holders_balance
    
    return {'other_issuance_balance': other_issuance_balance,
            'holders_balance': holders_balance,
            'allocated_tokens': allocated_tokens} 


### User Behavioral Processes

def p_staking(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    NOTE: this assumes that operators and nominators will always
    stake a given % of their free balance every timestep.

    TODO: enforce minimum staking amounts
    """
    operator_stake = state['operators_balance'] * params['operator_stake_per_ts']
    nominator_stake = state['nominators_balance'] * params['nominator_stake_per_ts']
    total_stake = operator_stake + nominator_stake

    return {'operators_balance': -operator_stake,
            'operator_pool_shares': operator_stake,
            'nominator_pool_shares': nominator_stake,
            'nominators_balance': -nominator_stake,
            'staking_pool_balance': total_stake}


def p_transfers(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    """
    delta_nominators = 0.0
    delta_holders = 0.0
    delta_farmers = 0.0
    delta_operators = 0.0

    # Farmers to Holders
    delta = state['farmers_balance'] * params['transfer_farmer_to_holder_per_day']
    delta_farmers -= delta
    delta_holders += delta

    # Operators to Holders
    delta = state['operators_balance'] * params['transfer_operator_to_holder_per_day']
    delta_operators -= delta
    delta_holders += delta

    # Holder to Nominators
    delta = state['holders_balance'] * params['transfer_holder_to_nominator_per_day']
    delta_holders -= delta
    delta_nominators += delta


    # Holder to Operators
    delta = state['holders_balance'] * params['transfer_holder_to_operator_per_day']
    delta_holders -= delta
    delta_operators += delta

    # TODO: add check on the resulting balances?

    
    return {'operators_balance': delta_operators, 
            'holders_balance': delta_holders, 
            'nominators_balance': delta_nominators, 
            'farmers_balance': delta_farmers} 