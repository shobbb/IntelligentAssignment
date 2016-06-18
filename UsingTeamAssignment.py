import requests
import json

#Test data
data = json.dumps({"users":[{"ranks":[1,0,2,3], "history":[4535,9841,9843], "pid":1023},{"ranks":[1,2,0,3], "history":[1023,9843,8542], "pid":4535},{"ranks":[0,2,3,1], "history":[3649,9841,9843], "pid":1363},{"ranks":[2,1,0,3], "history":[1363,1023,3649], "pid":9841}],"max_team_size":2})
header = {'content-type': 'application/json'}
response = requests.post("http://127.0.0.1:5000/merge_teams",data= data,headers=header)
print response.text
#The response from merge teams can be used in swap team members if
#history was given in the body of the request to merge teams	
response = requests.post("http://127.0.0.1:5000/swap_team_members", data=response.text,headers=header)
print response.text