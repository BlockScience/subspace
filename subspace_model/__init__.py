import logging


def setup_logging(
    filename='cadcad.log',
    level=logging.INFO,
    format='\n%(asctime)s - %(name)s - %(levelname)s\n%(message)s',
):
    # Create a logger
    logger = logging.getLogger('subspace-digital-twin')
    logger.setLevel(level)  # Set the logging level

    # Create a file handler and set level to INFO
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)

    # Create a console (stream) handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(format, '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info('------------subspace-digital-twin------------')


setup_logging()


from subspace_model.params import INITIAL_STATE, SAMPLES, SINGLE_RUN_PARAMS, TIMESTEPS
from subspace_model.structure import SUBSPACE_MODEL_BLOCKS

default_run_args = (
    INITIAL_STATE,
    {k: [v] for k, v in SINGLE_RUN_PARAMS.items()},
    SUBSPACE_MODEL_BLOCKS,
    TIMESTEPS,
    SAMPLES,
)

print(default_run_args)
