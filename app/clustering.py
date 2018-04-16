import scipy.cluster.vq as clst
import math
from user import User
from team import Team
import team
import weights as w

def get_clusters(points):
    centroids = clst.kmeans([point[:len(point)-1] for point in points],2)[0].tolist()
    c1, c2 = ([],[])
    for point in points:
        if team.dist(centroids[0],point) < team.dist(centroids[1],point):
            c1.append(point)
        else:
            c2.append(point)
    return [c1,c2]

# Recursively performing 2-means clustering
# until the number of each cluster is less than or equal to the max team size
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
    # the reason why appending 0 here is for later exper_date transformation, 
    # if stu did not bid the topic, the weight of that topic will be 0
    weights.append(0)
    exper_data = [[weights[int(data)-1] for data in row] for row in exper_data]
    count = 0 # count the # of stu who did not bid any topics
    stuff = []
    for i in range(len(exper_data)):
        if sum(exper_data[i]) == 0:
            stuff.append(users[i])
            count+=1
    print "{} student(s) who did not bid any topics.".format(count)
    for user in stuff:
        print user.pid # print pid of users who did not bid any topics
    # The reason why adding the index to the end of each item in exper_data is that
    # it is used for identify the corresponding user after performing k-means clustering
    build_teams([exper_data[i] + [i] for i in range(len(exper_data))],assignments,max_size)
    teams = [Team([users[user[-1]] for user in group]) for group in assignments]
    for team in teams:
        for other_team in team.team_prefs(teams):
            if team is not other_team and len(team.members) + len(other_team.members) <= max_size:
                team.merge_with_team(teams.pop(teams.index(other_team)))
    return (teams,users)
