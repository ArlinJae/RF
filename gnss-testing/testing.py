import os
import subprocess
import time
import psutil
from datetime import datetime

# Paths
gps_sdr_sim_path = "./gps-sdr-sim"
gnss_sdr_path = "gnss-sdr"
config_file = "gnss-sdr.conf"
rinex_file = "brdc3540.14n"
output_bin = "gpssim.bin"
log_file = "gnss-sdr.log"
orbital_motion_file = "orbital_motion.csv"

def generate_orbital_gps_signal():
    print("Generating orbital GPS signal...")
    cmd = f"{gps_sdr_sim_path} -e {rinex_file} -u {orbital_motion_file} -o {output_bin}"
    subprocess.run(cmd, shell=True, check=True)
    print("Orbital GPS signal generated.")

def run_gnss_sdr():
    print("Running GNSS-SDR...")
    cmd = f"{gnss_sdr_path} --config_file={config_file} > {log_file} 2>&1"
    start_time = time.time()
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cpu_usage_log = log_cpu_usage(process)
    process.wait()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"GNSS-SDR run completed in {elapsed_time:.2f} seconds.")
    return elapsed_time, cpu_usage_log

def measure_performance():
    print("Measuring performance...")
    cmd = f"/usr/bin/time -v {gnss_sdr_path} --config_file={config_file} > {log_file} 2>&1"
    result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)
    memory_usage = parse_memory_usage(result.stderr)
    print("Performance measurement completed.")
    return memory_usage

def parse_memory_usage(stderr_output):
    for line in stderr_output.split('\n'):
        if "Maximum resident set size" in line:
            return int(line.split(":")[1].strip())
    return 0

def log_cpu_usage(process):
    print("Logging CPU usage...")
    cpu_usage_log = []
    try:
        while process.poll() is None:
            cpu_usage_log.append(psutil.cpu_percent(interval=1))
    except psutil.NoSuchProcess:
        pass
    print("CPU usage logging completed.")
    return cpu_usage_log

def analyze_logs():
    print("Analyzing logs...")
    acquisition_count = 0
    tracking_count = 0
    with open(log_file, 'r') as file:
        for line in file:
            if "Acquisition" in line:
                acquisition_count += 1
            elif "Tracking" in line:
                tracking_count += 1
    print(f"Found {acquisition_count} acquisition messages and {tracking_count} tracking messages in logs.")
    return acquisition_count, tracking_count

if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Test started at {start_time}")

    generate_orbital_gps_signal()

    memory_usage = measure_performance()
    elapsed_time, cpu_usage_log = run_gnss_sdr()
    
    acquisition_count, tracking_count = analyze_logs()

    end_time = datetime.now()
    print(f"Test completed at {end_time}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Memory usage: {memory_usage} KB")
    print(f"Acquisitions: {acquisition_count}")
    print(f"Trackings: {tracking_count}")
    print(f"CPU usage log: {cpu_usage_log}")

    total_test_time = end_time - start_time
    print(f"Total test duration: {total_test_time}")

    print("Comprehensive orbital performance testing completed.")
