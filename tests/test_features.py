import pandas as pd
import pytest

from coupon_project.features import (
    COUPON_FREQUENCY,
    add_travel_time_band,
    build_respondent_id,
    check_journey_flags,
    matched_frequency,
)


def test_journey_flags_and_travel_time_band():
    df = pd.DataFrame({
        "toCoupon_GEQ5min": [1, 1, 1],
        "toCoupon_GEQ15min": [0, 1, 1],
        "toCoupon_GEQ25min": [0, 0, 1],
        "direction_same": [1, 0, 0],
        "direction_opp": [0, 1, 1],
    })
    assert check_journey_flags(df)["invalid_geq_hierarchy_count"] == 0
    out = add_travel_time_band(df)
    assert "travel_time_band" not in df.columns
    assert out["travel_time_band"].astype(str).tolist() == ["5-<15 min", "15-<25 min", ">=25 min"]

    bad = df.copy()
    bad.loc[0, "toCoupon_GEQ25min"] = 1
    with pytest.raises(ValueError):
        add_travel_time_band(bad)


def test_matched_frequency_and_respondent_id():
    df = pd.DataFrame({
        "coupon": ["Bar", "Coffee House", "Carry out & Take away", "Restaurant(<20)", "Restaurant(20-50)"],
        "Bar": ["1~3", "never", "never", "never", "never"],
        "CoffeeHouse": ["gt8", None, "never", "never", "never"],
        "CarryAway": ["never", "never", "4~8", "never", "never"],
        "RestaurantLessThan20": ["never", "never", "never", "less1", "never"],
        "Restaurant20To50": ["never", "never", "never", "never", "gt8"],
        "age": ["21", "21", "31", "31", "31"],
    })
    assert set(COUPON_FREQUENCY) == set(df["coupon"])
    matched = matched_frequency(df)
    assert matched.iloc[0] == "1~3"
    assert pd.isna(matched.iloc[1])
    assert matched.iloc[4] == "gt8"

    pid = build_respondent_id(df, ["age"])
    assert pid.tolist() == [0, 0, 1, 1, 1]
