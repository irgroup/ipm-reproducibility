import numpy as np
import pytrec_eval
from repro_eval.Evaluator import RpdEvaluator
from repro_eval.util import trim
import pandas as pd

TRIM_THRESH = 1000
QREL = './anserini/tools/topics-and-qrels/qrels.core18.txt'
REF_BASE = ''.join(['run.bm25.noStopwords.porter.title+description.core18.indri.porter_bm25(k1=', str(0.9), ',b=', str(0.4), ')_default'])
REF_ADV = ''.join(['run.bm25+rm3.noStopwords.porter.title+description.core18.indri.porter_bm25(k1=', str(0.9), ',b=', str(0.4), ')_rm3(fbTerms=10,fbDocs=10,originalQueryWeight=0.5)'])
ORIG_B = ''.join(['./anserini/runs/', REF_BASE])
ORIG_A = ''.join(['./anserini/runs/', REF_ADV])


def jacc_sim(l1, l2):
    inter_len = len(list(set(l1).intersection(l2)))
    union_len = (len(l1) + len(l2)) - inter_len
    return float(inter_len) / union_len

def main():

    rpd_eval = RpdEvaluator(qrel_orig_path=QREL,
                            run_b_orig_path=ORIG_B,
                            run_a_orig_path=ORIG_A,
                            run_b_rep_path=None,
                            run_a_rep_path=None)
    rpd_eval.trim(TRIM_THRESH)
    rpd_eval.evaluate()

    with open(QREL, 'r') as f_qrel:
        qrel_orig = pytrec_eval.parse_qrel(f_qrel)

    with open(ORIG_B) as f_in:
        run_base = pytrec_eval.parse_run(f_in)
    with open(ORIG_A) as f_in:
        run_adv = pytrec_eval.parse_run(f_in)

    docs_base = {topic: list(run_base.get(topic).keys())[:TRIM_THRESH] for topic in run_base.keys()}
    docs_adv = {topic: list(run_adv.get(topic).keys())[:TRIM_THRESH] for topic in run_adv.keys()}

    k = [round(x, 2) for x in np.arange(0.7, 1.1001, 0.05)]
    b = [round(x, 2) for x in np.arange(0.2, 0.6001, 0.05)]

    data_jacc_base = {}
    data_ktu_base = {}
    data_rbo_base = {}

    data_jacc_adv = {}
    data_ktu_adv = {}
    data_rbo_adv = {}

    for i, _k in enumerate(k):
        data_jacc_base[_k] = []
        data_ktu_base[_k] = []
        data_rbo_base[_k] = []

        data_jacc_adv[_k] = []
        data_ktu_adv[_k] = []
        data_rbo_adv[_k] = []

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


            rep_base_path = ''.join(['./anserini/runs/1strun/', rep_base])
            rep_adv_path = ''.join(['./anserini/runs/1strun/', rep_adv])

            with open(rep_base_path) as f_in_base, open(rep_adv_path) as f_in_adv:
            # with open(rep_base_path) as f_in_base:
                rep_base_run = pytrec_eval.parse_run(f_in_base)
                rep_adv_run = pytrec_eval.parse_run(f_in_adv)

            # base
            trim(rep_base_run, TRIM_THRESH)
            rep_docs_base = {topic: list(rep_base_run.get(topic).keys())[:TRIM_THRESH] for topic in rep_base_run.keys()}

            # adv
            trim(rep_adv_run, TRIM_THRESH)
            rep_docs_adv = {topic: list(rep_adv_run.get(topic).keys())[:TRIM_THRESH] for topic in rep_adv_run.keys()}

            # base
            jaccard_list_base = []
            inter_list_base = []
            swap_list_base = []

            # adv
            jaccard_list_adv = []
            inter_list_adv = []
            swap_list_adv = []

            # base
            for topic in docs_base.keys():
                _docs = docs_base.get(topic)
                _rep_docs = rep_docs_base.get(topic)
                inter = list(sorted(set(_docs[:TRIM_THRESH]).intersection(set(_rep_docs[:TRIM_THRESH]))))
                orig_idx = [doc for doc in _docs if doc in inter]
                rep_idx = [doc for doc in _rep_docs if doc in inter]
                jaccard_list_base.append(jacc_sim(_docs[:TRIM_THRESH], _rep_docs[:TRIM_THRESH]))
                inter_list_base.append(len(set(_docs[:TRIM_THRESH]).intersection(set(_rep_docs[:TRIM_THRESH]))))

            # adv
            for topic in docs_adv.keys():
                _docs = docs_adv.get(topic)
                _rep_docs = rep_docs_adv.get(topic)
                inter = list(sorted(set(_docs[:TRIM_THRESH]).intersection(set(_rep_docs[:TRIM_THRESH]))))
                orig_idx = [doc for doc in _docs if doc in inter]
                rep_idx = [doc for doc in _rep_docs if doc in inter]
                jaccard_list_adv.append(jacc_sim(_docs[:TRIM_THRESH], _rep_docs[:TRIM_THRESH]))
                inter_list_adv.append(len(set(_docs[:TRIM_THRESH]).intersection(set(_rep_docs[:TRIM_THRESH]))))


            data_jacc_base[_k].append(sum(jaccard_list_base)/len(jaccard_list_base))
            data_jacc_adv[_k].append(sum(jaccard_list_adv)/len(jaccard_list_adv))

            ktu = rpd_eval.ktau_union(run_b_score=rep_base_run, run_a_score=rep_adv_run)
            data_ktu_base[_k].append((np.array(list(ktu.get('baseline').values())).mean()))
            data_ktu_adv[_k].append((np.array(list(ktu.get('advanced').values())).mean()))

            rbo = rpd_eval.rbo(run_b_score=rep_base_run, run_a_score=rep_adv_run)
            data_rbo_base[_k].append(np.array(list(rbo.get('baseline').values())).mean())
            data_rbo_adv[_k].append(np.array(list(rbo.get('advanced').values())).mean())


    # base
    print('jaccard')
    df_jacc = pd.DataFrame(data_jacc_base, index=[b]).T
    print(df_jacc.to_latex())
    print()
    print('ktu')
    df_ktu = pd.DataFrame(data_ktu_base, index=[b]).T
    print(df_ktu.to_latex())
    print()
    print('rbo')
    df_rbo = pd.DataFrame(data_rbo_base, index=[b]).T
    print(df_rbo.to_latex())
    print()
    df = pd.concat([df_jacc, df_rbo, df_ktu], axis=1, keys=['JACC', 'RBO', 'KTU'])
    print(df.stack(0).to_latex(float_format="%.4f", multirow=True))

    # adv
    print('jaccard')
    df_jacc_adv = pd.DataFrame(data_jacc_adv, index=[b]).T
    print(df_jacc_adv.to_latex())
    print()
    print('ktu')
    df_ktu_adv = pd.DataFrame(data_ktu_adv, index=[b]).T
    print(df_ktu_adv.to_latex())
    print()
    print('rbo')
    df_rbo_adv = pd.DataFrame(data_rbo_adv, index=[b]).T
    print(df_rbo_adv.to_latex())
    print()
    df_adv = pd.concat([df_jacc_adv, df_rbo_adv, df_ktu_adv], axis=1, keys=['JACC', 'RBO', 'KTU'])
    print(df_adv.stack(0).to_latex(float_format="%.4f", multirow=True))


if __name__ == '__main__':
    main()
