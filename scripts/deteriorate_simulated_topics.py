# Import libraries
import pytrec_eval
import numpy
import collections
import operator
import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns
from repro_eval.Evaluator import RpdEvaluator
import pandas as pd
import time
from tqdm import tqdm

from deterioration_functions import (colormap_ktu, 
                                     colormap_rbo, 
                                     colormap_rmse,
                                     colormap_n_rmse, 
                                     colormap_pvalues,
                                     deteriorate_run)

run_name = 'ideal'
# run_name = 'realistic'
# run_name = 'reversed'

# Path to input ranking and qrels (here we consider a single topic)
# Path to the run
run_file_path = './data/simulated_topics/sim_topic_' + run_name + '_rb1_100.txt'
# Qrels
# qrels_file_path = './data/simulated_topics/sim_qrel_100.txt'
qrels_file_path = './data/simulated_topics/sim_qrel_200.txt'


# Ratio: percentage of topics we want to modify
# Float in [0, 1]
ratio = 1

# Location: on which rank positions we want to replace documents and swap documents
# Source: we pick a document from the source, [s_1 s_2] (rank positions start from 1)
source = [1, 500]
# Destination: we move a document to the destination, [d_1 d_2] (rank positions start from 1)
# Documents are replaced in the destination
destination = [501, 1000]

# Bolean paramenter
# True: prints some text output for each topic
verbose = False
show_plot = False

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
iteration_step = 5

# Swap and replacement values
swaps_replacement_values = range(0, (max_n_iterations + 1), iteration_step)
# Number of iterations
n_iterations = len(swaps_replacement_values)

ktu = {}
rbo = {}
rmse = {}
n_rmse = {}

start_time = time.time()

# For each number of swaps
for number_swaps in swaps_replacement_values:
    # for each number of replacement
    for number_replacements in swaps_replacement_values:
        # for all the possible modalities
        for mode in ['worse', 'better', 'worsebetter', 'betterworse']:
            
            print('Number of Swaps: %d, Number of replacements: %d, Mode: %s' % (number_swaps, number_replacements, mode))
            
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
            
print('--- %s minutes ---' % ((time.time() - start_time) / 60))

plt.figure()
colormap_ktu(swaps_replacement_values, 250, 50, ktu, -1, 1, run_name, './', show_plot)
del ktu

plt.figure()
colormap_rbo(swaps_replacement_values, 250, 50, rbo, 0, 1, run_name, './', show_plot)
del rbo

plt.figure()
colormap_rmse(swaps_replacement_values, 250, 50, rmse, 0, 1, run_name, 'baseline', 'ndcg', './', show_plot)
plt.figure()
colormap_rmse(swaps_replacement_values, 250, 50, rmse, 0, 1, run_name, 'baseline', 'P_10', './', show_plot)
plt.figure()
colormap_rmse(swaps_replacement_values, 250, 50, rmse, 0, 1, run_name, 'baseline', 'map', './', show_plot)
del rmse

plt.figure()
colormap_n_rmse(swaps_replacement_values, 250, 50, n_rmse, 0, 1, run_name, 'baseline', 'ndcg', './', show_plot)
plt.figure()
colormap_n_rmse(swaps_replacement_values, 250, 50, n_rmse, 0, 1, run_name, 'baseline', 'P_10', './', show_plot)
plt.figure()
colormap_n_rmse(swaps_replacement_values, 250, 50, n_rmse, 0, 1, run_name, 'baseline', 'map', './', show_plot)
del n_rmse
