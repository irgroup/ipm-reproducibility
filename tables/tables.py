import pickle
import numpy
import pandas as pd


def get_df(swaps_replacement_values, max_label, label_step, measure_score):
    # Input parameters:
    # - swaps_replacement_values: array with the values of swap/replacements to be used
    # - max_label: maximum value of swap/replacements to be shown as a label
    # - label_step: steps for labels in the heatmap
    # - measure_score: dictionary, key (number_swaps, number_replacements, mode) and values evaluated run (rep_eval object)
    
    n_iterations = len(swaps_replacement_values)
    size = ((n_iterations) * 2) - 1
    data_base = numpy.empty((size, size))
    data_base[:] = numpy.NaN
    
    topics_ids = list(measure_score[(0, 0, 'better')].get('baseline').keys())
    
    for swap_idx in range(0, n_iterations):
        for replacement_idx in range(0, n_iterations):
            ktu_first = measure_score[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'better')].get('baseline')
            ktu_first_avg = 0
            for topic in topics_ids:
                ktu_first_avg = ktu_first_avg + ktu_first.get(topic)
            data_base[n_iterations - swap_idx - 1, n_iterations + replacement_idx - 1] = ktu_first_avg / len(topics_ids)
    
            ktu_third = measure_score[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'worse')].get('baseline')
            ktu_third_avg = 0
            for topic in topics_ids:
                ktu_third_avg = ktu_third_avg + ktu_third.get(topic)
            data_base[n_iterations + swap_idx - 1, n_iterations - replacement_idx - 1] = ktu_third_avg / len(topics_ids)
            
            ktu_second = measure_score[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'betterworse')].get('baseline')
            ktu_second_avg = 0
            for topic in topics_ids:
                ktu_second_avg = ktu_second_avg + ktu_second.get(topic)
            data_base[n_iterations - swap_idx - 1, n_iterations - replacement_idx - 1] = ktu_second_avg / len(topics_ids)
            
            ktu_fourth = measure_score[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'worsebetter')].get('baseline')
            ktu_fourth_avg = 0
            for topic in topics_ids:
                ktu_fourth_avg = ktu_fourth_avg + ktu_fourth.get(topic)
            data_base[n_iterations + swap_idx - 1 , n_iterations + replacement_idx - 1] = ktu_fourth_avg / len(topics_ids)
    
    df = pd.DataFrame(data_base)    
    df.columns = list(range(-max_label, max_label + 1, label_step))
    df.index = list(reversed(range(-max_label, max_label + 1, label_step)))
    
    return df

def _get_df(swaps_replacement_values, max_label, label_step, rmse, measure='map', run_type='baseline'):
    n_iterations = len(swaps_replacement_values)
    size = ((n_iterations) * 2) - 1
    data_base = numpy.empty((size, size))
    data_base[:] = numpy.NaN
    
    
    for swap_idx in range(0, n_iterations):
        for replacement_idx in range(0, n_iterations):
            data_base[n_iterations - swap_idx - 1, n_iterations + replacement_idx - 1] = rmse[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'better')].get(run_type)[measure]
            data_base[n_iterations + swap_idx - 1, n_iterations - replacement_idx - 1] = rmse[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'worse')].get(run_type)[measure]
            data_base[n_iterations - swap_idx - 1, n_iterations - replacement_idx - 1] = rmse[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'betterworse')].get(run_type)[measure]        
            data_base[n_iterations + swap_idx - 1 , n_iterations + replacement_idx - 1] = rmse[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'worsebetter')].get(run_type)[measure]        
    
    df = pd.DataFrame(data_base)    
    df.columns = list(range(-max_label, max_label + 1, label_step))
    df.index = list(reversed(range(-max_label, max_label + 1, label_step)))
    
    return df
    
source = [1, 500]
max_n_iterations = round((source[1] - source[0] + 1) / 2)
iteration_step = 50
swaps_replacement_values = range(0, (max_n_iterations + 1), iteration_step)
    

