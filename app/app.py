#!flask/bin/python
from flask import Flask
import flask
from user import User
from team import Team
import user
import json
import clustering as clst
import top_trading_cycles as ttc

def extract_users(req):
	exper_data,users = ([],[])
	for user in req['users']:
		exper_data.append([float(data) for data in user['ranks']])
		if "history" in user:
			users.append(User(exper_data[-1],user['pid'],user['history']))
		else:
			users.append(User(exper_data[-1],user['pid']))
	return exper_data,users

def send_teams_as_json(teams): #this method currently uses the classes defined for bidding
	json_obj = [[user.pid for user in team.members] for team in teams]
	return flask.Response(json.dumps({"teams":json_obj,"users":flask.request.json['users']}),  mimetype='application/json')
	
def extract_task_data(req):
	#extract json data and convert to python object here
	#do not necessarily have to use user class here, it is already defined if you would like to use it
	return req
	
def send_assigned_tasks_as_json(tasks):
	#convert python objects to simple maps and lists
	return flask.Response(json.dumps({"info":tasks}))

app = Flask(__name__)

@app.route('/merge_teams',methods=['POST'])
def clstbuild():
    if not 'users' in flask.request.json or not 'max_team_size' in flask.request.json or sum([not 'ranks' in user or not 'pid' in user for user in flask.request.json['users']]) > 0:
    	flask.abort(400)
    data,users = extract_users(flask.request.json)
    teams,users = clst.kmeans_assignment(data,users, flask.request.json['max_team_size'])
    return send_teams_as_json(teams)

@app.route('/assign_tasks',methods=['POST']) #Add topic code here
def ttctrading():
	if not 'users' in flask.request.json or not 'teams' in flask.request.json or sum([not 'history' in user or not 'ranks' in user or not 'pid' in user for user in flask.request.json['users']]) > 0: #check for required fields in json request here
		flask.abort(400)
	users = extract_task_data(flask.request.json) #extract json data into necessary format
	
	assignments = ttc.team_swap(users) #method where assignment algorithm is run
	return send_assigned_tasks_as_json(assignments) #returning a flask response object

if __name__ == "__main__":
	app.run(debug=True)