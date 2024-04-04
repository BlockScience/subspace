from subspace_model.types import *
import pandas as pd # type: ignore
from typing import Callable
## Types

 # A Tensor with (simulation, subset, run, timestep) dimensions
TimestepTensor: object = pd.DataFrame

 # A Tensor with (simulation, subset, run) dimensions
TrajectoryTensor = pd.DataFrame

KPI = float
SuccessThreshold = bool
GoalUtility = float
GoalThreshold = bool

TrajectoryKPI = Callable[[TimestepTensor], KPI] # type: ignore
TrajectoryThreshold = Callable[[KPI, list[KPI]], SuccessThreshold]
TrajectoryGoalUtility = Callable[[list[KPI]], GoalUtility]
TrajectoryGoalThreshold = Callable[[GoalThreshold, list[GoalThreshold]], GoalThreshold]

class TrajectoryKPIandThreshold(NamedTuple):
    kpi_function: TrajectoryKPI
    threshold_function: TrajectoryThreshold
