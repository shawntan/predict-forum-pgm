#!/usr/bin/python2
import os
import numpy as np
import cPickle as pickle
from collections import defaultdict
import lib.io.pickled_globals
import lib.graphs as graphs

def main():
	directory = 'graphs/prob_dist'
	if not os.path.exists(directory): os.makedirs(directory)
	for i in range(1,10):
		hist  = pickle.load(open('graphs/histograms/w%d_histograms'%(i+1),'rb'))
		model = [] 
		for topic_hist in hist:
			total     = sum(topic_hist[i] for i in topic_hist)
			prob_dist = defaultdict(float,((i,topic_hist[i]/float(total)) for i in topic_hist))
			model.append(prob_dist)
			print prob_dist
		pickle.dump(model,open('graphs/prob_dist/dist_t%03d'%i,'wb'))


def time_dist(topic_dist,model,limit = 24*3*2):
	t_dist = np.zeros(limit)
	for i in range(limit):
		t_dist[i] = sum(model[t][i] * topic_dist[t] for t in range(len(topic_dist)))
	t_dist = t_dist/sum(t_dist)
	return t_dist
if __name__ == '__main__':
	#main()
	model = pickle.load(open('graphs/prob_dist/dist_t%03d'%9,'rb'))
	#print model
	print time_dist([0.1 for i in range(9)],model)
