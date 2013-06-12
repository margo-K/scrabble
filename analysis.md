#Measuring Performance
To examine performance of the Scrabble-Suggester, we will both time large
numbers of sample queries to get aggregate statistics about performance
and profile individual queries of interest to better understand the 
implementations strengths and weaknesses.

###Metrics
* **sample mean time/query**
* **sample standard deviation in time/query**: helps us gauge how 
good a metric for performance mean time is; if we have a smaller 
standard deviation (and a sufficiently large sample size) our mean time 
can provide a reasonable portrait of performance
* **sample worst time/query**: important for real-world use; even with a 
good mean time performance, a bad worst-time performance can mean a bad app

###Variables
* length of Q
* size of K

To examine the effect of each of these variables, we will calculate values of the 
metrics holding each one constant.

###Choosing what to Sample
When trying to generate a representative sample set of queries, we must
consider what type of queries we can expect. Barring outside restrictions,
there is no limit to the size of the query string. However, there is a limit
on the query-length that can possibly be returned from the index. We can 
'limit' the effect of queries longer than the max word length in the dictionary
by checking the length of a query before querying the index (and short circuiting
if it is too long). Once we establish that this short-circuiting works, we know
that these queries will not be the bottlenecks in our performance time, and
we can instead sample from the space of queries of length 1...max_word_length. 
In our sample word list that is value 21, but the value is dynamically calculated
for each word list.


We can see from the diagram below that the number of possible n-length
sequences of letters (a-z) grows very fast with n. Choosing uniformly
from the set of all queries of length 1...k, would that we would be much
more likely to get a query of size 11, for example, than a query of size 3. 
Furthermore, because the likelihood of finding a match in the dictionary
decreases rapidly with n, our analysis would be weighted heavily towards
queries that produce no results, which would potentially skew our portrait
of the program's performance.

Along with the fact that an important parameter of the indexer is maxn, the 
maximum length sequence indexed, these reasons suggest that it
might be useful to also separately measure and analyze the performance metrics 
for different query lengths.

**Total n-Length Sequences**

n  |   With Replacement   |  In Scrabble Dictionary  |  Probability of a Match 
--- |--------------------| ------------------------|--------------------------
1   |    26              |             26           |           100%
2   |     676            |            584            |         86.39%
3   |     17576          |               6590         |           37.49%
4   |     456976         |               35275       |            7.72%
5   |     11881376       |               82456       |            0.69%
6   |    308915776       |             111031        |          0.04%
7   |     8031810176     |              110211       |           0%
8   |     208827064576    |              86020       |            0%
9   |     5429503678976    |             54833       |            0%
10  |     141167095653376   |            31534       |            0%
11  |     3670344486987776   |           18421       |            0%

###Generating Sample Queries
To generate sample queries, we must decide on a probability distribution to sample.
If we assume that our Scrabble-Suggester is intended to be used during an 
actual game of Scrabble, we quickly realize that there are many factors which
complicate the determination of this distribution. One approximation
would be to use the distribution of Scrabble tiles in the set. However, because this 
information was not included in the specifications and we can imagine a world in 
which you play a 'Scrabble'-like game that does not have the exact specifications of 
real-world Scrabble, we will instead use a distribution drawn from the dictionary.

If we make the simplifying assumption that the letters on the board can be considered
a random selection of letters from words in the dictionary (a 'bag' that includes
the tiles necessary to form all the words in the dictionary), then we can say
that the distribution of letters is equal to P, the distribution in the dictionary itself.

In this case, to generate sample queries of length k, we generate random
permutations of k-letters, where the set of letters is a
random combination drawn from P and all permutations of those letters are equally likely.
Note: duplicates are 'allowed' by virtue of the fact that each tile is counted as a separate 
object, irrespective of its face value.


####Tools
* ```random``` module: ```random.choice```,```random.shuffle```

###Measurement
We use the ```timeit``` module to time the ```main```
function for each suggester for 3 trials of 10 function calls each (with number of function 
calls being determined experimentally). The minimum value 
is recorded of these trials is recorded because, as the timeit documentation notes, 
variance in times is usually caused by other processes, not the code itself. 

