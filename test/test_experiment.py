from subspace_model.experiment import sanity_check_run


def test_sanity_check_run():
    sim_df = sanity_check_run()
    print(sim_df)
