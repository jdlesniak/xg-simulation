from understatapi import UnderstatClient

def get_team_and_opponent_xg_dict(team_slug: str, season: str) -> dict:
    """
    Returns a dict of per-match xG lists for `team_slug` and its opponent.
    
    Output format:
      {
        <match_id>: {
          "datetime": <match datetime string>,
          "<team_slug>": [xG1, xG2, …],
          "<opponent_name>": [xG1, xG2, …]
        },
        …
      }
    """
    result = {}
    with UnderstatClient() as client:
        matches = client.team(team=team_slug).get_match_data(season=season)
        for m in matches:
            m_id      = m["id"]
            dt        = m["datetime"]
            side      = m["side"]        # 'h' or 'a'
            home_team = m["h"]["title"]
            away_team = m["a"]["title"]

            if side == "h":
                opponent       = away_team
                shots_key      = "h"
                opp_shots_key  = "a"
            else:
                opponent       = home_team
                shots_key      = "a"
                opp_shots_key  = "h"

            shots_data = client.match(match=str(m_id)).get_shot_data()

            # extract only xG values
            team_xg = [float(s["xG"]) for s in shots_data[shots_key]]
            opp_xg  = [float(s["xG"]) for s in shots_data[opp_shots_key]]

            result[m_id] = {
                "datetime":     dt,
                team_slug:      team_xg,
                opponent:       opp_xg,
            }

    return result