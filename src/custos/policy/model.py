from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

from custos.enums import OnCastFail, OnConflict, OnMissing
from custos.errors import PolicyError


@dataclass(frozen=True)
class CastPolicy:
    on_cast_fail: OnCastFail = OnCastFail.ERROR
    datetime_format: str | None = None


@dataclass(frozen=True)
class SchemaPolicy:
    rename: dict[str, str] = field(default_factory=dict)
    types: dict[str, str] = field(default_factory=dict)  # e.g. {"order_id": "int"}
    cast: CastPolicy = field(default_factory=CastPolicy)
    on_missing: OnMissing = OnMissing.WARN
    on_conflict: OnConflict = OnConflict.ERROR


@dataclass(frozen=True)
class Policy:
    version: int = 1
    schema: SchemaPolicy = field(default_factory=SchemaPolicy)


_ALLOWED_TYPES = {"int", "float", "string", "bool", "datetime", "date"}


def policy_from_dict(raw: Mapping[str, Any]) -> Policy:
    if not isinstance(raw, Mapping):
        raise PolicyError("Policy must be a mapping (dict-like).")

    version = raw.get("version", 1)
    if version != 1:
        raise PolicyError(f"Unsupported policy version: {version}")

    schema_raw = raw.get("schema", {}) or {}
    if not isinstance(schema_raw, Mapping):
        raise PolicyError("`schema` must be a mapping.")

    # --- rename ---
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

    # --- types ---
    types_raw = schema_raw.get("types", {}) or {}
    if not isinstance(types_raw, Mapping):
        raise PolicyError("`schema.types` must be a mapping of column->type.")

    types: dict[str, str] = {}
    for col, typ in types_raw.items():
        if not isinstance(col, str) or not isinstance(typ, str):
            raise PolicyError("`schema.types` must map string column names to string type names.")
        t = typ.strip().lower()
        if t not in _ALLOWED_TYPES:
            raise PolicyError(f"Unsupported type '{typ}' for column '{col}'. Allowed: {sorted(_ALLOWED_TYPES)}")
        types[col] = t

    # --- behaviors ---
    on_missing = OnMissing(schema_raw.get("on_missing", OnMissing.WARN))
    on_conflict = OnConflict(schema_raw.get("on_conflict", OnConflict.ERROR))

    cast_raw = schema_raw.get("cast", {}) or {}
    if not isinstance(cast_raw, Mapping):
        raise PolicyError("`schema.cast` must be a mapping.")

    on_cast_fail = OnCastFail(cast_raw.get("on_cast_fail", OnCastFail.ERROR))
    datetime_format = cast_raw.get("datetime_format", None)
    if datetime_format is not None and not isinstance(datetime_format, str):
        raise PolicyError("`schema.cast.datetime_format` must be a string or null.")

    return Policy(
        version=version,
        schema=SchemaPolicy(
            rename=rename,
            types=types,
            cast=CastPolicy(on_cast_fail=on_cast_fail, datetime_format=datetime_format),
            on_missing=on_missing,
            on_conflict=on_conflict,
        ),
    )
