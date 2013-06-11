
from pprint import pprint
from queries import generate_query_strings
from brutesuggester import BruteSortedSuggester
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
	

class Logger(object):
	def __init__(self,setup_str,fn_str,name):
		self.setup_str = setup_str
		self.fn_str = fn_str
		self.log = []
		self.name = name

	def time(self,q):
		for k in [5,10,100,1000]:
			timer = Timer(self.fn_str,self.setup_str.format(q,k))
			self.log.append(min(timer.repeat(3,number=10)))

	def stats(self):
		data = self.log
		return avg(data),stdev(data),min(data),max(data)

	def report(self):
		return '{:^20}{:^20}{:^20}{:^20}{:^20}'.format(self.name,*self.stats())


if __name__=='__main__':
   #  grams_setup="ss = __import__('scrabble-suggester');gs=ss.GramSuggester();Q='{}';K={}"
   #  grams_fn = 'gs.top_results(Q,K)'

   #  sorted_setup="from brutesuggester import BruteSortedSuggester;ss=BruteSortedSuggester('dictionary.txt');Q='{}';K={}"
   #  sorted_fn = 'ss.top_results(Q,K)'
   #  for i in xrange(1,7):
   #  	queries = generate_query_strings(size=2,query_number=10)
   #  	print "Done generating queries"
   #  	print '{:^20}{:^20}{:^20}{:^20}{:^20}'.format('Suggester','Mean','Stdev','Min','Max')
   #  	print '{:-^100}'.format('')
   #  	g = LogItem(grams_setup,grams_fn,name='Scrabble Suggester')
   #  	s = LogItem(sorted_setup,sorted_fn,name='Brute Sorted')
   #  	for q in queries:
	  #   	g.time(q)
	  #   	s.time(q)
	 	# print g.report()
	 	# print s.report()
    grams_setup="ss = __import__('scrabble-suggester');name='suggester';Q='{}';K={};printing=False"
    grams_fn = 'ss.main([name,Q,K],printing)'

    sorted_setup="from brutesuggester import main;name='brutesuggester';Q='{}';K={}"
    sorted_fn = 'main([name,Q,K])'

    g = Logger(grams_setup,grams_fn,name='Scrabble Suggester')
    s = Logger(sorted_setup,sorted_fn,name='Brute Sorted Suggester')
    for i in xrange(1):
    	queries = generate_query_strings(size=2,query_number=100)
    	print "Done generating queries"
    	print 'N-val:{}{:^20}{:^20}{:^20}{:^20}{:^20}'.format(i,'Suggester','Mean','Stdev','Min','Max')
    	print '{:-^100}'.format('')
    	for query in queries:
    		g.time(query)
    		# s.time(query)
    	print g.report()
    	# print s.report()

   




