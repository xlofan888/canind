import pandas as pd
from src.transforms.scoring import interpolate_score, calculate_momentum

def test_interpolation():
    assert interpolate_score(6.5, [[5.5,0],[6.5,50],[7.5,100]]) == 50

def test_momentum():
    df = pd.DataFrame([
        {"indicator_id":"unemployment","reference_period":"2026-07","value":6.0},
        {"indicator_id":"unemployment","reference_period":"2026-08","value":6.5},
    ])
    assert calculate_momentum(df) < 0
