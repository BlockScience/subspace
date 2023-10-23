from subspace_model.logic import *
from typing import Callable
from copy import deepcopy

## Non processed blocks

SUBSPACE_MODEL_BLOCKS: list[dict] = [
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
        'ignore': False,
        'policies': {
            'operator_rewards': p_operator_reward 
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
            # TODO #6 add `storage fees` block logic
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
            #TODO #5 add `compute fees` block logic
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
            #TODO #4 add `direct allocations` block logic
        },
        'variables': {
            'holders_balance': add_suf,
            'issuance_balance': add_suf
        }
    },
    {
        'label': 'Slash',
        'policies': {
            # TODO #3 add `slash` block logic
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
            # TODO
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
            # TODO #2 add `transfers` block logic
        },
        'variables':  {
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'holders_balance': add_suf,
            'farmers_balance': add_suf
        }
    }
]


## Post Processing

blocks: list[dict] = []
for block in SUBSPACE_MODEL_BLOCKS:
    _block = deepcopy(block)
    for variable, suf in block.get('variables', {}).items():
        if suf == add_suf:
            _block['variables'][variable] = add_suf(variable)
        elif suf == replace_suf:
            _block['variables'][variable] = replace_suf(variable)
        else:
            pass

SUBSPACE_MODEL_BLOCKS = deepcopy(blocks)



# TODO: #1 `add_suf` handling logic
# done!
# TODO: #7 `replace_suf` handling logic
# done!