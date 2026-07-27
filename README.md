# 🛡️ Platform Surveillance System

An automated, industrial-grade Python system surveillance tool designed for continuous system health auditing, resource tracking, active process scanning, and automated incident response via SMTP email alerts.

---

## 🌟 Key Features

* **Comprehensive System Auditing:**
  * **Microprocessor Metrics:** Captures active CPU cores and real-time CPU utilization percentage.
  * **Memory Tracking:** Monitors total available RAM and active usage percentage.
  * **Network Traffic:** Tracks total data transmitted (upload) and received (download) in Megabytes (MB).
* **Process Tracking:** Scans all active processes, logging Process ID (PID), Process Name, Username, Status, CPU percentage, and Memory usage.
* **Automated Scheduling:** Executes periodic scans based on user-specified time intervals using the `schedule` library.
* **Conditional SMTP Email Alerts:** Automatically emails the detailed surveillance `.log` file as an attachment using **SMTP SSL** whenever CPU usage exceeds a configurable threshold.

---

## 📋 Prerequisites & Installation

1. Ensure **Python 3.8+** is installed on your computer.
2. Install the required Python packages using your terminal or IDE package installer:
   ```bash
   pip install schedule
   pip install psutil

## ⚙️ Configuration Setup

# Defined CPU threshold for triggering email alerts
CPU_THRESHOLD = 80.0

def Send_Email(log_path, current_cpu):
    # Configure your credentials and recipient details
    sender_email = "your_email@gmail.com"
    sender_password = "your_16_digit_app_password"  # Google App Password
    receiver_email = "receiver_email@gmail.com"

 ## 🚀 Usage

 Run the script from your command prompt, terminal, or Python IDE (VS Code, PyCharm, IDLE) by supplying two positional arguments: execution interval (in minutes) and output directory name.

 python surveillance.py <Time_Interval_In_Minutes> <Log_Folder_Name>

 ## 📂 Project Structure

├── surveillance.py       # Main Python surveillance automation script
├── .gitignore            # Git rules to exclude temporary logs (*.log, __pycache__)
├── README.md             # Complete project documentation
└── MarvellousLogs/       # Folder created automatically to store generated .log files
    └── Marvellous_2026-07-27_07_44-17.log


 ## 📄 Output Log File Sample

 --------------------------------------------------
----Marvellous platform surveillance system----
Log file created at: 2026-07-27_07_44-17
--------------------------------------------------

--------System Report--------
Number of active CPU cores: 4
CPU Usage: 84.50 %
--------------------------------------------------
RAM Usage: 62.30 %
Total RAM Available: 17056432128
--------------------------------------------------
Network Usage Report
Sent : 142.50 MB
Received : 890.12 MB
--------------------------------------------------
PID:       1024
Name:      chrome.exe
User Name: SYSTEM
Status:    running
CPU usage: 12.40
RAM usage: 3.10
--------------------------------------------------
PID:       4812
Name:      python.exe
User Name: Administrator
Status:    running
CPU usage: 78.10
RAM usage: 1.80
--------------------------------------------------
----------------------End of log file----------------------
--------------------------------------------------


## 🛠️ Built With

Python 3
psutil - Cross-platform process and system monitoring module
schedule - Periodic job scheduling framework
smtplib / email - Built-in Python MIME email and SMTP client libraries
 
