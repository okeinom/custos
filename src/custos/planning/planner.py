from __future__ import annotations

from custos.planning.plan import Plan
from custos.planning.steps import CastTypesStep, RenameColumnsStep
from custos.policy.model import Policy


class Planner:
    def __init__(self, policy: Policy):
        self.policy = policy

    def build(self) -> Plan:
        steps = []

        # 1) rename first
        if self.policy.schema.rename:
            steps.append(
                RenameColumnsStep(
                    mapping=self.policy.schema.rename,
                    on_missing=self.policy.schema.on_missing,
                    on_conflict=self.policy.schema.on_conflict,
                )
            )

        # 2) then cast
        if self.policy.schema.types:
            steps.append(
                CastTypesStep(
                    types=self.policy.schema.types,
                    on_cast_fail=self.policy.schema.cast.on_cast_fail,
                    datetime_format=self.policy.schema.cast.datetime_format,
                )
            )

        return Plan(steps=tuple(steps))
