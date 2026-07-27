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
