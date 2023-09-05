import csv

def fcfs(processes):
    processes.sort(key=lambda p: p.arrival_time) # sort processes by arrival time
    current_time = processes[0].arrival_time # start at the arrival time of the first process
    finish_times = []
    response_times = []
    turnaround_times = []
    ratios = []
    disk_io_history = []

    # Calculate finish time, response time, turnaround time, and ratio for each process
    for p in processes:
        # Determine disk io times and add to disk io history
        disk_io_times = []
        if p.io_time > 0:
            disk_io_times = p.io_activity
        disk_io_history.append(disk_io_times)

        # Process Disk I/O (if any)
        while disk_io_times and current_time == disk_io_times[0]:
            current_time += p.io_time
            disk_io_times.pop(0)

        # Calculate finish time
        finish_time = current_time + p.service_time # Finish time is current time + service time
        finish_times.append(finish_time)

        # Calculate response time
        response_time = current_time - p.arrival_time # Response time is current time - arrival time
        response_times.append(response_time)

        # Calculate turnaround time
        turnaround_time = finish_time - p.arrival_time # Turnaround time is finish time - arrival time
        turnaround_times.append(turnaround_time)

        # Calculate ratio
        ratio = turnaround_time / p.service_time # Ratio is turnaround time / service time
        ratios.append(ratio)

        # Update current time to finish time
        current_time = finish_time

    # Calculate throughput
    total_service_time = sum([p.service_time for p in processes])
    throughput = len(processes) / total_service_time

    # Write the results to a CSV file
    with open('fcfs_results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Process', 'Finish Time', 'Response Time', 'Turnaround Time', 'Ratio', 'Throughput'])
        for i, p in enumerate(processes):
            writer.writerow([p.pid, finish_times[i], response_times[i], turnaround_times[i], ratios[i], throughput])
