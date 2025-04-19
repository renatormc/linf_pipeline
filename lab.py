from custom_type import SIM_METHOD
from labtypes import Case, CaseQueue, Equipment, Evidence, FinishedCaseDeposit, Step
from models import CaseModel, DBSession, EquipmentModel, WorkerModel


class Lab:
    def __init__(self, method: SIM_METHOD) -> None:
        self.method = method
        self.case_queue = CaseQueue()
        self.finished_case_deposit = FinishedCaseDeposit()
        self.equipments: list[Equipment] = []
        self.workers_cases: dict[str, int] = {}
        self.load_cases()
        self.load_equipments()

    def load_cases(self) -> None:
        with DBSession() as db_session:
            for c in db_session.query(CaseModel).all():
                evidences = [Evidence(e.id, [Step(name=s.name, duration=s.duration) for s in e.steps]) for e in c.evidences]
                self.case_queue.add_case(Case(c.id, evidences))

    def load_equipments(self) -> None:
        with DBSession() as db_session:
            for e in db_session.query(EquipmentModel).all():
                self.equipments.append(Equipment(e.name, e.lenght, e.capacity - e.lenght))

    def associate_worker(self, name: str, case: Case) -> None:
        case.worker = name
        self.workers_cases[name] = case.id

    def dessociate_worker(self, case: Case) -> None:
        if case.worker:
            del self.workers_cases[case.worker]
            case.worker = None

    def update(self) -> None:
        if self.method == "current":
            self.update_current()
        else:
            self.update_pipeline()

    def update_current(self) -> None:
        pass

    def update_pipeline(self) -> None:
        for eq in reversed(self.equipments):
            objs = eq.pop_finished()
            eq.start_new()
