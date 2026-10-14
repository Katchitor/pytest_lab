import pytest


@pytest.mark.smoke
def test_add(calc):
    assert calc.add(2, 2) == 4


def test_subtract(calc):
    pass


@pytest.mark.parametrize("a, b, expected", [
    (2, 2, 4),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add_parametrized(calc, a, b, expected):
    assert calc.add(a, b) == expected


def test_divide_by_zero(calc):
    with pytest.raises(ValueError):
        calc.divide(1, 0)


@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, False),
])
def test_is_even(calc, n, expected):
    assert calc.is_even(n) is expected
