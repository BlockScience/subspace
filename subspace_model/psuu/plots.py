from typing import Callable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier  # type: ignore
from sklearn.tree import DecisionTreeClassifier  # type: ignore
from sklearn.tree import plot_tree  # type: ignore

from subspace_model.psuu import GOVERNANCE_SURFACE_PARAMS


def create_decision_tree_importances_plot(data: pd.DataFrame,
                                          col_name: str,
                                          params_to_use: list = [],
                                          plot_width: float = 36,
                                          plot_height: float = 12,
                                          success_criteria: Callable | str = ''):
    if len(params_to_use) == 0:
        features = GOVERNANCE_SURFACE_PARAMS
    else:
        features= params_to_use

    X = data.loc[:, features]

    if isinstance(success_criteria, str):
        if success_criteria == 'smaller_than_median':
            y = data.loc[:, col_name] < data.loc[:, col_name].median()
        elif success_criteria == 'larger_than_median':
            y = data.loc[:, col_name] > data.loc[:, col_name].median()
        else:
            raise Exception('criteria not specified')
    else:
            y = data[col_name].map(lambda x: success_criteria(x, data[col_name]))

    model = DecisionTreeClassifier(max_depth=3)
    rf = RandomForestClassifier()
    model.fit(X, y)
    rf.fit(X, y)

    X_cols = list(X.columns)

    rf_df = (pd.DataFrame(list(zip(X_cols, rf.feature_importances_)),
                       columns=['features', 'importance'])
             .sort_values(by='importance', ascending=False)
             )

    fig, axes = plt.subplots(nrows=2,
                             figsize=(plot_width, plot_height),
                             dpi=100,
                             gridspec_kw={'height_ratios': [3, 1]})

    (ax_dt, ax_rf) = axes[0], axes[1]
    plot_tree(model,
              rounded=True,
              proportion=True,
              fontsize=8,
              feature_names=X_cols,
              class_names=['threshold not met', 'threshold met'],
              filled=True,
              ax=ax_dt)
    ax_dt.set_title(
        f'Decision Tree for {col_name}, score: {model.score(X, y) :.0%}. N: {len(X) :.2e}')
    sns.barplot(data=rf_df,
                x=rf_df.features,
                y=rf_df.importance,
                ax=ax_rf,
                label='small')
    plt.setp(ax_rf.xaxis.get_majorticklabels(), rotation=45)
    ax_rf.set_title('Feature importance')
    plt.show()

    return fig, axes




def create_impact_dist_plots_by_kpi(df_to_use: pd.DataFrame,
                                          kpi_cols: list[str],
                                          plot_height: float = 3.5,
                                          plot_width: float = 3.5):
    # Define the custom color palette
    custom_palette = ["#000000", "#FF0000"]
    sns.set_palette(custom_palette)

    fig_width = plot_width * len(kpi_cols)
    fig_height = plot_height

    # Create a plot object with subplots.
    fig, axs = plt.subplots(len(phase_cols), len(kpi_cols),
                            figsize=(fig_width, fig_height),
                            sharex='row', sharey='row',
                            gridspec_kw={'hspace': 0.65, 'wspace': 0.65})
    fig.subplots_adjust(top=0.89)
    fig.suptitle("Phase Impact Plot", y = 1.0)

    for row_num, param in enumerate(phase_cols):
        for col_num, kpi in enumerate(kpi_cols):
            sns.kdeplot(
                data=df_to_use,
                x=kpi,
                hue=param,
                ax=axs[row_num, col_num],
                palette=custom_palette,
#                common_norm = True
            )
            axs[row_num, col_num].set_title(f"Impact of \n {param} \n on {kpi}",
                                            fontsize=10)

    plt.show()
    return fig, axs


def create_utility_outcomes_per_parameters_heatmap(utility_df: pd.DataFrame):
    kpi_by_subset = utility_df.groupby('subset').mean()
    row_sums = kpi_by_subset.sum(axis=1)
    sorted_df = kpi_by_subset.loc[row_sums.sort_values(ascending=False).index]

    chart = sorted_df.reset_index(drop=True).hvplot.heatmap(rot=35, height=800, width=800, fontscale=1, cmap='YlGn', title='Sorted Utility outcomes by Parameter Subset', ylabel='Parameter Subset', xlabel='KPI Utility', rasterize=True)
    return chart
