from __future__ import annotations

import logging
from typing import Any

import pandas as pd

from custos.enums import OnConflict, OnMissing
from custos.errors import ExecutionError
from custos.planning.plan import Plan
from custos.planning.steps import RenameColumnsStep
from custos.report.models import Report
from custos.execution.base import Executor

log = logging.getLogger(__name__)


class PandasExecutor(Executor):
    engine_name = "pandas"

    def execute(self, df: Any, plan: Plan, mode: str) -> tuple[pd.DataFrame, Report]:
        if not isinstance(df, pd.DataFrame):
            raise ExecutionError("PandasExecutor expects a pandas.DataFrame")

        rows_in = int(df.shape[0])
        cols_in = list(df.columns)

        out = df.copy()

        report = Report(
            engine=self.engine_name,
            mode=mode,
            rows_in=rows_in,
            rows_out=rows_in,
            columns_in=cols_in,
            columns_out=list(out.columns),
        )

        for step in plan.steps:
            if isinstance(step, RenameColumnsStep):
                out = self._rename(out, step, report, mode)
            else:
                raise ExecutionError(f"Unsupported step type for pandas: {type(step)}")

        # finalize report
        report.rows_out = int(out.shape[0])
        report.columns_out = list(out.columns)
        return out, report

    def _rename(
        self,
        df: pd.DataFrame,
        step: RenameColumnsStep,
        report: Report,
        mode: str,
    ) -> pd.DataFrame:
        mapping = step.mapping

        # Check missing source columns
        missing = [src for src in mapping.keys() if src not in df.columns]
        if missing:
            msg = f"Missing source columns for rename: {missing}"
            if step.on_missing == OnMissing.ERROR:
                raise ExecutionError(msg)
            if step.on_missing == OnMissing.WARN:
                log.warning(msg)
                report.add("rename_missing_sources", missing=missing)
            else:
                report.add("rename_missing_sources_ignored", missing=missing)

        # Only apply mapping for sources that exist
        effective = {src: tgt for src, tgt in mapping.items() if src in df.columns}

        # Detect conflicts (target already exists as a different column)
        conflicts = []
        for src, tgt in effective.items():
            if tgt in df.columns and tgt != src:
                conflicts.append({"source": src, "target": tgt})

        if conflicts:
            msg = f"Rename conflicts (target already exists): {conflicts}"
            if step.on_conflict == OnConflict.ERROR:
                raise ExecutionError(msg)
            if step.on_conflict == OnConflict.OVERWRITE:
                log.warning(msg + " (overwriting targets)")
                report.add("rename_conflicts_overwrite", conflicts=conflicts)
            else:
                raise ExecutionError(msg)

        if mode == "dry_run":
            report.add("rename_dry_run", mapping=effective)
            return df

        df2 = df.rename(columns=effective)
        report.add("rename_applied", mapping=effective)
        return df2
