import csv
import random

filename = "processes.csv"

# Create a CSV file if it doesn't already exist
try:
    with open(filename, 'x', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Process", "Arrival time", "Service time", "Disk I/O time (total)", "Disk I/O activity"])
except FileExistsError:
    pass

processes = []
total_service_time = 0
prev_arrival_time = 0  # initialize previous arrival time
while total_service_time < 600:
    process_id = len(processes) + 1
    service_time = random.randint(1, 12)
    disk_io_time = random.randint(0, 2)
    disk_io_activity = [random.randint(0, 7) for i in range(disk_io_time)] if disk_io_time > 0 else "na"
    
    # Generate a random arrival time that is no more than 5 units greater than the previous arrival time
    max_arrival_time = prev_arrival_time + 5
    arrival_time = random.randint(prev_arrival_time + 1, max_arrival_time)
    prev_arrival_time = arrival_time
    
    processes.append((process_id, arrival_time, service_time, disk_io_time, disk_io_activity))
    total_service_time += service_time

with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Process", "Arrival time", "Service time", "Disk I/O time (total)", "Disk I/O activity"])
    for process in processes:
        writer.writerow(process)
