from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from custos.planning.steps import RenameColumnsStep

Step = Union[RenameColumnsStep]


@dataclass(frozen=True)
class Plan:
    steps: tuple[Step, ...]
