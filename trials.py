#!/usr/bin/env python

from pprint import pprint
from queries import generate_query_strings
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
    def __init__(self,setup_str,fn_str,k_vals=[5,10,50,100,500,1000],n_vals=range(1,17)):
        self.setup_str = setup_str
        self.fn_str = fn_str
        self.logk = {k:[] for k in k_vals}
        self.logn = {n:[] for n in n_vals}
        self.k_vals = k_vals
        self.n_vals = n_vals

    def timek(self,q,number=10):
            for k in self.k_vals:
                timer = Timer(self.fn_str,self.setup_str.format(q,k))
                time = min(timer.repeat(3,number=number))/number
                self.logk[k].append(time)

    def timen(self,k,number=10):
        for n in self.n_vals:
            queries = generate_query_strings(n,query_number=100)
            for q in queries:
                timer = Timer(self.fn_str,self.setup_str.format(q,k))
                time = min(timer.repeat(3,number=number))/number
                self.logn[n].append(time)

    def stats(self,val,log):
        data = log[val]
        return avg(data),stdev(data),max(data)

    def report(self,log,constant,variables):
        print '{:^10}|{:^20}|{:^20}|{:^20}|'.format(constant,'Mean','StdDev','Max')
        print '{:-^10}|{:-^20}|{:-^20}|{:-^20}'.format('','','','')
        for val in variables:
    		print '{:^10}|{:^20}|{:^20}|{:^20}'.format(val,*self.stats(val,log))



if __name__=='__main__':
    grams_setup="ss = __import__('scrabble-suggester');name='suggester';Q='{}';K={};printing=False"
    grams_fn = 'ss.main([name,Q,K],printing)'

    for n in [1,2,10,15,20]:
            g = Logger(grams_setup,grams_fn,n_vals=n)
            queries = generate_query_strings(n,query_number=100)
            for query in queries:
                g.timek(query)
            print "N:{}".format(n)
            g.report(g.logk,'K',g.)

    for query in queries:
        g.timek(query)
        g.report(g.logk,'K',g._kvals)

    for k in [5,10,50,100,500,1000]:
        print k
        g.timen(k)
        g.report(g.logn,'N',g.n_vals)

import csv
import datetime as dt
import matplotlib.pyplot as plt

x,y = [],[]
csv_reader = csv.reader(open('data.csv'))
for line in csv_reader:
    x.append(int(line[0]))
    y.append(dt.datetime.strptime(line[1],'%M:%S.%f'))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(y,x,'o-')
fig.autofmt_xdate()

    



   




