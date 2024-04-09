from dataclasses import dataclass

from subspace_model.const import ISSUANCE_FOR_FARMERS, MAX_CREDIT_ISSUANCE, ISSUED_AT_LAUNCH
from subspace_model.types import SubspaceModelState

INITIAL_STATE = SubspaceModelState(
    # Time Variables
    timestep=0,
    substep=0,
    days_passed=0.0,
    delta_days=0.0,
    delta_blocks=0,
    blocks_passed=0,

    # Metrics
    ## Supply Related
    circulating_supply=ISSUED_AT_LAUNCH,
    user_supply=0.0,
    issued_supply=0.0,
    sum_of_stocks=0.0,
    earned_supply=0.0,
    earned_minus_burned_supply=0.0,
    total_supply=0.0,

    ## Network Related
    block_utilization=0.0,
    compute_fee_volume=0.0,
    storage_fee_volume=0.0,

    ## Reward Related
    rewards_to_nominators=0.0,
    per_recipient_reward=0.0,
    proposer_bonus_reward=0.0,
    reward_to_proposer=0.0,
    reward_to_voters=0.0,

    # Governance Variables
    dsf_relative_disbursal_per_day=0.0,  # How much %/day of DSF's goes to farmers

    # Stocks
    reward_issuance_balance=ISSUANCE_FOR_FARMERS,
    other_issuance_balance=MAX_CREDIT_ISSUANCE - ISSUANCE_FOR_FARMERS - ISSUED_AT_LAUNCH,
    operators_balance=0.0,
    nominators_balance=0.0,
    holders_balance=ISSUED_AT_LAUNCH,
    farmers_balance=0.0,
    staking_pool_balance=0.0,
    fund_balance=0.0,
    burnt_balance=0.0,

    # Staking Pool Shares
    nominator_pool_shares=0.0,
    operator_pool_shares=0.0,
    
    # Deterministic Variables
    block_reward=float('nan'),
    blockchain_history_size=0,
    total_space_pledged=0,
    allocated_tokens=0.0,
    buffer_size=0,

    # Environmental Variables

    ## Fee Related
    average_priority_fee=0.0,

    ## Tx Related
    average_compute_weight_per_tx=0.0,
    average_transaction_size=256,
    transaction_count=0,
    average_compute_weight_per_bundle=0.0,
    average_bundle_size=0,
    bundle_count=0,

    # Uncategorized Terms
    storage_fee_per_rewards=0.0,
    avg_blockspace_usage=0.0,
    reference_subsidy=0.0,
    compute_fee_multiplier=0.0,
    free_space=0.0,
    extrinsic_length_in_bytes=0.0,
    storage_fee_in_credits_per_bytes=0.0,
    priority_fee_volume=0.0,
    consensus_extrinsic_fee_volume=0.0,
    max_normal_weight=0.0,
    max_bundle_weight=0.0,
    target_block_fullness=0.0,
    adjustment_variable=0.0,
    storage_fees_to_farmers=0.0,
    storage_fees_to_fund=0.0,
    target_block_delta=0.0,
    targeted_adjustment_parameter=0.0,
    tx_compute_weight=0.0,
    # Allocations
    allocated_tokens_investors = 0.0,
    allocated_tokens_founders = 0.0,
    allocated_tokens_team = 0.0,
    allocated_tokens_advisors = 0.0,
    allocated_tokens_vendors = 0.0,
    allocated_tokens_ambassadors = 0.0,
    allocated_tokens_testnets = 0.0525 * MAX_CREDIT_ISSUANCE,
    allocated_tokens_foundation = 0.15 * MAX_CREDIT_ISSUANCE,
    allocated_tokens_subspace_labs = 0.07 * MAX_CREDIT_ISSUANCE,
    allocated_tokens_ssl_priv_sale = 0.019 * MAX_CREDIT_ISSUANCE,
    community_owned_supply = 0.0,

    ## Cummulative Metrics
    cumm_rewards=0.0,
    cumm_storage_fees_to_farmers=0.0,
    cumm_compute_fees_to_farmers=0.0,
)
