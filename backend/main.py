from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Outrigger Pressure API")

# ---- Request model ----
class PressureRequest(BaseModel):
    crane_model: str
    counterweight_t: float
    outrigger_base: str
    radius_m: float
    slew_position: str
    pad_width_m: float
    pad_length_m: float
    soil_capacity_kPa: float


# ---- Response model ----
class PressureResponse(BaseModel):
    status: str
    governing_outrigger: str
    governing_load_t: float
    governing_load_kN: float
    bearing_area_m2: float
    ground_pressure_kPa: float
    utilisation_percent: float
    warnings: list[str]


@app.post("/calculate-pressure", response_model=PressureResponse)
def calculate_pressure(request: PressureRequest):
    """
    MOCK IMPLEMENTATION
    Real calculation will be added later
    """

    governing_load_t = 43.0
    governing_load_kN = governing_load_t * 9.81
    bearing_area = request.pad_width_m * request.pad_length_m
    ground_pressure = governing_load_kN / bearing_area
    utilisation = (ground_pressure / request.soil_capacity_kPa) * 100

    return {
        "status": "OK",
        "governing_outrigger": "FR",
        "governing_load_t": governing_load_t,
        "governing_load_kN": round(governing_load_kN, 1),
        "bearing_area_m2": round(bearing_area, 2),
        "ground_pressure_kPa": round(ground_pressure, 1),
        "utilisation_percent": round(utilisation, 1),
        "warnings": [
            "Mock response – real chart data not yet connected"
        ]
    }
