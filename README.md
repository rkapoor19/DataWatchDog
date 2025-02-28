# DataWatchDog 🐶  
A lightweight monitoring tool for dataset changes and transformations in production jobs. It alerts on Slack or Microsoft Teams when anomalies are detected.  

## Features  
✔ Detects schema changes (added/removed columns)  
✔ Identifies statistical data drift  
✔ Sends real-time alerts to Slack or Teams  

## Installation  
```bash
pip install -r requirements.txt
from datawatchdog import DataWatchDog
import pandas as pd

old_data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
new_data = pd.DataFrame({"A": [1, 2, 100], "B": [4, 5, 6], "C": [7, 8, 9]})

watchdog = DataWatchDog(webhook_url="YOUR_SLACK_OR_TEAMS_WEBHOOK")
watchdog.check_data_drift(old_data, new_data)
## **🔹 Step 6: Push Your Code to GitHub**
Now, push everything to GitHub:  
```bash
git add .
git commit -m "Initial commit: DataWatchDog open-source release"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/DataWatchDog.git
git push -u origin main
