
def test_calculate_goal_score():
    import pandas as pd
    import numpy as np
    from subspace_model.psuu.kpis import calculate_goal_score
    new_col = 'G2_score'
    N = 100
    d = {"mean_relative_community_owned_supply": np.linspace(0.0, 1.0, N), "cumm_rewards_before_1yr": np.linspace(0.0, 100.0, N)}
    df = pd.DataFrame(d)
    new_df = calculate_goal_score(df, 'G2_community_incentives', new_col)
    assert new_col in new_df
    assert new_df[new_col].dtype == float
    assert new_df.isnull().sum().sum() == 0.0
    for kpi in d.keys():
        assert f"label_{kpi}" in new_df
        assert (new_df[f"label_{kpi}"].dtype == int) or (new_df[f"label_{kpi}"].dtype == bool)




