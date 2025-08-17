from understatapi import UnderstatClient
import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
## load the paths
from utilities.paths import *
from scripts.get_data import *
from scripts.simulate_results import *

def execute_simulation(team_slug, season, n_sims = 10_000):
    xg_dict = get_team_and_opponent_xg_dict(team_slug, season)
    sim_out = simulate_games(xg_dict, n_sims)
    results = results_table(sim_out)

    return results

if __name__ == "__main__":
    res = execute_simulation("Manchester_United", "2024")
    print(res.head())