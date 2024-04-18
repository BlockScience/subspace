import pandas as pd
from subspace_model.psuu import GOVERNANCE_SURFACE_PARAMS
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree  # type: ignore
from sklearn.tree import DecisionTreeClassifier  # type: ignore
from sklearn.ensemble import RandomForestClassifier  # type: ignore
import seaborn as sns
from typing import Callable

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