##Performance
###Trends
From **Graph 1**, the graph of query time versus Q-length, we can see that query time 
stabilizes as query-length grows, which makes sense given the short-circuiting of queries 
longer than the maximum word length in the dictionary. We can also see that for shorter 
query lengths (under 5), there is a large different between K values, with a leap in query 
time for ```K = 500``` and ```K = 1000```. Using cProfile, for a sample query we  see that 
the majority of the time in the main function is spent in the ```_words``` function, 
which translates word rankings into words themselves. Though the percall time is less 
than 1 millisecond (the calibration of cProfile), the function call time accumulates as K grows.

**K=1000**
```
$python -m cProfile scrabble-suggester cat 1000

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      1    0.001    0.001    0.032    0.032   scrabble-suggester:102(main)
    856    0.007    0.000    0.026    0.000   scrabble-suggester:31(_word)
```
However, for a lower value of K, the total contribution of _word is 
still in the milliseconds.

**K=100**
```
$python -m cProfile scrabble-suggester cat 100

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      100    0.001    0.000    0.003    0.000 scrabble-suggester:31(_word)
```
If we anticipate a lot of queries with large K-values(over ~200), we 
should consider removing the rankings abstraction layer entirely and storing 
the words themselves. However, if we were putting this in production with
a datastore that could accommodate storing ints directly, we would need 
to consider that storing ints instead of words in the index would take
up roughly half as much space (when our ints are in the range 0...100,000, as
they are with this dictionary).


From **Graph2**, the graph of query-time vs. K-values, we can see that
K values affect query time dramatically for small query lengths and have little
to no effect on large queries. Interestingly, this cannot be attributed entirely
to the short-circuiting of longer queries because this trend is observable at
```Q = 10``` and ```Q = 5```, which are far below the max word length of 21 
for the corpus. For queries of length 1 and 2, growth of query time grows 
approximately linearly with K.

We see from profiling a few test cases that in addition to the costs associated
with _word, the cost of file I/O starts to become more significant when a
large number of matches are asked for because a much larger number of files
must be searched to ensure that the top K matches have been found. 

**Common 1-gram: Q='e'**
```
$python -m cProfile scrabble-suggester e 1000

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      1    0.002    0.002    0.124    0.124   scrabble-suggester:102(main)
   1000    0.093    0.000    0.116    0.000 scrabble-suggester:31(_word)
   1002    0.007    0.000    0.007    0.000 {open}
   1001    0.004    0.000    0.004    0.000 {method 'readline' of 'file' objects}
      1    0.003    0.003    0.122    0.122 scrabble-suggester:83(_top)
```
**Uncommon 1-gram: Q='z'**
```
$python -m cProfile scrabble-suggester z 1000

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.001    0.001    0.039    0.039 scrabble-suggester:102(main)
     1000    0.014    0.000    0.033    0.000 scrabble-suggester:31(_word)
        1    0.002    0.002    0.038    0.038 scrabble-suggester:83(_top)
     1001    0.004    0.000    0.004    0.000 {method 'readline' of 'file' objects}
     1002    0.006    0.000    0.006    0.000 {open}
     1001    0.005    0.000    0.005    0.000 {posix.stat}


```
###Specifics
For a useable app, we will assume that a query time in the milliseconds is 
usually sufficiently fast and anything better than that is very good.

####Worst Case
Worse Case Time: 0.0338598012924 seconds, for K=1000, Qsize=1.
However, worst-case query times an order of magnitude greater than milliseconds
only occur in  other cases that have been tracked:
* Qsize = 2,3
* K-value=500,1000 
Considering again the particular application, it seems clear that these types of 
queries, while possible, do not make much sense in terms of effectively using
a Scrabble solver. A person using the app would have to be requesting 500 or 1000 
matches for a single letter, far more than a person could reasonably process if 
a human is the intended end user. If however, the solver is used in another program
that say returns all matches to a substring that are composed only of letters in your
hand, this would be a reasonable or perhaps even expected query size.

####Mean Time
For all categories shown in the tables, mean query time does not exceed 6.22 ms
and for all but 6 entries in the tables (low Qsize; high K-size), mean query time 
is less than 1 ms. Additionally, we not that standard deviations in all cases are less 
than or equal to the order of magnitude of the mean but only 4 table entries have actual 
standard deviation values which would change the order of magnitude of 1 standard 
deviation slower than the mean time. This means that with regards to average case performance, 
the queries match or surpass our metric for speed.

