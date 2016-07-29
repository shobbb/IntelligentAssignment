def get_col(data,pos):
    return [val[pos] for val in data]

def find_costs(data,mts):
	costs = []
	for priority in range(int(max(data[0]))):
		val = []
		for col in range(len(data[0])):
			col = get_col(data,col)
			if col.count(priority+1)>0:
				val.append(abs(mts - col.count(priority+1)))
		costs.append(float(sum(val))/(mts*len(val)))
	return costs
            

def find_weights(data,mts):
	weights = []
	costs = find_costs(data,mts)
	for priority in range(int(max(data[0]))):
		weights.append((max(data[0])/(priority+1))/costs[priority])
	return weights