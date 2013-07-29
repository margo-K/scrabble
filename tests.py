#!/usr/bin/env python

import unittest
indexer = __import__('scrabble-indexer')
suggester = __import__('scrabble-suggester')
from trials import TrialRunner
from brutesuggester import BruteSuggester

class SuggesterTests(unittest.TestCase):
	def setUp(self):
		self.suggester = suggester.GramSuggester()

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


class LoggerTests(unittest.TestCase):
	def setUp(self):
		self.t = TrialRunner()

	def test_kys(self):
		K = [100,1000]
		qsize = 5
		trials = self.t._kys(K,qsize)
		self.assertEqual(len(trials),len(K))

	def test_qys_logging(self):
		Qsizes = [500,600]
		k = 70
		self.t._qys(Qsizes,k)
		self.assertEqual(Qsizes,sorted(self.t._log['Q'].keys()))

	def test_log_times(self):
		qsize,k,times = 10,100,[5,6,7]
		self.t._log_times(qsize,k,times)
		self.assertEqual(self.t._log['Q'][qsize],times)

	def test_get_time_logging(self):
		qsize, k = 3,100
		total_trials = 100 #default value
		self.t._log['Q'][qsize] = [1]
		len_before = len(self.t._log['Q'][qsize])
		self.t.get_time(3,10)
		len_after = len(self.t._log['Q'][qsize])
		self.assertEqual(len_after-len_before,total_trials)

	def test_logging(self):
		qsizes=[10,20,30]
		self.t.plotQ(qsizes)
		self.assertEqual(qsizes,sorted(self.t._log['Q'].keys()))


if __name__ == '__main__':
	unittest.main()
