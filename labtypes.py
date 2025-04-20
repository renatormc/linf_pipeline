
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class CaseAndEvidence:
    case: 'Case'
    evidence: 'Evidence'


class CaseQueue:
    def __init__(self) -> None:
        self.cases: list['Case'] = []

    def add_case(self, value: 'Case') -> None:
        self.cases.append(value)

    def pop_next(self) -> 'Case':
        return self.cases.pop()

    def pop_next_waiting_equipment(self, name: str) -> Optional[CaseAndEvidence]:
        for i, case in enumerate(self.cases):
            for ev in case.evidences:
                if ev.equipment is None and ev.next_step and ev.next_step.name == name:
                    return CaseAndEvidence(
                        case=self.cases.pop(i),
                        evidence=ev
                    )
        return None


class Case:
    def __init__(self, id: int, evidences: list['Evidence']) -> None:
        self.id = id
        self.evidences = evidences
        for ev in self.evidences:
            ev.case = self
        self._finished_evidences: list[int] = []
        self.total_evidences = len(evidences)
        self.worker: str | None = None
    
    def register_finish_evidence(self, ev: 'Evidence') -> None:
        if not ev.id in self._finished_evidences:
            self._finished_evidences.append(ev.id)

    @property
    def is_finished(self) -> bool:
        return self.total_evidences == len(self._finished_evidences)

    

class Step:
    def __init__(self, name: str, duration: timedelta) -> None:
        self.name = name
        self.duration = duration


class Evidence:
    def __init__(self, id: int, case: 'Case', steps: list[Step]) -> None:
        self.id = id
        self.case = case
        self.steps: list[Step] = steps
        self.steps_map = {e.name: e for e in self.steps}
        self.steps_name = [e.name for e in self.steps]
        self.steps_finished: list[str] = []
        self.next_step: Optional['Step'] = steps[0]
        self._finish_executing: datetime | None = None
        self.equipment: Optional['Equipment'] = None

    @property
    def finish_executing_timestamp(self) -> datetime:
        if not self._finish_executing:
            raise Exception("finish_executing was not set")
        return self._finish_executing

    @finish_executing_timestamp.setter
    def finish_executing_timestamp(self, value: datetime) -> None:
        self._finish_executing = value

    @property
    def is_finished(self) -> bool:
        return self.next_step is None
    
    def get_step_by_name(self, name: str) -> 'Step':
        return self.steps_map[name]

    def register_step_finished(self, name: str) -> None:
        index = self.steps_name.index(name)
        if index == len(self.steps) - 1:
            self.next_step = None
            self.case.register_finish_evidence(self)


class Equipment:
    def __init__(self, name: str,  quantity: int,  buffer_size: int) -> None:
        self.name = name
        self.buffer_size = buffer_size
        self.quantity = quantity
        self.buffer: list[Evidence] = []
        self.executing: list[Evidence] = []

    @property
    def vacancies(self) -> int:
        return self.buffer_size - len(self.buffer)

    def add_evidence(self, ev: 'Evidence') -> None:
        if len(self.buffer) == self.buffer_size:
            raise Exception("buffer full")
        self.buffer.append(ev)
        ev.equipment = self

    def start_new(self, time: datetime) -> list[Evidence]:
        ret: list[Evidence] = []
        while True:
            if len(self.buffer) == 0 or len(self.executing) == self.quantity:
                break
            obj = self.buffer.pop()
            obj.finish_executing_timestamp = time + obj.get_step_by_name(self.name).duration
            self.executing.append(obj)
            ret.append(obj)
        return ret
    
    def get_finished(self, time: datetime) -> list[Evidence]:
        return [e for e in self.executing if e.finish_executing_timestamp >= time]
    
    def pop_finished_evidence(self, ev: Evidence) -> None:
        index = self.executing.index(ev)
        self.executing.pop(index)
    
    # def pop_finished(self, time: datetime) -> list[Evidence]:
    #     evs: list[Evidence] = []
    #     i = 0
    #     while i < len(self.executing):
    #         ev = self.executing[i]
    #         if ev.finish_executing_timestamp >= time:
    #             ev = self.executing.pop(i)
    #             ev.equipment = None
    #             ev.register_step_finished(ev.)
    #             evs.append(ev)
    #         else:
    #             i += 1
    #     return evs
