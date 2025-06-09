from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

app = FastAPI(title="AAS Time Series API", version="1.0.0")

# Load sensor submodels from file at startup
DATA_FILE = Path("api-json.json")
with open(DATA_FILE, "r") as f:
    SENSORS = json.load(f)

def get_sensor_by_id(idShort: str):
    for sensor in SENSORS:
        if sensor["idShort"] == idShort:
            return sensor
    return None

@app.get("/api/v1/aas/assetid/submodels/time-series", tags=["AAS"])
def get_time_series_submodel():
    """
    Get all sensors (time-series submodel) for asset_123.
    """
    return SENSORS

@app.get("/api/v1/aas/assetid/submodels/time-series/{sensor_id}", tags=["AAS"])
def get_sensor(sensor_id: str):
    """
    Get a single sensor by idShort (sensor_id) for asset_123.
    """
    sensor = get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@app.get("/api/v1/aas/assetid/submodels/time-series/{sensor_id}/min", tags=["AAS"])
def get_sensor_min(sensor_id: str):
    """
    Get a minimal sensor representation: idShort and its property values.
    """
    sensor = get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    # Create a values dict from the sensor's "value" array
    values = {}
    for entry in sensor["value"]:
        # Handle MultiLanguageProperty (use first language if available)
        if entry.get("modelType") == "MultiLanguageProperty" and "value" in entry:
            val = entry["value"][0]["text"] if entry["value"] else None
        else:
            val = entry.get("value")
        values[entry["idShort"]] = val
    return {"idShort": sensor["idShort"], "values": values}