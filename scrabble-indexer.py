import cPickle
import sys
from scrabble import ngram,sorted_word_list

class GramIndexer(object):
	def __init__(self,source,index_name='gramindex.txt',maxn=4):
		self._dictionary = sorted_word_list(source)
		self._words = {num:word for num,word in self.ranked_words}
		self._maxn = maxn
		self._index_name = index_name

	@property
	def ranked_words(self):
		"""Returns a sorted list of the dictionary words and their rankings"""
		return enumerate(self._dictionary) # ranked words

	def supergram(self,word):
		"""Generates all n-grams of the word, in the range n=1..self.maxn

		At each iteration, it yields a tuple: (n,n-grams(word))
		"""
		max_length = min(len(word),self._maxn)
		for i in range(1,max_length+1):
			yield i,ngram(word,n=i)

	def index_grams(self,word_rank,n,grams):
		"""
		Adds each set of n-grams for a word to the index assigned to 
		grams of size n

		* uses the word's rank instead string as the value
		Ex: Word: ''

		"""
		index = self.index[n]

		for gram in grams:
			entry = index.setdefault(gram,[])
			entry.append(word_rank)

	def generate_index(self):
		"""Indexes all n-grams of size 1..maxn that appear in the Scrabble dictionary,
		storing the ranking of each word that contains that n-gram

		Ex: self.index[4]=> index of 2-grams
			To find all matches for 'ourd': 
			g.index[4]['ourd'] => [69474, 80707, 88030, 93060, 96907, 100629, 100630, 106365]
			
			Where:
				69474 => 'bourdons'
				80707 => 'bourdon'
				88030 => 'sourdines'
			    93060 => 'gourdes', etc.
			                                  """
		self.index = {n:{} for n in range(self._maxn+1)}
		for position,word in self.ranked_words:
			for n,grams in self.supergram(word):
				self.index_grams(position,n,grams)

	def export_index(self):
		"""Pickles a copy of the index and word key and writes it to disk"""
		with open(self._index_name,'w') as f:
			cPickle.dump(self._words,f,2)
			cPickle.dump(self.index,f,2)
		print "Index has been written to {}".format(self._index_name)

if __name__ == '__main__':
	if len(sys.argv)==2:
		word_source = sys.argv[1]
		g = GramIndexer(word_source)
		g.generate_index()
		g.export_index()
	else:
		print "Correct Usage: scrabble-indexer word-list"
