class User:
    def __init__(self,topic_rank,pid,history=[]):
        self.topic_rank = topic_rank #essentially a list of bids
        self.pid = pid
        self.history = history #made to hold a history of users this user has teamed with

    def __str__(self):
      return str(self.pid)

    def worked_with(user1,user2): #checks if two users have worked together
   		for user in user1.history:
   			if user2.pid == user:
   				return True
   		return False
    worked_with = staticmethod(worked_with)

    def user_with_pid(users,pid): #finds user with pid
      for user in users:
        if user.pid == pid:
          return user
      return None
    user_with_pid = staticmethod(user_with_pid)

