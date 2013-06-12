#!/usr/bin/env python

import unittest
from brutesuggester import BruteSuggester
indexer = __import__('scrabble-indexer')
suggester = __import__('scrabble-suggester')


class IndexerTests(unittest.TestCase):
	def setUp(self):
		self.indexer = indexer.GramIndexer('dictionary.txt')

	def test_supergram(self):
		self.indexer._maxn = 4
		word = 'hydra'
		actual_grams = [['h','y','d','r','a'],['hy','yd','dr','ra'],['hyd','ydr','dra'],
			['hydr','ydra']]
		suggester_grams = self.indexer.supergram(word)
		test_grams = zip(actual_grams,suggester_grams)
		failures = [grams for grams in test_grams if set(grams[0]).difference(set(grams[1]))]
		self.assertEqual(failures,[])

	def test_supergram_empty(self):
		word = ''
		self.assertEqual([],list(self.indexer.supergram(word)))

	def test_index_grams(self):
		pass

	def test_generate_index(self):
		pass

class SuggesterTests(unittest.TestCase):
	def setUp(self):
		self.suggester = suggester.GramSuggester()
		self.source = ''

	def test_maxgrams(self):
		self.suggester._maxn = 3
		Q = 'apple'
		failures = set(self.suggester.maxgrams(Q)).difference(set(['app','ppl','ple']))
		self.assertEqual(failures,set([]))

	def test_null_maxgrams(self):
		self.suggester._maxn = 3
		Q = ''
		self.assertEqual(self.suggester.maxgrams(Q),[])
	
	def test_word(self):
		rank,word = (0,'photosynthesizing')
		self.assertEqual(self.suggester._word(rank),word)

	def test_intersect(self):
		"""Checks that values yielded are all matches to the substring combo"""
		grams = ['cart','rats']
		matches = self.suggester.gramintersect(*grams)
		failures = [word for word in matches if 'cart' not in word or 'rats' not in word]
		self.assertEqual(failures,[])

	def test_intersect_empty(self):
		pass

	def test_intersect_single(self):
		Q = 'art'
		grams = self.suggester.maxgrams(Q)
		self.assertEqual(list(self.suggester._gram_intersect(*grams)),list(self.suggester._matches(Q)))
		
	def test_intersect(self):
		l1 = [2,5,7,9,13]
		l2 = [1,2,11,12,13]
		self.assertEqual(list(self.suggester._intersect(l1,l2)),[2,13])

	def test_intersect_empty(self):
		l1 = [1,2,3,4,5]
		l2 = [8,9,10,11]
		self.assertEqual(list(self.suggester._intersect(l1,l2)),[])

	def test_matches_not_in_dic(self):
		Q = 'xyzw'
		self.assertEqual(list(self.suggester._matches(Q)),[])
		
	def test_exact_matches(self):
		Q = 'hippo'
		words = ['hippopotamus','liposuction','hippocampus','other']
		results = self.suggester.exact_matches(Q,words)
		self.assertEqual(list(results),['hippopotamus','hippocampus'])

	def test_top_results(self):
		Q,K = 'creat',100
		brute_suggester = BruteSuggester('dictionary.txt')

		brute_results = brute_suggester.top_results(Q,K)
		my_results = self.suggester.top_results(Q,K)
		self.assertEqual(brute_results,my_results)

	def test_top_results_nomatch(self):
		self.assertEqual([],self.suggester.top_results('xyxqrt',100))

	def test_top_results_nointersect(self):
		Q,K = 'kps',10
		max_grams = ['kp','ps']
		self.assertEqual(list(self.suggester.top_results(Q,K)),[])
	

if __name__ == '__main__':
	unittest.main()