###Graphs and Tables
####Graph 1: By Q-Length
![Plot of Query Time by Q](https://raw.github.com/margo-K/scrabble/master/plotallQ.png)


 Qsize     |        Mean        |       StdDev       |        Max         |    Sample Size     |
----------|--------------------|--------------------|--------------------|---------------------| 
    1     |  0.00622266726494  |  0.00880763869786  |  0.0338598012924   |        1500        |
    2     |  0.00520350405375  |  0.00808910228081  |  0.0271007061005   |        1500        |
    3     |  0.00176726584435  |  0.00340238386554  |  0.0263221025467   |        500         |
    4     | 0.000198155593872  | 0.000450228360158  |  0.00640239715576  |        500         |
    5     | 0.000123783175151  | 0.000286718126331  |  0.00571448802948  |        1500        |
    6     | 0.000132260227203  | 0.000271357717063  |  0.00349009037018  |        500         |
    7     | 0.000123203372955  | 0.000189234339906  |  0.00233521461487  |        500         |
    8     |  0.00012249083519  | 0.000183618900038  |  0.0020788192749   |        500         |
    9     | 0.000141733169556  |  0.00025199264131  |  0.00412619113922  |        500         |
    10    | 0.000138571421305  | 0.000347670038404  |  0.0124555110931   |        1500        |
    11    | 0.000135672140121  | 5.44617706162e-05  |  0.00103199481964  |        500         |
    12    | 0.000159800338745  | 0.000118369013599  |  0.00197379589081  |        500         |
    13    | 0.000156826448441  | 2.27665244367e-05  | 0.000277590751648  |        500         |
    14    | 0.000169707918167  | 0.000110408603708  |  0.00259919166565  |        500         |
    15    |  0.0001888422966   | 0.000285800978475  |  0.00655770301819  |        500         |
    16    | 0.000193169641495  | 0.000108876062545  |  0.00258469581604  |        500         |
    17    | 0.000210278224945  | 3.95513549602e-05  |  0.00039119720459  |        500         |
    18    | 0.000237156629562  | 6.17300363615e-05  | 0.000462508201599  |        500         |
    19    | 0.000249270963669  | 6.45340571274e-05  | 0.000465679168701  |        500         |
    20    | 0.000240786329905  | 4.20846352834e-05  | 0.000463700294495  |        1500        |
    21    | 0.000268870401382  | 6.04218399207e-05  | 0.000524020195007  |        500         |
    22    | 2.20260620117e-05  | 4.97312252342e-06  | 3.64065170288e-05  |        500         |
    23    | 2.21381187439e-05  | 5.26507043898e-06  | 3.84092330933e-05  |        500         |
    24    | 2.15384483337e-05  |  4.3914489825e-06  | 3.63111495972e-05  |        500         |
    25    | 2.10228919983e-05  | 3.53102699314e-06  | 3.61919403076e-05  |        500         |
    26    | 2.17039108276e-05  | 4.72490144393e-06  | 3.86953353882e-05  |        500         |
    27    | 2.19566822052e-05  | 4.95611368139e-06  | 4.49180603027e-05  |        500         |
    28    | 2.09206581116e-05  | 3.12992124256e-06  | 3.26871871948e-05  |        500         |
    29    | 2.08265781403e-05  | 3.05415419837e-06  | 3.33070755005e-05  |        500         |


####Graph 2: By K
![Plot of Query Time by K](https://raw.github.com/margo-K/scrabble/master/plotallK.png)


    K     |        Mean        |       StdDev       |        Max         |    Sample Size    |
----------|--------------------|--------------------|-------------------- |-------------------|
    1     | 0.000123975324631  | 8.71729505899e-05  | 0.000987601280212   |       500         |
    2     | 0.000134800767899  | 7.48280691178e-05  | 0.000809788703918   |       500         |
    5     | 0.000169207143784  | 0.000110805460071  |  0.00209729671478   |       500         |
    10    | 0.000167451571016  | 0.000134965341251  |  0.00165739059448   |       3400        |
    20    | 0.000349965715408  | 0.000597631403832  |  0.0124555110931    |       500         |
    50    | 0.000303339263972  | 0.000482665202151  |  0.00412619113922   |       3400        |
   100    | 0.000452426693019  | 0.000847267088732  |  0.00571448802948   |       3400        |
   200    |  0.0020487967968   |  0.00241021375145  |  0.0052855014801    |       500         |
   500    |  0.00161437943402  |  0.00403683348466  |  0.0159264087677    |       3400        |
   1000   |  0.0029900542708   |  0.00799236612603  |  0.0338598012924    |       3400        |



