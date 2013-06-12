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
In our sample word_list, that is:

**Max Word Length**: 21

       Word             Length     Points
----------------------------------------------
* counterdemonstrations   21         26
* hyperaggressivenesses   21         34
* microminiaturizations   21         36


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

n      With Replacement       In Scrabble Dictionary      Probability of a Match 
																(rounded to 1/100%)

1        26                            26                      100%
2        676                           584                     86.39%
3        17576                         6590                    37.49%
4        456976                        35275                   7.72%
5        11881376                      82456                   0.69%
6        308915776                     111031                  0.04%
7        8031810176                    110211                  0%
8        208827064576                  86020                   0%
9        5429503678976                 54833                   0%
10       141167095653376               31534                   0%
11       3670344486987776              18421                   0%

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

###Tables

####Varying Q-Length

**K = 5**
    N     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    1     | 0.000157168626785  | 2.47192505839e-06  | 0.000171804428101  
    2     |  0.00015743803978  | 1.40627032024e-05  | 0.000167894363403  
    3     | 0.000113336801529  | 6.23784284785e-05  | 0.000166988372803  
    4     | 5.08892536163e-05  | 5.46924130771e-05  | 0.000168085098267  
    5     | 9.38868522644e-05  | 0.000153273754487  |  0.00110759735107  
    6     | 0.000105253458023  | 0.000213458464448  |  0.0015841960907   
    7     | 8.26301574707e-05  | 0.000143317180467  |  0.00131630897522  
    8     | 0.000167098999023  | 0.000592875065958  |  0.00485479831696  
    9     | 7.77666568756e-05  | 1.16772089116e-05  |  0.00010130405426  
    10    | 0.000112557649612  | 0.000197806306884  |  0.00199830532074  
    11    | 9.90908145905e-05  | 1.37304698971e-05  | 0.000125598907471  
    12    | 0.000106130361557  | 1.52162944585e-05  | 0.000138998031616  
    13    | 0.000119716644287  | 1.67704855812e-05  | 0.000155806541443  
    14    | 0.000127433776855  | 1.41146601507e-05  | 0.000163698196411  
    15    | 0.000138896465302  | 1.71169605175e-05  | 0.000175189971924  
    16    | 0.000143567800522  | 1.60827341152e-05  | 0.000181794166565 

**K = 10**
    N     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    1     | 0.000217161178589  | 6.00501030107e-05  |  0.00028600692749  
    2     | 0.000219061732292  | 6.29034268824e-05  |  0.00030369758606  
    3     | 0.000154088377953  | 9.93186702313e-05  | 0.000290608406067  
    4     |  6.3653588295e-05  |  7.7638004001e-05  | 0.000292801856995  
    5     | 9.61290597916e-05  | 0.000193532822117  |  0.00198848247528  
    6     | 0.000108199834824  | 0.000206561805645  |  0.00159289836884  
    7     | 9.62823629379e-05  | 0.000182773290603  |  0.00152781009674  
    8     | 0.000138956904411  | 0.000514049014213  |  0.00485479831696  
    9     | 8.39178562164e-05  | 6.96042274874e-05  |  0.0010509967804   
    10    | 0.000103331685066  | 0.000147382818165  |  0.00199830532074  
    11    | 0.000100559353828  | 1.41118508844e-05  |  0.00014169216156  
    12    | 0.000105989217758  | 1.54816916608e-05  | 0.000146007537842  
    13    | 0.000119041204453  | 1.50470343235e-05  | 0.000155806541443  
    14    | 0.000129662871361  | 1.73241639509e-05  | 0.000186109542847  
    15    | 0.000141732096672  |  1.844291799e-05   | 0.000192809104919  
    16    | 0.000149391412735  | 2.13541213861e-05  | 0.000232601165771  

**K = 50**
    N     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    1     | 0.000569263855616  | 0.000501517060039  |  0.00168070793152  
    2     | 0.000541322549184  | 0.000477621265249  |  0.00128471851349  
    3     | 0.000306636810303  | 0.000381058562742  |  0.00127151012421  
    4     | 9.76786613464e-05  | 0.000211029376207  |  0.00126099586487  
    5     | 9.38093662262e-05  |  0.0001901927292   |  0.00198848247528  
    6     | 0.000111997842789  | 0.000260359959047  |  0.00321049690247  
    7     |  9.4230890274e-05  | 0.000164854141731  |  0.00152781009674  
    8     |   0.000117045482   |  0.00042209787926  |  0.00485479831696  
    9     | 9.98957157135e-05  | 0.000180087432609  |  0.00250351428986  
    10    | 9.88728205363e-05  | 0.000120750623101  |  0.00199830532074  
    11    | 0.000100056409836  | 1.39653050167e-05  |  0.00014169216156  
    12    | 0.000106862465541  | 1.51781725034e-05  | 0.000146007537842  
    13    | 0.000118352333705  | 1.50535346067e-05  | 0.000155806541443  
    14    | 0.000129193226496  | 1.64883843351e-05  | 0.000186109542847  
    15    | 0.000139797925949  |  1.7794692091e-05  | 0.000192809104919  
    16    | 0.000149126291275  | 1.98180043675e-05  | 0.000232601165771

