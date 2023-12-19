import logging

logger = logging.getLogger('subspace-digital-twin')
import glob

# logging.basicConfig(filename='cadcad.log', level=logging.INFO)
import os
from datetime import datetime

import click
import IPython
import pandas as pd
import panel as pn

from subspace_model import default_run_args
from subspace_model.experiments.charts import (
    ab_block_utilization,
    ab_circulating_supply,
    ab_circulating_supply_volatility,
    ab_nominator_pool_shares,
    ab_operator_pool_shares,
)
from subspace_model.experiments.experiment import (
    fund_inclusion,
    issuance_sweep,
    reward_split_sweep,
    sanity_check_run,
    standard_stochastic_run,
    sweep_credit_supply,
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
    'sanity_check_run': sanity_check_run,
    'standard_stochastic_run': standard_stochastic_run,
    'issuance_sweep': issuance_sweep,
    'fund_inclusion': fund_inclusion,
    'reward_split_sweep': reward_split_sweep,
    'sweep_credit_supply': sweep_credit_supply,
}

experiment_charts = {
    'sanity_check_run': [],
    'standard_stochastic_run': [
        # ab_circulating_supply,
        # ab_operator_pool_shares,
        # ab_nominator_pool_shares,
        # ab_block_utilization,
    ],
    'issuance_sweep': [
        # ab_circulating_supply,
        # ab_operator_pool_shares,
        # ab_nominator_pool_shares,
        # ab_block_utilization,
        # ab_circulating_supply_volatility,
    ],
    'fund_inclusion': [],
    'reward_split_sweep': [],
    'sweep_credit_supply': [
        # ab_circulating_supply,
        # ab_operator_pool_shares,
        # ab_nominator_pool_shares,
        # ab_block_utilization,
        # ab_circulating_supply_volatility,
    ],
}


def write_pickle_results(df, directory: str, filename: str):
    filepath = os.path.join(directory, filename)

    # Check if the directory exists, create it if it doesn't
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the DataFrame
    df.to_pickle(filepath, compression='gzip')
    logger.info(f'Results saved to {filepath}.')


def find_latest_simulation(experiment: str) -> str | None:
    pattern = f'data/simulations/{experiment}-*.pkl.gz'
    files = glob.glob(pattern)

    if experiment not in list(experiments.keys()):
        logger.warning(
            f'Experiment {experiment} not found. Try one of: {list(experiments.keys())}'
        )
        return None

    if not files:
        logger.warning(
            f'No data found for experiment: {experiment}. Try generating data with `python -m subspace_model -e {experiment}'
        )
        return None

    # Get the most recent file based on modification time
    latest_file = max(files, key=os.path.getmtime)

    # Get the timestamp of the experiment
    timestamp = '-'.join(latest_file.split('-')[1:]).replace('.pkl.gz', '')

    return timestamp


def get_charts(df: pd.DataFrame, experiment: str):
    charts = [
        (plot.__name__, plot(df, experiment)) for plot in experiment_charts[experiment]
    ]

    return charts


def save_charts(experiment: str):
    logger.info(f'Visualizing experiment: {experiment}...')
    latest_simulation_timestamp = find_latest_simulation(experiment)
    if latest_simulation_timestamp is not None:
        latest_simulation = (
            f'data/simulations/{experiment}-{latest_simulation_timestamp}.pkl.gz'
        )
        df = pd.read_pickle(latest_simulation)

        # Check if the directory exists, create it if it doesn't
        directory = f'data/charts/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        charts = get_charts(df, experiment)
        for chart_name, chart in charts:
            logger.info(f'Generating chart {chart_name} for experiment {experiment}...')
            chart.write_image(
                f'{directory}{experiment}-{latest_simulation_timestamp}-{chart_name}.png'
            )


def run_experiment(experiment: str, pickle: bool, samples: int | None = None):
    """
    Run an experiment and optionally pickle the results.
    """
    logger.info(f'Executing experiment: {experiment}...')
    experiment_run = experiments[experiment]
    if samples is not None:
        df = experiment_run(SAMPLES=samples)
    else:
        df = experiment_run()

    logger.info(f'{experiment} executed.')
    logger.info(df)

    # Conditionally pickle the results
    if pickle:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        write_pickle_results(
            df,
            directory='data/simulations/',
            filename=f'{experiment}-{timestamp}.pkl.gz',
        )


@click.command()
@click.option(
    '-e',
    '--experiment',
    'experiment',
    type=click.Choice(experiments.keys(), case_sensitive=False),
    default='standard_stochastic_run',
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
@click.option(
    '-a',
    '--run-all',
    'run_all',
    default=False,
    is_flag=True,
    help='Run all experiments.',
)
@click.option(
    '-v',
    '--visualize',
    'visualize',
    default=False,
    is_flag=True,
    help='Visualize the most recent results of the selected experiment. Combine with -e or -a to select which experiment results to visualize.',
)
@click.option(
    '-s',
    '--samples',
    'samples',
    default=None,
    type=int,
    help='Set Sample size; if not set runs default sample size.',
)
def main(
    experiment: str,
    pickle: bool,
    interactive: bool,
    log_level: str,
    clear_cache: bool,
    run_all: bool,
    visualize: bool,
    samples: int | None,
) -> None:
    # Initialize logging

    logger.info(f'Initializing main...')
    logger.info(f'Setting log level to {log_level}...')
    logger.setLevel(log_levels[log_level])

    # Conditionally clear the cache
    if clear_cache:
        logger.info(f'Clearing caches for all experiments.')
        pn.state.clear_caches()

    # All experiments selected
    if run_all:
        for experiment in list(experiments.keys()):
            if visualize:
                save_charts(experiment)
            else:
                run_experiment(experiment, pickle, samples)

    # Single experiment selected
    else:
        if visualize:
            save_charts(experiment)
        else:
            run_experiment(experiment, pickle, samples)

    # Conditionally drop into an IPython shell
    if interactive:
        IPython.embed()


if __name__ == '__main__':
    main()
