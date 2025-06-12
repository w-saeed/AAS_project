# Asset Administration Shell Project

This project automates the transformation of CSV data files into an Asset Administration Shell (AAS) models. It reads structured CSV files containing time series or asset-related data and converts them into standardized AAS submodels using the IDTA templates.

![save_last](https://github.com/user-attachments/assets/c53c6f6b-07d6-4942-b2c9-097576f08376)


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
