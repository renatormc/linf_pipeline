from dataclasses import dataclass
from datetime import datetime
from typing import Literal


SIM_METHOD = Literal['current', 'pipeline']

@dataclass
class TimeValue:
    time: datetime
    day_sequence: int