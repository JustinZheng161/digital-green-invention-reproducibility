"""Pre-specified model-upgrade experiments for the matched firm-year panel.

Upgrade A: compare a parsimonious, theory-motivated control block with the locked
full block without selecting a favorable p-value.
Upgrade B: winsorize the exposure before log1p and refit the same TWFE OLS and
conditional PPML specifications.

The outputs are aggregate tables only. They are descriptive sensitivities, not
causal estimates or a universal performance leaderboard.
"""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import pyfixest as pf

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DATA_ROOT = Path(os.environ.get("DGI_PRIVATE_DATA_ROOT", PROJECT_ROOT / "data/private"))
PANEL_PATH = PRIVATE_DATA_ROOT / "derived/matched_panel_private.csv"
OUT = PROJECT_ROOT / "results/tables"
OUT.mkdir(parents=True, exist_ok=True)

FULL_CONTROLS = [
    "leverage", "cash_flow", "firm_size", "book_to_market", "roa", "growth",
    "fixed_asset_ratio", "equity_balance", "independent_directors", "board_size",
    "largest_holder", "employee_scale", "ceo_duality", "soe",
]
CORE_CONTROLS = ["firm_size", "leverage", "roa", "growth", "soe"]
NO_GOVERNANCE_CONTROLS = ["leverage", "cash_flow", "firm_size", "book_to_market", "roa", "growth", "fixed_asset_ratio", "equity_balance", "largest_holder", "employee_scale", "soe"]
NO_FINANCIAL_CONTROLS = ["firm_size", "independent_directors", "board_size", "largest_holder", "employee_scale", "ceo_duality", "soe"]

panel = pd.read_csv(PANEL_PATH).sort_values(["firm_id", "year"]).reset_index(drop=True)
panel["green_quality_log"] = np.log1p(panel["green_invention_count"])
panel["log_dt"] = np.log1p(panel["dt_raw"])
for c in ["green_quality_log", "log_dt", *FULL_CONTROLS]:
    panel[c] = pd.to_numeric(panel[c], errors="coerce")

# Common complete-case sample for each control block, with no p-value based deletion.
def fit_row(label, estimator, outcome, regressor, controls, data, upgrade):
    rhs = " + ".join([regressor, *controls])
    formula = f"{outcome} ~ {rhs} | firm_id + year"
    fit = estimator(formula, data=data, vcov={"CRV1": "firm_id"})
    beta = float(fit.coef().loc[regressor])
    se = float(fit.se().loc[regressor])
    return {
        "Upgrade": upgrade,
        "Model": label,
        "Estimator": "TWFE OLS" if estimator is pf.feols else "Conditional PPML",
        "Outcome": outcome,
        "Regressor": regressor,
        "Controls": "+".join(controls),
        "Coefficient": beta,
        "Clustered SE": se,
        "p_value": float(fit.pvalue().loc[regressor]),
        "95% CI lower": beta - 1.959964 * se,
        "95% CI upper": beta + 1.959964 * se,
        "Candidate N": int(len(data)),
        "Estimator N": int(fit._N),
        "Firms": int(fit._data["firm_id"].nunique()),
    }

rows = []
# Upgrade A/B: control-block ablations. No outcome-specific p-value selection is used.
for block_name, controls, upgrade in [
    ("Core pre-specified block", CORE_CONTROLS, "A_control_block"),
    ("No-governance block", NO_GOVERNANCE_CONTROLS, "A_control_block"),
    ("No-financial-controls block", NO_FINANCIAL_CONTROLS, "B_control_block"),
    ("Locked full block", FULL_CONTROLS, "A_control_block"),
]:
    d = panel.dropna(subset=["green_quality_log", "log_dt", *controls]).copy()
    rows.append(fit_row(f"{block_name}: log outcome", pf.feols, "green_quality_log", "log_dt", controls, d, upgrade))
    rows.append(fit_row(f"{block_name}: count outcome", pf.fepois, "green_invention_count", "log_dt", controls, d, upgrade))

# Upgrade B: fixed 1%/99% exposure winsorization, retaining the same full control block.
lo, hi = panel["dt_raw"].quantile([0.01, 0.99])
panel["dt_raw_winsor_1_99"] = panel["dt_raw"].clip(lo, hi)
panel["log_dt_winsor_1_99"] = np.log1p(panel["dt_raw_winsor_1_99"])
d = panel.dropna(subset=["green_quality_log", "log_dt_winsor_1_99", *FULL_CONTROLS]).copy()
rows.append(fit_row("1%/99% winsorized exposure: log outcome", pf.feols, "green_quality_log", "log_dt_winsor_1_99", FULL_CONTROLS, d, "B_exposure_winsorization"))
rows.append(fit_row("1%/99% winsorized exposure: count outcome", pf.fepois, "green_invention_count", "log_dt_winsor_1_99", FULL_CONTROLS, d, "B_exposure_winsorization"))

out = pd.DataFrame(rows)
out["p-value display"] = out["p_value"].map(lambda p: "<0.001" if p < 0.001 else f"{p:.4f}")
out.to_csv(OUT / "model_upgrade_sensitivities.csv", index=False)

notes = f"""# Model-upgrade sensitivity results

The file reports two pre-specified ablations and one robustness check. Ablation A compares a small theory-motivated block (`{'+'.join(CORE_CONTROLS)}`), a no-governance block (`{'+'.join(NO_GOVERNANCE_CONTROLS)}`), and the locked full block. Ablation B removes the financial controls and retains size/governance controls. No specification is selected using its p-value. The robustness check clips raw DT at the sample 1st and 99th percentiles before applying `ln(1+DT)` and refits the identical firm/year fixed-effects models. The clipping thresholds are `{lo:.8g}` and `{hi:.8g}`.

These are association sensitivities under the matched observational design. Conditional PPML has a distinct estimator-retained sample because all-zero firms do not identify a conditional firm effect. The results must not be interpreted as causal effects or as a machine-learning accuracy score.
"""
(OUT / "model_upgrade_sensitivities.md").write_text(notes, encoding="utf-8")
print(out.to_markdown(index=False))
