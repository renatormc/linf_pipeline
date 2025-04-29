from dataclasses import dataclass
from datetime import datetime
from typing import Literal


SIM_METHOD = Literal['individual', 'pipeline']

@dataclass
class TimeValue:
    time: datetime
    day_sequence: int