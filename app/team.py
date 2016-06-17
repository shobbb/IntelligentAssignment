from user import User
import math

def dist(p1,p2):
  return math.sqrt(sum([(p1[i] - p2[i])**2 for i in range(len(p1))]))

class Team:
    members = []
    def __init__(self,members):
      self.members = members

    def __str__(self):
    	return ",".join([str(user) for user in self.members])
    
    def users_to_pawn(self,user=[]):
      users = []
      for member in self.members+user:
        for teammember in self.members+user:
          if member is not teammember and User.worked_with(member,teammember):
            users.append(member)
      return users

    def centroid_value(self):
      return [sum([member.topic_rank[topic] for member in self.members])/len(self.members) for topic in range(len(self.members[0].topic_rank))]

    def take_user_from(self,team,user):
      self.members.append(team.members.pop(team.members.index(user)))

    def merge_with_team(self,team):
      for member in team.members:
        self.members.append(member)

    def user_prefs(self,users):
      users = sorted(users,key=lambda user: dist(self.centroid_value(),user.topic_rank))
      return sorted(users,key=lambda user: user in self.users_to_pawn([user]))

    def team_prefs(self,teams):
      return sorted(teams,key=lambda team: dist(self.centroid_value(),team.centroid_value()))

    def team_with_user(teams,user):
    	for team in teams:
    		if user in team.members:
    			return team
    	return None
    team_with_user = staticmethod(team_with_user)