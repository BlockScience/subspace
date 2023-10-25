
def circulating_supply(state):
    return (state['operators_balance'] 
            + state['nominators_balance'] 
            + state['holders_balance']
            + state['farmers_balance'])

def user_supply(state):
    return circulating_supply(state) + state['staking_pool_balance']

def issued_supply(state):
    return user_supply(state) + state['fund_balance'] + state['burnt_balance']