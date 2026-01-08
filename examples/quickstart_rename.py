from pathlib import Path
import pandas as pd
from custos import PolicyTransformer


# Always resolve policy relative to this file
POLICY_PATH = Path(__file__).resolve().parent / "policy.yml"


df = pd.DataFrame({
    "Total Price": [10.5, 20.0, 30.25],
    "Order ID": [101, 102, 103],
    "email": ["john@test.com", "bad-email", None],
})

transformer = PolicyTransformer(
    policy=POLICY_PATH,
    mode="dry_run",
)

df_out, report = transformer.apply(df)

print("Original DF:")
print(df.head())

print("\nTransformed DF:")
print(df_out.head())

print("\nCustos actions:")
for action in report.actions:
    print(f"- {action.kind}: {action.details}")
