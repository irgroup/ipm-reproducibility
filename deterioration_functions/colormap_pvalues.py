# Copyright 2020-2021 University of Copenhagen, Denmark
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Maria Maistro (mm@di.ku.dk)

import numpy
import pandas as pd
import seaborn as sns
import matplotlib as plt

# Function to print colormaps for p-values
def colormap_pvalues(swaps_replacement_values, max_label, label_step, pvalue, run_name, run_type, measure, ouput_path, show_plot = False):
    # Input parameters:
    # - swaps_replacement_values: array with the values of swap/replacements to be used
    # - maximum value of swap/replacements to be shown as a label
    # - label_step: steps for labels in the heatmap
    # - rmse: dictionary, key (number_swaps, number_replacements, mode) and values evaluated run (rep_eval object)
    # - run_name: string, name of the run
    # - run_type: string, baseline or advanced
    # - measure: measure to be used, use trec_eval names
    # - ouput_path: path to the directory where the figure will be saved
    # - show_plot: boolean variable, true to show the plots
    
    # Number of iterations, needed to compute the colormap size
    n_iterations = len(swaps_replacement_values)
    # n_iterations = int(round(len(swaps_replacement_values)/2, 0))
    # Define the size of the heatnap
    size = ((n_iterations) * 2) - 1
    # Initialize the matrix for the hasmap
    data_base = numpy.empty((size, size))
    # Fill the matrix with NaN values
    data_base[:] = numpy.NaN
    
    
    # Get the values and map them to the corresponding index of the colormap
    for swap_idx in range(0, n_iterations):
        for replacement_idx in range(0, n_iterations):
            # First quadrant, positive swaps and positive replacements
            data_base[n_iterations - swap_idx - 1, n_iterations + replacement_idx - 1] = pvalue[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'better')].get(run_type)[measure]
    
            # Third quadrant: negative swaps and negative replacements
            data_base[n_iterations + swap_idx - 1, n_iterations - replacement_idx - 1] = pvalue[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'worse')].get(run_type)[measure]

            # Second quadrant: positive swaps and negative replacements
            data_base[n_iterations - swap_idx - 1, n_iterations - replacement_idx - 1] = pvalue[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'betterworse')].get(run_type)[measure]        
    
            # Fourth quadrant: negative swaps and positive replacements
            data_base[n_iterations + swap_idx - 1 , n_iterations + replacement_idx - 1] = pvalue[(swaps_replacement_values[swap_idx], swaps_replacement_values[replacement_idx], 'worsebetter')].get(run_type)[measure]        
    
    # Type of color-grading 
    COLORMAP = "rocket"
    
    # Convert the numpy array in a data frame
    data_base = pd.DataFrame(data_base)
    
    # Null values will be replaced by white color
    # This is not needed for the final version
    mask = data_base.isnull()
    
    # Maximum number of swaps and replacements applied
    max_n_iterations = swaps_replacement_values[-1]
    
    # Set the labels to appear in the heatmap
    xlabels = list(range(-max_label, max_label + 1, label_step))
    ylabels = list(reversed(range(-max_label, max_label + 1, label_step)))
    
    # Plot the heatmap with given labels
    ax = sns.heatmap(data_base, mask = mask, cmap = COLORMAP, 
                     xticklabels = xlabels, yticklabels = ylabels, cbar_kws = {'label': 'p-value'})
    # Set the labels in the correct positions
    # Set the labels in the correct positions
    tick_locator = plt.ticker.LinearLocator(len(xlabels))
    ax.xaxis.set_major_locator(tick_locator)
    ax.yaxis.set_major_locator(tick_locator)
    # Set labels corresponding to ticks
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels, rotation = 0)
    # Print horizontal and vertical lines
    ax.axhline(data_base.shape[0] / 2, color = 'k', linewidth = 0.5)
    ax.axvline(data_base.shape[1] / 2, color = 'k', linewidth = 0.5)
    
    # get proper measure names for figure titels
    if measure == 'map':
        measure_name = 'MAP'
    elif measure == 'ndcg':
        measure_name = 'nDCG'
    elif measure == 'P_10':
        measure_name = 'P@10'
    
    # Figure title
    plt.pyplot.title('p-value with %s' % measure_name)
    # Set x and y axis labels
    plt.pyplot.ylabel('Swaps')
    plt.pyplot.xlabel('Replacements')
    
    # Define the name of the output file
    ouput_file_path = ouput_path + '_'.join(['p_value', run_name, run_type, measure, str(max_n_iterations)]) + '.pdf'
    # Save the figure    
    plt.pyplot.savefig(ouput_file_path, bbox_inches='tight')
    if show_plot:
        # show the figure
        plt.pyplot.show()