from subspace_model.types import SubspaceModelState

def circulating_supply(state: SubspaceModelState):
    return (state['operators_balance'] 
            + state['nominators_balance'] 
            + state['holders_balance']
            + state['farmers_balance'])

def user_supply(state: SubspaceModelState):
    return circulating_supply(state) + state['staking_pool_balance']

def issued_supply(state: SubspaceModelState):
    return user_supply(state) + state['fund_balance'] + state['burnt_balance']

def sum_of_stocks(state: SubspaceModelState):
    return issued_supply(state) + state['other_issuance_balance'] + state['reward_issuance_balance']