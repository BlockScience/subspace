import logging

from subspace_model.types import SubspaceModelState


def circulating_supply(state: SubspaceModelState):
    # print(f'Days passed: {state["days_passed"]}...')
    # print('Calculating circulating supply...')
    # print('Operating Balance: ', round(state['operators_balance']))
    # print('Nominator Balance: ', round(state['nominators_balance']))
    # print('Holder Balance: ', round(state['holders_balance']))
    # print('Farmer Balance: ', round(state['farmers_balance']))
    return (
        state['operators_balance']
        + state['nominators_balance']
        + state['holders_balance']
        + state['farmers_balance']
    )


def user_supply(state: SubspaceModelState):
    return circulating_supply(state) + state['staking_pool_balance']


def earned_supply(state: SubspaceModelState):
    return user_supply(state) + state['fund_balance']


def issued_supply(state: SubspaceModelState):
    return (
        sum_of_stocks(state) - state['burnt_balance'] - state['reward_issuance_balance']
    )   # TODO Document the identity


def sum_of_stocks(state: SubspaceModelState):
    return (
        earned_supply(state)
        + state['other_issuance_balance']
        + state['reward_issuance_balance']
        + state['burnt_balance']
    )
