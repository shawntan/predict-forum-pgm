import random
import math
import json
import re
import collections
import numpy as np
class LDASampler(object):
	"""
	A Gibbs sampler for collapsed LDA. 

	Allows approximate sampling from the posterior distribution over
	assignments of topic labels to words in a collapsed LDA model, which is
	derived from LDA by integrating out the topic and document parameters. 
	These parameters are estimated later from a particular assignment.
	See Griffiths and Steyvers (2004): 
	http://www.pnas.org/content/101/suppl.1/5228.full.pdf
	"""

	def __init__(self, docs=None, num_topics=None, alpha=0.1, beta=0.1, state=None):
		"""
		Initialize sampler for the given data or load previous run.
		"""
		if state:
			self.__dict__ = json.loads(state)
		else:
			self.a = float(alpha)
			self.b = float(beta)
			self.T = int(num_topics)
			self.docs = docs
			self.vocab = list(set(word for doc in self.docs 
										for word in doc))
			self.D = len(self.docs)  
			self.W = len(self.vocab)

			# mapping from words to integers
			to_int = dict((word, w) for (w, word) in enumerate(self.vocab))

			# count data for Gibbs sampling         
			self.nt = np.zeros(self.T)#[0] * self.T
			self.nd = np.array([len(doc) for doc in self.docs])
			self.nwt = np.zeros((len(self.vocab),self.T)) # [[0] * self.T for _ in self.vocab]
			self.ndt = np.zeros((len(self.docs),self.T))  # [[0] * self.T for _ in self.docs]
			# initialize topic assignments and counts
			self.assignments = []
			for d, doc in enumerate(docs):
				for i, word in enumerate(doc):
					w = to_int[word]
					t = random.randint(0, self.T - 1)
					z = [d, i, w, t]
					self.assignments.append(z)
			for z in self.assignments:
				d, _, w, t = z
				self.nt[t] += 1
				self.nwt[w][t] += 1
				self.ndt[d][t] += 1

			self.assignments = np.array(self.assignments)

	def to_json(self):
		"""
		Representation of sampler in JSON.
		"""
		return json.dumps(self.__dict__)

	def next(self):
		"""
		Sample a new state for the topic assignments.
		"""
		for z in self.assignments:
			self.sample(z)

	def sample(self, z):
		"""
		Sample a new value for topic assignment z.
		"""
		d, _, w, old_t = z

		# decrement counts for current topic
		self.nt[old_t] -= 1
		self.ndt[d][old_t] -= 1
		self.nwt[w][old_t] -= 1

		# sample a new topic
		unnorm_ps = []
		for t in range(self.T):
			unnorm_ps.append(self.f(d, w, t))
		r = random.random() * sum(unnorm_ps)
		new_t = self.T - 1
		for i in range(self.T):
			r = r - unnorm_ps[i]
			if r < 0:
				new_t = i
				break
		z[3] = new_t

		# increment counts for new topic
		self.nt[new_t] += 1
		self.ndt[d][new_t] += 1
		self.nwt[w][new_t] += 1

	def f(self, d, w, t):
		"""
		A quantity proportional to the probability of topic t being assigned
		to word w in document d.
		"""
		return ((self.ndt[d][t] + self.a) * 
				(self.nwt[w][t] + self.b) / 
				(self.nt[t] + self.W * self.b))

	def pw_z(self, w, t):
		"""
		Probability of word w given topic t.
		"""
		return (self.nwt[w][t] + self.b) / (self.nt[t] + self.W * self.b)

	def pz_d(self, d, t):
		"""
		Probability of topic t given document d.
		"""
		return (self.ndt[d][t] + self.a) / (self.nd[d] + self.T * self.a)

	def estimate_phi(self):
		"""
		Return estimated phi based on predictive distribution over words.
		"""
		return [[self.pw_z(w, t) for w in range(self.W)] 
									for t in range(self.T)]

	def estimate_theta(self):
		"""
		Return estimated theta based on predictive distribution over topics.
		"""
		return [[self.pz_d(d, t) for t in range(self.T)] 
									for d in range(self.D)]

	def topic_keys(self, num_displayed=30):
		"""
		Return most probable words for each topic.
		"""
		phi = self.estimate_phi()
		tks = []
		for w_ps in phi:
			tuples = [(p, self.vocab[i]) for i, p 
											in enumerate(w_ps)]
			tuples.sort(reverse=True)
			tks.append([word for (p, word) 
								in tuples[:num_displayed]])
		return tks

	def doc_keys(self, num_displayed=5, threshold=.02):
		"""
		Return most probable topics for each document.
		"""
		theta = self.estimate_theta()
		dks = []
		for t_ps in theta:
			tuples = [(p, t) for t, p 
								in enumerate(t_ps)]
			tuples.sort(reverse=True)
			dks.append([(p, t) for (p, t)
							in tuples[:num_displayed]
							if p >= threshold])
		return dks

	def doc_detail(self, d):
		"""
		Show topic and summary of topic for each word in the document.
		"""
		tks = self.topic_keys(num_displayed=5)
		for w, word in enumerate(self.docs[d]):
			topic = 0
			max_p = 0
			for t in range(self.T):
				p = self.f(d, w, t)
				if p > max_p:
					max_p = p
					topic = t
			s = ' '.join(tks[topic])
			print '%s \t %i %s' % (word, topic, s)

	def symKL(P, Q):
		"""
		Symmetric KL divergence of distributions P and Q.
		"""
		return sum((P[i] - Q[i]) * math.log(P[i] / Q[i]) 
					for i in range(len(P)))
	def doc_distribution(self,doc):
		"""
		doc: list of tokens for document
		"""
		result = np.zeros(self.T)
		for w in doc:
			try:
				w = self.vocab.index(w)
				# maximise over the topics to get highest probability
				t = max(range(self.T) , key=lambda x: self.pw_z(w,x) )
				result[t] += 1
			except Exception: pass
		result = result/sum(result)
		return result
