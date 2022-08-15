from pytrec_eval import RelevanceEvaluator
import pytrec_eval

qrel_path = 'qrels.toy'
with open(qrel_path, 'r') as f_qrel:
    qrel_orig = pytrec_eval.parse_qrel(f_qrel)
    rel_eval = pytrec_eval.RelevanceEvaluator(qrel_orig, pytrec_eval.supported_measures)
    
# run_path = 'run_a'
# run_path = 'run_b'
run_path = 'run_c'
with open(run_path, 'r') as f_run:
    run = pytrec_eval.parse_run(f_run)
    
   
evaluations = rel_eval.evaluate(run)
# P_10 = sum([scores.get('P_10') for scores in evaluations.values()]) / len(evaluations.values())
# print(P_10)
print(evaluations.get('1').get('P_10'))
print(evaluations.get('2').get('P_10'))
print(evaluations.get('3').get('P_10'))


from repro_eval import Evaluator
rpd_eval = Evaluator.RpdEvaluator(qrel_orig_path=qrel_path, run_b_orig_path='run_a')


run_path = 'run_b'
with open(run_path, 'r') as f_run:
    run = pytrec_eval.parse_run(f_run)
rpd_eval.run_b_rep = run 
rpd_eval.evaluate()
print()
print('Run B')
print('RMSE:', rpd_eval.rmse().get('baseline').get('P_10'))
print('RBO:', sum([score for score in rpd_eval.rbo().get('baseline').values()]) / len(rpd_eval.rbo().get('baseline').values()))
print('KTU:', sum([score for score in rpd_eval.ktau_union().get('baseline').values()]) / len(rpd_eval.ktau_union().get('baseline').values()))

run_path = 'run_c'
with open(run_path, 'r') as f_run:
    run = pytrec_eval.parse_run(f_run)
rpd_eval.run_b_rep = run 
rpd_eval.evaluate()
print()
print('Run C')
print('RMSE:', rpd_eval.rmse().get('baseline').get('P_10'))
print('RBO:', sum([score for score in rpd_eval.rbo().get('baseline').values()]) / len(rpd_eval.rbo().get('baseline').values()))
print('KTU:', sum([score for score in rpd_eval.ktau_union().get('baseline').values()]) / len(rpd_eval.ktau_union().get('baseline').values()))