from subspace_model.types import *
from subspace_model.const import *
from cadCAD_tools.types import Signal, VariableUpdate # type: ignore
from typing import Callable
from scipy.stats import poisson, norm # type: ignore
from subspace_model.metrics import *
from random import randint
from math import ceil, floor

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

def s_delta_blocks(params: SubspaceModelParams, 
                        _2, 
                        _3, 
                        state: SubspaceModelState, 
                        signal) -> VariableUpdate:
    """
    """
    delta_seconds = signal['delta_days'] * (24 * 60 * 60)
    delta_blocks = delta_seconds / params['block_time_in_seconds']
    return ('delta_blocks', delta_blocks)


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
    XXX: there's a hard cap on how much can be issued.
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
    XXX: Assumed to be zero
    """
    reward = 0.0
    return {'other_issuance_balance': -reward, 'operators_balance': reward}


## Environmental processes

def p_pledge_sectors(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    Decide amount of commited bytes to be added based on an
    gaussian process.

    XXX: depends on an stochastic process assumption.
    """
    new_sectors = int(max(norm.rvs(params['avg_new_sectors_per_day'], params['std_new_sectors_per_day']), 0))
    new_bytes = new_sectors * SECTOR_SIZE
    return {'space_pledged': new_bytes}

def p_archive(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    TODO: check if underlying assumptions / terminology are valid. 
    TODO: revisit assumption on the supply & demand matching.
    FIXME: homogenize terminology
    """
    realized_depth = state['delta_blocks']
    segments_supply = realized_depth / params['archival_depth']
    
    tx_volume = state['transaction_count'] * state['average_transaction_size']
    new_buffer_bytes = tx_volume
    current_buffer = new_buffer_bytes + state['buffer_size']
    segments_demand = current_buffer / params['archival_buffer_segment_size']
    segments_being_archived = floor(int(min(segments_supply, segments_demand)))

    new_history_bytes = 0
    if segments_being_archived > 0:
        new_buffer_bytes += -1 * SEGMENT_SIZE * segments_being_archived
        new_history_bytes += SEGMENT_HISTORY_SIZE * segments_being_archived
    
    return {'history_size': new_history_bytes,
            'buffer_size': new_buffer_bytes}

def s_average_base_fee(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average base fee during an timestep through
    a Gaussian process.
    XXX: depends on an stochastic process assumption.
    """
    return ('average_base_fee', max(norm.rvs(params['avg_base_fee'], params['std_base_fee']), params['min_base_fee']))

def s_average_priority_fee(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average priority fee during an timestep through
    a Gaussian process.
    XXX: depends on an stochastic process assumption.
    """
    return ('average_priority_fee', max(norm.rvs(params['avg_priority_fee'], params['std_priority_fee']), 0))

def s_average_compute_weight_per_tx(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average compute weights per transaction through a Gaussian process.
    XXX: depends on an stochastic process assumption.
    """
    return ('average_compute_weight_per_tx', max(norm.rvs(params['avg_compute_weights_per_tx'], params['std_compute_weights_per_tx']), params['min_compute_weights_per_tx']))

def s_average_transaction_size(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average transaction size through a Gaussian process.
    XXX: depends on an stochastic process assumption.
    """
    return ('average_transaction_size', max(norm.rvs(params['avg_transaction_size'], params['std_transaction_size']), params['min_transaction_size']))

def s_transaction_count(params: SubspaceModelParams, _2, _3, _4, _5) -> VariableUpdate:
    """
    Simulate the ts-average transaction size through a Poisson process.
    XXX: depends on an stochastic process assumption.
    """
    return ('transaction_count', max(poisson.rvs(params['avg_transaction_count_per_day']),0))

## Compute & Operator Fees
def p_storage_fees(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    HACK: If holders balance is insufficient, then the amount of paid fees 
    will be lower even though the transactions still go through.

    References: 
    - https://github.com/subspace/subspace/blob/53dca169379e65b4fb97b5c7753f5d00bded2ef2/crates/pallet-transaction-fees/src/lib.rs#L271
    """
    # Input
    credit_supply = issued_supply(state)
    total_space_pledged = state['space_pledged']
    blockchain_size = state['history_size']
    replication_factor = params['replication_factor']

    free_space = total_space_pledged - blockchain_size * replication_factor

    if free_space > 0:
        storage_fee_in_credits_per_bytes = credit_supply / free_space
    else:
        storage_fee_in_credits_per_bytes = credit_supply

    # Compute total storage fees during this timestep
    # TODO: use average storage fee rather than immediate storage fee instead
    
    transaction_bytes = state['transaction_count'] * state['average_transaction_size']
    total_storage_fees = storage_fee_in_credits_per_bytes * transaction_bytes

    eff_total_storage_fees = min(total_storage_fees, state['holders_balance'] / 2) # HACK

    # Fee distribution
    fees_to_fund = params['fund_tax_on_storage_fees'] * eff_total_storage_fees
    fees_to_farmers = eff_total_storage_fees - fees_to_fund
    

    return {'farmers_balance': fees_to_farmers,
            'fund_balance': fees_to_fund,
            'holders_balance': -eff_total_storage_fees,
            'storage_fee_volume': eff_total_storage_fees}


def p_compute_fees(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    HACK: If holders balance is insufficient, then the amount of paid fees 
    will be lower even though the transactions still go through.
    """
    compute_weights = state['average_compute_weight_per_tx'] * state['transaction_count']
    base_fees = state['average_base_fee'] * compute_weights
    priority_fees = state['average_priority_fee'] * compute_weights
    
    total_fees = base_fees + priority_fees
    eff_total_fees = min(total_fees, state['holders_balance']) # HACK
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
    XXX: depends on an stochastic process assumption.
    TODO: validate if correct
    """
    slash_value = 0.0
    slash_to_fund = 0.0
    slash_to_holders = 0.0
    operator_shares_to_subtract = 0.0
    slash_to_burn = 0.0

    # XXX: no slash occurs if the pool balance is zero.
    pool_balance = state['staking_pool_balance']
    if pool_balance > 0:
        slash_count = poisson.rvs(params['avg_slash_per_day'])
        slash_value = min(slash_count * params['slash_function'](state), state['operators_balance'])
        if slash_value > 0:
            slash_to_fund = slash_value * params['slash_to_fund']
            slash_to_holders = slash_value * params['slash_to_holders']
            slash_to_burn = slash_value - (slash_to_fund + slash_to_holders)

            # XXX: we assume that the slash is aplied on the staking pool
            # and that its effect is to reduce the operator shares
            # by using an invariant product as a assumption.
            
            pool_balance_after = pool_balance - slash_value
            total_shares = state['operator_pool_shares'] + state['nominator_pool_shares']
            operator_shares_to_subtract = total_shares * (pool_balance_after / pool_balance - 1.0)
        else:
            slash_value = 0.0


    return {'staking_pool_balance': -slash_value, 
            'fund_balance': slash_to_fund, 
            'holders_balance': slash_to_holders, 
            'operator_pool_shares': operator_shares_to_subtract,
            'burnt_balance': slash_to_burn} 

def p_unvest(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    Impl notes: 30% of total. 
    22% to be unvested with 24mo and 8% to be unvested with 48mo.
    25% total to be unlocked after 12mo and linearly afterwards.

    # TODO: parametrize / generalize the schedule
    # TODO: what happens if there's less than 51% community owned?
    """
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
    XXX: this assumes that operators and nominators will always
    stake a given % of their free balance every timestep.
    XXX: assumes an invariant product
    TODO: enforce minimum staking amounts
    """
    if state['operator_pool_shares'] > 0 or state['nominator_pool_shares'] > 0:
        invariant = state['staking_pool_balance'] / (state['operator_pool_shares'] + state['nominator_pool_shares'])
        #invariant = 1
    elif state['operator_pool_shares'] == 0 and state['nominator_pool_shares'] == 0:
        invariant = 1
    else:
        invariant = None

    # Stake operation
    operator_stake_fraction = norm.rvs(params['operator_avg_stake_per_ts'], params['operator_std_stake_per_ts'])
    if operator_stake_fraction > 0:
        operator_stake = state['operators_balance'] * operator_stake_fraction
    elif invariant > 0:
        operator_stake = state['operator_pool_shares']  * operator_stake_fraction * invariant
    else:
        operator_stake = 0.0

    nominator_stake_fraction = norm.rvs(params['nominator_avg_stake_per_ts'], params['nominator_avg_stake_per_ts'])
    if nominator_stake_fraction > 0:
        nominator_stake = state['nominators_balance'] * nominator_stake_fraction
    elif invariant > 0:
        nominator_stake = state['nominator_pool_shares'] * nominator_stake_fraction * invariant
    else:
        nominator_stake = 0.0

    total_stake = operator_stake + nominator_stake

    # NOTE: for handling withdraws bigger than the pool itself.
    if -total_stake > state['staking_pool_balance']:
        old_total_stake = total_stake
        total_stake = -state['staking_pool_balance']
        scale = total_stake / old_total_stake
        operator_stake *= scale
        nominator_stake *= scale




    return {'operators_balance': -operator_stake,
            'operator_pool_shares': operator_stake / invariant,
            'nominator_pool_shares': nominator_stake / invariant,
            'nominators_balance': -nominator_stake,
            'staking_pool_balance': total_stake}


def p_transfers(params: SubspaceModelParams, _2, _3, state: SubspaceModelState) -> Signal:
    """
    XXX: stakeholders will always transfer a give % of their balance every ts
    """
    delta_nominators = 0.0
    delta_holders = 0.0
    delta_farmers = 0.0
    delta_operators = 0.0

    # Farmers to Holders
    if state['farmers_balance'] > 0:
        delta = state['farmers_balance'] * params['transfer_farmer_to_holder_per_day']
        delta_farmers -= delta
        delta_holders += delta

    # Operators to Holders
    if state['farmers_balance'] > 0:
        delta = state['operators_balance'] * params['transfer_operator_to_holder_per_day']
        delta_operators -= delta
        delta_holders += delta

    # Holder to Nominators
    if state['holders_balance'] > 0:
        delta = state['holders_balance'] * params['transfer_holder_to_nominator_per_day']
        delta_holders -= delta
        delta_nominators += delta

        # Holder to Operators
        delta = state['holders_balance'] * params['transfer_holder_to_operator_per_day']
        delta_holders -= delta
        delta_operators += delta
    
    return {'operators_balance': delta_operators, 
            'holders_balance': delta_holders, 
            'nominators_balance': delta_nominators, 
            'farmers_balance': delta_farmers} 

def s_block_utilization(params: SubspaceModelParams, 
                        _2, 
                        _3, 
                        state: SubspaceModelState, 
                        _5) -> VariableUpdate:
    """
    """
    size = state['transaction_count'] * state['average_transaction_size']
    max_size = params['max_block_size'] * DAY_TO_SECONDS * params['block_time_in_seconds']
    value = size / max_size
    return ('block_utilization', value)