import logging

from subspace_model.types import SubspaceModelState, SubspaceModelParams, Credits


def circulating_supply(state: SubspaceModelState) -> Credits:
    return (
        state["operators_balance"]
        + state["nominators_balance"]
        + state["holders_balance"]
        + state["farmers_balance"]
    )


def user_supply(state: SubspaceModelState) -> Credits:
    return circulating_supply(state) + state["staking_pool_balance"]


def earned_supply(state: SubspaceModelState) -> Credits:
    return user_supply(state) + state["fund_balance"]


def issued_supply(state: SubspaceModelState) -> Credits:
    return (
        sum_of_stocks(state) - state["burnt_balance"] - state["reward_issuance_balance"]
    )  # TODO Document the identity


def earned_minus_burned_supply(state: SubspaceModelState) -> Credits:
    return earned_supply(state) - state["burnt_balance"]


def total_supply(state: SubspaceModelState) -> Credits:
    return issued_supply(state) - state["burnt_balance"]


def sum_of_stocks(state: SubspaceModelState) -> Credits:
    return (
        earned_supply(state)
        + state["other_issuance_balance"]
        + state["reward_issuance_balance"]
        + state["burnt_balance"]
    )


def storage_fee_per_rewards(state: SubspaceModelState) -> Credits:
    return state["storage_fee_volume"] / max(1, state["block_reward"])

def community_vested_supply(state: SubspaceModelState, params: SubspaceModelParams) -> Credits:
    return state['allocated_tokens'] * params['community_vested_supply_fraction']

def community_owned_supply(state: SubspaceModelState, params: SubspaceModelParams) -> Credits:
    return issued_supply(state) + community_vested_supply(state, params) + params['initial_community_owned_supply_pct_of_max_credits'] * params['max_credit_supply']


def community_owned_supply_fraction(state: SubspaceModelState, params: SubspaceModelParams, initial_supply: Credits):
    return community_owned_supply(state, params, initial_supply) / total_supply(state)


def per_recipient_reward(state: SubspaceModelState, params: SubspaceModelParams):
    return state['block_reward'] * (1 - params['reward_proposer_share']) * (1 / params['reward_recipients'])


def proposer_bonus_reward(state: SubspaceModelState, params: SubspaceModelParams):
    return state['block_reward'] * params['reward_proposer_share']


def reward_to_proposer(state: SubspaceModelState, params: SubspaceModelParams):
    return per_recipient_reward(state, params) + proposer_bonus_reward(state, params)

def reward_to_voters(state: SubspaceModelState, params: SubspaceModelParams):
    # NOTE: assumes that the only other recipient is the block proposer
    return per_recipient_reward(state, params) * (params['reward_recipients'] - 1)
