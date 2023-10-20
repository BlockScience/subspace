from subspace_model.params import SINGLE_RUN_PARAMS, INITIAL_STATE, TIMESTEPS, SAMPLES
from subspace_model.structure import SUBSPACE_MODEL_BLOCKS

default_run_args = (INITIAL_STATE,
                     {k: [v] for k, v in SINGLE_RUN_PARAMS.items()},
                    SUBSPACE_MODEL_BLOCKS,
                    TIMESTEPS,
                    SAMPLES)