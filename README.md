#Intelligent Assignment

Intelligent assignment creates teams, based off of each individual users ranking of topic preference, using k-means clustering. This webservice requires an input of each users ranks and unique id, as well as the max team size. This also uses top trading cycles to switch members of teams who have already worked with other members on that team.

Accessing the service
------------------

###1) Access the Webservice online
The service is hosted at: http://peerlogic.org/intelligent_assignment/[method name]. This service can be called without copying the code onto your local machine. 

###2) Run it on your local machine
The service can be copied from its github repository (https://github.com/peerlogic/IntelligentAssignment). It should be deployed as a webservice; though, it will also require the python libraries flask and scipy:

-[Scipy](https://www.scipy.org/scipylib/download.html)

-[Flask](https://pypi.python.org/pypi/Flask)

Methods
------------------

###Creating teams (/merge_teams):
Uses K-means clustering to group users with similar topic interests. Works to eliminate competition for any single topic and increase the likelihood that each user obtains their most preferred topic. 

**Sample input and output**:

-Input: 
```
{"users":[{"ranks":[1,0,2,3], "pid":1023},{"ranks":[1,2,0,3], "pid":4535},{"ranks":[0,2,3,1], "pid":1363},{"ranks":[2,1,0,3], "pid":9841}],"max_team_size":4}
```

-Output: 
```
{"users": [{"ranks": [1,0,2,3],"pid": 1023},{"ranks": [1,2,0,3],"pid": 4535},{"ranks": [0,2,3,1],"pid": 1363},{"ranks": [2,1,0,3],"pid": 9841}],"teams": [[1363,9841],[1023,4535]]}
```

###Swapping Team Members (/swap_team_members):
Uses Top Trading Cycles to swap members, that have already worked with members on their team, with other teams' members. This method only swaps a max of one member per team per run. Begins by first sorting the list of available members by distance from the teams centroid and then by whether or not other members of the team have worked with them. This method requires a history of users that each user has worked with, along with the general information.

**Sample input and output**:

-Input: 
```
{"users":[{"ranks":[1,0,2,3], "history":[4535,9841,9843], "pid":1023},{"ranks":[1,2,0,3], "history":[1023,9843,8542], "pid":4535},{"ranks":[0,2,3,1], "history":[3649,9841,9843], "pid":1363},{"ranks":[2,1,0,3], "history":[1363,1023,3649], "pid":9841}],"teams": [[1023,2549],[4535,9843],[1363,1867,3649],[9841,8542,7521]]} 
```
-Output:
```
{"users": [{"ranks": [1, 0, 2, 3], "pid": 1023, "history": [4535, 9841, 9843]}, {"ranks": [1, 2, 0, 3], "pid": 4535, "history": [1023, 9843, 8542]}, {"ranks": [0, 2, 3, 1], "pid": 1363, "history": [3649, 9841, 9843]}, {"ranks": [2, 1, 0, 3], "pid": 9841, "history": [1363, 1023, 3649]}], "teams": [[9841, 4535], [1023, 1363]]}
```

Client Code Example
------------------

```python

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
```
