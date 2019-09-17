import random
random.seed(7)
import copy
import os
from classes import all_noun_classes
from classes import all_verbs
from classes import adjectives
from classes import adverbs
from classes import plurals

def flatten(l):
    if isinstance(l[0], list):
        return([item for sublist in l for item in sublist])
    else:
        return(l)

def get_det(subj_class, obj_class):
    if subj_class == 'human':
        subj_det = 'my'
    else:
        subj_det = 'the'

    if(obj_class == 'human'):
        obj_det = 'my'
    elif(obj_class == 'achievable'): 
        if subj_class == 'antipower':
            obj_det = 'its'
        else:
            obj_det = ['his', 'her'][random.randint(0,1)]
    else:
        obj_det = 'the'
    return(subj_det, obj_det)

def get_adj(c, noun_classes, adj_classes, l):
    if random.randint(0,1) == 1:
        adj = ''
        adj_class = noun_classes[c][2]
        random.shuffle(adj_class)
        found_adj = False
        for item in adj_class:
            adjs = adj_classes[item]
            random.shuffle(adjs)
            for a in adjs:
                if a not in l:
                    adj = ' %s'%a
                    if random.randint(0,4) < 2:  # 2 out of 5 times also add a modifier to the adjective
                        mod = ['extremely', 'quite', 'really', 'rather'][random.randint(0, 3)]
                        adj = ' %s %s'%(mod, a)
                    found_adj = True
                    break
            if found_adj:
                break
    else:
        adj = ''
    return(adj)

def get_adv(verb, verb_classes, adv_classes, l):
    if random.randint(0,1) == 1:
        adv = ''
        adv_class = verb_classes[verb][2]
        random.shuffle(adv_class)
        found_adv = False
        for item in adv_class:
            advs = adv_classes[item]
            random.shuffle(advs)
            for a in advs:
                if not a in l:
                    adv = ' %s'%a
                    found_adv = True
                    break
            if found_adv:
                break
    else:
        adv = ''
    return(adv)


def pluralize(noun):
    if random.randint(0,4) < 2:
        return(plurals[noun])
    else:
        return(noun)

