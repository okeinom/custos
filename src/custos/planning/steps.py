from __future__ import annotations
from dataclasses import dataclass

from custos.enums import OnConflict, OnMissing


@dataclass(frozen=True)
class RenameColumnsStep:
    mapping: dict[str, str]
    on_missing: OnMissing
    on_conflict: OnConflict

