
from pprint import pprint
from queries import generate_query_strings
# from brutesuggester import BruteSuggester,BruteSortedSuggester
import pdb
import math
from timeit import Timer
import sys

def avg(s):
	return sum(s)/float(len(s))

def stdev(s):
	return math.sqrt(variance(s))
	
def variance(s):
	return avg(map(lambda x: (x - avg(s))**2, s))
	

class LogItem(object):
	def __init__(self,setup_str,fn_str,name):
		self.setup_str = setup_str
		self.fn_str = fn_str
		self.log = {k:[] for k in [5,10,100,1000]}
		# self.k = K
		self.name = name

	def time(self,q):
		for k in [5,10,100,1000]:
			timer = Timer(self.fn_str,self.setup_str.format(q,k))
			self.log[k].append(min(timer.repeat(3,number=10)))

	def stats(self,k):
		data = self.log[k]
		return avg(data),stdev(data),min(data),max(data)

	def report(self):
		print '{:^20}{:^20}{:^20}{:^20}{:^20}'.format('K','Mean','Stdev','Min','Max')
		print '{:-^100}'.format('')
		for k in sorted(list(self.log.keys())):
			print '{:^20}{:^20}{:^20}{:^20}{:^20}'.format(k,*self.stats(k))


if __name__=='__main__':
  
    queries = generate_query_strings(size=4,query_number=100)
    print "Done generating queries"
    grams_setup="ss = __import__('scrabble-suggester');gs=ss.GramSuggester();Q='{}';K={}"
    grams_fn = 'gs.top_results(Q,K)'

    # sorted_setup="from brutesuggester import BruteSortedSuggester;ss=BruteSortedSuggester('dictionary.txt');Q='{}';K={}"
    # sorted_fn = 'ss.top_results(Q,K)'

    g = LogItem(grams_setup,grams_fn,name='Scrabble Suggester')
    # s = LogItem(sorted_setup,sorted_fn,name='brutesorted')

    for q in queries:
    	g.time(q)
    g.report()

    	# s.time(q)
    	# s.report()
    	

