"""Reproducible analysis for Digital Transformation and Green Innovation.

Raw and derived microdata are intentionally retained outside the public repository.
The script downloads no data; see data/DATA_MANIFEST.md for DOI download locations.
"""
from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfixest as pf
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Point this to the `data` directory of the separate private repository.
PRIVATE_DATA_ROOT = Path(os.environ.get("DGI_PRIVATE_DATA_ROOT", PROJECT_ROOT / "data/private"))
GREEN_PATH = PRIVATE_DATA_ROOT / "raw/extracted/green/map-green innovation/dataset-final.dta"
DT_PATH = PRIVATE_DATA_ROOT / "raw/extracted/dt/Digital transformation and strategic risk taking dataset/Digita Transformation and-Strategic Risk Taking Dataset.xlsx"
DERIVED = PRIVATE_DATA_ROOT / "derived"
RESULTS = PROJECT_ROOT / "results"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"
METADATA = PRIVATE_DATA_ROOT / "metadata"
for directory in (DERIVED, TABLES, FIGURES, METADATA):
    directory.mkdir(parents=True, exist_ok=True)

# Field map is deliberately explicit, so a future data revision fails visibly rather than silently.
GREEN_COLS = {
    "股票代码": "firm_id",
    "会计年度": "year",
    "资产负债率": "leverage",
    "Cflow": "cash_flow",
    "Size": "firm_size",
    "BM": "book_to_market",
    "ROA": "roa",
    "Growth": "growth",
    "固定资产比率": "fixed_asset_ratio",
    "股权制衡度": "equity_balance",
    "Indep": "independent_directors",
    "董事会规模": "board_size",
    "第一大股东持股比率": "largest_holder",
    "Staff": "employee_scale",
    "Dual": "ceo_duality",
    "soe": "soe",
    "当年联合申请的绿色发明数量": "green_invention_count",
    "当年联合申请的绿色实用新型数量": "green_utility_count",
    "Lngp": "green_output_log",
}
DT_COLS = {
    "Stockcode": "firm_id",
    "Year": "year",
    "Digital Transformation": "dt_raw",
}
CONTROLS = [
    "leverage", "cash_flow", "firm_size", "book_to_market", "roa", "growth",
    "fixed_asset_ratio", "equity_balance", "independent_directors", "board_size",
    "largest_holder", "employee_scale", "ceo_duality", "soe",
]


