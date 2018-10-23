import pickle

d = {}

with open('log.txt', 'wb') as f:
    pickle.dump(d, f)    