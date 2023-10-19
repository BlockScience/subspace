from subspace_model.logic import *
from typing import Callable


SUBSPACE_MODEL_BLOCKS = [
    {
        'label': 'Time Tracking',
        'ignore': False,
        'desc': 'Updates the time in the system',
        'policies': {
            'evolve_time': p_evolve_time
        },
        'variables': {
            'days_passed': s_days_passed,
            'delta_days': s_delta_days
        }
    },
    {
        'label': 'Block Rewards (Inflow)',
        'desc': '#TODO',
        'policies': {
            'fund_rewards': None,
            'issuance_rewards': None
        },
        'variables': {
            'fund_balance': None,
            'issuance_balance': None,
            'block_reward': None
        }
    },
    {
        'label': 'Block Rewards (Outflow)',
        'desc': '#TODO',
        'policies': {
            'proposer_rewards': None,
            'voter_rewards': None,
            'data_rewards': None
        },
        'variables': {
            'farmers_balance': None,
            'fund_balance': None
        }
    }, 
    {
        'label': 'Storage Fees',
        'desc': '#TODO',
        'policies': {
            #TODO
        }
        'variables': {
            'holders_balance': None,
            'farmers_balance': None,
            'fund_balance': None
        }
    }, 
    {
        'label': 'Compute Fees',
        'desc': '#TODO',
        'policies': {
            #TODO
        }
        'variables': {
            'holders_balance': None,
            'farmers_balance': None,
            'operators_balance': None,
            'nominators_balance': None
        }
    }
]