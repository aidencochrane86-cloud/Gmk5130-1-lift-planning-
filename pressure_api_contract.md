# Outrigger Pressure API – Contract (v1)

This document defines the input and output for the outrigger
pressure calculation engine.

---

## Request (Frontend → Backend)

```json
{
  "crane_model": "GMK5130-1",
  "counterweight_t": 23.5,
  "outrigger_base": "Full",
  "radius_m": 16,
  "slew_position": "45_over_side",
  "pad_width_m": 1.2,
  "pad_length_m": 1.2,
  "soil_capacity_kPa": 300
}
