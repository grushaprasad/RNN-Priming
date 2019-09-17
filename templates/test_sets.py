import os

def flatten(l):
    if isinstance(l[0], list):
        #print(l)
        return([item for sublist in l for item in sublist])
    else:
        return(l)

def get_overlap(x,y):
    with open(x) as f:
        x_lines = f.read().splitlines()
        x_words = [str.split(x) for x in x_lines]
        x_words = set(flatten(x_words))

    with open(y) as f:
        y_lines = f.read().splitlines()
        y_words = [str.split(y) for y in y_lines]
        y_words = set(flatten(y_words))

    print(x_words.intersection(y_words))

fnames = os.listdir('./adapt/10/')

for fname in fnames:
    print(fname)
    get_overlap('./adapt/10/'+fname, './test/10/'+fname)
    get_overlap('./adapt/20/'+fname, './test/20/'+fname)
    print('-----------------')





#get_overlap('./adapt/10/listA_adapt_ocont.txt', './test/10/listA_test_ocont.txt')
#get_overlap('test.txt', 'adapt.txt')