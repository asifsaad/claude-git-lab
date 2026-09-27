from tipcalc.calc import split_bill


def test_split_even_with_default_tip():
    assert split_bill(100, 4) == 27.5


def test_split_with_custom_tip():
    assert split_bill(200, 2, tip_pct=15) == 115.0


def test_split_rounds_to_two_decimals():
    assert split_bill(10, 3, tip_pct=0) == 3.33
