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
            'delta_days': replace_suf
        }
    },
    {
        'label': 'Farmer Rewards (Inflow)',
        'ignore': True,
        'policies': {
            'fund_reward': p_fund_reward,
            'issuance_reward': p_issuance_reward
        },
        'variables': {
            'fund_balance': add_suf,
            'issuance_balance': add_suf,
            'block_reward': replace_suf
        }
    },
    {
        'label': 'Farmer Rewards (Outflow)',
        'ignore': False,
        'policies': {
            'split_farmer_rewards': p_split_reward
        },
        'variables': {
            'farmers_balance': add_suf,
            'fund_balance': add_suf
        }
    }, 
    {
        'label': 'Operator Rewards',
        'ignore': True,
        'policies': {
            # TODO
        },
        'variables': {
            'issuance_balance': add_suf,
            'operators_balance': add_suf
        }
    },
    {
        'label': 'Storage Fees',
        'ignore': True,
        'policies': {
            # TODO
        },
        'variables': {
            'holders_balance': add_suf,
            'farmers_balance': add_suf,
            'fund_balance': add_suf
        }
    }, 
    {
        'label': 'Compute Fees',
        'ignore': True,
        'policies': {
            #TODO
        },
        'variables': {
            'holders_balance': add_suf,
            'farmers_balance': add_suf,
            'operators_balance': add_suf,
            'nominators_balance': add_suf
        }
    }, 
    {
        'label': 'Direct Allocations',
        'ignore': True,
        'policies': {
            #TODO
        },
        'variables': {
            'holders_balance': add_suf,
            'issuance_balance': add_suf
        }
    },
    {
        'label': 'Slash',
        'policies': {
        },
        'variables': {
            'operators_balance': add_suf,
            'fund_balance': add_suf,
            'holders_balance': add_suf,
            'burnt_balance': add_suf
        }
    },
    {
        'label': 'Staking / Unstaking',
        'policies': {

        },
        'variables': {
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'staking_pool_balance': add_suf
        }
    },
    {
        'label': 'Transfers',
        'policies': {
            # TODO
        },
        'variables':  {
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'holders_balance': add_suf,
            'farmers_balance': add_suf
        }
    }
]