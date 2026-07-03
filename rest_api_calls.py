import requests

base_url = "https://jsonmock.hackerrank.com/api"

def get_data(base_url, route, max_pages=None, **params):
    url = base_url + "/" + route

    do_get_all = "page" not in params
    if do_get_all:
        params["page"] = 1

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()['data']

    if do_get_all:
        total_pages = response.json()['total_pages']
        for p in range(2, total_pages+1):
            params["page"] = p
            response = requests.get(url, params=params)
            response.raise_for_status()
            data.extend(response.json()["data"])
            if max_pages and max_pages == p:
                break

    return data

#### Example 1 ####
route = "football_matches"
params = {
    "year":2011,
}
data = get_data(base_url, route, max_pages=2, **params)

#### Example 2 ####
route = "football_matches"
def get_total_goals(team, year):
    data = get_data(base_url, route, year=year, team1=team)
    goals = sum([int(m['team1goals']) for m in data])

    data = get_data(base_url, route, year=year, team2=team)
    goals += sum([int(m['team2goals']) for m in data])

    return goals

get_total_goals("Barcelona", 2011)

#### Example 3 ####
route = "football_matches"
def get_total_matches(team, year):
    data1 = get_data(base_url, route, year=year, team1=team)
    data2 = get_data(base_url, route, year=year, team2=team)

    return len(data1) + len(data2)

get_total_matches("Barcelona", 2011)

#### Example 4 ####
route = "football_matches"
def get_total_wins(team, year):
    data = get_data(base_url, route, year=year, team1=team)
    wins = sum([1 for m in data if int(m['team1goals']) > int(m['team2goals'])])

    data = get_data(base_url, route, year=year, team2=team)
    wins += sum([1 for m in data if int(m['team1goals']) < int(m['team2goals'])])

    return wins

get_total_wins("Barcelona", 2011)

#### Example 5 ####
from dataclasses import dataclass
from collections import defaultdict
@dataclass
class TeamStats:
    team: str = ""
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    goal_difference: int = 0
    points: int = 0
    

def get_stats(year, max_pages = None):
    teams = defaultdict(TeamStats)
    data = get_data(base_url, route, max_pages=max_pages, year=year)
    for m in data:
        t1 = m["team1"]
        t2 = m["team2"]
        for t in [t1, t2]:
            goals_for = int(m["team1goals"]) if t== t1 else int(m["team2goals"])
            goals_against =  int(m["team1goals"]) if t== t2 else int(m["team2goals"])
            goal_difference = goals_for - goals_against
            teams[t].team = t
            teams[t].played += 1
            teams[t].goals_for += goals_for
            teams[t].goals_against += goals_against
            teams[t].goal_difference += goal_difference 
            teams[t].wins += 1 if goal_difference > 0 else 0
            teams[t].losses += 1 if goal_difference <0 else 0
            teams[t].draws += 1 if goal_difference == 0 else 0
            teams[t].points += 3 if goal_difference > 0 else 1 if goal_difference == 0 else 0
    return teams

teams = get_stats(2011, max_pages=2)
ranking = sorted(
    teams.items(),
    key=lambda item: (
        -item[1].points,
        -item[1].goal_difference,
        -item[1].goals_for,
        item[0]
    )
)
team_names = [team for team, _ in ranking]
team_names

#### Example 6 ####
#### Example 7 ####