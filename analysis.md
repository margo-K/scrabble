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
    Q     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    1     |  0.00024092130661  | 0.000184198227564  | 0.000619101524353  
    2     | 0.000240613517761  | 0.000185870226632  | 0.000707411766052  
    3     |  0.00017414894104  | 0.000175856875159  | 0.000693893432617  
    4     | 7.55299091339e-05  | 0.000112053620181  | 0.000701189041138  
    5     |  0.0001007883358   | 0.000252191107291  |  0.00818679332733  
    6     | 0.000102079143524  | 0.000246862282419  |  0.00572831630707  
    7     | 0.000113526134491  | 0.000288548220969  |  0.00640788078308  
    8     | 0.000107241716385  | 0.000229500544192  |  0.00559279918671  
    9     | 0.000111322717667  | 0.000220517618179  |  0.00581040382385  
    10    | 0.000111949850963  |  0.00014904994791  |  0.00570960044861  
    11    | 0.000119719896317  | 0.000119534992561  |  0.00309739112854  
    12    | 0.000128167743683  | 0.000101689266909  |  0.00283968448639  
    13    | 0.000139417705536  | 0.000128911197289  |  0.00430769920349  
    14    | 0.000144495096207  | 2.55186856019e-05  |  0.00100638866425  
    15    |  0.00016085193634  | 2.92127624062e-05  | 0.000387501716614  
    16    | 0.000166948318481  | 2.15124780318e-05  | 0.000282382965088  
    17    | 0.000179989757538  | 2.41204787887e-05  |  0.00037100315094  
    18    | 0.000196786231995  | 3.23745322406e-05  | 0.000383806228638  
    19    | 0.000205074625015  | 3.23986459967e-05  | 0.000511002540588  
    20    | 0.000210894441605  | 2.32941445155e-05  |  0.00036039352417  
    21    | 0.000222603359222  | 2.45526273561e-05  | 0.000326418876648  
    22    | 0.000233162870407  | 2.53159915596e-05  |  0.00044469833374  
    23    | 0.000245542221069  |  2.6317320428e-05  |   0.000399518013   
    24    | 0.000257812490463  | 2.64849098096e-05  | 0.000434708595276  
    25    | 0.000276347455978  | 4.22834369677e-05  | 0.000578188896179  
    26    | 0.000285082931519  | 3.41323293555e-05  | 0.000554704666138  
    27    |  0.00029969461441  | 4.32465648032e-05  |  0.0006019115448   
    28    | 0.000301849727631  | 2.93930061307e-05  | 0.000487899780273  
    29    |  0.00031374212265  | 3.01451839418e-05  | 0.000504112243652  
    50    |  0.0005436021626   | 4.02244462885e-05  | 0.000839710235596  
   100    |  0.00110142831802  | 6.02766440121e-05  |  0.0014228105545   
   500    |  0.00580801815987  | 0.000444604641121  |   0.010320186615   
   1000   |  0.0120997688234   | 0.000872279989738  |  0.0222482919693


###Varying K
![Query Time by K](username.github.com/scrabble/img/image.jpg)
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



