import pandas as pd

results_npi = []
results_agr = []
embedtype = 'tied'
results_dir_base = '../tied_accuracies'
for corpus_size in ('2m','10m','20m'):
    for nhid in (100,200,400,800,1600):
        for corpus_var in "a b c d e".split():
            results_dir = results_dir_base+'/results_'+str(nhid)+'_'+corpus_size+'_'+corpus_var+'_0_'+embedtype+'/rnn/full_sent/'
            results_file = 'overall_accs.txt'
            with open(results_dir+results_file,'r') as f:
                for line in f:
                    key,value = line.strip().split(': ')
                    if 'npi' in key:
                        results = results_npi
                        key = ' ('.join(key.split('('))
                    else:
                        results = results_agr
                    results.append([key,nhid,corpus_size,corpus_var,float(value)])
results = results_agr
resultsdf = pd.DataFrame(results,columns=('syntax','d_model','corpus_size','corpus_var','accuracy'))

resultsdf.to_csv('../tied_accuracies/all_acc.dat', sep='\t')