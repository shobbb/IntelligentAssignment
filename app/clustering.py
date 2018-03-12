import scipy.cluster.vq as clst
import math
from user import User
from team import Team
import team
import weights as w

def get_clusters(points):
    cen = clst.kmeans([point[:len(point)-1] for point in points],2)[0].tolist()
    c1, c2 = ([],[])
    if c2:
        for point in points:
            if team.dist(cen[0],point) < team.dist(cen[1],point):
                c1.append(point)
            else:
                c2.append(point)
    else:
        split = int(len(points)/2)
        return [points[:split],points[split:]]
    return [c1,c2]

def build_teams(people,teams,max_size):
    if len(people) <= max_size:
        teams.append(people)
        return
    clusters = get_clusters(people)
    build_teams(clusters[0],teams,max_size)
    build_teams(clusters[1],teams,max_size)

def kmeans_assignment(exper_data,users,max_size):
    assignments = []
    weights = w.find_weights(exper_data,max_size)
    weights.append(0)
    exper_data = [[weights[int(data)-1] for data in row] for row in exper_data]

    build_teams([exper_data[i] + [i] for i in range(len(exper_data))],assignments,max_size)
    teams = [Team([users[user[-1]] for user in group]) for group in assignments]
    for team in teams:
        for other_team in team.team_prefs(teams):
            if team is not other_team and len(team.members) + len(other_team.members) <= max_size:
                team.merge_with_team(teams.pop(teams.index(other_team)))
    return (teams,users)
