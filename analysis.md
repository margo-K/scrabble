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
In our sample word_list, that is 21, but the value is dynamically created for each
word list.


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
for different query lengths(k).

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
Note: duplicates are 'allowed' by virtue of the fact that each tile is counted as a separate object, irrespective of its face value.


####Tools
* ```random``` module: ```random.choice```,```random.shuffle```

###Measurement
We use the ```timeit``` module to time the ```main```
function for each suggester for 3 trials of 10 function calls each (with number of function calls being determined experimentally). The minimum value 
is recorded of these trials is recorded because, as the timeit documentation notes, 
variance in times is usually caused by other processes, not the code itself. 

##Performance

###Varying Q-Length
https://github.com/margo-K/searching
![Query Time by Q](https://github.com/margo-K/scrabble/raw/img/image.jpg)
  Q     |        Mean        |       StdDev       |        Max         |    Sample Size     |
----------|--------------------|--------------------|------------------ |------------------  |
    1     | 0.000297544145584  | 0.000246092529857  |  0.00120449066162 |         500         |
    2     | 0.000284784603119  | 0.00021316431486   | 0.000969195365906 |       500         |
    3     | 0.000213437271118  | 0.000220189621758  |  0.00106971263885 |         500         |
    4     | 9.57478046417e-05  | 0.000109950200647  | 0.000660300254822 |         500         |
    5     | 0.000108694028854  | 0.000178669381696  |  0.00231609344482 |         500         |
    6     | 0.000131019973755  | 0.000184636886924  |  0.00180311203003 |         500         |
    7     | 0.000144563531876  | 0.000257118542256  |  0.00258100032806 |         500         |
    8     | 0.000136407184601  | 0.000286750585199  |  0.00554971694946 |         500         |
    9     | 0.000129082393646  | 0.000132879192236  |  0.00170731544495 |         500         |
    10    | 0.000139148396604  | 0.000163367133532  |  0.00473189353943 |         3400        |
    11    | 0.000146607160568  | 0.000115281023421  |  0.00190901756287 |         500         |
    12    | 0.000164684247971  | 0.000209833118426  |  0.00403220653534 |         500         |
    13    | 0.000184964704514  | 0.000254214423801  |  0.00497579574585 |         500         |
    14    |  0.0001860704422   | 0.000286010743122  |  0.00656018257141 |         500         |
    15    | 0.000191701841354  | 8.12595250353e-05  |  0.00193939208984 |         500         |
    16    | 0.000199178981781  | 2.05493792178e-05  | 0.000264406204224 |         500         |
    17    | 0.000212193632126  | 2.41156305773e-05  | 0.000317907333374 |         500         |
    18    | 0.000222793245316  | 2.66168353512e-05  | 0.000369501113892 |         500         |
    19    | 0.000236497068405  | 2.66192587737e-05  |  0.00040271282196 |         500         |
    20    | 0.000251847600937  | 2.79579197963e-05  | 0.000397706031799 |         500         |
    50    | 2.04342253068e-05  | 9.12629413613e-07  | 3.49998474121e-05 |         3400        |
   100    | 2.02958583832e-05  |  6.3064148418e-07  | 3.26871871948e-05 |         3400        |         
   500    | 2.03140132567e-05  | 4.43688401963e-07  |  3.2901763916e-05 |         3400        |        
   1000   | 2.05006846066e-05  | 4.91615967671e-07  | 3.34978103638e-05 |         2900        |


###Varying K
![Query Time by K](https://github.com/margo-K/scrabble/blob/master/plotallK.png)
    K     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    1     | 0.000714686351664  |  0.00217430094834  |   0.014982509613   
    2     | 0.000174448656214  | 0.000151288340663  |  0.00640788078308  
    5     | 0.000738747808513  |  0.00224753687369  |  0.0207509040833   
    10    | 0.000740016736704  |  0.0021841245137   |  0.0136183977127   
    20    | 0.000222869659292  | 0.000171672884953  |  0.00544078350067  
    50    |  0.00392765800476  |  0.00453043270495  |  0.0139693021774   
   100    |  0.00390201322556  |  0.00449518569567  |  0.0167447805405   
   200    |  0.00395143192291  |  0.0046163479402   |  0.0161000967026   
   500    |  0.00396718921661  |  0.00465693783821  |  0.0222482919693   
   1000   |  0.00396172812462  |  0.00467555570501  |  0.0213823080063  



