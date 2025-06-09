# Asset Administration Shell Project

This project provides a simple pipeline to convert CSV time series data into a JSON structure. It uses Docker for containerized processing.

---

## Getting Started

## 1. Start the Services

Navigate to the `src` directory and run:

```bash
docker compose up -d
```

### Add new csv

1- Once the containers are up and running, place your CSV file inside the `data` directory at the root of the project.

2- Navigate to the `src/main_service` directory open file `main.py`

3- Change the file name

```bash
def main():
    csv_file = 'data/sample_timeseries_sleep10ms.csv'
    # Read only the first 500 rows
    df = pd.read_csv(csv_file)
    print(df.head(500))
```
4- Start the container `Builder`

5- The generated JSON file will be saved in Folder `data/TimeSeriesDataInstance.json`

## 2. REST API

### Swagger ui
```bash
http://localhost:8000/docs#/AAS
```
