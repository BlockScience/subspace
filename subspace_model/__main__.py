import logging

logger = logging.getLogger('subspace-digital-twin')
# logging.basicConfig(filename='cadcad.log', level=logging.INFO)
import os
from datetime import datetime

import click
import IPython
import panel as pn
from cadCAD_tools.execution import easy_run

from subspace_model import default_run_args
from subspace_model.experiment import (
    escrow_inclusion_sweep_run,
    issuance_sweep,
    reward_split_sweep,
    sanity_check_run,
    standard_run,
    standard_stochastic_run,
)

# Define a dictionary to map string log levels to their corresponding constants in logging module
log_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

experiments = {
    'escrow_inclusion_sweep_run': escrow_inclusion_sweep_run,
    'issuance_sweep': issuance_sweep,
    'reward_split_sweep': reward_split_sweep,
    'sanity_check_run': sanity_check_run,
    'standard_run': standard_run,
    'standard_stochastic_run': standard_stochastic_run,
    'easy_run': easy_run,
}


@click.command()
@click.option(
    '-e',
    '--experiment',
    'experiment',
    type=click.Choice(experiments.keys(), case_sensitive=False),
    default='standard_run',
    help='Select an experiment to run.',
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
@click.option(
    '-c',
    '--clear-cache',
    'clear_cache',
    default=False,
    is_flag=True,
    help='Clear cache for all experiments.',
)
def main(
    experiment: str,
    pickle: bool,
    interactive: bool,
    log_level: str,
    clear_cache: bool,
) -> None:
    if clear_cache:
        logger.info(f'Clearing caches for all experiments.')
        pn.state.clear_caches()
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logger.info(f'Initializing main at {timestamp}')
    logger.info(f'Setting log level to {log_level}')
    logger.setLevel(log_levels[log_level])
    if experiment == 'easy_run':
        df = easy_run(*default_run_args)
        logger.info('Easy run executed.')
    else:
        experiment_run = experiments[experiment]
        df = experiment_run()
        logger.info(f'{experiment} executed.')
    if pickle:
        filename = f'data/simulations/multi-run-{experiment}-{timestamp}.pkl.gz'
        df.to_pickle(filename, compression='gzip')
        logger.info(f'Results saved to {filename}.')

    logger.info(df)

    if interactive:
        IPython.embed()


if __name__ == '__main__':
    main()
