import logging

logger = logging.getLogger('subspace-digital-twin')
# logging.basicConfig(filename='cadcad.log', level=logging.INFO)
import os
from datetime import datetime

import click
import IPython
from cadCAD_tools.execution import easy_run

from subspace_model import default_run_args
from subspace_model.experiment import standard_run

# Define a dictionary to map string log levels to their corresponding constants in logging module
log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


@click.command()
@click.option(
    '-e',
    '--experiment-run',
    'experiment_run',
    default=False,
    is_flag=True,
    help='Run an experiment.',
)
@click.option(
    '-p',
    '--pickle',
    'pickle',
    default=False,
    is_flag=True,
    help='Pickle results to data/simulations/.',
)
@click.option(
    '-i',
    '--interactive',
    'interactive',
    default=False,
    is_flag=True,
    help='Drop into an IPython shell for interactive exploration.',
)
@click.option(
    '-l',
    '--log-level',
    'log_level',
    type=click.Choice(log_levels.keys(), case_sensitive=False),
    default='info',
    help='Set the logging level.',
)
def main(experiment_run: bool, pickle: bool, interactive: bool, log_level: str) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logger.info(f'Initializing main at {timestamp}')
    logger.info(f'Setting log level to {log_level}')
    logger.setLevel(log_levels[log_level])
    if experiment_run is False:
        df = easy_run(*default_run_args)
        logger.info('Easy run executed.')
    else:
        df = standard_run()
        logger.info('Standard run executed.')
    if pickle:
        filename = f'data/simulations/multi-run-{timestamp}.pkl.gz'
        df.to_pickle(filename, compression='gzip')
        logger.info(f'Results saved to {filename}.')

    logger.info(df)

    if interactive:
        IPython.embed()


if __name__ == '__main__':
    main()
