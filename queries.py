import random

counts = {'a': 68582, 'c': 34287, 'b': 17798, 'e': 106758, 'd': 34552, 'g': 27848, 'f': 12714,
          'i': 77412, 'h': 20200, 'k': 9370, 'j': 1780, 'm': 24741, 'l': 47011, 'o': 54542, 
          'n': 60513, 'q': 1632, 'p': 25789, 's': 86547, 'r': 64965, 'u': 31161, 't': 57059, 
          'w': 8535, 'v': 9186, 'y': 13473, 'x': 2700, 'z': 3750}

def make_population(letter_counts):
    population = []
    for item in counts.iterkeys():
      population.extend([item]*counts[item])
    return population

def queries(size,K,sample_size=100):
    population = make_population(counts)
    samples = [random.sample(population,size) for k in xrange(sample_size)]
    for s in samples:
        random.shuffle(s)#in-place shuffle
    queries = [''.join(s) for s in samples]
    return [(query,K) for query in queries]
