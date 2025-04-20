from datetime import datetime
from typing import Optional
from custom_type import SIM_METHOD
from labtypes import Case, CaseQueue, Equipment, Evidence, FinishedCaseDeposit, Step
from models import CaseModel, DBSession, EquipmentModel, WorkerModel


class Lab:
    def __init__(self, method: SIM_METHOD) -> None:
        self.method = method
        self.cases_waiting = CaseQueue()
        self.cases_running = CaseQueue()
        self.cases_finished = CaseQueue()
        self.equipments: list[Equipment] = []
        self.equipments_map: dict[str, Equipment] = {}
        self.workers_cases: dict[str, int] = {}
        self.load_cases()
        self.load_equipments()
        

    def load_cases(self) -> None:
        with DBSession() as db_session:
            for c in db_session.query(CaseModel).all():
                evidences = [Evidence(e.id, c, [Step(name=s.name, duration=s.duration) for s in e.steps]) for e in c.evidences]
                self.cases_waiting.add_case(Case(c.id, evidences))

    def load_equipments(self) -> None:
        with DBSession() as db_session:
            for e in db_session.query(EquipmentModel).all():
                eq = Equipment(e.name, e.lenght, e.capacity - e.lenght)
                self.equipments.append(eq)
                self.equipments_map[eq.name] = eq

    def associate_worker(self, name: str, case: Case) -> None:
        case.worker = name
        self.workers_cases[name] = case.id

    def dessociate_worker(self, case: Case) -> None:
        if case.worker:
            del self.workers_cases[case.worker]
            case.worker = None
            
    def get_finished_executing_evidences(self, time: datetime) -> dict[str, list['Evidence']]:
        waiting: dict[str, list['Evidence']] = {}
        for eq in reversed(self.equipments):
            evs = eq.get_finished(time)
            try:
                waiting[eq.name] += evs
            except KeyError:
                waiting[eq.name] = evs
        return waiting
           
    def update(self, time: datetime) -> None:
        if self.method == "current":
            self.update_current(time)
        else:
            self.update_pipeline(time)

    def update_current(self, time: datetime) -> None:
        pass
    

    def update_pipeline(self, time: datetime) -> None:
        waiting = self.get_finished_executing_evidences(time)
