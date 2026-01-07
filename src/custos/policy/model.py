from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

from custos.enums import OnConflict, OnMissing
from custos.errors import PolicyError


@dataclass(frozen=True)
class SchemaPolicy:
    rename: dict[str, str] = field(default_factory=dict)
    on_missing: OnMissing = OnMissing.WARN
    on_conflict: OnConflict = OnConflict.ERROR


@dataclass(frozen=True)
class Policy:
    version: int = 1
    schema: SchemaPolicy = field(default_factory=SchemaPolicy)


def policy_from_dict(raw: Mapping[str, Any]) -> Policy:
    if not isinstance(raw, Mapping):
        raise PolicyError("Policy must be a mapping (dict-like).")

    version = raw.get("version", 1)
    if version != 1:
        raise PolicyError(f"Unsupported policy version: {version}")

    schema_raw = raw.get("schema", {}) or {}
    if not isinstance(schema_raw, Mapping):
        raise PolicyError("`schema` must be a mapping.")

    rename_raw = schema_raw.get("rename", {}) or {}
    if not isinstance(rename_raw, Mapping):
        raise PolicyError("`schema.rename` must be a mapping of source->target.")

    rename: dict[str, str] = {}
    for k, v in rename_raw.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise PolicyError("`schema.rename` must map string keys to string values.")
        if not k.strip() or not v.strip():
            raise PolicyError("`schema.rename` keys/values cannot be empty.")
        rename[k] = v

    on_missing = OnMissing(schema_raw.get("on_missing", OnMissing.WARN))
    on_conflict = OnConflict(schema_raw.get("on_conflict", OnConflict.ERROR))

    return Policy(
        version=version,
        schema=SchemaPolicy(
            rename=rename,
            on_missing=on_missing,
            on_conflict=on_conflict,
        ),
    )
