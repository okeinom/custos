from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from custos.planning.steps import CastTypesStep, QualityRulesStep, RenameColumnsStep

Step = Union[RenameColumnsStep, CastTypesStep, QualityRulesStep]


@dataclass(frozen=True)
class Plan:
    steps: tuple[Step, ...]
