def get_col(data,pos):
    return [val[pos] for val in data]

def find_costs(data,mts,mxp):
	costs = []
	for priority in range(mxp):
		val = []
		for col in range(len(data[0])):
			selection = get_col(data,col)
			if selection.count(priority+1)>0:
				val.append(abs(mts - selection.count(priority+1)))
		if sum(val) == 0:
			val.append(1)
		costs.append(float(sum(val))/(mts*len(val)))
	return costs

def find_benefit(mxp,current_pri,data,mts):
	benefit = []
	for col in range(len(data[0])):
		selection = get_col(data,col)
		if selection.count(current_pri)>mts:
			benefit.append(mts)
		else:
			benefit.append(selection.count(current_pri))
	print float(sum(benefit))/len(data)
	return (mxp/current_pri)*(sum(benefit)/len(data))


def find_weights(data,mts):
	weights = []
	max_priority = 0
	for user in data:
		max_priority = max(max_priority,int(max(user)))
	costs = find_costs(data,mts,max_priority)
	for priority in range(max_priority):
		weights.append(find_benefit(max_priority,priority+1,data,mts)/costs[priority])
	return weights