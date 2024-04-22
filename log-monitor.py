import os
import sys
import time
import signal
import subprocess

class LogMonitor:
    def __init__(self, log_file):
        self.log_file = log_file
        self.keywords = ["error", "warning", "critical"]  # Add more keywords as needed

    def tail_logs(self):
        try:
            with subprocess.Popen(["tail", "-F", self.log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as process:
                for line in process.stdout:
                    self.analyze_log(line)
        except KeyboardInterrupt:
            print("\nStopping log monitoring...")
            sys.exit(0)

    def analyze_log(self, log_entry):
        for keyword in self.keywords:
            if keyword in log_entry.lower():
                print(f"Found '{keyword}' in log: {log_entry.strip()}")

    def start_monitoring(self):
        print(f"Monitoring log file: {self.log_file}")
        self.tail_logs()

def signal_handler(sig, frame):
    print("\nCtrl+C detected. Exiting...")
    sys.exit(0)

def main():
    if len(sys.argv) != 2:
        print("Usage: python log_monitor.py <log_file_path>")
        sys.exit(1)

    log_file = sys.argv[1]
    if not os.path.isfile(log_file):
        print("Error: Log file does not exist.")
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)

    monitor = LogMonitor(log_file)
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
