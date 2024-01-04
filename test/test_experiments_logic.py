from subspace_model.const import BLOCKS_PER_MONTH, BLOCKS_PER_YEAR
from subspace_model.experiments.logic import SubsidyComponent, NORMAL_GENERATOR, POISSON_GENERATOR, POSITIVE_INTEGER, MAGNITUDE


def test_reference_subsidy():
    two_years = 2 * BLOCKS_PER_YEAR
    component1 = SubsidyComponent(0, two_years, 10_000, 10_000 / two_years)

    assert sum([component1(t=0)]) == 10_000 / two_years
    assert sum([component1(t=two_years - 1)]) == 10_000 / two_years
    assert sum([component1(t=two_years)]) == 0

    component2 = SubsidyComponent(0, BLOCKS_PER_MONTH, 10_000, 1_000 / BLOCKS_PER_MONTH)
    assert sum([component2(t=0)]) == 1_000 / BLOCKS_PER_MONTH
    assert sum([component2(t=BLOCKS_PER_MONTH - 1)]) == 1_000 / BLOCKS_PER_MONTH
    assert sum([component2(t=BLOCKS_PER_MONTH)]) == 1_000 / BLOCKS_PER_MONTH
    assert sum([component2(t=BLOCKS_PER_MONTH + 1)]) < 1_000 / BLOCKS_PER_MONTH


def test_generators():
    normal = MAGNITUDE(NORMAL_GENERATOR(0.1, 0.1))(0, 0)
    assert (normal >= 0) and (normal <= 1)
