#!/usr/bin/env python

import itertools
import heapq
from scrabble import ngram,ismatch,file_namer
from functools import partial
import sys
import os
import string

class GramSuggester(object):
	def __init__(self,maxn=4,index_dir='grams',word_dir='words'):
		self._maxn = maxn
		self._word_file_fn = partial(file_namer,word_dir) #generates names of files for rank-> word index
		self._gram_file_fn = partial(file_namer,index_dir) #generates names of files for gram-> matches index
		self._open_files = [] #all open files at a given time
		with open('maxwordlength.txt','r') as f:
			self._max_word_length = int(f.readline().strip(string.whitespace))

	def maxgrams(self,Q):
		"""Returns a list of the n-grams of maxsize for a given query

		Ex: if self.maxn = 4 (i.e. the index only indexes up to 4-grams):
			maxgram('octopus') => ['octo', 'topu', 'ctop', 'opus'], 4)
			maxgram('hat') =>  ['hat'], 3)
			                 """
		maxsize = min(len(Q),self._maxn)
		return ngram(Q,maxsize) if maxsize > 0 else []


	def _word(self,word_rank):
		"""Returns the word corresponding to an absolute word_rank

		Ex: word(0) =>  photosynthesizing, 
		which means that photosynthesizing has the highest scrabble score
		in the dictionary                                            """

		word_file = self._word_file_fn(word_rank)
		if os.path.exists(word_file):
			with open(word_file,'r') as f:
				return f.readline().strip(string.whitespace)

	def _matches(self,gram):
		"""Returns an open file that corresponds to matches to gram"""
		gram_file = self._gram_file_fn(gram)

		if not os.path.exists(gram_file):
			return []

		match_generator = open(gram_file)
		self._open_files.append(match_generator)

		return (int(word.strip('\n')) for word in match_generator)

	def _merge(self,*its):
		"""Returns an iterator over the merged elements in *its, or [] if one of its 
		is empty"""
		return heapq.merge(*its) if [] not in its else []

	def _intersect(self,*its):
		"""Returns a generator that yields all values that appear in the sorted iterators *its """
		return (value for value,instances in itertools.groupby(self._merge(*its)) 
			     if len(list(instances))==len(its))

	def _gram_intersect(self,*grams):
	    """Returns a generator that yields all values that match all grams in *grams """
	    if len(grams)==1:
	    	return self._matches(grams[0])
	    intersection = self._intersect(*map(self._matches,grams))
	    return intersection
		
	def _words(self,rank_it):
		"""Returns a lazy iterator of the words that correspond to the ranks in rank_it
		Ex: words([69474,80707]) => iter(['bourdons','bourdon']) """
		return itertools.imap(self._word,rank_it)
	
	def exact_matches(self,Q,word_it):
		"""Returns a lazy iterator over all words in word_it that match the query string
		exactly"""
		matches_query = partial(ismatch,Q)
		return itertools.ifilter(matches_query,word_it)

	def _top(self,K,it):
		"""Returns the top K items from it"""
		return list(itertools.islice(it,K))

	def _close_files(self):
		"""Closes all files that have been opened over the course of the query"""
		for f in self._open_files:
			f.close()
			self._open_files.remove(f)
	
	def top_results(self,Q,K):
		"""Returns the top K words that match Q"""
		intersection = self._words(self._gram_intersect(*self.maxgrams(Q)))
		matches = self.exact_matches(Q,intersection)
		results = self._top(K,matches)

		self._close_files()
		return results

def main(argv=None,printing=True):
    if argv is None:
        argv = sys.argv
    if len(argv)==3:
    	Q = argv[1]
    	K = int(argv[2])
    	g = GramSuggester()
    	if len(Q) > g._max_word_length:
    		results = []
    	else: 
    		results = g.top_results(Q,K)
    	if printing:
	    	print "\n-----Results-----"
	    	for result in results:
	    		print result
    	return results
    else:
		print "Correct Usage: scrabble-suggester Q K"



if __name__ == '__main__':
	main()
