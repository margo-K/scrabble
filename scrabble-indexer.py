#!/usr/bin/env python

import cPickle
import sys
import os
from scrabble import ngram,sorted_word_list,file_namer
from functools import partial

import pdb


class GramIndexer(object):
	def __init__(self,source,index_dir='grams',maxn=4,word_dir='words'):
		self._dictionary = sorted_word_list(source)
		self._maxn = maxn
		self._word_dir = word_dir
		self._index_dir = index_dir
		self._index = {}

	@property
	def ranked_words(self):
		"""Returns a sorted list of the dictionary words and their rankings"""

		return enumerate(self._dictionary) # ranked words

	def supergram(self,word):
		"""Generates lists of all n-grams of the word, in the range n=1..self.maxn"""

		max_length = min(len(word),self._maxn)
		for i in range(1,max_length+1):
			yield ngram(word,n=i)


	def index(self,word_rank,grams):
		"""
		Adds each word to the matches for each if its n-grams, for n=1...maxn
		* uses the word's rank instead string as the value
		"""
		for gram in grams:
			entry = self._index.setdefault(gram,[])
			entry.append(word_rank)

	def generate_index(self):
		"""Indexes all n-grams of size 1..maxn that appear in the Scrabble dictionary,
		storing the absolute ranking of each word that contains that n-gram

		Ex: if maxn==4:
			To find all matches for 'ourd': 
			open('grams/ourd.txt') => [69474, 80707, 88030, 93060, 96907, 100629, 100630, 106365]
			
			Where:
				69474 => 'bourdons'
				80707 => 'bourdon'
				88030 => 'sourdines'
			    93060 => 'gourdes', etc.
			                                  """
			
		for word_rank,word in self.ranked_words:
			for grams in self.supergram(word):
				self.index(word_rank,grams)

	def export(self,dic,folder,single_val=False):
		if not os.path.exists(folder):
			os.makedirs(folder)
		for key,values in dic.iteritems():
			with open(file_namer(folder,key),'w') as f:
				if single_val:
					f.write(values+'\n')
				else:
					for value in values:
						f.write(str(value)+'\n')

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(sys.argv)==2:
    	word_source = sys.argv[1]
    	g = GramIndexer(word_source)
    	g.generate_index()
    	word_index = {rank:word for rank,word in g.ranked_words}

    	g.export(g._index,g._index_dir)
    	g.export(word_index,g._word_dir,single_val=True)
    else:
    	print "Correct Usage: scrabble-indexer word-list"

if __name__ == '__main__':
	main()

