from __future__ import annotations
from enum import Enum


class Mode(str, Enum):
    STRICT = "strict"
    DROP = "drop"
    DRY_RUN = "dry_run"


class OnMissing(str, Enum):
    ERROR = "error"
    WARN = "warn"
    IGNORE = "ignore"


class OnConflict(str, Enum):
    ERROR = "error"
    OVERWRITE = "overwrite"
