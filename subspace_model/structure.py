import logging

logger = logging.getLogger('subspace-digital-twin')
from copy import deepcopy
from typing import Callable

from subspace_model.logic import *

# Non processed blocks

_SUBSPACE_MODEL_BLOCKS: list[dict] = [
    {
        'label': 'Time Tracking',
        'ignore': False,
        'desc': 'Updates the time in the system',
        'policies': {'evolve_time': p_evolve_time},
        'variables': {
            'days_passed': s_days_passed,
            'delta_days': replace_suf,
            'delta_blocks': s_delta_blocks,
        },
    },
    {
        'label': 'Environmental Processes',
        'ignore': False,
        'policies': {'sector_onboarding': p_pledge_sectors},
        'variables': {
            'average_base_fee': s_average_base_fee,
            'average_priority_fee': s_average_priority_fee,
            'average_compute_weight_per_tx': s_average_compute_weight_per_tx,
            'transaction_count': s_transaction_count,
            'average_transaction_size': s_average_transaction_size,
            'space_pledged': add_suf,
            'average_compute_weight_per_bundle': s_average_compute_weight_per_bundle,
            'bundle_count': s_bundle_count,
        },
    },
    {
        'label': 'Archival Process and Compute Block Utilization',
        'policies': {'archival': p_archive},
        'variables': {
            'history_size': add_suf,
            'buffer_size': add_suf,
            'block_utilization': s_block_utilization,
        },
    },
    {
        'label': 'Farmer Rewards (Inflow)',
        'ignore': False,
        'policies': {
            'fund_reward': p_fund_reward,
            'issuance_reward': p_issuance_reward,
        },
        'variables': {
            'fund_balance': add_suf,
            'reward_issuance_balance': add_suf,
            'block_reward': replace_suf,
        },
    },
    {
        'label': 'Farmer Rewards (Outflow)',
        'ignore': False,
        'policies': {'split_farmer_rewards': p_split_reward},
        'variables': {'farmers_balance': add_suf, 'fund_balance': add_suf},
    },
    {
        'label': 'Operator Rewards',
        'ignore': False,
        'policies': {'operator_rewards': p_operator_reward},
        'variables': {'other_issuance_balance': add_suf, 'operators_balance': add_suf},
    },
    {
        'label': 'Storage Fees',
        'ignore': False,
        'policies': {'storage_fees': p_storage_fees},
        'variables': {
            'holders_balance': add_suf,
            'farmers_balance': add_suf,
            'fund_balance': add_suf,
            'storage_fee_volume': replace_suf,
        },
    },
    {
        'label': 'Compute Fees',
        'ignore': False,
        'policies': {'compute_fees': p_compute_fees},
        'variables': {
            'farmers_balance': add_suf,
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'holders_balance': add_suf,
            'compute_fee_volume': replace_suf,
            'rewards_to_nominators': replace_suf,
        },
    },
    {
        'label': 'Direct Allocations',
        'ignore': False,
        'policies': {'unvest': p_unvest},
        'variables': {
            'holders_balance': add_suf,
            'other_issuance_balance': add_suf,
            'allocated_tokens': replace_suf,
        },
    },
    {
        'label': 'Slash',
        'ignore': False,
        'policies': {'slash': p_slash},
        'variables': {
            'staking_pool_balance': add_suf,
            'fund_balance': add_suf,
            'holders_balance': add_suf,
            'operator_pool_shares': add_suf,
            'burnt_balance': add_suf,
        },
    },
    {
        'label': 'Staking / Unstaking',
        'ignore': False,
        'policies': {
            'staking': p_staking,
        },
        'variables': {
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'staking_pool_balance': add_suf,
            'operator_pool_shares': add_suf,
            'nominator_pool_shares': add_suf,
        },
    },
    {
        'label': 'Transfers',
        'ignore': False,
        'policies': {'transfers': p_transfers},
        'variables': {
            'operators_balance': add_suf,
            'nominators_balance': add_suf,
            'holders_balance': add_suf,
            'farmers_balance': add_suf,
        },
    },
    {
        'label': 'Metrics',
        'policies': {},
        'variables': {
            'circulating_supply': lambda _1, _2, _3, s, _5: (
                'circulating_supply',
                circulating_supply(s),
            ),
            'user_supply': lambda _1, _2, _3, s, _5: ('user_supply', user_supply(s)),
            'issued_supply': lambda _1, _2, _3, s, _5: (
                'issued_supply',
                issued_supply(s),
            ),
            'sum_of_stocks': lambda _1, _2, _3, s, _5: (
                'sum_of_stocks',
                sum_of_stocks(s),
            ),
        },
    },
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

logger.debug('SUBSPACE_MODEL_BLOCKS: \n%s', [b['label'] for b in SUBSPACE_MODEL_BLOCKS])
