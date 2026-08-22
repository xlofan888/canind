import os
import yaml
from pathlib import Path
from datetime import datetime, timezone
from src.database.repository import init_db, upsert_observations, save_scores, read_observations
from src.collectors.demo import demo_frame
from src.transforms.scoring import calculate_recession_risk, calculate_momentum, calculate_breadth, calculate_transition

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run():
    init_db()

    # v0.1 uses demo data to guarantee a working app.
    # Replace/extend this block with mapped StatsCan vector IDs as they are validated.
    df = demo_frame()
    rows = df.to_dict("records")
    upsert_observations(rows)

    all_data = read_observations()
    thresholds = load_yaml("config/thresholds.yaml")["recession"]
    scores = {
        "recession_risk": calculate_recession_risk(all_data, thresholds),
        "transition_score": calculate_transition(all_data),
        "momentum_score": calculate_momentum(all_data),
        "breadth_score": calculate_breadth(all_data),
    }
    save_scores(scores)
    return scores

if __name__ == "__main__":
    print(run())
