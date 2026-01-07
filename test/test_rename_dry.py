import pandas as pd
from custos import PolicyTransformer

def test_rename_dry_run_does_not_modify():
    df = pd.DataFrame({"A": [1]})
    policy = {"schema": {"rename": {"A": "a"}}}

    t = PolicyTransformer(policy, mode="dry_run")
    out, report = t.apply(df)

    assert "A" in out.columns
    assert "a" not in out.columns
