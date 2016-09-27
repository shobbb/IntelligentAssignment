from user import User
from team import Team

def detect_cycles(graph):
    cycles = []
    for key in graph.keys():
        skey,ckey,cycle = (key,key,[])
        while ckey not in cycle:
            cycle.append(ckey)
            ckey = graph[ckey][0]
        if skey is ckey and sorted(cycle) not in cycles:
            cycles.append(sorted(cycle))
    return cycles


def top_trading_cycles(teams,users):
    while teams:
        graph = {}
        for team in teams:
            for user in team.user_prefs(users):
                if(Team.team_with_user(teams,user)):
                    graph[team] = (Team.team_with_user(teams,user),user)
                    break
        cycles = detect_cycles(graph)
        for cycle in cycles:
            for team in cycle:
                team.take_user_from(graph[team][0],graph[team][1])
            for team in cycle:
                teams.pop(teams.index(team))


def team_swap(teams,users):
    auct_users,auct_teams = ([],[])
    for team in teams:
        if team.users_to_pawn():
            auct_users = auct_users + team.users_to_pawn()
            auct_teams.append(team)
    top_trading_cycles(auct_teams,auct_users)
