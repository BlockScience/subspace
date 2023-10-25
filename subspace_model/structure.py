from subspace_model.logic import *
from typing import Callable
from copy import deepcopy

# Non processed blocks

_SUBSPACE_MODEL_BLOCKS: list[dict] = [
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
        'label': 'Environmental Processes',
        'ignore': False,
        'policies': {
            'sector_onboarding': p_commit_sectors,
            'archival': p_archive
        },
        'variables': {
            'average_base_fee': s_average_base_fee,
            'average_priority_fee': s_average_priority_fee,
            'average_compute_units': s_average_compute_units,
            'transaction_count': s_transaction_count,
            'commit_size_in_bytes': add_suf,
            'history_size_in_bytes': add_suf
        }
    },
    {
        'label': 'Farmer Rewards (Inflow)',
        'ignore': False,
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
        'ignore': False,
        'policies': {
            'storage_fees': p_storage_fees
        },
        'variables': {
            'holders_balance': add_suf,
            'farmers_balance': add_suf,
            'fund_balance': add_suf,
            'storage_fee_volume': replace_suf
        }
    },
    {
        'label': 'Compute Fees',
        'ignore': False,
        'policies': {
            'compute_fees': p_compute_fees
        },
        'variables': {
            'farmers_balance': add_suf,
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'compute_fee_volume': replace_suf
        }
    },
    {
        'label': 'Direct Allocations',
        'ignore': False,
        'policies': {
            'unvest': p_unvest
        },
        'variables': {
            'holders_balance': add_suf,
            'issuance_balance': add_suf
        }
    },
    {
        'label': 'Slash',
        'ignore': False,
        'policies': {
            'slash': p_slash
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
        'ignore': False,
        'policies': {
            'staking': p_staking
        },
        'variables': {
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'staking_pool_balance': add_suf
        }
    },
    {
        'label': 'Transfers',
        'ignore': False,
        'policies': {
            'transfers': p_transfers
        },
        'variables':  {
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'holders_balance': add_suf,
            'farmers_balance': add_suf
        }
    }
]


# Post Processing

blocks: list[dict] = []
for block in [b for b in _SUBSPACE_MODEL_BLOCKS if b.get('ignore', False) != True]:
    _block = deepcopy(block)
    for variable, suf in block.get('variables', {}).items():
        if suf == add_suf:
            _block['variables'][variable] = add_suf(variable)
        elif suf == replace_suf:
            _block['variables'][variable] = replace_suf(variable)
        else:
            pass
    blocks.append(_block)

SUBSPACE_MODEL_BLOCKS = deepcopy(blocks)