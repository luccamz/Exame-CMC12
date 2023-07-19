from dataclasses import dataclass, field

@dataclass
class Requirements:
    wb: float = 0.0
    pm: float = 0.0
    err: float = 0.0
    delta_wb: float = field(init=False)
    delta_pm: float = field(init=False)

    def __post_init__(self):
        self.delta_wb = 0.0001*self.wb
        self.delta_pm = 0.001*self.pm