from uuid import uuid4

RUN_LENGTH = 1000
NUM_REL = 100

with open('sim_run.txt', 'w') as f_run, open('sim_qrel.txt', 'w') as f_qrels:

    rel_cnt = 0
    for r in range(0, RUN_LENGTH):
        topic = 1
        docid = uuid4().hex
        q0 = 'Q0'
        rank = r
        score = (RUN_LENGTH - r) / RUN_LENGTH
        tag = 'ipm-repro'

        f_run.write(' '.join([str(topic), q0, docid, str(rank), str(score), tag, '\n']))

        rel = 1 if rel_cnt < 100 else 0
        f_qrels.write(' '.join([str(topic), '0', docid, str(rel), '\n']))
        rel_cnt += 1
