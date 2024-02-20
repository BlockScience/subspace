from dataclasses import dataclass

from subspace_model.const import ISSUANCE_FOR_FARMERS, MAX_CREDIT_ISSUANCE
from subspace_model.types import SubspaceModelState

INITIAL_STATE = SubspaceModelState(
    days_passed=0,
    blocks_passed=0,
    # Metrics
    circulating_supply=0.0,
    user_supply=0.0,
    earned_supply=0.0,
    issued_supply=0.0,
    earned_minus_burned_supply=0.0,
    total_supply=0.0,
    sum_of_stocks=0.0,
    storage_fee_per_rewards=0.0,
    block_utilization=0.0,
    # Governance Variables
    dsf_relative_disbursal_per_day=0.0,  # How much %/day of DSF's goes to farmers
    # Stock Balances
    reward_issuance_balance=ISSUANCE_FOR_FARMERS,
    other_issuance_balance=MAX_CREDIT_ISSUANCE - ISSUANCE_FOR_FARMERS,
    operators_balance=0.0,
    nominators_balance=0.0,
    holders_balance=0.0,
    farmers_balance=0.0,
    staking_pool_balance=0.0,
    fund_balance=0.0,
    burnt_balance=0.0,
    # Staking Pool Shares
    nominator_pool_shares=0.0,
    operator_pool_shares=0.0,
    # Variables
    block_reward=0.0,
    blockchain_history_size=0,
    total_space_pledged=0,
    allocated_tokens=0.0,
    buffer_size=0,
    reference_subsidy=0.0,
    # Environmental Variables
    average_priority_fee=0.0,
    average_compute_weight_per_tx=0.0,
    average_transaction_size=256,
    transaction_count=0.0,
    average_compute_weight_per_bundle=0.0,
    average_bundle_size=0.0,
    bundle_count=0.0,
    compute_fee_multiplier=0.0,
    compute_fee_volume=0.0,
    free_space=0.0,
    extrinsic_length_in_bytes=0.0,
    storage_fee_in_credits_per_bytes=0.0,
    transaction_byte_fee=0.0,
    storage_fee_volume=0.0,
    priority_fee_volume=0.0,
    consensus_extrinsic_fee_volume=0.0,
    rewards_to_nominators=0.0,
    max_normal_weight=0.0,
    max_bundle_weight=0.0,
    target_block_fullness=0.0,
    adjustment_variable=0.0,
    storage_fees_to_farmers=0.0,
    storage_fees_to_fund=0.0,
    target_block_delta=0.0,
    targeted_adjustment_parameter=0.0,
    tx_compute_weight=0.0,
)