# To do: Add a table: is human? which for every noun specifies if it is human
def create_sents(args):  #for one sentence]
    # If noun is plural, change was to were
    if str.split(args['obj'])[-1] in plurals.keys(): #i.e. it is singular
        was = 'was'
    else:
        was = 'were'

    # If the adverb was time, then we want it to come post-verbally
    rc_adv = args['rc_adv'].strip() in adverbs['time']
    subjmv_adv = args['subjmv_adv'].strip() in adverbs['time']
    objmv_adv = args['objmv_adv'].strip() in adverbs['time']

    if rc_adv and (subjmv_adv or objmv_adv):
        adv_pos = 3
    elif rc_adv:
        adv_pos = [1,3][random.randint(0,1)]
    elif (subjmv_adv or objmv_adv):
        adv_pos = [2,3][random.randint(0,1)]
    else: 
        adv_pos = random.randint(0,3)

    if adv_pos == 0:  # RC adv first, MV adv first
        src = '%s that%s %s %s%s %s %s .'%(args['subj'], args['rc_adv'], args['verb'], args['obj'], args['subjmv_adv'], args['subj_mv'], args['obj2'])
        orc = '%s that %s%s %s%s %s %s .'%(args['obj'], args['subj'], args['rc_adv'], args['verb'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        orrc = '%s %s%s %s%s %s %s .'%(args['obj'], args['subj'], args['rc_adv'], args['verb'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        prc = '%s that %s%s %s by %s%s %s %s .'%(args['obj'], was, args['rc_adv'], args['verb'], args['subj'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        prrc = '%s%s ra%s by %s%s %s %s .'%(args['obj'], args['rc_adv'], args['verb'], args['subj'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        ocont = '%s%s %s %s and%s %s %s .'%(args['obj'], args['rc_adv'], args['verb'], args['subj'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        scont = '%s%s %s %s and%s %s %s .'%(args['subj'], args['rc_adv'], args['verb'], args['obj'], args['subjmv_adv'], args['subj_mv'], args['obj2'])

    elif adv_pos == 1:  # RC adv second, MV adv first
        src = '%s that %s %s%s%s %s %s .'%(args['subj'], args['verb'], args['obj'], args['rc_adv'], args['subjmv_adv'], args['subj_mv'], args['obj2'])
        orc = '%s that %s %s%s%s %s %s .'%(args['obj'], args['subj'], args['verb'], args['rc_adv'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        orrc = '%s %s %s%s%s %s %s .'%(args['obj'], args['subj'], args['verb'], args['rc_adv'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        prc = '%s that %s %s by %s%s%s %s %s .'%(args['obj'], was, args['verb'], args['subj'], args['rc_adv'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        prrc = '%s %s by %s%s%s %s %s .'%(args['obj'], args['verb'], args['subj'], args['rc_adv'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        ocont = '%s %s %s%s and%s %s %s .'%(args['obj'], args['verb'], args['subj'], args['rc_adv'], args['objmv_adv'], args['obj_mv'], args['obj3'])
        scont = '%s %s %s%s and%s %s %s .'%(args['subj'], args['verb'], args['obj'], args['rc_adv'], args['subjmv_adv'], args['subj_mv'], args['obj2'])


    elif adv_pos == 2:  # RC adv first, MV adv second
        src = '%s that%s %s %s %s %s%s .'%(args['subj'], args['rc_adv'], args['verb'], args['obj'], args['subj_mv'], args['obj2'], args['subjmv_adv'])
        orc = '%s that %s%s %s %s %s%s .'%(args['obj'], args['subj'], args['rc_adv'], args['verb'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        orrc = '%s %s%s %s %s %s%s .'%(args['obj'], args['subj'], args['rc_adv'], args['verb'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        prc = '%s that %s%s %s by %s %s %s%s .'%(args['obj'], was, args['rc_adv'], args['verb'], args['subj'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        prrc = '%s%s %s by %s %s %s%s .'%(args['obj'], args['rc_adv'], args['verb'], args['subj'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        ocont = '%s%s %s %s and %s %s%s .'%(args['obj'], args['rc_adv'], args['verb'], args['subj'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        scont = '%s%s %s %s and %s %s%s .'%(args['subj'], args['rc_adv'], args['verb'], args['obj'], args['subj_mv'], args['obj2'], args['subjmv_adv'])

    else: # RC adv second, MV adv second
        src = '%s that %s %s%s %s %s%s .'%(args['subj'], args['verb'], args['obj'], args['rc_adv'], args['subj_mv'], args['obj2'], args['subjmv_adv'])
        orc = '%s that %s %s%s %s %s%s .'%(args['obj'], args['subj'], args['verb'], args['rc_adv'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        orrc = '%s %s %s%s %s %s%s .'%(args['obj'], args['subj'], args['verb'], args['rc_adv'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        prc = '%s that %s %s by %s%s %s %s%s .'%(args['obj'], was, args['verb'], args['subj'], args['rc_adv'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        prrc = '%s %s by %s%s %s %s%s .'%(args['obj'], args['verb'], args['subj'], args['rc_adv'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        ocont = '%s %s %s%s and %s %s%s .'%(args['obj'], args['verb'], args['subj'], args['rc_adv'], args['obj_mv'], args['obj3'], args['objmv_adv'])
        scont = '%s %s %s%s and %s %s%s .'%(args['subj'], args['verb'], args['obj'], args['rc_adv'], args['subj_mv'], args['obj2'], args['subjmv_adv'])

    return({'src': src, 'orc':orc, 'orrc':orrc, 'prc':prc, 'prrc':prrc, 'ocont': ocont, 'scont': scont})

#print(list(verbs.keys())[0:10])

def get_mv(class_list, verbs_used, verb_list, noun_classes):
    random.shuffle(class_list)
    found_mv = False

    for i in range(len(class_list)): #by the end of the loop I will have an mv and subj/obj class if it is possible to have it. 
        c = class_list[i]
        mv_list = noun_classes[c][1]
        random.shuffle(mv_list)
        for verb in mv_list:
            if verb in verb_list and verb not in verbs_used:  #if I can find mv for a class that has not been used, I am done
                mv = verb
                found_mv = True 
                break
        if found_mv:
            break
    if not found_mv:
        return([0,0])
    else:
        return([c, mv])


def get_classes(verb, verbs_used, verb_list, noun_classes):
    subj_classes = verb[0]
    subj_class, subj_mv = get_mv(subj_classes, verbs_used, verb_list, noun_classes) 

    obj_classes = verb[1]
    obj_class, obj_mv = get_mv(obj_classes, verbs_used, verb_list, noun_classes)

    return(subj_class, subj_mv, obj_class, obj_mv)


def create_set(verb_classes, noun_classes, adj_classes, adv_classes, n):
    verb_list = list(verb_classes.keys())
    args_list = [] 
    verbs_used = set()  
    nouns_used = set()
    adjs_used = set()
    advs_used = set()

    # verb_ind = 0  # having this here does not allow for verb repetition
    # random.shuffle(verb_list)
    for i in range(n):
        #print(i)
        verb_ind = 0  
        subj_class, subj_mv, obj_class, obj_mv = 0,0,0,0

        found_verb = False

        while not found_verb and verb_ind < len(verb_list):
            verb = verb_list[verb_ind]
            verb_ind +=1
            # if verb not in verbs_used:
            verbs_used.add(verb)
            subj_class, subj_mv, obj_class, obj_mv = get_classes(verb_classes[verb], verbs_used, verb_list, noun_classes)
            if subj_mv != 0 and obj_mv != 0:
                found_verb = True
                verbs_used.add(subj_mv)
                verbs_used.add(obj_mv)
            else:
                verbs_used.remove(verb)


        subj_det, obj_det = get_det(subj_class, obj_class)
        subj_list =  flatten(noun_classes[subj_class][0])
        subj = subj_list[random.randint(0, len(subj_list)-1)]


        obj_list =  flatten(noun_classes[obj_class][0])
        obj = subj
        if len(obj_list) > 1:  #if its possible to have different subject and object, do that. 
            while obj == subj:
                obj = obj_list[random.randint(0, len(obj_list)-1)]

    # Get object for MV when subject is subject of RC
        obj2_classes = copy.deepcopy(flatten(verb_classes[subj_mv][1]))

        random.shuffle(obj2_classes)
        obj2 = obj
        if len(obj2_classes) > 1: 
            while obj2 in [subj, obj]:
                obj2_class = obj2_classes.pop()
                for item in noun_classes[obj2_class][0]:
                    if item not in [subj, obj]:
                        obj2 = item
                        break
        else:
            obj2_class = obj2_classes[0]
            for item in noun_classes[obj2_class][0]:
                if item not in [subj, obj]:
                    obj2 = item
                    break


        _, obj2_det = get_det(subj_class, obj2_class)
        

        obj3_classes = copy.deepcopy(flatten(verb_classes[obj_mv][1]))
        random.shuffle(obj3_classes)
        obj3 = obj
        if len(obj3_classes) > 1:
            while obj3 in [subj, obj]:
                obj3_class = obj3_classes.pop()
                for item in noun_classes[obj3_class][0]:
                    if item not in [subj, obj]:
                        obj3 = item
                        break
        else:
            obj3_class = obj3_classes[0]
            for item in noun_classes[obj3_class][0]:
                if item not in [subj, obj]:
                    obj3 = item
                    break

        _, obj3_det = get_det(obj_class, obj3_class)


        subj_adj = get_adj(subj_class, noun_classes, adj_classes, [])
        obj_adj = get_adj(obj_class, noun_classes, adj_classes, [subj_adj])
        obj2_adj = get_adj(obj2_class, noun_classes, adj_classes, [subj_adj, obj_adj])
        obj3_adj = get_adj(obj3_class, noun_classes, adj_classes, [subj_adj, obj_adj, obj2_adj])   #does this make it more likely that obj3 will not have adjs? 
        #print(subj, obj, obj2, obj3)

        nouns_used.add(subj)
        nouns_used.add(obj)
        nouns_used.add(obj2)
        nouns_used.add(obj3)

        if subj_adj != '': 
            adjs_used.add(str.split(subj_adj)[-1])
        if obj_adj != '': 
            adjs_used.add(str.split(obj_adj)[-1])
        if obj2_adj != '': 
            adjs_used.add(str.split(obj2_adj)[-1])
        if obj3_adj != '': 
            adjs_used.add(str.split(obj3_adj)[-1])

        subj = '%s%s %s'%(subj_det, subj_adj, pluralize(subj))
        obj = '%s%s %s'%(obj_det, obj_adj, pluralize(obj))
        obj2 = '%s%s %s'%(obj2_det, obj2_adj, pluralize(obj2))
        obj3 = '%s%s %s'%(obj3_det, obj3_adj, pluralize(obj3))

        rc_adv = get_adv(verb, verb_classes, adv_classes, [])
        subjmv_adv = get_adv(subj_mv, verb_classes, adv_classes, [rc_adv])
        objmv_adv = get_adv(obj_mv, verb_classes, adv_classes, [rc_adv, subjmv_adv])

        if rc_adv != '':
            advs_used.add(rc_adv.strip())
        if subjmv_adv != '':
            advs_used.add(subjmv_adv.strip())
        if objmv_adv != '':
            advs_used.add(objmv_adv.strip())


        args_list.append({'verb': verb, 'subj_mv': subj_mv, 'obj_mv': obj_mv, 'subj': subj, 'obj': obj, 'obj2': obj2, 'obj3':obj3, 'rc_adv': rc_adv, 'subjmv_adv': subjmv_adv, 'objmv_adv': objmv_adv})

    return((args_list, verbs_used, nouns_used, adjs_used, advs_used))


def get_adapt_test(nadapt, ntest):
    ### ADAPT ###
    # Get a subset of nouns for adapt
    adapt_noun_classes = {}

    for key in all_noun_classes.keys():
        curr_all_nouns = all_noun_classes[key][0]
        random.shuffle(curr_all_nouns)
        curr_nouns = curr_all_nouns[0:(int(len(curr_all_nouns)/2)+1)]

        adapt_noun_classes[key] = (curr_nouns, all_noun_classes[key][1], all_noun_classes[key][2])

    adapt_adj_classes = {}
    for key in adjectives.keys():
        curr = adjectives[key]
        random.shuffle(curr)
        adapt_adjs = curr[0:int((len(curr)/2))]
        adapt_adj_classes[key] = adapt_adjs

    adapt_adv_classes = {}
    for key in adverbs.keys():
        curr = adverbs[key]
        random.shuffle(curr)
        adapt_advs = curr[0:(int(len(curr)/2))]
        adapt_adv_classes[key] = adapt_advs

    # Get a subset of adverbs for adapt. Plus exclude noun classes if they are not in adapt
    adapt_verb_classes = {}

    for v in all_verbs.keys():
        curr_subj_classes = [x for x in all_verbs[v][0] if x in adapt_noun_classes]
        curr_obj_classes = [x for x in all_verbs[v][1] if x in adapt_noun_classes]

        if len(curr_subj_classes) > 0 and len(curr_obj_classes) > 0:
            adapt_verb_classes[v] = (curr_subj_classes, curr_obj_classes, all_verbs[v][2])

    # Get test set
    adapt_args_list, verbs_used, nouns_used, adjs_used, advs_used = create_set(adapt_verb_classes, adapt_noun_classes, adapt_adj_classes, adapt_adv_classes, nadapt)

    ### TEST ###
    # Get nouns and adjectives not used in adapt
    test_adj_classes = {}
    for key in adjectives.keys():
        curr = set(adjectives[key])
        test_adjs = list(curr.difference(adjs_used))
        test_adj_classes[key] = test_adjs


    test_adv_classes = {}
    for key in adverbs.keys():
        curr = set(adverbs[key])
        test_advs = list(curr.difference(advs_used))
        test_adv_classes[key] = test_advs

    test_noun_classes = {}

    for key in all_noun_classes.keys():
        curr_all_nouns = set(all_noun_classes[key][0])
        curr_test_nouns = list(curr_all_nouns.difference(nouns_used))
        curr_all_verbs = set(all_noun_classes[key][1])
        curr_test_verbs = list(curr_all_verbs.difference(verbs_used))

        if len(curr_test_verbs) > 0 and len(curr_test_nouns) > 1:
            test_noun_classes[key] = (curr_test_nouns, curr_test_verbs, all_noun_classes[key][2]) 

    # Get verbs and adverbs not used in adapt
    test_verb_classes = {}
    test_verbs = set(all_verbs.keys()).difference(verbs_used)

    for v in test_verbs:
        curr_subj_classes = [x for x in all_verbs[v][0] if x in test_noun_classes]
        curr_obj_classes = [x for x in all_verbs[v][1] if x in test_noun_classes]

        # curr_all_advs = set(all_verbs[v][2])
        # curr_test_advs = list(curr_all_advs.difference(advs_used))

        if len(curr_subj_classes) > 0 and len(curr_obj_classes) > 0:
            test_verb_classes[v] = (curr_subj_classes, curr_obj_classes, all_verbs[v][2])
            # print(test_verb_classes[v])
            # print(all_verbs[v])
            # print('------c')
    
    #Get test set
    test_args_list, _, _, _, _ = create_set(test_verb_classes, test_noun_classes, test_adj_classes, test_adv_classes, ntest)
    return(adapt_args_list, test_args_list)


def make_files(args_list, fname):
    conds = ['orc', 'orrc', 'ocont', 'prc', 'prrc', 'scont', 'src']

    #re-write any old files that exist
    for cond in conds:
        curr_fname = '%s_%s.txt'%(fname, cond)
        f = open(curr_fname, 'w')
        f.close()

    #add sentences to files
    for args in args_list:
        sents = create_sents(args)
        for sent in sents.keys():
            curr_fname = '%s_%s.txt'%(fname, sent)
            f = open(curr_fname, 'a')
            f.write('%s\n'%sents[sent])
            f.close()


def create_lists(l, nadapt, ntest):
    for i,name in enumerate(l):
        if not os.path.exists('./adapt/%s'%nadapt):
            os.makedirs('./adapt/%s'%nadapt)
        if not os.path.exists('./test/%s'%nadapt):
            os.makedirs('./test/%s'%nadapt)

        adapt_args, test_args = get_adapt_test(nadapt, ntest)
        adapt_fname = './adapt/%s/list%s'%(str(nadapt), name)
        make_files(adapt_args, adapt_fname)
        test_fname = './test/%s/list%s'%(str(nadapt), name)
        make_files(test_args, test_fname)


lists = ['1','2','3','4','5','6','7','8','9','10']
create_lists(lists, 20, 50)
create_lists(lists, 10, 50)

"""
Constraints:
-- No lexical overlap between adapt and test
-- No verb/ lexical item repetition in the same sentence
-- There can be verb repetition. Uncomment 181, 182 and 193 and indent appropriately to not have verb repetition within adapt/test. But this might not work for large numbers
"""
