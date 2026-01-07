from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from custos.planning.steps import CastTypesStep, RenameColumnsStep

Step = Union[RenameColumnsStep, CastTypesStep]


@dataclass(frozen=True)
class Plan:
    steps: tuple[Step, ...]
