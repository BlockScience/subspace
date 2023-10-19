from typing import Annotated, TypedDict, Union
from dataclasses import dataclass


Days = Annotated[float, 'days']  # Number of days
Credits = Annotated[float, "SSC"]  # Filecoin currency
PerYear = Annotated[float, "1/year"]  # Yearly rate
Year = Annotated[float, "year"]  # Number of years

class SubspaceModelState(TypedDict):
    days_passed: Days
    delta_days: Days
    operators_balance: Credits
    nominators_balance: Credits
    holders_balance: Credits
    farmers_balance: Credits
    staking_pool_balance: Credits
    escrow_fund_balance: Credits

class SubspaceModelParams(TypedDict):
    label: str
    timestep_in_days: Days

class SubspaceModelSweepParams(TypedDict):
    label: list[str]
    timestep_in_days: list[Days]