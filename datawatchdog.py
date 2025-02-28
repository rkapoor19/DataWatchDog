import os
import json
import requests
import pandas as pd
from datetime import datetime

class DataWatchDog:
    def __init__(self, webhook_url, threshold=0.1, alert_channel="slack"):
        """Initialize DataWatchDog with webhook URL and alert threshold."""
        self.webhook_url = webhook_url
        self.threshold = threshold  # Tolerance for data changes
        self.alert_channel = alert_channel

    def check_data_drift(self, old_df, new_df):
        """Compare two datasets and detect changes in schema and statistics."""
        drift_report = {}
        
        # Check for schema changes
        old_columns, new_columns = set(old_df.columns), set(new_df.columns)
        added_cols, removed_cols = new_columns - old_columns, old_columns - new_columns
        if added_cols or removed_cols:
            drift_report["schema_changes"] = {
                "added_columns": list(added_cols),
                "removed_columns": list(removed_cols)
            }
        
        # Check for statistical drift
        num_cols = old_df.select_dtypes(include=["number"]).columns
        for col in num_cols:
            old_mean, new_mean = old_df[col].mean(), new_df[col].mean()
            drift = abs(new_mean - old_mean) / (old_mean + 1e-9)
            if drift > self.threshold:
                drift_report[col] = {
                    "old_mean": old_mean,
                    "new_mean": new_mean,
                    "drift_percentage": drift * 100
                }
        
        if drift_report:
            self.send_alert(drift_report)
        return drift_report

    def send_alert(self, message):
        """Send alert to Slack or Teams."""
        payload = {"text": f"🚨 DataWatchDog Alert: {json.dumps(message, indent=2)}"}
        headers = {"Content-Type": "application/json"}
        
        if self.webhook_url:
            requests.post(self.webhook_url, data=json.dumps(payload), headers=headers)
            print("Alert sent successfully!")
        else:
            print("Webhook URL not provided.")

# Example Usage
if __name__ == "__main__":
    # Sample datasets
    old_data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    new_data = pd.DataFrame({"A": [1, 2, 100], "B": [4, 5, 6], "C": [7, 8, 9]})
    
    # Initialize with Slack/Teams webhook
    watchdog = DataWatchDog(webhook_url="https://hooks.slack.com/services/your-webhook")
    drift_report = watchdog.check_data_drift(old_data, new_data)
    print("Drift Report:", drift_report)