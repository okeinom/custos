from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from custos.planning.steps import CastTypesStep, PiiStep, QualityRulesStep, RenameColumnsStep

Step = Union[RenameColumnsStep, CastTypesStep, QualityRulesStep, PiiStep]


@dataclass(frozen=True)
class Plan:
    steps: tuple[Step, ...]
