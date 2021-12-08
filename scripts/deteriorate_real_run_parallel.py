# Import libraries
import pytrec_eval
import pickle
from repro_eval.Evaluator import RpdEvaluator
import time
from multiprocessing import Manager, Pool

from deterioration_functions import deteriorate_run, colormap_ktu, colormap_rbo, colormap_rmse, colormap_n_rmse, colormap_pvalues

# Path to input ranking and qrels (here we consider a single topic)
# Run Name
# run_name = 'BM25'
run_name = 'RM3'
# Path to the run
run_file_path = './data/real_runs/run_' + run_name + '.txt'
# run_file_path = '../../data/core18/run_baseline_timo/run_timo_321_363'
# Qrels
qrels_file_path = './data/real_runs/qrels_common_core_2018.txt'
# qrels_file_path = '../../data/core18/qrels/qrels_common_core_2018_321_363.txt'

# Ratio: percentage of topics we want to modify
# Float in [0, 1]
ratio = 1

# Location: on which rank positions we want to replace documents and swap documents
# Source: we pick a document from the source, [s_1 s_2] (rank positions start from 1)
# source = [1, 5]
source = [1, 500]
# Destination: we move a document to the destination, [d_1 d_2] (rank positions start from 1)
# Documents are replaced in the destination
# destination = [6, 10]
destination = [501, 1000]

# Bolean paramenter
# True: prints some text output for each topic
verbose = False
show_plot = False
cores = 12

manager = Manager()

ktu = manager.dict()
rbo = manager.dict()
rmse = manager.dict()
n_rmse = manager.dict()
pvalue = manager.dict()


def repro_measures(*args):
    number_swaps = args[0]
    number_replacements = args[1]
    mode = args[2]
    
    # Deteriorate the original run
    deteriorated_run = deteriorate_run(run_file_path, qrels_file_path, ratio, source, destination,
                                    mode, number_swaps, number_replacements, verbose)
    
    # Initialize and rpd object
    rpd_eval = RpdEvaluator()
    # Set all the field of the rpd object
    rpd_eval.run_b_orig = run_orig
    rpd_eval.run_b_rep = deteriorated_run
    
    rpd_eval.rel_eval = pytrec_eval.RelevanceEvaluator(qrels, pytrec_eval.supported_measures)

    rpd_eval.trim()
    rpd_eval.evaluate()
    
    ktu[(number_swaps, number_replacements, mode)] = rpd_eval.ktau_union()
    rbo[(number_swaps, number_replacements, mode)] = rpd_eval.rbo()
    rmse[(number_swaps, number_replacements, mode)] = rpd_eval.rmse()
    n_rmse[(number_swaps, number_replacements, mode)] = rpd_eval.nrmse()
    pvalue[(number_swaps, number_replacements, mode)] = rpd_eval.ttest()

# Import the original run
# The run is a nested dictionary with: key: topic ids, value: a dictionary
# The nested dictionary has: key: doc ids, value: doc scores
with open(run_file_path, 'r') as f_run:
    run_orig = pytrec_eval.parse_run(f_run)

# Import the qrels
# The qrels is a nested dictionary with: key: topic ids, value: a dictionary
# The nested dictionary has: key: doc ids, value: relevance labels
with open(qrels_file_path, 'r') as f_qrel:
    qrels = pytrec_eval.parse_qrel(f_qrel)


# Number of iterations: corresponds to the number of swaps
# In this case is the size of the interval
max_n_iterations = round((source[1] - source[0] + 1) / 2)
# Iteration step, i.e. step of numbers of replacements and swaps
iteration_step = 1

# Save the in a dictionary where each item is a RpdEvaluator object
# key: pair (s, r, m) where s is the number of swaps, r the number of replacement and m is the mode
# timo: i think it is not required to keep all the deteriorated runs in memory
# rpd_eval_dictionary = {}

# Swap and replacement values
swaps_replacement_values = range(0, (max_n_iterations + 1), iteration_step)
# Number of iterations
n_iterations = len(swaps_replacement_values)

combinations = []

# For each number of swaps
for number_swaps in swaps_replacement_values:
    # for each number of replacement
    for number_replacements in swaps_replacement_values:
        # for all the possible modalities
        for mode in ['worse', 'better', 'worsebetter', 'betterworse']:
            combinations.append((number_swaps, number_replacements, mode))


start_time = time.time()

with Pool(processes=cores) as pool:
    pool.starmap(repro_measures, combinations) 
            
# Store KTU
file_name = './measure_scores/' + run_name +'/' + run_name + '_ktu.p'
with open(file_name, 'wb') as f:
    pickle.dump(dict(ktu), f)
    
# Store RBO
file_name = './measure_scores/' + run_name +'/' + run_name + '_rbo.p'
with open(file_name, 'wb') as f:
    pickle.dump(dict(rbo), f)
    
# Store RMSE
file_name = './measure_scores/' + run_name +'/' + run_name + '_rmse.p'
with open(file_name, 'wb') as f:
    pickle.dump(dict(rmse), f)
    
# Store nRMSE
file_name = './measure_scores/' + run_name +'/' + run_name + '_nrmse.p'
with open(file_name, 'wb') as f:
    pickle.dump(dict(n_rmse), f)
    
# Store p-values
file_name = './measure_scores/' + run_name +'/' + run_name + '_pvalue.p'
with open(file_name, 'wb') as f:
    pickle.dump(dict(pvalue), f)

print('--- %s minutes ---' % ((time.time() - start_time) / 60))
