class User:
    def __init__(self,topic_rank,pid,history=[]):
        self.topic_rank = topic_rank
        self.pid = pid
        self.history = history

    def __str__(self):
      return str(self.pid)

    def worked_with(user1,user2):
   		for user in user1.history:
   			if user2.pid == user:
   				return True
   		return False
    worked_with = staticmethod(worked_with)

    def user_with_pid(users,pid):
      for user in users:
        if user.pid == pid:
          return user
      return None
    user_with_pid = staticmethod(user_with_pid)

