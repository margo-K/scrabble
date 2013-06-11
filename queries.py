import random


counts = {'a': 68582, 'c': 34287, 'b': 17798, 'e': 106758, 'd': 34552, 'g': 27848, 'f': 12714, 'i': 77412, 'h': 20200, 'k': 9370, 'j': 1780, 'm': 24741, 'l': 47011, 'o': 54542, 'n': 60513, 'q': 1632, 'p': 25789, 's': 86547, 'r': 64965, 'u': 31161, 't': 57059, 'w': 8535, 'v': 9186, 'y': 13473, 'x': 2700, 'z': 3750}

def make_population(counts):
    pop = []
    for item in counts.iterkeys():
      pop.extend([item]*counts[item])
    return pop

population = make_population(counts)

def generate_queries(max_size=3,query_number=100,K=10):
    queries = []
    for i in xrange(2,max_size+1):
      samples = [random.sample(population,i) for k in xrange(query_number)]
      for s in samples:
          random.shuffle(s)
      queries.extend([''.join(s) for s in samples])
    return [(query,K) for query in queries]

def generate_query_strings(size=5,query_number=100):
    population = make_population(counts)
    queries = []
    samples = [random.sample(population,size) for k in xrange(query_number)]
    for s in samples:
        random.shuffle(s)
        queries.append(''.join(s))
    return queries


if __name__ == '__main__':
  # pop = make_population(counts)
  # query_strings = generate_queries()
  # print queries
    print generate_query_strings(query_number=10)
