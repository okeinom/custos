from pathlib import Path
from pprint import pprint
import pandas as pd
from custos import PolicyTransformer

POLICY_PATH = Path(__file__).resolve().parent / "policy.yml"

# Include one bad value so casting has something to do
df = pd.DataFrame({
    "Total Price": ["10.5", "oops", "30.25"],   # "oops" will fail float
    "Order ID": ["101", "102", "x"], 
    "email": ["john@test.com", "bad-email", None],           # "x" will fail int
})

transformer = PolicyTransformer(
    policy=POLICY_PATH,
    mode="strict",   # NOTE: casting behavior is controlled by policy.cast.on_cast_fail
)

df_out, report = transformer.apply(df)

print("Original DF:")
print(df.head())

print("\nTransformed DF:")
print(df_out.head())

print("\nCustos actions:")
for action in report.actions:
    print(f"- {action.kind}: {action.details}")

print("\nReport summary:")
print("rows_in:", report.rows_in)
print("rows_out:", report.rows_out)
print("columns_in:", report.columns_in)
print("columns_out:", report.columns_out)

print("\nActions (structured):")
pprint([{"kind": a.kind, "details": a.details} for a in report.actions])