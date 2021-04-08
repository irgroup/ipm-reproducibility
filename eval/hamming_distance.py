import numpy as np
import pytrec_eval
from repro_eval.Evaluator import RpdEvaluator
from repro_eval.util import trim
import pandas as pd

from scipy.spatial.distance import hamming
from difflib import SequenceMatcher

TRIM_THRESH = 1000
QREL = '../anserini/tools/topics-and-qrels/qrels.core18.txt'
PATH_RUNS = '/path/to/runs/'
REF_BASE = ''.join(['run.bm25.noStopwords.porter.title+description.core18.indri.porter_bm25(k1=', str(0.9), ',b=', str(0.4), ')_default'])
REF_ADV = ''.join(['run.bm25+rm3.noStopwords.porter.title+description.core18.indri.porter_bm25(k1=', str(0.9), ',b=', str(0.4), ')_rm3(fbTerms=10,fbDocs=10,originalQueryWeight=0.5)'])
ORIG_B = ''.join([PATH_RUNS, REF_BASE])
ORIG_A = ''.join([PATH_RUNS, REF_ADV])


def binarize_run(qrel, run):
    bin_rel_dict = {}
    for topic, ranking in run.items():
        bin_rel = []
        for doc, score in ranking.items():
            rel = qrel.get(topic).get(doc)
            if rel:
                # bin_rel.append(1)
                bin_rel.append(1)  # binarize multi-graded relevance
            else:
                bin_rel.append(0)
        bin_rel_dict[topic] = bin_rel
    return bin_rel_dict


def _hamming_distance(bin_ref, bin_rep):
    for topic, bin_run in bin_ref.items():
        yield topic, hamming(bin_run, bin_rep.get(topic))


def hamming_distance(bin_ref, bin_rep):
    return dict(_hamming_distance(bin_ref, bin_rep))


def _ratio(bin_ref, bin_rep):
    for topic, bin_run in bin_ref.items():
        seq_match = SequenceMatcher(None, bin_run, bin_rep.get(topic))
        yield topic, seq_match.ratio()


def ratio(bin_ref, bin_rep):
    return dict(_ratio(bin_ref, bin_rep))


def main():

    with open(QREL, 'r') as f_qrel:
        qrel_orig = pytrec_eval.parse_qrel(f_qrel)

    with open(ORIG_B) as f_in:
        run_base = pytrec_eval.parse_run(f_in)

    with open(ORIG_A) as f_in:
        run_adv = pytrec_eval.parse_run(f_in)

    trim(run_base, TRIM_THRESH)
    trim(run_adv, TRIM_THRESH)

    bin_rel_base = binarize_run(qrel_orig, run_base)
    bin_rel_adv = binarize_run(qrel_orig, run_adv)

    k = [round(x, 2) for x in np.arange(0.7, 1.1001, 0.05)]
    b = [round(x, 2) for x in np.arange(0.2, 0.6001, 0.05)]

    # BASE
    binarized_runs_base = {}
    hamming_distances_base = {}
    hamming_distances_avg_base = {}
    ratio_base = {}
    ratio_avg_base = {}

    # ADV
    binarized_runs_adv = {}
    hamming_distances_adv = {}
    hamming_distances_avg_adv = {}
    ratio_adv = {}
    ratio_avg_adv = {}

    for _k in k:
        for _b in b:
            rep_base = ''.join(['run.bm25.noStopwords.porter.title+description.core18.indri.porter_bm25(k1=',
                                str(_k),
                                ',b=',
                                str(_b),
                                ')_default'])

            rep_adv = ''.join(['run.bm25+rm3.noStopwords.porter.title+description.core18.indri.porter_bm25(k1=',
                                str(_k),
                                ',b=',
                                str(_b),
                                ')_rm3(fbTerms=10,fbDocs=10,originalQueryWeight=0.5)'])

            rep_base_path = ''.join([PATH_RUNS, rep_base])
            rep_adv_path = ''.join([PATH_RUNS, rep_adv])

            with open(rep_base_path) as f_in_base, open(rep_adv_path) as f_in_adv:
                rep_base_run = pytrec_eval.parse_run(f_in_base)
                rep_adv_run = pytrec_eval.parse_run(f_in_adv)

            trim(rep_base_run, TRIM_THRESH)
            trim(rep_adv_run, TRIM_THRESH)

            # BASE
            bin_rel_base_rep = binarize_run(qrel_orig, rep_base_run)
            binarized_runs_base[(_k, _b)] = bin_rel_base_rep

            hamming_base_rep = hamming_distance(bin_rel_base, bin_rel_base_rep)
            hamming_distances_base[(_k, _b)] = hamming_base_rep
            hamming_distances_avg_base[(_k, _b)] = sum(hamming_base_rep.values())/len(hamming_base_rep.values())

            ratio_base_rep = ratio(bin_rel_base, bin_rel_base_rep)
            ratio_base[(_k, _b)] = ratio_base_rep
            ratio_avg_base[(_k, _b)] = sum(ratio_base_rep.values())/len(ratio_base_rep.values())

            # ADV
            bin_rel_adv_rep = binarize_run(qrel_orig, rep_adv_run)
            binarized_runs_adv[(_k, _b)] = bin_rel_adv_rep

            hamming_adv_rep = hamming_distance(bin_rel_adv, bin_rel_adv_rep)
            hamming_distances_adv[(_k, _b)] = hamming_adv_rep
            hamming_distances_avg_adv[(_k, _b)] = sum(hamming_adv_rep.values())/len(hamming_adv_rep.values())

            ratio_adv_rep = ratio(bin_rel_adv, bin_rel_adv_rep)
            ratio_adv[(_k, _b)] = ratio_adv_rep
            ratio_avg_adv[(_k, _b)] = sum(ratio_adv_rep.values())/len(ratio_adv_rep.values())


    print('Hamming - BASE - ',TRIM_THRESH, ' docs per topic')
    data_hamming_base = {}
    for _k in k:
        data_hamming_base[_k] = []
        for _b in b:
            data_hamming_base[_k].append(hamming_distances_avg_base.get((_k, _b)))
    df_hamming_base = pd.DataFrame(data_hamming_base, index=[b]).T
    print(df_hamming_base.to_latex(float_format="%.4f"))

    print('Ratio - BASE - ', TRIM_THRESH, ' docs per topic')
    data_ratio_base = {}
    for _k in k:
        data_ratio_base[_k] = []
        for _b in b:
            data_ratio_base[_k].append(ratio_avg_base.get((_k, _b)))
    df_ratio_base = pd.DataFrame(data_ratio_base, index=[b]).T
    print(df_ratio_base.to_latex(float_format="%.4f"))

    print('Hamming - ADV - ', TRIM_THRESH, ' docs per topic')
    data_hamming_adv = {}
    for _k in k:
        data_hamming_adv[_k] = []
        for _b in b:
            data_hamming_adv[_k].append(hamming_distances_avg_adv.get((_k, _b)))
    df_hamming_adv = pd.DataFrame(data_hamming_adv, index=[b]).T
    print(df_hamming_adv.to_latex(float_format="%.4f"))

    print('Ratio - ADV - ', TRIM_THRESH, ' docs per topic')
    data_ratio_adv = {}
    for _k in k:
        data_ratio_adv[_k] = []
        for _b in b:
            data_ratio_adv[_k].append(ratio_avg_adv.get((_k, _b)))
    df_ratio_adv = pd.DataFrame(data_ratio_adv, index=[b]).T
    print(df_ratio_adv.to_latex(float_format="%.4f"))


if __name__ == '__main__':
    main()