with open('tables.tex', 'w') as f_out: 

    # Scenario 1 - Perfect ranking - KTU
    file_name = './measure_scores/simulated/rb1.0/ideal_ktu.p'
    with open(file_name, 'rb') as f:
        ktu = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, ktu)
    
    f_out.write('Scenario 1 - Perfect ranking - KTU\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del ktu    
    del df 
    
    # Scenario 1 - Realistic ranking - KTU
    file_name = './measure_scores/simulated/rb1.0/realistic_ktu.p'
    with open(file_name, 'rb') as f:
        ktu = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, ktu)
    
    f_out.write('Scenario 1 - Realistic ranking - KTU\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del ktu    
    del df 
    
    # Scenario 1 - Reversed ranking - KTU
    file_name = './measure_scores/simulated/rb1.0/reversed_ktu.p'
    with open(file_name, 'rb') as f:
        ktu = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, ktu)
    
    f_out.write('Scenario 1 - Reversed ranking - KTU\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del ktu    
    del df 
    
    # Scenario 2 - Perfect ranking - KTU
    file_name = './measure_scores/simulated/rb0.5/ideal_ktu.p'
    with open(file_name, 'rb') as f:
        ktu = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, ktu)
    
    f_out.write('Scenario 2 - Perfect ranking - KTU\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del ktu    
    del df 
    
    # Scenario 2 - Realistic ranking - KTU
    file_name = './measure_scores/simulated/rb0.5/realistic_ktu.p'
    with open(file_name, 'rb') as f:
        ktu = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, ktu)
    
    f_out.write('Scenario 2 - Realistic ranking - KTU\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del ktu    
    del df 
    
    # Scenario 2 - Reversed ranking - KTU
    file_name = './measure_scores/simulated/rb0.5/reversed_ktu.p'
    with open(file_name, 'rb') as f:
        ktu = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, ktu)
    
    f_out.write('Scenario 2 - Reversed ranking - KTU\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del ktu    
    del df 

    # Scenario 3 - BM25 - KTU
    file_name = './measure_scores/BM25/BM25_ktu.p'
    with open(file_name, 'rb') as f:
        ktu = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, ktu)
    
    
    f_out.write('Scenario 3 - BM25 - KTU\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
        
    del ktu    
    del df 
    
    # Scenario 3 - RM3 - KTU
    file_name = './measure_scores/RM3/RM3_ktu.p'
    with open(file_name, 'rb') as f:
        ktu = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, ktu)
    
    
    f_out.write('Scenario 3 - BM25 - KTU\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
        
    del ktu    
    del df 

    # Scenario 1 - Perfect ranking - RBO
    file_name = './measure_scores/simulated/rb1.0/ideal_rbo.p'
    with open(file_name, 'rb') as f:
        rbo = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, rbo)
    
    f_out.write('Scenario 1 - Perfect ranking - RBO\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rbo    
    del df 
    
    # Scenario 1 - Realistic ranking - RBO
    file_name = './measure_scores/simulated/rb1.0/realistic_rbo.p'
    with open(file_name, 'rb') as f:
        rbo = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, rbo)
    
    f_out.write('Scenario 1 - Realistic ranking - RBO\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rbo    
    del df 
    
    # Scenario 1 - Reversed ranking - RBO
    file_name = './measure_scores/simulated/rb1.0/reversed_rbo.p'
    with open(file_name, 'rb') as f:
        rbo = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, rbo)
    
    f_out.write('Scenario 1 - Reversed ranking - RBO\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rbo    
    del df 
    
    # Scenario 2 - Perfect ranking - RBO
    file_name = './measure_scores/simulated/rb0.5/ideal_rbo.p'
    with open(file_name, 'rb') as f:
        rbo = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, rbo)
    
    f_out.write('Scenario 2 - Perfect ranking - RBO\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rbo    
    del df 
    
    # Scenario 2 - Realistic ranking - RBO
    file_name = './measure_scores/simulated/rb0.5/realistic_rbo.p'
    with open(file_name, 'rb') as f:
        rbo = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, rbo)
    
    f_out.write('Scenario 2 - Realistic ranking - RBO\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rbo    
    del df 
    
    # Scenario 2 - Reversed ranking - RBO
    file_name = './measure_scores/simulated/rb0.5/reversed_rbo.p'
    with open(file_name, 'rb') as f:
        rbo = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, rbo)
    
    f_out.write('Scenario 2 - Reversed ranking - RBO\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rbo    
    del df 

    # Scenario 3 - BM25 - RBO
    file_name = './measure_scores/BM25/BM25_rbo.p'
    with open(file_name, 'rb') as f:
        rbo = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, rbo)
    
    f_out.write('Scenario 3 - BM25 - RBO\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
        
    del rbo    
    del df 
    
    # Scenario 3 - RM3 - RBO
    file_name = './measure_scores/RM3/RM3_rbo.p'
    with open(file_name, 'rb') as f:
        rbo = pickle.load(f)
    df = get_df(swaps_replacement_values, 250, 50, rbo)
    
    f_out.write('Scenario 3 - BM25 - RBO\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
        
    del rbo    
    del df 
    
        # Scenario 1 - Perfect ranking - RMSE - MAP  
    file_name = './measure_scores/simulated/rb1.0/ideal_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'map')
    
    f_out.write('Scenario 1 - Perfect ranking - RMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 1 - Perfect ranking - RMSE - NDCG
    file_name = './measure_scores/simulated/rb1.0/ideal_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'ndcg')
    
    f_out.write('Scenario 1 - Perfect ranking - RMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 1 - Perfect ranking - RMSE - P@10 
    file_name = './measure_scores/simulated/rb1.0/ideal_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'P_10')
    
    f_out.write('Scenario 1 - Perfect ranking - RMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
  
    # Scenario 1 - Realistic ranking - RMSE - AP
    file_name = './measure_scores/simulated/rb1.0/realistic_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'map')
    
    f_out.write('Scenario 1 - Realistic ranking - RMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 

    # Scenario 1 - Realistic ranking - RMSE - NDCG
    file_name = './measure_scores/simulated/rb1.0/realistic_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'ndcg')
    
    f_out.write('Scenario 1 - Realistic ranking - RMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 1 - Realistic ranking - RMSE - P@10 
    file_name = './measure_scores/simulated/rb1.0/realistic_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'P_10')
    
    f_out.write('Scenario 1 - Realistic ranking - RMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 1 - Reversed ranking - RMSE - AP 
    file_name = './measure_scores/simulated/rb1.0/reversed_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'map')
    
    f_out.write('Scenario 1 - Reversed ranking - RMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df  
    
    # Scenario 1 - Reversed ranking - RMSE - NDCG
    file_name = './measure_scores/simulated/rb1.0/reversed_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'ndcg')
    
    f_out.write('Scenario 1 - Reversed ranking - RMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 1 - Reversed ranking - RMSE - P@10 
    file_name = './measure_scores/simulated/rb1.0/reversed_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'P_10')
    
    f_out.write('Scenario 1 - Reversed ranking - RMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 2 - Perfect ranking - RMSE - MAP  
    file_name = './measure_scores/simulated/rb0.5/ideal_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'map')
    
    f_out.write('Scenario 2 - Perfect ranking - RMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 2 - Perfect ranking - RMSE - NDCG
    file_name = './measure_scores/simulated/rb0.5/ideal_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'ndcg')
    
    f_out.write('Scenario 2 - Perfect ranking - RMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 2 - Perfect ranking - RMSE - P@10 
    file_name = './measure_scores/simulated/rb0.5/ideal_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'P_10')
    
    f_out.write('Scenario 2 - Perfect ranking - RMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
  
    # Scenario 2 - Realistic ranking - RMSE - AP
    file_name = './measure_scores/simulated/rb0.5/realistic_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'map')
    
    f_out.write('Scenario 2 - Realistic ranking - RMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 

    # Scenario 2 - Realistic ranking - RMSE - NDCG
    file_name = './measure_scores/simulated/rb0.5/realistic_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'ndcg')
    
    f_out.write('Scenario 2 - Realistic ranking - RMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 2 - Realistic ranking - RMSE - P@10 
    file_name = './measure_scores/simulated/rb0.5/realistic_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'P_10')
    
    f_out.write('Scenario 2 - Realistic ranking - RMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 2 - Reversed ranking - RMSE - AP 
    file_name = './measure_scores/simulated/rb0.5/reversed_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'map')
    
    f_out.write('Scenario 2 - Reversed ranking - RMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df  
    
    # Scenario 2 - Reversed ranking - RMSE - NDCG
    file_name = './measure_scores/simulated/rb0.5/reversed_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'ndcg')
    
    f_out.write('Scenario 2 - Reversed ranking - RMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 2 - Reversed ranking - RMSE - P@10 
    file_name = './measure_scores/simulated/rb0.5/reversed_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'P_10')
    
    f_out.write('Scenario 2 - Reversed ranking - RMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 

    # Scenario 3 - BM25 - RMSE - AP
    file_name = './measure_scores/BM25/BM25_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'map')
    
    f_out.write('Scenario 3 - BM25 - RMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 3 - BM25 - RMSE - NDCG
    file_name = './measure_scores/BM25/BM25_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'ndcg')
    
    f_out.write('Scenario 3 - BM25 - RMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 3 - BM25 - RMSE - P@10
    file_name = './measure_scores/BM25/BM25_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'P_10')
    
    f_out.write('Scenario 3 - BM25 - RMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df
    
    # Scenario 3 - RM3 - RMSE - AP
    file_name = './measure_scores/RM3/RM3_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'map')
    
    f_out.write('Scenario 3 - RM3 - RMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 3 - RM3 - RMSE - NDCG
    file_name = './measure_scores/RM3/RM3_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'ndcg')
    
    f_out.write('Scenario 3 - RM3 - RMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df 
    
    # Scenario 3 - RM3 - RMSE - P@10
    file_name = './measure_scores/RM3/RM3_rmse.p'
    with open(file_name, 'rb') as f:
        rmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, rmse, 'P_10')
    
    f_out.write('Scenario 3 - RM3 - RMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del rmse    
    del df  
    
    # Scenario 1 - Perfect ranking - nRMSE - MAP  
    file_name = './measure_scores/simulated/rb1.0/ideal_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'map')
    
    f_out.write('Scenario 1 - Perfect ranking - nRMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 1 - Perfect ranking - nRMSE - NDCG
    file_name = './measure_scores/simulated/rb1.0/ideal_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'ndcg')
    
    f_out.write('Scenario 1 - Perfect ranking - nRMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 1 - Perfect ranking - nRMSE - P@10 
    file_name = './measure_scores/simulated/rb1.0/ideal_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'P_10')
    
    f_out.write('Scenario 1 - Perfect ranking - nRMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
  
    # Scenario 1 - Realistic ranking - nRMSE - AP
    file_name = './measure_scores/simulated/rb1.0/realistic_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'map')
    
    f_out.write('Scenario 1 - Realistic ranking - nRMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 

    # Scenario 1 - Realistic ranking - nRMSE - NDCG
    file_name = './measure_scores/simulated/rb1.0/realistic_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'ndcg')
    
    f_out.write('Scenario 1 - Realistic ranking - nRMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 1 - Realistic ranking - nRMSE - P@10 
    file_name = './measure_scores/simulated/rb1.0/realistic_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'P_10')
    
    f_out.write('Scenario 1 - Realistic ranking - nRMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 1 - Reversed ranking - nRMSE - AP 
    file_name = './measure_scores/simulated/rb1.0/reversed_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'map')
    
    f_out.write('Scenario 1 - Reversed ranking - nRMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df  
    
    # Scenario 1 - Reversed ranking - nRMSE - NDCG
    file_name = './measure_scores/simulated/rb1.0/reversed_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'ndcg')
    
    f_out.write('Scenario 1 - Reversed ranking - nRMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 1 - Reversed ranking - nRMSE - P@10 
    file_name = './measure_scores/simulated/rb1.0/reversed_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'P_10')
    
    f_out.write('Scenario 1 - Reversed ranking - nRMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 2 - Perfect ranking - nRMSE - MAP  
    file_name = './measure_scores/simulated/rb0.5/ideal_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'map')
    
    f_out.write('Scenario 2 - Perfect ranking - nRMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 2 - Perfect ranking - nRMSE - NDCG
    file_name = './measure_scores/simulated/rb0.5/ideal_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'ndcg')
    
    f_out.write('Scenario 2 - Perfect ranking - nRMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 2 - Perfect ranking - nRMSE - P@10 
    file_name = './measure_scores/simulated/rb0.5/ideal_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'P_10')
    
    f_out.write('Scenario 2 - Perfect ranking - nRMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
  
    # Scenario 2 - Realistic ranking - nRMSE - AP
    file_name = './measure_scores/simulated/rb0.5/realistic_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'map')
    
    f_out.write('Scenario 2 - Realistic ranking - nRMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 

    # Scenario 2 - Realistic ranking - nRMSE - NDCG
    file_name = './measure_scores/simulated/rb0.5/realistic_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'ndcg')
    
    f_out.write('Scenario 2 - Realistic ranking - nRMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 2 - Realistic ranking - nRMSE - P@10 
    file_name = './measure_scores/simulated/rb0.5/realistic_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'P_10')
    
    f_out.write('Scenario 2 - Realistic ranking - nRMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 2 - Reversed ranking - nRMSE - AP 
    file_name = './measure_scores/simulated/rb0.5/reversed_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'map')
    
    f_out.write('Scenario 2 - Reversed ranking - nRMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df  
    
    # Scenario 2 - Reversed ranking - nRMSE - NDCG
    file_name = './measure_scores/simulated/rb0.5/reversed_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'ndcg')
    
    f_out.write('Scenario 2 - Reversed ranking - nRMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 2 - Reversed ranking - nRMSE - P@10 
    file_name = './measure_scores/simulated/rb0.5/reversed_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'P_10')
    
    f_out.write('Scenario 2 - Reversed ranking - nRMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 

    # Scenario 3 - BM25 - nRMSE - AP
    file_name = './measure_scores/BM25/BM25_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'map')
    
    f_out.write('Scenario 3 - BM25 - nRMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 3 - BM25 - nRMSE - NDCG
    file_name = './measure_scores/BM25/BM25_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'ndcg')
    
    f_out.write('Scenario 3 - BM25 - nRMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 3 - BM25 - nRMSE - P@10
    file_name = './measure_scores/BM25/BM25_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'P_10')
    
    f_out.write('Scenario 3 - BM25 - nRMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df
    
    # Scenario 3 - RM3 - nRMSE - AP
    file_name = './measure_scores/RM3/RM3_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'map')
    
    f_out.write('Scenario 3 - RM3 - nRMSE - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 3 - RM3 - nRMSE - NDCG
    file_name = './measure_scores/RM3/RM3_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'ndcg')
    
    f_out.write('Scenario 3 - RM3 - nRMSE - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df 
    
    # Scenario 3 - RM3 - nRMSE - P@10
    file_name = './measure_scores/RM3/RM3_nrmse.p'
    with open(file_name, 'rb') as f:
        nrmse = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, nrmse, 'P_10')
    
    f_out.write('Scenario 3 - RM3 - nRMSE - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del nrmse    
    del df  
 
    # Scenario 3 - BM25 - p-value - AP
    file_name = './measure_scores/BM25/BM25_pvalue.p'
    with open(file_name, 'rb') as f:
        pvalue = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, pvalue, 'map')
    
    f_out.write('Scenario 3 - BM25 - p-value - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del pvalue    
    del df 
    
    # Scenario 3 - BM25 - p-value - NDCG
    file_name = './measure_scores/BM25/BM25_pvalue.p'
    with open(file_name, 'rb') as f:
        pvalue = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, pvalue, 'ndcg')
    
    f_out.write('Scenario 3 - BM25 - p-value - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del pvalue    
    del df 
    
    # Scenario 3 - BM25 - p-value - P@10
    file_name = './measure_scores/BM25/BM25_pvalue.p'
    with open(file_name, 'rb') as f:
        pvalue = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, pvalue, 'P_10')
    
    f_out.write('Scenario 3 - BM25 - p-value - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del pvalue    
    del df
    
    # Scenario 3 - RM3 - p-value - AP
    file_name = './measure_scores/RM3/RM3_pvalue.p'
    with open(file_name, 'rb') as f:
        pvalue = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, pvalue, 'map')
    
    f_out.write('Scenario 3 - RM3 - p-value - MAP\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del pvalue    
    del df 
    
    # Scenario 3 - RM3 - p-value - NDCG
    file_name = './measure_scores/RM3/RM3_pvalue.p'
    with open(file_name, 'rb') as f:
        pvalue = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, pvalue, 'ndcg')
    
    f_out.write('Scenario 3 - RM3 - p-value - NDCG\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del pvalue    
    del df 
    
    # Scenario 3 - RM3 - p-value - P@10
    file_name = './measure_scores/RM3/RM3_pvalue.p'
    with open(file_name, 'rb') as f:
        pvalue = pickle.load(f)
    df = _get_df(swaps_replacement_values, 250, 50, pvalue, 'P_10')
    
    f_out.write('Scenario 3 - RM3 - p-value - P@10\n')
    f_out.write(df.to_latex(float_format="%.4f"))
    f_out.write('\n')
    
    del pvalue    
    del df  