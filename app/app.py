#!/usr/bin/env python -B
import flask,json
from flask import Flask
import clustering as clst
import top_trading_cycles as ttc
import intelligent_assignment as ia
from user import User

def extract_data(req):
	x,w,data_id= ([],[],[])
	for point in req['bids']:
		x.append(point['ranks'])
		w.append(point['weight'])
		data_id.append(point['id'])
	return x,w,data_id

def extract_users(req):
	exper_data,users = ([],[])
	for user in req['users']:
		exper_data.append([float(data) for data in user['ranks']])
		if "history" in user:
			users.append(User(exper_data[-1],user['pid'],user['history']))
		else:
			users.append(User(exper_data[-1],user['pid']))
	return exper_data,users

def send_data_as_json(teams):
	json_obj = [[user.pid for user in team.members] for team in teams]
	return flask.Response(json.dumps({"teams":json_obj,"users":flask.request.json['users']}),  mimetype='application/json')

app = Flask(__name__)

@app.route('/merge_teams',methods=['POST'])
def clstbuild():
    if not 'users' in flask.request.json or not 'max_team_size' in flask.request.json or sum([not 'ranks' in user or not 'pid' in user for user in flask.request.json['users']]) > 0:
    	flask.abort(400)
    data,users = extract_users(flask.request.json)
	# x,w,data_id = extract_data(flask.request.json)
	# ia.intelligent_assignment(x,w,data_id,flask.request.json['max_team_size'])
    teams,users = clst.kmeans_assignment(data, users, flask.request.json['max_team_size'])
    return send_data_as_json(teams)

@app.route('/swap_team_members',methods=['POST'])
def ttctrading():
	if not 'users' in flask.request.json or not 'teams' in flask.request.json or sum([not 'history' in user or not 'ranks' in user or not 'pid' in user for user in flask.request.json['users']]) > 0:
		flask.abort(400)
	users = extract_users(flask.request.json)[1]
	teams = [Team([User.user_with_pid(users,pid) for pid in data]) for data in flask.request.json['teams']]
	ttc.team_swap(teams,users)
	return send_data_as_json(teams)

if __name__ == "__main__":
	app.run(debug=True)
