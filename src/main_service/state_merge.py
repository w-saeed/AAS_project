import pandas as pd
import json

class StateMerge:
    def __init__(self, result: pd.DataFrame):
        # Always work with a copy to avoid mutating the original DataFrame
        self.result = result.copy()
        if 'record_count' in self.result.columns:
            self.result['record_count'] = self.result['record_count'].astype(int)
    
    def merge(self, state_json: str) -> pd.DataFrame:
        """Merge previous state into the current result DataFrame."""
        state_list = json.loads(state_json)
        state_df = pd.DataFrame(state_list)
        state_df['record_count'] = state_df['record_count'].astype(int)
        
        # Merge or append
        for _, row in state_df.iterrows():
            # Here you can merge on more columns if you want (like measurement_type)
            sensor_id = row["sensor_id"]
            mask = self.result["sensor_id"] == sensor_id
            if mask.any():
                idx = self.result[mask].index[0]
                self.result.at[idx, "record_count"] += row["record_count"]
                self.result.at[idx, "sampling_interval"] = row["sampling_interval"]
            else:
                new_row = {
                    "sensor_id": row["sensor_id"],
                    "measurement_type": row["measurement_type"],
                    "record_count": row["record_count"],
                    "sampling_interval": row["sampling_interval"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"]
                }
                self.result = pd.concat([self.result, pd.DataFrame([new_row])], ignore_index=True)
        return self.result