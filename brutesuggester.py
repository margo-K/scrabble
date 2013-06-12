#!/usr/bin/env python

from scrabble import scrabble_score, ismatch
import string
import sys

class BruteSuggester(object):
	def __init__(self,source='dictionary.txt'):
		self.source = source

	def top_results(self,Q,K):
		with open(self.source,'r') as f:
			matches = []
			for word in f:
				if ismatch(Q,word):
					matches.append(word.strip(string.whitespace))
			matches.sort(key=scrabble_score,reverse=True)
			return matches[:K]

class BruteSortedSuggester(object):
	def __init__(self,source='dictionary.txt'):
		with open(source,'r') as f:
		    self.wl = [word.strip(string.whitespace) for word in f]
	        self.wl.sort(key=scrabble_score,reverse=True)

	def top_results(self,Q,K):
		matches = []
		for word in self.wl:
			if len(matches)==K:
				return matches
			if ismatch(Q,word):
				matches.append(word)
		return matches

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv)==3:
		Q = argv[1]
		K = int(argv[2])
		b = BruteSortedSuggester()
		results = b.top_results(Q,K)
		return results
    else:
		print "Correct Usage: brutesuggester.py Q K"

if __name__ == '__main__':
	main()

	