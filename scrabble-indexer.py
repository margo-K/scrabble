#!/usr/bin/env python

import cPickle
import sys
import os
from scrabble import ngram,sorted_word_list,gram_file
from functools import partial

import pdb


class GramIndexer(object):
	def __init__(self,source,index_folder='grams/',maxn=4):
		self._dictionary = sorted_word_list(source)
		self._words = {num:word for num,word in self.ranked_words}
		self._maxn = maxn
		self._index_folder = index_folder
		self._gram_file = partial(gram_file,folder=self._index_folder)


	@property
	def ranked_words(self):
		"""Returns a sorted list of the dictionary words and their rankings"""
		return enumerate(self._dictionary) # ranked words

	def supergram(self,word):
		"""Generates lists of all n-grams of the word, in the range n=1..self.maxn
		"""
		max_length = min(len(word),self._maxn)
		for i in range(1,max_length+1):
			yield ngram(word,n=i)


	def index_grams(self,word_rank,grams):
		"""
		Adds each word to all the files that contain its gram

		* uses the word's rank instead string as the value

		"""
		for gram in grams:
			with open(self._gram_file(gram),'a') as f:
				f.write(str(word_rank)+'\n')

	def generate_index(self):
		"""Indexes all n-grams of size 1..maxn that appear in the Scrabble dictionary,
		storing the ranking of each word that contains that n-gram

		Ex: if maxn==4:
			To find all matches for 'ourd': 
			open('grams/ourd.txt') => [69474, 80707, 88030, 93060, 96907, 100629, 100630, 106365]
			
			Where:
				69474 => 'bourdons'
				80707 => 'bourdon'
				88030 => 'sourdines'
			    93060 => 'gourdes', etc.
			                                  """
		if not os.path.exists(index_folder):
			os.makedirs(index_folder)
			
		for position,word in self.ranked_words:
			for grams in self.supergram(word): # make so all words indexed before writing to a file
				self.index_grams(position,grams)

if __name__ == '__main__':
	if len(sys.argv)==2:
		word_source = sys.argv[1]
		g = GramIndexer(word_source)
		g.generate_index()
	else:
		print "Correct Usage: scrabble-indexer word-list"
