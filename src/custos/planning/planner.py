from __future__ import annotations

from custos.planning.plan import Plan
from custos.planning.steps import CastTypesStep, QualityRulesStep, RenameColumnsStep
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

        # 3) then quality
        qp = self.policy.schema.quality
        if qp.rules:
            steps.append(
                QualityRulesStep(
                    rules=tuple(
                        {
                            "column": r.column,
                            "not_null": r.not_null,
                            "min": r.min,
                            "max": r.max,
                            "accepted_values": r.accepted_values,
                            "on_fail": r.on_fail.value,
                        }
                        for r in qp.rules
                    ),
                    default_on_fail=qp.default_on_fail,
                )
            )

        return Plan(steps=tuple(steps))
