import itertools
import heapq
from scrabble import ngram,ismatch
import cPickle
from functools import partial
import sys


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

		Ex: values('octo') => [33883, 42033, 42956, 42957, 48766, 52321, 52322, 52323, 
		59771, 63517, 63518, 64582, 71175, 74865, 74866, 75892, 82157, 85543, 85544, 91969]

		"""
		index = self.index[len(gram)]

		return (value for value in index[gram])
	

	def intersect(self,*grams):
	    """Returns a generator that yields all values matching all n-grams in grams """
	    gram_matches = [self.values(gram) for gram in grams]

	    if len(gram_matches)==1:
	    	return gram_matches.pop()

		return (value for value,instances in itertools.groupby(heapq.merge(*gram_matches)) 
			if len(list(instances))==len(gram_matches))

	def top_results(self,Q,K):
		grams,n = self.maxgram(Q)
		matches_query = partial(ismatch,Q)

		try:
			#All words that contain all the n-grams of the query string
			possible_matches = itertools.imap(self.word,self.intersect(*grams)) 

			#All words that exactly match the query string
			exact_matches = itertools.ifilter(matches_query,possible_matches)

			return list(itertools.islice(exact_matches,K))
		except KeyError:
			return []

if __name__ == '__main__':
	if len(sys.argv)==3:
		Q = sys.argv[1]
		K = int(sys.argv[2])
		print "Loading Index..."
		g = GramSuggester()
		print "\n-----Results-----"
		for result in g.top_results(Q,K):
			print result
	else:
		print "Correct Usage: scrabble-suggester Q K"

