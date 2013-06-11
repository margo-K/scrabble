import itertools
import heapq
from scrabble import ngram,ismatch
import cPickle
import pdb
from functools import partial

from queries import generate_queries
import time

def run_with_log(g):
	log =[]
	failures = 0
	failures_list = []
	for q,k in generate_queries():
		before = time.time()
		results = g.top_results(q,k)
		after = time.time()
		print q,k,after-before

		if after-before > .001:
			if results:
				log.append((q,after-before))
			else:
				failures+=1
				failures_list.append(q)
		log.sort(key=lambda x: x[1],reverse=True)
	print "Total Over:{}".format(len(log))
	print log
	print "Failures{}:{}".format(failures,failures_list)

class GramSuggester(object):
	def __init__(self,index_name='gramindex.txt',maxn=4):
		self.maxn = maxn
		with open(index_name,'r') as f:
			self.words = cPickle.load(f)
			self.index = cPickle.load(f)

	def maxgram(self,Q):
		"""Returns a tuple of the maximum size n-grams of Q and that maxn value

		Ex: if self.maxn = 4 (i.e. the index only indexes up to 4-grams):
			maxgram('octopus') => (set(['octo', 'topu', 'ctop', 'opus']), 4)
			maxgram('hat') =>  (set[('hat')], 3)                 """

		maxsize = min(len(Q),self.maxn)
		return ngram(Q,maxsize),maxsize

	def word(self,word_rank):
		"""Returns the word corresponding to an absolute word_rank

		Ex: word(0) =>  photosynthesizing, 
		which means that photosynthesizing has the highest scrabble score
		in the dictionary                                             """
		return self.words[word_rank]

	def values(self,gram):
		"""Generator that yields ranks of words matching gram, in 
		descending order of scrabble score (and ascending rank)

		Ex: values('octo') => [33883, 42033, 42956, 42957, 48766, 52321, 52322, 52323, 59771, 63517, 63518, 64582,
		 71175, 74865, 74866, 75892, 82157, 85543, 85544, 91969]

		"""
		index = self.index[len(gram)]

		return (value for value in index[gram])
		# for item in index[gram]: # generator expression
		# 	yield item

	# def get_buckets(self,gramlist,n):
	# 	"""Returns a list of generators for each n-gram in the list"""
	# 	index = self.index[n]
	# 	return [self.values(gram) for gram in gramlist]

	def intersect(self,*grams):
	    """Returns a generator of all values in the intersection of the sorted
	    iterators, *its"""
	    l = [self.values(gram) for gram in grams]
	    if len(l)==1:
	    	yield self.values(gram).next()#want to change to both returning an iterator

	    for value, instances in itertools.groupby(heapq.merge(*l)): ## Figure out what this does when intersection is nothing
	        if len(list(instances)) == len(l):
			    yield value

	def top_results(self,Q,K):
		grams,n = self.maxgram(Q)
		matches_query = partial(ismatch,Q)

		try:
			words = itertools.imap(self.word,self.intersect(*grams))
			exact_matches = itertools.ifilter(matches_query,words)
			return [item for item in itertools.islice(exact_matches,K)]
		except KeyError:
			# print "{} was not found".format(Q)
			return []

if __name__ == '__main__':
	g = GramSuggester()
	# print g.maxgram('hat')
	# print g.maxgram('octopus')
	# print list(g.values('octo'))
	print g.top_results('minty',10)
	run_with_log(g)
	# pdb.set_trace()

