from lab import Lab


lab = Lab()
res = lab.case_queue.pop_next_waiting_equipment('Higienização')
if res:
    print(res.evidence.steps_names)
