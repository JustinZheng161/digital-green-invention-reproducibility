"""Aggregate regression checks for model-upgrade sensitivities."""
from pathlib import Path
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "results/tables/model_upgrade_sensitivities.csv"
assert path.exists() and path.stat().st_size > 100
out = pd.read_csv(path)
assert len(out) == 10
assert set(out["Upgrade"]) == {"A_control_block", "B_control_block", "B_exposure_winsorization"}
full_ols = out.loc[out["Model"].eq("Locked full block: log outcome")].iloc[0]
core_ols = out.loc[out["Model"].eq("Core pre-specified block: log outcome")].iloc[0]
no_fin_ppml = out.loc[out["Model"].eq("No-financial-controls block: count outcome")].iloc[0]
win_ppml = out.loc[out["Model"].eq("1%/99% winsorized exposure: count outcome")].iloc[0]
assert math.isclose(float(full_ols["Coefficient"]), 0.01962785, abs_tol=1e-6)
assert math.isclose(float(core_ols["Coefficient"]), 0.0216351, abs_tol=1e-6)
assert math.isclose(float(no_fin_ppml["Coefficient"]), 0.0787538, abs_tol=1e-6)
assert math.isclose(float(win_ppml["Coefficient"]), 0.0932056, abs_tol=1e-6)
assert (out["Estimator N"] == 6443).sum() == 5
assert (out["Estimator N"] == 2774).sum() == 5
assert out["Firms"].isin([1337, 505]).all()
print("PASS: model-upgrade ablation and exposure-robustness outputs match locked aggregate values.")
