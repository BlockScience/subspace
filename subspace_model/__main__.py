import logging

logger = logging.getLogger('subspace-digital-twin')
import glob

# logging.basicConfig(filename='cadcad.log', level=logging.INFO)
import os
from datetime import datetime

import click
import IPython
import pandas as pd

pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

from subspace_model.experiments.charts import (  # mc_total_supply,
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
    sweep_over_single_component_and_credit_supply,
)
from subspace_model.experiments.metrics import (
    profit1_mean,
    profit1_trajectory,
    total_supply_max,
    total_supply_mean,
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
    'sweep_over_single_component_and_credit_supply': sweep_over_single_component_and_credit_supply,
}

experiment_charts = {
    'sanity_check_run': [],
    'standard_stochastic_run': [ab_block_utilization],
    'issuance_sweep': [],
    'fund_inclusion': [],
    'reward_split_sweep': [],
    'sweep_credit_supply': [ab_block_utilization],
}

experiment_timestep_metrics = {
    'sanity_check_run': [],
    'standard_stochastic_run': [],
    'issuance_sweep': [],
    'fund_inclusion': [],
    'reward_split_sweep': [],
    'sweep_credit_supply': [],
}

experiment_trajectory_metrics = {
    'sanity_check_run': [total_supply_mean, total_supply_max, profit1_mean],
    'standard_stochastic_run': [total_supply_mean, total_supply_max, profit1_mean],
    'issuance_sweep': [],
    'fund_inclusion': [],
    'reward_split_sweep': [],
    'sweep_credit_supply': [],
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


def run_calculate_metrics(sim_df: pd.DataFrame, experiment: str):
    logger.info(f'Running metrics calculations for {experiment}...')

    # Timestep metrics
    timestep_metrics = experiment_timestep_metrics[experiment]
    if len(timestep_metrics):
        timestep_metrics_df = pd.concat(
            [metrics(sim_df) for metrics in timestep_metrics], axis=1
        )
    else:
        timestep_metrics_df = pd.DataFrame()
    logger.info(f'Timestep metrics for {experiment}:')
    logger.info(timestep_metrics_df)

    # Trajectory metrics
    trajectory_metrics = experiment_trajectory_metrics[experiment]
    if len(trajectory_metrics):
        trajectory_metrics_df = pd.concat(
            [metrics(sim_df) for metrics in experiment_trajectory_metrics[experiment]],
            axis=1,
        )
    else:
        trajectory_metrics_df = pd.DataFrame()
    logger.info(f'Trajectory metrics for {experiment}:')
    logger.info(trajectory_metrics_df)
    logger.info(f'Finished metrics calculations for {experiment}...')
    return timestep_metrics_df, trajectory_metrics_df


def run_experiment(
    experiment: str, samples: int | None = None, days: int | None = None
):
    """
    Run an experiment with for a given number of days and samples.
    """
    logger.info(f'Executing experiment: {experiment}...')
    experiment_run = experiments[experiment]
    if days is not None:
        if samples is not None:
            df = experiment_run(SAMPLES=samples, SIMULATION_DAYS=days)
        else:
            df = experiment_run(SIMULATION_DAYS=days)
    else:
        if samples is not None:
            df = experiment_run(SAMPLES=samples)
        else:
            df = experiment_run()

    logger.info(f'{experiment} executed.')
    logger.info(df)

    return df


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
@click.option(
    '-d',
    '--days',
    'days',
    default=None,
    type=int,
    help='Number of simulation days.',
)
@click.option(
    '-m',
    '--metrics',
    'calculate_metrics',
    default=False,
    is_flag=True,
    help='Run experiment metrics calculations. Optionally save to disk with -p.',
)
def main(
    experiment: str,
    pickle: bool,
    interactive: bool,
    log_level: str,
    run_all: bool,
    visualize: bool,
    samples: int | None,
    days: int | None,
    calculate_metrics: bool,
) -> None:
    # Initialize logging

    logger.info(f'Initializing main...')
    logger.info(f'Setting log level to {log_level}...')
    logger.setLevel(log_levels[log_level])

    # All experiments selected
    if run_all:
        for experiment in list(experiments.keys()):
            if visualize:
                save_charts(experiment)
                return
            else:
                sim_df = run_experiment(experiment, samples, days)
                if calculate_metrics:
                    timestep_metrics_df, trajectory_metrics_df = run_calculate_metrics(
                        sim_df,
                        experiment,
                    )

    # Single experiment selected
    else:
        if visualize:
            save_charts(experiment)
            return
        else:
            sim_df = run_experiment(experiment, samples, days)
            if calculate_metrics:
                timestep_metrics_df, trajectory_metrics_df = run_calculate_metrics(
                    sim_df, experiment
                )

    # Conditionally pickle the results
    if pickle:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        write_pickle_results(
            sim_df,
            directory='data/simulations/',
            filename=f'{experiment}-{timestamp}.pkl.gz',
        )
    if pickle and calculate_metrics:
        write_pickle_results(
            timestep_metrics_df,
            directory='data/metrics/',
            filename=f'{experiment}-timestep-metrics-{timestamp}.pkl.gz',
        )
        write_pickle_results(
            trajectory_metrics_df,
            directory='data/metrics/',
            filename=f'{experiment}-trajectory-metrics-{timestamp}.pkl.gz',
        )

    # Conditionally drop into an IPython shell
    if interactive:
        IPython.embed()


if __name__ == '__main__':
    main()
