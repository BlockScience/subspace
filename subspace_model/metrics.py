
def circulating_supply(state):
    return (state['operators_balance'] 
            + state['nominators_balance'] 
            + state['holders_balance']
            + state['farmers_balance'])

def user_supply(state):
    return state['circulating_supply'] + state['staking_pool_balance']

def issued_supply(state):
    return state['user_supply'] + state['fund_balance'] + state['burnt_balance']