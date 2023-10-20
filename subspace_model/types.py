from typing import Annotated, TypedDict, Union
from dataclasses import dataclass


Days = Annotated[float, 'days']  # Number of days
Credits = Annotated[float, "SSC"]  # Filecoin currency
PerYear = Annotated[float, "1/year"]  # Yearly rate
Year = Annotated[float, "year"]  # Number of years
Percentage = Annotated[float, '%']
    
class SubspaceModelState(TypedDict):
    days_passed: Days
    delta_days: Days
    issuance_balance: Credits
    operators_balance: Credits
    nominators_balance: Credits
    holders_balance: Credits
    farmers_balance: Credits
    staking_pool_balance: Credits
    fund_balance: Credits
    burnt_balance: Credits
    block_reward: Credits

class SubspaceModelParams(TypedDict):
    label: str
    timestep_in_days: Days
    reward_proposer_share: Percentage
    # Fees & Taxes
    fund_tax_on_proposer_reward: Percentage
    fund_tax_on_storage_fees: Percentage
    operator_tax_on_compute_revenue: Percentage

class SubspaceModelSweepParams(TypedDict):
    label: list[str]
    timestep_in_days: list[Days]