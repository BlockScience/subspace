from subspace_model.types import *
import pandas as pd # type: ignore
from typing import Callable, Optional, NamedTuple
## Types

 # A Tensor with (simulation, subset, run, timestep) dimensions
TimestepTensor = pd.DataFrame

# A subset of the TimestepTensor on which there's a single unique value for each of (simulation, subset, run) across the dataset.
TrajectoryDataFrame = TimestepTensor

 # A Tensor with (simulation, subset, run) dimensions
TrajectoryTensor = pd.DataFrame

KPI = float
SuccessThreshold = Optional[bool]


KPIWeights = dict[str, float]
GoalUtility = float
GoalThreshold = Optional[bool]

TrajectoryKPIFunction = Callable[[TrajectoryDataFrame], KPI] # type: ignore
TrajectoryThreshold = Callable[[KPI, list[KPI]], SuccessThreshold]
TrajectoryGoalUtility = Callable[[dict[str, KPI]], GoalUtility]
TrajectoryGoalThreshold = Callable[[GoalThreshold, list[GoalThreshold]], GoalThreshold]

class TrajectoryKPIandThreshold(NamedTuple):
    kpi_function: TrajectoryKPIFunction
    threshold_function: str
