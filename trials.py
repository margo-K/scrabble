#!/usr/bin/env python

from pprint import pprint
from queries import queries
import pdb
import math
from timeit import Timer
import sys
import matplotlib.pyplot as plt
grams_setup="ss = __import__('scrabble-suggester');name='suggester';Q='{}';K={};printing=False"
grams_fn = 'ss.main([name,Q,K],printing)'


def avg(s):
	return sum(s)/float(len(s))

def stdev(s):
	return math.sqrt(variance(s))
	
def variance(s):
	return avg(map(lambda x: (x - avg(s))**2, s))

def time(n,k,number=10):
    log = []
    for q,k in queries(size=n,K=k,number=1):
        timer = Timer(grams_fn,grams_setup.format(q,k))
        time = min(timer.repeat(3,number=number))/number
        log.append(time)
    return log

def report(log,name,variables):
    print '{:^10}|{:^20}|{:^20}|{:^20}|'.format(name,'Mean','StdDev','Max')
    print '{:-^10}|{:-^20}|{:-^20}|{:-^20}'.format('','','','')
    for val in variables:
        print '{:^10}|{:^20}|{:^20}|{:^20}'.format(val,*self.stats(log))

def stats(values):
    return avg(values),stdev(values),max(values)

def get_time(n,k):
    log = time(n,k)
    return avg(log)


def plot_Q(qsizes):
    """Plots a graph of Q length vs. time
    K-vals can be at most 4"""
    print "I at least got into the fn Q"
    x_data = qsizes
    k_vals = [10,50,100,500,1000]
    y_colors = (color for color in ["blue","red","green","yellow","purple"])

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1) # one row, one column, first plot
    # Plot the data.

    for k in k_vals:
        color = y_colors.next()
        y_vals = ys(qsizes,k)
        ax.scatter(x_data,y_vals,color=color,label="K:{}".format(k)) #color="blue", linestyle="dashed", linewidth="3")

    # Add a title.
    ax.set_title("Average Query Times by Query Length")
    # Add some axis labels.
    ax.set_xlabel("Q-Length")
    ax.set_ylabel("Time (s)")
    plt.legend(loc=2)

    # Produce an image.
    fig.show()
    fig.savefig("qplotallQ.png")

def plot_K(k_vals):
    """Plots a graph of K vs. time"""
    print "I at least got into the fn K"

    x_data = k_vals
    q_sizes = [1,2,5,10,20]
    y_colors = (color for color in ["blue","red","green","yellow","purple"])

    all_y = []

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1) # one row, one column, first plot

    for q in q_sizes:
        color = y_colors.next()
        y_vals = kys(q,k_vals)
        ax.scatter(x_data,y_vals,color=color,label="Q:{}".format(q)) #color="blue", linestyle="dashed", linewidth="3")

    # Add a title.
    ax.set_title("Average Query Times By K-Values")
    # Add some axis labels.

    ax.set_xlabel("K")
    ax.set_ylabel("Time (s)")
    plt.legend(loc=2)
    # Produce an image.
    fig.show()
    fig.savefig("qplotallK.png")

def kys(qsize,kvals):
    y_data = []
    for k in kvals:
        y_data.append(get_time(qsize,k))
    return y_data

def ys(qsizes,k):
    y_data = []
    for n in qsizes:
        y_data.append(get_time(n,k))
    return y_data

if __name__ == '__main__':
    plot_Q(range(1,10))
    plot_K(range(1,15))


   




