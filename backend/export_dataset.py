import json
import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).parent
EXCEL_PATH = PROJECT_ROOT / "GMK5130_Phase1_Outrigger_Loads.xlsx"
OUTPUT_PATH = PROJECT_ROOT / "backend" / "dataset.json"

CRANE_MODEL = "GMK5130-1"

records = []

# Sheet name → counterweight mapping
sheet_counterweights = {
    "40.1t": 40.1,
    "23.5t": 23.5,
    "6.0t": 6.0
}

# -----------------------------
# Read Excel & build dataset
# -----------------------------
for sheet, counterweight in sheet_counterweights.items():
    df = pd.read_excel(EXCEL_PATH, sheet_name=sheet)

    # Only keep rows that actually contain lift data
    df = df.dropna(subset=["Radius_m", "Slew_position"])

    for _, row in df.iterrows():
        outrigger_loads = {
            "FL": row.get("FL_t"),
            "FR": row.get("FR_t"),
            "RL": row.get("RL_t"),
            "RR": row.get("RR_t"),
        }

        # Find governing outrigger
        governing_outrigger = max(
            outrigger_loads,
            key=lambda k: outrigger_loads[k]
        )

        governing_load_t = float(outrigger_loads[governing_outrigger])

        records.append({
            "crane_model": CRANE_MODEL,
            "counterweight_t": counterweight,
            "outrigger_base": row["Outrigger_base"],
            "radius_m": float(row["Radius_m"]),
            "slew_position": row["Slew_position"],
            "governing_outrigger": governing_outrigger,
            "governing_load_t": governing_load_t
        })

# -----------------------------
# Write JSON for backend
# -----------------------------
with open(OUTPUT_PATH, "w") as f:
    json.dump(records, f, indent=2)

print(f"Exported {len(records)} records to {OUTPUT_PATH}")

