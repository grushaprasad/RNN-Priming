import os

def flatten(l):
    if isinstance(l[0], list):
        #print(l)
        return([item for sublist in l for item in sublist])
    else:
        return(l)

def get_overlap(x,y):
    with open(x) as f:
        f.readline()
        x_lines = f.read().splitlines()
        x_words = [str.split(x) for x in x_lines]
        x_words = set(flatten(x_words))

    with open(y) as f:
        f.readline()
        y_lines = f.read().splitlines()
        y_words = [str.split(y) for y in y_lines]
        y_words = set(flatten(y_words))

    print(x_words.intersection(y_words))

fnames = os.listdir('./adapt/')

for fname in fnames:
    print(fname)
    get_overlap('./adapt/'+fname, './test/'+fname)
    print('-----------------')





#get_overlap('./adapt/10/listA_adapt_ocont.txt', './test/10/listA_test_ocont.txt')
#get_overlap('test.txt', 'adapt.txt')