## Uncovering the syntactic organization in neural LMs using priming

This repository contains the templates, analysis code and the supplementary materials for the following paper:

Grusha Prasad, Marten van Schijndel and Tal Linzen. Using Priming to Uncover the Organization of Syntactic Representations in Neural Language Models. *In the proceedings of CoNLL 2019*.

### Using the template
In order to generate the adaptation and test sets for the seven structures described in the paper, run create_rcs.py. Edit lines 425-427 to change the number of lists and/or the number of items per adaptation and test set. 

You can also generate sentences with other structures that take roughly the similar arguments by editing the create_sents function to add the desired configuration. For example, you can generate simple transitive sentences by adding either of the following lines. 

```
transitive1 = '%s %s %s %s .'%(args['subj'], args['subjmv_adv'], args['subj_mv'], args['obj2'])
transitive2 = '%s %s %s %s .'%(args['obj'], args['verb'], args['subj'], args['rc_adv'])
```


### Replicating the analyses in the paper
scripts/conll2019_analyses.md is a complied R markdown document with all the code used to generate the plots and run the statistical analyses in the paper. You can replicate the analyses in the paper, or try out your own analyses by running scripts/conll2019_analyses.Rmd. In order to do that, you will first need to download the data from here: https://osf.io/3t5vf/. Uncompress each of the relevant files and place them in a folder called data.
  
The agreement_accuracy.zip file contains the agreement prediction accuracy for all the trained models on all the constructions in the Marven and Linzen syntatctic evaluation dataset (https://github.com/BeckyMarvin/LM_syneval). The dataframes.zip file contains all the pre-complied dataframes with surprisal values. The dataframes with *summary* in their filename contain surprisal values averaged across the entire sentence with unknown words excluded from this average. The other dataframes contain the word by word surprisal. You can load any of the dataframes into a variable called df using the following command in R

```
df <- readRDS(filepath)
```

If you want to compile the dataframes from scratch you can download the raw surprisal files in trained_model_surprisal.zip and untrained_model_surprisal.zip, and then use scripts/load_data.Rmd. In order to adapt and test your models from scratch, follow the instructions in this repository: https://github.com/vansky/neural-complexity


