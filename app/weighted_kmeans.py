from random import shuffle
from pyomo.environ import *
from numpy import linalg as la
from numpy import random as r
from collections import deque

import numpy as np

def build_model():
    model = AbstractModel()
    # create mathematical optimization model
    model.k = Param(within=NonNegativeIntegers)
    model.n = Param(within=NonNegativeIntegers)
    model.d = Param(within=NonNegativeIntegers)

    model.I = RangeSet(1, model.k)
    model.J = RangeSet(1, model.n)

    model.x = Param(model.d, model.n)

def get_clusters(X, pos, sites, k):
    clusters = [[] for i in range(k)]
    for i in range(X.shape[0]):
        distance = la.norm(sites-X[i,:],axis=1)
        clusters[np.argmin(distance)].append(pos[i])
    return clusters

def update_sites(k,sites,X,W):
    clusters,distances = (np.repeat(np.array(W),k,axis=0),np.zeros((X.shape[0],k)))
    for i in range(X.shape[0]):
        distance = la.norm(sites-X[i,:],axis=1)
        min_site = r.permutation(np.where(distance==np.min(distance))[0])[0]
        assignment_vector = np.zeros(k)
        assignment_vector[min_site] = 1
        distances[i,min_site] = np.min(distance)
        clusters[:,i] = clusters[:,i] * assignment_vector
    distances = np.matrix(clusters) * np.matrix(distances) / clusters.sum(axis=1)
    return clusters * X / clusters.sum(axis=1).reshape(k,1), distances.diagonal()

def weighted_kmeans(k,n,d,X,W,iters=1):
    # random initialization of sites
    clusterings = {}
    for i in range(iters):
        s,prev_s,distances = (r.permutation(X)[:k,:],np.zeros((k,d)),np.zeros(k))
        while np.sum(la.norm(s-prev_s,axis=1)) > 0:
            prev_s = s
            s,distances = update_sites(k,s,X,W)
        clusterings[np.sum(distances)/k] = s
    return clusterings[np.min(list(clusterings.keys()))]

def hierarchical_kmeans(n,d,X,W,k_plus):
    queue,pos,classif,clusterings = (deque([np.array(range(n))]),np.arange(n),0,np.zeros(n))
    while queue:
        c = queue.popleft()
        sub_X,sub_W,sub_n = (X[c,:],W[0,c],c.shape[0])
        if sub_X.shape[0] <= k_plus:
            clusterings[c] = classif
            classif+=1
            continue
        clusters = get_clusters(sub_X,pos[c],weighted_kmeans(2,sub_n,d,sub_X,sub_W,1),2)
        for cluster in clusters:
            queue.append(np.array(cluster))
    return clusterings