**K = 100**
    N     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    1     |  0.00104086083174  | 0.000925150228375  |  0.0025130033493   
    2     | 0.000977624833584  | 0.000902660033999  |  0.00251829624176  
    3     | 0.000528416454792  | 0.000752960109874  |  0.00290470123291  
    4     | 0.000125499844551  | 0.000301671480022  |  0.0027400970459   
    5     | 9.15948748589e-05  | 0.000190920941674  |  0.00198848247528  
    6     | 0.000103662073612  | 0.000239353368577  |  0.00321049690247  
    7     | 0.000105726599693  | 0.000207644527284  |  0.0018296957016   
    8     | 0.000115404188633  | 0.000378617757346  |  0.00485479831696  
    9     | 9.97356176376e-05  | 0.000169116267043  |  0.00250351428986  
    10    |  0.00010718691349  | 0.000178918189444  |  0.00230529308319  
    11    | 0.000101635277271  | 1.77029440413e-05  |  0.00024790763855  
    12    | 0.000110144495964  | 1.89411636487e-05  | 0.000220894813538  
    13    | 0.000121031463146  | 1.89921708019e-05  | 0.000262808799744  
    14    | 0.000130539596081  | 1.87356762039e-05  | 0.000229287147522  
    15    | 0.000139023900032  | 1.87825972427e-05  | 0.000266480445862  
    16    | 0.000157950997353  | 0.000183399594416  |  0.00380198955536  

**K = 1000**
    N     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    1     |  0.00590085911751  |  0.00975778279997  |   0.026907992363   
    2     |   0.004452865839   |  0.00835295750371  |  0.0294326066971   
    3     |  0.00126805462837  |  0.00344219821785  |  0.0268532991409   
    4     |  0.00012351026535  | 0.000307706722277  |  0.0027400970459   
    5     | 9.57321643829e-05  | 0.000201228695725  |  0.00207018852234  
    6     | 0.000108809518814  | 0.000277976430747  |  0.00374388694763  
    7     | 0.000104779815674  |  0.00020369088792  |  0.0018296957016   
    8     | 0.000114616441727  | 0.000356726120308  |  0.00485479831696  
    9     | 9.77091789246e-05  | 0.000157947023195  |  0.00250351428986  
    10    | 0.000103691005707  | 0.000160278876447  |  0.00230529308319  
    11    | 0.000103819990158  | 5.69940958145e-05  |  0.00131988525391  
    12    | 0.000111953401566  | 4.84153276818e-05  |  0.00111558437347  
    13    | 0.000121794939041  | 3.37531412643e-05  | 0.000754404067993  
    14    | 0.000129877614975  | 1.79588602589e-05  | 0.000229287147522  
    15    | 0.000139003944397  | 1.84232326811e-05  | 0.000266480445862  
    16    | 0.000156043767929  | 0.000164274166178  |  0.00380198955536 


####Varying K

Q-length = 1
   Kval   |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    5     | 0.000158394813538  | 5.60622145492e-06  |  0.000203609466553  
    10    | 0.000278919458389  | 5.59643913326e-06  |  0.000306105613708  
    50    |  0.00126315331459  | 2.47511991204e-05  |  0.00137989521027  
   100    |  0.00248504781723  | 4.49085415865e-05  |  0.00277171134949  
   500    |  0.0124195318222   |  0.00028602540385  |  0.0136636018753   
   1000   |  0.0249907004833   |  0.00046046797327  |  0.0266930103302   

Q-length = 2
    K     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    5     | 0.000159422159195  |  1.7925270092e-05  | 0.000233101844788  
    10    | 0.000278009414673  | 3.29858081951e-05  | 0.000305199623108  
    50    |  0.00119337415695  | 0.000262330348073  |  0.00140798091888  
   100    |  0.00222800827026  | 0.000659885171572  |  0.00293810367584  
   500    |  0.0093869664669   |  0.00483113238139  |   0.013892698288   
   1000   |  0.0174184339046   |  0.0105363944027   |  0.0272265911102   

Q-length = 10

        Kval                Mean              StdDev             Max         
--------------------------------------------------------------------------------
          5          9.91794109344e-05   6.6148620443e-05    0.000734224319458  
         10          9.87453937531e-05   6.57005630632e-05   0.000733580589294  
         50          9.80271339417e-05   6.60308965658e-05   0.00073757648468  
        100          9.84651565552e-05   6.65801424839e-05   0.000742540359497  
        500           9.9330997467e-05   6.81062014345e-05   0.000758938789368  
       1000          9.97967720032e-05   6.80492872329e-05   0.000755681991577  

Q-length = 20
   K     |        Mean        |       StdDev       |        Max         |
----------|--------------------|--------------------|--------------------
    5     | 0.000188385748863  | 2.17492817238e-05  | 0.000352501869202  
    10    | 0.000187715578079  | 2.12632055836e-05  | 0.000273489952087  
    50    | 0.000187812685966  | 2.14782698604e-05  | 0.000335884094238  
   100    | 0.000187556099892  | 2.09736235654e-05  | 0.000273585319519  
   500    | 0.000187666320801  | 2.10877386189e-05  | 0.000290083885193  
   1000   | 0.000187727570534  |  2.1329528824e-05  | 0.000301885604858  







