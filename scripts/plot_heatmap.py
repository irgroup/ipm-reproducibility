import pickle
from matplotlib.pyplot import figure
from deterioration_functions import (colormap_ktu, 
                                     colormap_rbo, 
                                     colormap_rmse,
                                     colormap_n_rmse, 
                                     colormap_pvalues)

run_name = 'BM25'
# run_name = 'RM3'
source = [1, 500]
show_plot = False
max_n_iterations = round((source[1] - source[0] + 1) / 2)
iteration_step = 5
swaps_replacement_values = range(0, (max_n_iterations + 1), iteration_step)

with open('measure_scores/' + run_name + '/' + run_name + '_ktu.p', 'rb') as f_in:
    ktu = pickle.load(f_in)
figure()
colormap_ktu(swaps_replacement_values, 250, 50, ktu, -1, 1, run_name, './figure/', show_plot)
del ktu 

with open('measure_scores/' + run_name + '/' + run_name + '_rbo.p', 'rb') as f_in:
    rbo = pickle.load(f_in)
figure()
colormap_rbo(swaps_replacement_values, 250, 50, rbo, 0, 1, run_name, './figure/', show_plot)
del rbo

with open('measure_scores/' + run_name + '/' + run_name + '_rmse.p', 'rb') as f_in:
    rmse = pickle.load(f_in)
figure()
colormap_rmse(swaps_replacement_values, 250, 50, rmse, 0, 1, run_name, 'baseline', 'ndcg', './figure/', show_plot)
figure()
colormap_rmse(swaps_replacement_values, 250, 50, rmse, 0, 1, run_name, 'baseline', 'P_10', './figure/', show_plot)
figure()
colormap_rmse(swaps_replacement_values, 250, 50, rmse, 0, 1, run_name, 'baseline', 'map', './figure/', show_plot)
del rmse

with open('measure_scores/' + run_name + '/' + run_name + '_nrmse.p', 'rb') as f_in:
    n_rmse = pickle.load(f_in)
figure()
colormap_n_rmse(swaps_replacement_values, 250, 50, n_rmse, 0, 1, run_name, 'baseline', 'ndcg', './figure/', show_plot)
figure()
colormap_n_rmse(swaps_replacement_values, 250, 50, n_rmse, 0, 1, run_name, 'baseline', 'P_10', './figure/', show_plot)
figure()
colormap_n_rmse(swaps_replacement_values, 250, 50, n_rmse, 0, 1, run_name, 'baseline', 'map', './figure/', show_plot)
del n_rmse

with open('measure_scores/' + run_name + '/' + run_name + '_pvalue.p', 'rb') as f_in:
    pvalue = pickle.load(f_in)
figure()
colormap_pvalues(swaps_replacement_values, 250, 50, pvalue, run_name, 'baseline', 'P_10', './figure/', show_plot)
figure()
colormap_pvalues(swaps_replacement_values, 250, 50, pvalue, run_name, 'baseline', 'ndcg', './figure/', show_plot)
figure()
colormap_pvalues(swaps_replacement_values, 250, 50, pvalue, run_name, 'baseline', 'map', './figure/', show_plot)
del pvalue
