#Scrabble Word Suggester
This project is a response to the following challenge:
```md
Build a word suggestion engine for Scrabble that takes in a given substring and returns the top K scoring scrabble words that contain that substring. Ex given "et", we want to find the top K scoring scrabble words that contain "et" anywhere in the word.

Please use the following scores for the letters and the dictionary provided: 
1 Point   - A, E, I, L, N, O, R, S, T and U.
2 Points  - D and G.
3 Points  - B, C, M and P.
4 Points  - F, H, V, W and Y.
5 Points  - K.
8 Points  - J and X.
10 Points - Q and Z.

**Restrictions**:
* Do not use any database, search libraries or scrabble libraries
* The index must be built on disk 

**Objective**
* Optimize for the speed of the suggester

**Interface**
The suggestion engine should be invoked from the unix shell like this:
    scrabble-indexer word-list-file => reads the word list and builds on-disk index
    scrabble-suggester Q K => returns the top K words that match the Query Q, sorted by their scores
```

##Example:
```
./scrabble-suggester cat 10

-> disqualifications
-> exemplifications
-> disqualification
-> excommunicating
-> excommunications
-> exemplification
-> excommunicated
-> excommunication
-> catheterization
-> excommunicates
```
##Contents
* **scrabble-suggester**: queries the index, returning the top K words for the query, Q
* **scrabble-indexer**: builds on-disk index
* analysis.md: analyzing performance characteristics of the program
* scrabble.py: helper functions used by both indexer 
and suggester
* queries.py: query generation
* trials.py: performance timing
* tests.py: unit tests
* scrabble_dictionary.txt: sample Scrabble dictionary for use with indexer

##Requirements
* **matplotlib** and **numpy** are required to run the tests and trials

##How it works
###Indexing
The scrabble suggester creates an index of all 1..maxn-grams in the word list and stores
them as key-value pairs where the key is the n-gram and the values are a sorted list of 
words matching that n-gram. Because of the requirements that the index be both on-disk 
and built without using a database, the file system is used as as a dictionary, where the 
file name is a key and the contents are the values. 

####In more depth:
For example, given ```word_list = [('bare',6),('arc',5)]``` and a ```maxn=3``, 
we index:
```
1-grams: [a,b,c,e,r]
2-grams: ['ba','ar','re','rc']
3-grams: ['arc','bar','are']
```

where ```index['ar'] = ['bare','arc']```

There is a large degree of duplication in the entries of the index, so we store
the absolute rank of the word instead of the word itself. In our example, this would mean 
```index['ar'] = [0,1]```, because 'bare' is the highest valued word in the dictionary and 'arc'
is the second highest-values word in the dictionary. Because of this, we store an additional
word index, where key=word rank and value=word.

As maxn grows, storage space required for the index balloons very quickly (see **Analysis**)
but the retrieval time drops. One reason this drop in retrieval time happens because one of the more
expensive operations in the implementation is ```_intersect```, and a larger maxn means finding
the intersection of fewer 'buckets'.
```
Ex: 
Q = 'arange'
maxn = 3
len(ngrams(Q,3)) = len(['ran', 'ara', 'ang', 'nge'])
				 = 4 buckets to intersect
maxn = 
len(ngrams(Q,5)) = len(['arang', 'range'])
                 = 2 buckets to intersect
```
Perhaps more importantly, as the substring gets longer, there are fewer elements/bucket, and their 
intersections tend to be smaller. This means that manually checking possible matches
for exact matches to the query string happens on a much smaller set of words.

Because of the tradeoff mentioned, ```maxn``` is parameterized so that the user can
choose which balance of space/time is most useful.

In this implementation, ```maxn=4``` was chosen as a default because it provides a good balance of 
speed and storage space. Motivation for choosing a larger n would come if there were a noticeable
drop-off in performance for queries larger than maxn. Performance tables in **Analysis** show that 
in fact, these queries perform better than smaller queries, suggesting that the gains from having
fewer results/gram and smaller intersections of those results are realized at this value of n.

###Querying
A query is issued in the following manner, where Q is a query string and K is the number of top 
results requested:
```
scrabble-suggester Q K
```
Given a Q, the following set of steps are performed to check for matches:

**1. Split Q into its n-grams and return matches for each n-gram**, 
where n the minimum of the length of the query and maxn, the max length sequences that have been indexed 
Ex: for ```maxn=3``, a 4-letter word would be split into its 3-grams; for ```maxn=5```, a 4-letter would be be returned directly as a 4-gram of itself

**2. Intersect the words matching each of the n-grams**

Ex: ```Q = 'cat' intersection('ca','at') => 'catapult,'carat','cat', etc.```
Note: in the actual index, all index entries for a substring are sorted by scrabble score, and the merge/intersect operation       maintains that sorting

**3. Filter the results of the intersection to yield only those which match the query
string exactly.** In the example above, if the ```Q='cat'```, 'carat' would be filtered out

**4. Return the first K such entries**

An important component of the implementation is that all of these operations are done lazily.
Instead of loading all matches at each stage into memory, iterators are returned that yield
results only as requested. This creates a processing pipeline connecting the top level
function, ```top_results(Q,K)``` used in Step 4, to the lowest-level 
function ```_matches(gram)```, used in Step 1. This significantly improves the performance
of the suggester, particularly for cases where K is small. Additionally, the two lowest 
level iterators, _matches(gram), which yields values matching a given gram, and _merge(*its), 
which yields values of the sorted, merged iterators (its), short-circuit to return empty lists
when their inputs make it impossible to yield matches for any K.



###Storage
Because of the requirement that the index be kept on disk instead of in memory, both indexes used (the gram index and the word index) are maintained as directories containing files whose names correspond
to each key. The file-system is thus used a key-value store, which proved to be quite efficient.
Additionally, because the ```open``` operation on a file in python supports iteration, the lazy nature of the implementation is maintained as values written to the file are separated by newlines.

Another option considered was the ```cPickle``` module, a faster implementation of the ```pickle``` module, which supports serialization and de-serialization of python objects. However, in repeated trials, unpickling became the bottleneck in the performance of the suggester, so this approach was abandoned.

