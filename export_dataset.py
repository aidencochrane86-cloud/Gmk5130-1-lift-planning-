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
    raw = pd.read_excel(EXCEL_PATH, sheet_name=sheet, header=None)

    current_base = None
    headers = None

    for _, row in raw.iterrows():
        first_cell = str(row[0]).strip()

        # Detect outrigger base line
        if first_cell.startswith("Outrigger base:"):
            current_base = first_cell.replace("Outrigger base:", "").strip()
            headers = None
            continue

        # Detect header row
        if first_cell == "Counterweight_t":
            headers = list(row)
            continue

        # Skip until headers and base are known
        if headers is None or current_base is None:
            continue

        # Build data row
        record = dict(zip(headers, row))

        # Skip empty rows
        if pd.isna(record.get("Radius_m")) or pd.isna(record.get("Slew_position")):
            continue

        outrigger_loads = {
            "FL": record.get("FL_t"),
            "FR": record.get("FR_t"),
            "RL": record.get("RL_t"),
            "RR": record.get("RR_t"),
        }

        governing_outrigger = max(
            outrigger_loads,
            key=lambda k: outrigger_loads[k]
        )

        records.append({
            "crane_model": CRANE_MODEL,
            "counterweight_t": counterweight,
            "outrigger_base": current_base,
            "radius_m": float(record["Radius_m"]),
            "slew_position": record["Slew_position"],
            "governing_outrigger": governing_outrigger,
            "governing_load_t": float(outrigger_loads[governing_outrigger])
        })

# -----------------------------
# Write JSON for backend
# -----------------------------
with open(OUTPUT_PATH, "w") as f:
    json.dump(records, f, indent=2)

print(f"Exported {len(records)} records to {OUTPUT_PATH}")
