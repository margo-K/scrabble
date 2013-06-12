#!/usr/bin/env python
import string
import os

#####################################################
# Scrabble Score calculation and Sorting
#####################################################
scrabble_scores = {'a': 1, 'c': 3, 'b': 3, 'e': 1, 'd': 2, 
'g': 2, 'f': 4, 'i': 1, 'h': 4, 'k': 5, 'j': 8, 'm': 3, 'l': 1,
 'o': 1, 'n': 1, 'q': 10, 'p': 3, 's': 1, 'r': 1, 'u': 1, 't': 1,
 'w': 4, 'v': 4, 'y': 4, 'x': 8, 'z': 10}

def scrabble_score(st,score_map=scrabble_scores): 
	"""Returns the scrabble total for st"""
	return sum([score_map[elem] for elem in st if elem not in string.whitespace])

def sorted_word_list(source,key=scrabble_score):
    """Returns a generator whose values are the words from the source, in sorted order"""
    with open(source,'r') as f:
	    word_list = list(f)   
	    word_list.sort(key=scrabble_score,reverse=True)
	    return [word.strip('\r\n') for word in word_list]

#####################################################
# N-gram calculation and matching
#####################################################
def ngram(word,n):
	"""Returns a set of all n-grams in a given word""" 
	ds = [word[i:i+n] for i in range(len(word)-n+1)]
	return list(set(ds))

def ismatch(Q,word):
	"""Returns true if the query string matches the word"""
	return Q in word


#####################################################
# Covenience function for generating names of files
# for persistent data
#####################################################

def file_namer(folder,keyval):
	"""Returns the name of the file that will contain a given keyvalue"""
	if type(keyval)!=str:
		keyval = str(keyval)
	path = os.path.join(folder,keyval)
	return path + '.txt'
