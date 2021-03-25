run_a = [1, 1, 0, 1, 0]
run_b = [0, 1, 0, 1, 1]

# compute edit distance with the help of the SequenceMatcher from the Python-native difflib module
# https://docs.python.org/3/library/difflib.html#sequencematcher-objects
from difflib import SequenceMatcher

seq_match = SequenceMatcher(None, run_a, run_b)

# Measure of the sequences’ similarity as a float in the range [0, 1].
# Where T is the total number of elements in both sequences, and M is the number of matches, this is 2.0*M / T.
# Note that this is 1.0 if the sequences are identical, and 0.0 if they have nothing in common.
ratio_ab = seq_match.ratio()
print(ratio_ab)

# Determine upper bound
ratio_ab_upper_bound = seq_match.real_quick_ratio()
print(ratio_ab_upper_bound)


# compute hamming distance with the help of the scipy module
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.hamming.html
from scipy.spatial.distance import hamming
hamming_distance = hamming(run_a, run_b)
print(hamming_distance)
