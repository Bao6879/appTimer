# App Timer

A Python script that runs in the background to automatically track how much time you spend on different applications on your Windows PC. It generates detailed daily text reports and visual pie charts from the data.

Features
- Real-time Tracking: Monitors active window changes to accurately log application usage, refreshing every second.
- Persistent Logging: Saves all data to a CSV file, so no data is lost if the script restarts.
- Daily Reports: Automatically generates a summary text report every day at 23:30.
- Visual Analytics: Creates a clear pie chart visualization of your daily app usage.
- User Control: Shutdown the script and generate a final report by pressing F12.

## How It Works

1. The script uses the pywin32 library to query the Windows API for the currently active window and its process ID.
2. The psutil library then converts this PID into a clean application name.
3. A state machine tracks application focus changes, calculating the duration spent on each app before logging it to a CSV file.
4. The schedule library handles the daily report generation.

## Snippet of Output Example

Daily App Usage Report - 2025-09-02
===================================
Code.exe: 0h 12m 56s
vivaldi.exe: 0h 18m 50s
...
===================================
Total time spent: 10 apps: 0h 34m 34s

<img width="1127" height="659" alt="usage_pie_chart_2025-09-02" src="https://github.com/user-attachments/assets/15c774d4-4ce2-4ad2-be7e-f193198dec32" />

## How to run

Clone the repo and install the requirements:

```
git clone https://github.com/Bao6879/appTimer
cd appTimer
pip install -r requirements.txt
```
Then run main.py
You should edit the cwd variable in the script to let it know where to put log files, reports, and pie charts.

## License

This project is licensed under the MIT License.
