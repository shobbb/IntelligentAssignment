from numpy import random as r
import numpy as np
import weighted_kmeans as wkmeans

def intelligent_assignment(x,w,data_id,mts):
    print(weights)
    print(wkmeans.hierarchical_kmeans(n,d,data,weights,3))

n,d = (100,3)
data = np.matrix(r.randint(100, size=(n,d)))
weights = np.matrix(r.randint(1,4, size=(1,n)))
intelligent_assignment(data,weights,[],3)
