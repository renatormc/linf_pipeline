from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Protocol


@dataclass
class TaskObject:
    object: 'Objeto'
    task_duration: timedelta
    start: datetime | None = None
    end: datetime | None = None


class Equipamento:

    def __init__(self, tipo: str, quantidade: int, buffer_size: int) -> None:
        self.on_finish:  Callable[[str, int], None] | None = None
        self.on_release: Callable[[str, int], None] | None = None
        self.quantidade = quantidade
        self.buffer_size = buffer_size
        self._buffer: list[TaskObject] = []
        self._running: list[TaskObject] = []
        self._finished: list[TaskObject] = []
        self.tipo = tipo

    def update(self, time: datetime) -> None:
        n = 0
        for task_object in self._running:
            if task_object.end and task_object.end <= time:
                self._running.remove(task_object)
                self._finished.append(task_object)
                n += 1
        self.start_new(time)
        if n > 0 and self.on_finish is not None:
            self.on_finish(self.tipo, n)

    def start_new(self, time: datetime) -> None:
        n = len(self._running) + len(self._finished) - self.quantidade
        if len(self._buffer) < n:
            n = len(self._buffer)
        for i in range(n):
            task_object = self._buffer.pop(0)
            task_object.start = time
            task_object.end = time + task_object.task_duration
            self._running.append(task_object)
        if n > 0 and self.on_release is not None:
            self.on_release(self.tipo, n)

    def pop_finished(self, time: datetime) -> list['Objeto']:
        finished = self._finished
        self._finished = []
        self.start_new(time)
        return [task_object.object for task_object in finished]

    def push_object(self, obj: 'Objeto', task_duration: timedelta, time: datetime) -> None:
        if len(self._buffer) >= self.buffer_size:
            raise Exception("Equipamento cheio")
        self._buffer.append(TaskObject(obj, task_duration))
        self.start_new(time)



class Objeto(Protocol):
    @property
    def id(self) -> str:
        pass
