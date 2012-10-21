import cPickle as pickle
import sys
import lib.io.pickled_globals
import lib.graphs as graphs
from hist_to_probdist import time_dist
from lib.io.reader import windowed,filter_tokenise
window_size = 15
time_bin 	= 20
def load_model(topics):
	timdist = pickle.load(open('graphs/prob_dist/dist_t%03d'%topics,'rb'))
	lda		= pickle.load(
			open('global_objs/w%d_t%d_learnt_topics'%(window_size,topics),'rb')
			)
	return lda,timdist
def main():
	print "loading documents..."
	documents	= ['data/'+i.strip() for i in open(sys.argv[1],'r')]
	print documents
	lda, time_model = load_model(9)
	docs = ((' '.join(w[2]),dt) for w,dt in windowed(documents,window_size))
	
	for doc,dt in docs:
		topic_dist = lda.doc_distribution(filter_tokenise(doc))
		dt_dist    = time_dist(topic_dist,time_model,limit=24*3*7)
		print sum((i*(time_bin/2)) * p for i,p in enumerate(dt_dist)), dt

if __name__ == "__main__":
	main()

		




