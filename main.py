import time
from datetime import datetime, date
import csv
import matplotlib.pyplot as plt
import psutil
import win32process
import win32gui
import schedule
import keyboard
import pandas as pd
def get_active_window_pid():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        return pid
    except Exception as e:
        print(f"Error getting PID: {e}")
        return None
LOG_FILE = "D:/CV/AppTimer/log.csv"
try:
    with open(LOG_FILE, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Start Time", "End Time", "Duration", "App Name"])
except FileExistsError:
    pass
def generate_report():
    df = pd.read_csv(LOG_FILE, parse_dates=['Start Time', 'End Time'])
    today = date.today()
    todays_data = df[df['Start Time'].dt.date == today]

    summary = todays_data.groupby('App Name')['Duration'].sum()

    report_filename = f"D:/CV/AppTimer/usage_report_{today.strftime('%Y-%m-%d')}.txt"
    with open(report_filename, 'w') as f:
        f.write(f"Daily App Usage Report - {today}\n")
        f.write("===================================\n")
        totalTime=0
        totalApps=0
        for app, total_seconds in summary.items():
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = (total_seconds % 3600) % 60
            totalTime+=total_seconds
            totalApps+=1
            f.write(f"{app}: {hours}h {minutes}m {seconds}s\n")
        f.write("===================================\n")
        totalHours=totalTime//3600
        totalMinutes=(totalTime%3600)//60
        totalSeconds=(totalTime%3600)%60
        f.write(f"Total time spent: {totalApps} apps: {totalHours}h {totalMinutes}m {totalSeconds}s\n")
    print(f"Report saved to {report_filename}")

    if summary.empty:
        print("No data to plot for today.")
        return
    threshold = 300

    significant_usage = summary[summary >= threshold]
    other_usage = summary[summary < threshold].sum()

    if other_usage > 0:
        significant_usage['Other'] = other_usage        

    labels = significant_usage.index.tolist()
    sizes = significant_usage.values.tolist()

    fig, ax = plt.subplots(figsize=(12, 8)) 

    wedges, texts = ax.pie(sizes, startangle=90)

    legend_labels = [f'{l} ({s/3600:.1f}h)' for l, s in zip(labels, sizes)]
    ax.legend(wedges, legend_labels, title="Applications", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    ax.axis('equal')  
    plt.title(f'App Usage Time - {today}', weight='bold', size=14)
    
    chart_filename = f"D:/CV/AppTimer/usage_pie_chart_{today.strftime('%Y-%m-%d')}.png"
    plt.savefig(chart_filename, dpi=100, bbox_inches='tight')
    plt.close()

    print(f"Pie chart saved to {chart_filename}")

previousApp=None
startTime=datetime.now()

schedule.every().day.at("23:30").do(generate_report)
while True:
    schedule.run_pending()
    activePid = get_active_window_pid()
    if activePid>0:
        try:
            processName = psutil.Process(activePid).name()
        except psutil.NoSuchProcess:
            processName = "Nonexistent"
        except psutil.AccessDenied:
            processName = "Nonexistent"
        if previousApp==None:
            previousApp=processName
    else:
        processName = "None"

    if processName!=previousApp:
        if previousApp is not None:
            endTime = datetime.now()
            duration = endTime - startTime
            durationSeconds = int(duration.total_seconds())

            with open(LOG_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([startTime.isoformat(), endTime.isoformat(), durationSeconds, previousApp])
            
            previousApp=processName
            startTime=datetime.now()
    if keyboard.is_pressed('f12'):
        endTime = datetime.now()
        duration = endTime - startTime
        durationSeconds = int(duration.total_seconds())
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([startTime.isoformat(), endTime.isoformat(), durationSeconds, processName])
        generate_report()
        break
    time.sleep(1)