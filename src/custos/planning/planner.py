from __future__ import annotations

from custos.planning.plan import Plan
from custos.planning.steps import RenameColumnsStep
from custos.policy.model import Policy


class Planner:
    def __init__(self, policy: Policy):
        self.policy = policy

    def build(self) -> Plan:
        steps = []

        # v1: only rename
        if self.policy.schema.rename:
            steps.append(
                RenameColumnsStep(
                    mapping=self.policy.schema.rename,
                    on_missing=self.policy.schema.on_missing,
                    on_conflict=self.policy.schema.on_conflict,
                )
            )

        return Plan(steps=tuple(steps))
