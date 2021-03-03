import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import pytrec_eval
from repro_eval.Evaluator import RpdEvaluator
from repro_eval.util import trim
import pandas as pd

QREL = '../anserini/tools/topics-and-qrels/qrels.core18.txt'
COLORMAP = "coolwarm"  # None, YlOrBr, coolwarm
PATH_RUNS = '/path/to/runs/'

# REPRO_MEASURE = 'KTU'
# REPRO_MEASURE = 'RBO'
REPRO_MEASURE = 'RMSE'
# REPRO_MEASURE = 'ER'
# REPRO_MEASURE = 'DRI'
# REPRO_MEASURE = 'TTEST'

# MEASURE = 'P_10'
MEASURE = 'ndcg'
# MEASURE = 'map'

ref_base = ''.join(['run.bm25.noStopwords.porter.title+description.core18.indri.porter_bm25(k1=', str(0.9), ',b=', str(0.4), ')_default'])
ref_adv = ''.join(['run.bm25+rm3.noStopwords.porter.title+description.core18.indri.porter_bm25(k1=', str(0.9), ',b=', str(0.4), ')_rm3(fbTerms=10,fbDocs=10,originalQueryWeight=0.5)'])
ORIG_B = ''.join([PATH_RUNS, ref_base])
ORIG_A = ''.join([PATH_RUNS, ref_adv])

measures_with_base_and_adv = ['RMSE', 'TTEST', 'KTU', 'RBO']


def main():
    rpd_eval = RpdEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_a_orig_path=ORIG_A,
                            run_b_rep_path=None,
                            run_a_rep_path=None)
    # rpd_eval.trim(10)
    rpd_eval.evaluate()

    k = [round(x, 2) for x in np.arange(0.7, 1.1001, 0.05)]
    b = [round(x, 2) for x in np.arange(0.2, 0.6001, 0.05)]

    if REPRO_MEASURE in measures_with_base_and_adv:
        data_base = np.zeros(shape=(len(k), len(b)))
        data_adv = np.zeros(shape=(len(k), len(b)))
    else:
        data = np.zeros(shape=(len(k), len(b)))

    for i, _k in enumerate(k):

        if REPRO_MEASURE in measures_with_base_and_adv:
            row_base = []
            row_adv = []
        else:
            row = []
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
                # base
                rep_base_run = pytrec_eval.parse_run(f_in_base)
                # trim(rep_base_run, 10)
                scores_base = rpd_eval.evaluate(rep_base_run)

                # adv
                rep_adv_run = pytrec_eval.parse_run(f_in_adv)
                # trim(rep_adv_run, 10)
                scores_adv = rpd_eval.evaluate(rep_adv_run)

                if REPRO_MEASURE == 'KTU':
                    ktu = rpd_eval.ktau_union(run_b_score=rep_base_run, run_a_score=rep_adv_run)
                    row_base.append(np.array(list(ktu.get('baseline').values())).mean())
                    row_adv.append(np.array(list(ktu.get('advanced').values())).mean())


                if REPRO_MEASURE == 'RBO':
                    rbo = rpd_eval.rbo(run_b_score=rep_base_run, run_a_score=rep_adv_run)
                    row_base.append(np.array(list(rbo.get('baseline').values())).mean())
                    row_adv.append(np.array(list(rbo.get('advanced').values())).mean())

                if REPRO_MEASURE == 'RMSE':
                    rmse = rpd_eval.rmse(run_b_score=scores_base, run_a_score=scores_adv)
                    row_base.append(rmse.get('baseline').get(MEASURE))
                    row_adv.append(rmse.get('advanced').get(MEASURE))

                if REPRO_MEASURE == 'ER':
                    er = rpd_eval.er(run_b_score=scores_base, run_a_score=scores_adv)
                    row.append(er.get(MEASURE))

                if REPRO_MEASURE == 'DRI':
                    dri = rpd_eval.dri(run_b_score=scores_base, run_a_score=scores_adv)
                    row.append(dri.get(MEASURE))

                if REPRO_MEASURE == 'TTEST':
                    pval = rpd_eval.ttest(run_b_score=scores_base, run_a_score=scores_adv)
                    row_base.append(pval.get('baseline').get(MEASURE))
                    row_adv.append(pval.get('advanced').get(MEASURE))

        if REPRO_MEASURE in measures_with_base_and_adv:
            data_base[i] = row_base
            data_adv[i] = row_adv
        else:
            data[i] = row

    if REPRO_MEASURE in measures_with_base_and_adv:
        df_base = pd.DataFrame(data_base)
        ax = sns.heatmap(data_base, xticklabels=b, yticklabels=k, cbar_kws={'label': REPRO_MEASURE}, cmap=COLORMAP)
        if REPRO_MEASURE in ['RBO', 'KTU']:
            plt.title('BM25')
        else:
            plt.title(''.join(['BM25 - ', MEASURE.upper()]))
        plt.ylabel("k1")
        plt.xlabel("b")

        if REPRO_MEASURE in ['RBO', 'KTU']:
            plt.savefig(''.join(['BM25_', REPRO_MEASURE.upper(), '.pdf']), bbox_inches='tight')
        else:
            plt.savefig(''.join(['BM25_', MEASURE.upper(), '_', REPRO_MEASURE.upper(), '.pdf']), bbox_inches='tight')

        plt.show()

        ax = sns.heatmap(data_adv, xticklabels=b, yticklabels=k, cbar_kws={'label': REPRO_MEASURE}, cmap=COLORMAP)
        if REPRO_MEASURE in ['RBO', 'KTU']:
            plt.title('BM25+RM3')
        else:
            plt.title(''.join(['BM25+RM3 - ', MEASURE.upper()]))
        plt.ylabel("k1")
        plt.xlabel("b")

        if REPRO_MEASURE in ['RBO', 'KTU']:
            plt.savefig(''.join(['BM25+RM3_', REPRO_MEASURE.upper(), '.pdf']), bbox_inches='tight')
        else:
            plt.savefig(''.join(['BM25+RM3_', MEASURE.upper(), '_', REPRO_MEASURE.upper(), '.pdf']), bbox_inches='tight')

        plt.show()
    else:
        ax = sns.heatmap(data, xticklabels=b, yticklabels=k, cbar_kws={'label': REPRO_MEASURE}, cmap=COLORMAP)
        plt.title(''.join(['BASE: BM25; ADV: BM25+RM3 - ', MEASURE.upper()]))
        plt.ylabel("k1")
        plt.xlabel("b")
        plt.savefig(''.join(['BASE_BM25_ADV_BM25+RM3_', MEASURE.upper(), '_', REPRO_MEASURE.upper(), '.pdf']), bbox_inches='tight')
        plt.show()


if __name__ == '__main__':
    main()