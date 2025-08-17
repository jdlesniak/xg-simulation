import numpy as np
import pandas as pd

def simulate_games(xg_dict: dict, n_sims: int) -> dict:
    """
    Simulate matches based on per‐shot xG, returning points, datetime, and total xG.

    Parameters
    ----------
    xg_dict : dict
        {
          match_id: {
            "datetime": "...",
            team_name:    [xG1, xG2, …],
            opponent_name:[xG1, xG2, …]
          },
          …
        }
    n_sims : int
        Number of Monte Carlo simulations per match.

    Returns
    -------
    sim_results : dict
        {
          match_id: {
            "datetime": "<match datetime>",
            "<team_name>":      np.ndarray(shape=(n_sims,), dtype=int),
            "<opponent_name>":  np.ndarray(shape=(n_sims,), dtype=int),
            "<team_name>_total_xg":     float,
            "<opponent_name>_total_xg": float
          },
          …
        }
    """
    rng = np.random.default_rng()
    sim_results = {}

    for match_id, info in xg_dict.items():
        # pull out the datetime for this match
        match_dt = info["datetime"]

        # identify team & opponent keys
        keys = [k for k in info if k != "datetime"]
        team, opponent = keys[0], keys[1]

        # arrays of xG values
        team_xg = np.array(info[team], dtype=float)
        opp_xg  = np.array(info[opponent], dtype=float)

        # compute total xG
        total_xg_team = float(team_xg.sum())
        total_xg_opp  = float(opp_xg.sum())

        # simulate goals
        team_goals = (rng.random((n_sims, team_xg.size)) <= team_xg).sum(axis=1)
        opp_goals  = (rng.random((n_sims, opp_xg.size))  <= opp_xg).sum(axis=1)

        # assign points
        pts_team = np.where(
            team_goals >  opp_goals, 3,
            np.where(team_goals == opp_goals, 1, 0)
        )
        pts_opp = np.where(
            opp_goals >  team_goals, 3,
            np.where(opp_goals  == team_goals, 1, 0)
        )

        # build result entry
        sim_results[match_id] = {
            "datetime":               match_dt,
            team:                     pts_team,
            opponent:                 pts_opp,
            f"{team}_total_xg":       total_xg_team,
            f"{opponent}_total_xg":   total_xg_opp
        }

    return sim_results

def results_table(sim_out: dict) -> pd.DataFrame:
    """
    Convert simulation output into a summary table of expected points and total xG, including match date.

    Parameters
    ----------
    sim_out : dict
        {
          match_id: {
            "datetime": "YYYY-MM-DD HH:MM:SS",
            team_name:         np.ndarray(shape=(n_sims,), dtype=int),
            opponent_name:     np.ndarray(shape=(n_sims,), dtype=int),
            "<team_name>_total_xg":    float,
            "<opponent_name>_total_xg": float
          },
          …
        }

    Returns
    -------
    pd.DataFrame
        Columns:
          - match_id
          - date                 (MM-DD-YYYY)
          - team
          - team_total_xg
          - expected_points
          - opponent
          - opponent_total_xg
          - opponent_expected_points
    """
    rows = []
    for match_id, results in sim_out.items():
        # Extract and format date
        raw_dt = results["datetime"]
        date = pd.to_datetime(raw_dt).strftime("%m-%d-%Y")

        # Identify the two teams (skip the "datetime" key)
        teams = [k for k in results.keys() if k not in {"datetime"} and not k.endswith("_total_xg")]
        team, opponent = teams[0], teams[1]

        # Compute expected points
        pts_team = results[team].mean()
        pts_opp  = results[opponent].mean()

        # Extract total xG values
        team_total_xg = results[f"{team}_total_xg"]
        opp_total_xg  = results[f"{opponent}_total_xg"]

        rows.append({
            "match_id":                    match_id,
            "date":                        date,
            "team":                        team,
            "team_total_xg":               team_total_xg,
            "expected_points":             pts_team,
            "opponent":                    opponent,
            "opponent_total_xg":           opp_total_xg,
            "opponent_expected_points":    pts_opp
        })

    return pd.DataFrame(rows)

