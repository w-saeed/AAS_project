#==============================================================================
# imports
#==============================================================================
import pandas as pd
import joblib
import json
import os
from template_generator import TemplateGenerator
from json_generator import JsonGenerator
from state_merge import StateMerge
import subprocess


#==============================================================================
# helper functions
#==============================================================================
# Converte columns into string 
def format_dataframe_to_string(df):
    df = df.copy()
    # Convert datetime columns only if they are datetime dtype
    if pd.api.types.is_datetime64_any_dtype(df['start_time']):
        df['start_time'] = df['start_time'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    if pd.api.types.is_datetime64_any_dtype(df['end_time']):
        df['end_time'] = df['end_time'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    if not pd.api.types.is_string_dtype(df['record_count']):
        df['record_count'] = df['record_count'].astype(str)
    if not pd.api.types.is_string_dtype(df['sampling_interval']):
        df['sampling_interval'] = df['sampling_interval'].astype(str)
    return df


# Main business logic for formatting, generating JSON, and saving state
def process_and_save(result: pd.DataFrame, state_path: str, template_path: str, output_path: str, api_json_path: str):
    """Main business logic for formatting, generating JSON, and saving state."""
    result = format_dataframe_to_string(result)
    builder = TemplateGenerator(result)
    segments_json = builder.build_segments_json()
    modifier = JsonGenerator(template_path)
    modifier.append_segments(segments_json)
    modifier.save(output_path)
    joblib.dump(result.to_json(orient='records'), state_path)
    with open(api_json_path, 'w') as json_file:
        json.dump(segments_json, json_file, indent=4)




#==============================================================================
# main
#==============================================================================
def main():
    csv_file = 'data/sample_timeseries_sleep10ms.csv'
    # Read only the first 500 rows
    df = pd.read_csv(csv_file)
    print(df.head(500))

    df['timestamp'] = pd.to_datetime(df['timestamp_iso'])

    # Grouped stats function
    def sensor_stats(group):
        times = group['timestamp'].sort_values()
        deltas = times.diff().dt.total_seconds().dropna()
        return pd.Series({
            'record_count': len(group),
            'sampling_interval': deltas.median() if not deltas.empty else 0,
            'start_time': times.min(),
            'end_time': times.max()
        })

    # Get per-sensor stats
    result = df.groupby(['sensor_id', 'measurement_type']).apply(sensor_stats).reset_index()


    # converte this 3 columns into string 
    result['sampling_interval'] = result['sampling_interval'].astype(str)
    result['start_time'] = result['start_time'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    result['end_time'] = result['end_time'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    #==============================================================================
    # state
    #==============================================================================
    # File paths
    state_path = 'state.joblib'
    template_path = 'template.json'
    output_path = 'data/TimeSeriesDataInstance.json'
    api_json_path = 'api-json.json'

    try:
        if os.path.exists(state_path):
            print("State file exists.")
            state_json = joblib.load(state_path)
            merger = StateMerge(result)
            merged_result = merger.merge(state_json)
            process_and_save(merged_result, state_path, template_path, output_path, api_json_path)
            subprocess.run(['docker', 'restart', "REST-API"], check=True)
        else:
            print("State file does NOT exist.")
            process_and_save(result, state_path, template_path, output_path, api_json_path)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