def coerce_key(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["firm_id"] = pd.to_numeric(out["firm_id"], errors="raise").astype("int64")
    out["year"] = pd.to_numeric(out["year"], errors="raise").astype("int64")
    return out


def key_summary(frame: pd.DataFrame) -> dict:
    duplicate_rows = int(frame.duplicated(["firm_id", "year"]).sum())
    return {
        "rows": int(len(frame)),
        "firms": int(frame["firm_id"].nunique()),
        "years": [int(x) for x in sorted(frame["year"].unique())],
        "duplicate_firm_year_rows": duplicate_rows,
    }


def estimate_table_row(name: str, fit, regressor: str = "log_dt") -> dict:
    coef = float(fit.coef().loc[regressor])
    se = float(fit.se().loc[regressor])
    p = float(fit.pvalue().loc[regressor])
    ci_low = coef - 1.959964 * se
    ci_high = coef + 1.959964 * se
    nobs = int(fit._N) if hasattr(fit, "_N") else None
    return {
        "Model": name,
        "Regressor": regressor,
        "Coefficient": coef,
        "SE (firm-clustered)": se,
        "p-value": p,
        "95% CI lower": ci_low,
        "95% CI upper": ci_high,
        "N": nobs,
    }


def fit_model(name: str, estimator, formula: str, data: pd.DataFrame, regressor: str) -> tuple[dict, object]:
    fit = estimator(formula, data=data, vcov={"CRV1": "firm_id"})
    return estimate_table_row(name, fit, regressor), fit


# 1) Read and key-audit the data.
green = pd.read_stata(GREEN_PATH, convert_categoricals=False)
dt = pd.read_excel(DT_PATH, sheet_name="Digital Transformation")
missing_green = sorted(set(GREEN_COLS) - set(green.columns))
missing_dt = sorted(set(DT_COLS) - set(dt.columns))
if missing_green or missing_dt:
    raise KeyError({"missing_green_columns": missing_green, "missing_dt_columns": missing_dt})

green = coerce_key(green[list(GREEN_COLS)].rename(columns=GREEN_COLS))
dt = coerce_key(dt[list(DT_COLS)].rename(columns=DT_COLS))

# The green source defines the temporal window. Make source restriction transparent.
dt_restricted = dt.loc[dt["year"].between(2014, 2020)].copy()
for label, frame in (("green", green), ("dt_full", dt), ("dt_2014_2020", dt_restricted)):
    if frame.duplicated(["firm_id", "year"]).any():
        duplicates = frame.loc[frame.duplicated(["firm_id", "year"], keep=False), ["firm_id", "year"]].head(20)
        raise ValueError(f"{label} has duplicate firm-year keys:\n{duplicates}")

merged = green.merge(dt_restricted, how="inner", on=["firm_id", "year"], validate="one_to_one", indicator=True)
if not (merged["_merge"] == "both").all():
    raise AssertionError("Unexpected non-inner merge outcome")
merged = merged.drop(columns="_merge")

# 2) Construct outcomes and transformed regressor. Counts must be non-negative.
for count_column in ("green_invention_count", "green_utility_count"):
    if (merged[count_column] < 0).any():
        raise ValueError(f"Negative count found in {count_column}")
if (merged["dt_raw"] < 0).any():
    raise ValueError("Digital-transformation score contains a negative value")
merged["green_quality_log"] = np.log1p(merged["green_invention_count"])
merged["green_utility_log"] = np.log1p(merged["green_utility_count"])
merged["log_dt"] = np.log1p(merged["dt_raw"])
merged = merged.sort_values(["firm_id", "year"]).reset_index(drop=True)
merged["log_dt_lag1"] = merged.groupby("firm_id")["log_dt"].shift(1)
merged["previous_year"] = merged.groupby("firm_id")["year"].shift(1)
merged.loc[merged["year"] - merged["previous_year"] != 1, "log_dt_lag1"] = np.nan

# Preserve an auditable complete-case sample used by every main estimate.
main = merged.dropna(subset=["green_invention_count", "green_quality_log", "log_dt", *CONTROLS]).copy()
if len(main) == 0:
    raise ValueError("No complete observations after applying the declared control set")
main.to_csv(DERIVED / "matched_panel_private.csv", index=False)

# 3) Diagnostics.
within_sd = main.groupby("firm_id")["dt_raw"].std(ddof=1)
firm_mean_dt = main.groupby("firm_id")["dt_raw"].transform("mean")
within_ss = float(((main["dt_raw"] - firm_mean_dt) ** 2).sum())
total_ss = float(((main["dt_raw"] - main["dt_raw"].mean()) ** 2).sum())
variance_components = {
    "dt_total_sd": float(main["dt_raw"].std(ddof=1)),
    "dt_between_firm_sd": float(main.groupby("firm_id")["dt_raw"].mean().std(ddof=1)),
    "mean_dt_within_firm_sd": float(within_sd.mean()),
    "within_to_total_variance_ratio": within_ss / total_ss,
    "green_invention_zero_share": float((main["green_invention_count"] == 0).mean()),
}

# VIF is calculated on a constant plus the declared regressor and controls; it is descriptive only.
vif_frame = main[["log_dt", *CONTROLS]].replace([np.inf, -np.inf], np.nan).dropna()
vif_x = sm.add_constant(vif_frame)
vif_results = pd.DataFrame({
    "variable": vif_x.columns,
    "VIF": [variance_inflation_factor(vif_x.values, i) for i in range(vif_x.shape[1])],
})
vif_results.to_csv(TABLES / "vif_diagnostics.csv", index=False)

match_diagnostics = pd.DataFrame({
    "variable": ["leverage", "cash_flow", "firm_size", "green_output_log"],
    "green_source_mean": [float(green[c].mean()) for c in ["leverage", "cash_flow", "firm_size", "green_output_log"]],
    "matched_complete_case_mean": [float(main[c].mean()) for c in ["leverage", "cash_flow", "firm_size", "green_output_log"]],
})
match_diagnostics.to_csv(TABLES / "sample_selection_diagnostics.csv", index=False)

# 4) Estimation. All specifications use the same declared controls and firm-clustered CRV1 SE.
controls_formula = " + ".join(CONTROLS)
models = []
fits = {}

specifications = [
    ("M0: OLS, log quality, raw DT, firm and year FE", pf.feols, f"green_quality_log ~ dt_raw + {controls_formula} | firm_id + year", main, "dt_raw"),
    ("M1: OLS, log quality, log DT, firm and year FE", pf.feols, f"green_quality_log ~ log_dt + {controls_formula} | firm_id + year", main, "log_dt"),
    ("M2: OLS, patent count, log DT, firm and year FE", pf.feols, f"green_invention_count ~ log_dt + {controls_formula} | firm_id + year", main, "log_dt"),
    ("M3: PPML, patent count, log DT, firm and year FE", pf.fepois, f"green_invention_count ~ log_dt + {controls_formula} | firm_id + year", main, "log_dt"),
    ("M4: OLS, utility-patent log, log DT, firm and year FE", pf.feols, f"green_utility_log ~ log_dt + {controls_formula} | firm_id + year", main, "log_dt"),
]
for name, estimator, formula, data, regressor in specifications:
    row, fit = fit_model(name, estimator, formula, data, regressor)
    models.append(row)
    fits[name] = fit

# Lagged model uses no contemporaneous digital score and therefore has a smaller predeclared sample.
lagged = main.dropna(subset=["log_dt_lag1"]).copy()
lag_row, lag_fit = fit_model(
    "M5: PPML, lagged DT, firm and year FE",
    pf.fepois,
    f"green_invention_count ~ log_dt_lag1 + {controls_formula} | firm_id + year",
    lagged,
    "log_dt_lag1",
)
models.append(lag_row)
fits[lag_row["Model"]] = lag_fit

model_results = pd.DataFrame(models)
model_results["p-value display"] = model_results["p-value"].map(lambda x: "<0.001" if x < 0.001 else f"{x:.4f}")
model_results.to_csv(TABLES / "main_model_results.csv", index=False)

# 5) Decision-relevant figures.
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
plot_df = model_results.copy()
plot_df["label"] = ["OLS log quality\nraw DT; firm+year FE", "OLS log quality\nlog DT; firm+year FE", "OLS count\nlog DT; firm+year FE", "PPML count\nlog DT; firm+year FE", "OLS utility log\nlog DT; firm+year FE", "PPML lagged count\nfirm+year FE"]
y = np.arange(len(plot_df))
ax.errorbar(plot_df["Coefficient"], y,
            xerr=[plot_df["Coefficient"] - plot_df["95% CI lower"], plot_df["95% CI upper"] - plot_df["Coefficient"]],
            fmt="o", color="#1f4e79", ecolor="#6b8eaa", capsize=3)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_yticks(y, plot_df["label"])
ax.set_xlabel("Estimated DT coefficient; 95% CI (DT treatment stated for each model)")
ax.set_title("Model-sensitive association estimates")
fig.tight_layout()
fig.savefig(FIGURES / "coefficient_comparison.png", bbox_inches="tight")
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
axes[0].hist(main["dt_raw"], bins=50, color="#1f4e79", alpha=0.85)
axes[0].set_title("Raw digital-transformation score")
axes[0].set_xlabel("DT")
axes[0].set_ylabel("Firm-year observations")
axes[1].bar(["Zero", "Positive"], [(main["green_invention_count"] == 0).mean(), (main["green_invention_count"] > 0).mean()], color=["#b24c4c", "#2f855a"])
axes[1].set_ylim(0, 1)
axes[1].set_ylabel("Share of observations")
axes[1].set_title("Green invention-patent count")
for bar in axes[1].patches:
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{bar.get_height():.1%}", ha="center")
fig.tight_layout()
fig.savefig(FIGURES / "distribution_diagnostics.png", bbox_inches="tight")
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
long = match_diagnostics.melt(id_vars="variable", var_name="sample", value_name="mean")
pivot = long.pivot(index="variable", columns="sample", values="mean")
pivot.plot(kind="bar", ax=ax, color=["#a5b9c9", "#1f4e79"])
ax.set_ylabel("Mean (variable-specific scale)")
ax.set_xlabel("")
ax.set_title("Pre-match versus matched complete-case means")
ax.legend(title="Sample")
fig.tight_layout()
fig.savefig(FIGURES / "sample_selection_diagnostics.png", bbox_inches="tight")
plt.close(fig)

# 6) Machine-readable and reviewer-readable execution record.
audit = {
    "run_utc": datetime.now(timezone.utc).isoformat(),
    "source_files": {
        "green": str(GREEN_PATH.relative_to(PRIVATE_DATA_ROOT)),
        "digital_transformation": str(DT_PATH.relative_to(PRIVATE_DATA_ROOT)),
    },
    "source_keys": {
        "green": key_summary(green),
        "dt_full": key_summary(dt),
        "dt_restricted_2014_2020": key_summary(dt_restricted),
        "matched_pre_complete_case": key_summary(merged),
        "matched_complete_case": key_summary(main),
        "lagged_complete_case": key_summary(lagged),
    },
    "variance_components": variance_components,
    "main_controls": CONTROLS,
    "models": model_results.drop(columns=["p-value display"]).to_dict(orient="records"),
}
(METADATA / "analysis_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

summary_lines = [
    "# Reproduction and Optimized-Model Run",
    "",
    "## Sample and Key Validation",
    "",
    "```json",
    json.dumps(audit["source_keys"], ensure_ascii=False, indent=2),
    "```",
    "",
    "## Model Results",
    "",
    model_results[["Model", "Regressor", "Coefficient", "SE (firm-clustered)", "p-value display", "95% CI lower", "95% CI upper", "N"]].to_markdown(index=False),
    "",
    "## Diagnostics",
    "",
    pd.DataFrame([variance_components]).T.rename(columns={0: "value"}).to_markdown(),
    "",
    "## Specification Notes",
    "",
    "All estimates include the declared firm-level controls and are clustered by firm. M0, M1, M2, M4 and M5 use firm and year fixed effects. M3 uses PPML with firm and year fixed effects, enabling a count-link model while retaining zero outcomes and absorbing time-invariant firm heterogeneity. Firms whose outcome is zero in every observed year do not identify a conditional Poisson firm effect and are therefore excluded by the estimator; its reported estimation sample must not be presented as identical to the OLS sample. The PPML estimator is an association model, not a causal design.",
    "",
    "The raw and matched microdata are private outputs. This summary, aggregate tables and figures may be shared publicly only after a license and disclosure review.",
]
(TABLES / "reproduction_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

print("Analysis completed")
print(json.dumps(audit, ensure_ascii=False, indent=2))
