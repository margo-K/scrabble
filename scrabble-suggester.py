#!/usr/bin/env python

import itertools
import heapq
from scrabble import ngram,ismatch,gram_file
import cPickle
from functools import partial
import sys
import importlib
import os
import pdb
si = __import__('scrabble-indexer')

class GramSuggester(object):
	def __init__(self,index_folder='grams',maxn=4):
		self._maxn = maxn
		self._index_folder = index_folder
		self._gram_file = partial(gram_file,self._index_folder)
		self._open_files = [] # list of all files opened for a given query
		self._words = si.GramIndexer('dictionary.txt')._words


	def maxgram(self,Q):
		"""Returns a tuple of the maximum size n-grams of Q and that maxn value

		Ex: if self.maxn = 4 (i.e. the index only indexes up to 4-grams):
			maxgram('octopus') => (set(['octo', 'topu', 'ctop', 'opus']), 4)
			maxgram('hat') =>  (set[('hat')], 3)
			                 """
		maxsize = min(len(Q),self._maxn)
		return ngram(Q,maxsize) if maxsize > 0 else []

	def word(self,word_rank):
		"""Returns the word corresponding to an absolute word_rank

		Ex: word(0) =>  photosynthesizing, 
		which means that photosynthesizing has the highest scrabble score
		in the dictionary                                             """
		return self._words[word_rank]

	def matches(self,gram):
		"""Returns an open file that corresponds to matches to gram"""
		fn = self._gram_file(gram)
		if not os.path.exists(fn):
			return []

		open_file = open(fn)
		self._open_files.append(open_file)
		return (int(word.strip('\n')) for word in open_file)

	def _merge(self,*its):
		"""Merges the sorted iterators in *its, returning an empty list if any of them is empty"""
		if [] in its:
			return []
		return heapq.merge(*its)

	def _intersect(self,*its):
		"""Returns a generator that yields all values that appear in all *its """
		intersection = (value for value,instances in itertools.groupby(self._merge(*its)) if len(list(instances))==len(its))

		return intersection

	def intersect(self,*grams):
	    """Returns a generator that yields all values matching all n-grams in grams """
	    if len(grams)==1:
	    	return self.matches(grams[0])
	    intersection = self._intersect(*map(self.matches,grams))
	    return intersection
		
	def gram_matches(self,Q):
		"""Returns a lazy iterator over all words that contain matches to all ngrams
		in the query string"""
		gram_s = itertools.imap(self.word,self.intersect(*self.maxgram(Q)))
		return gram_s
	
	def exact_matches(self,Q):
		"""Returns a lazy iterator over all words that match the query string
		exactly"""
		matches_query = partial(ismatch,Q)
		return itertools.ifilter(matches_query,self.gram_matches(Q))
	
	def top_results(self,Q,K):
		"""Returns an iterator over the top K words that match the
		query string"""
		results = list(itertools.islice(self.exact_matches(Q),K))
		for f in self._open_files:
			f.close()
		return results


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

