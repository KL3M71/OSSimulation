import csv

def srt(processes):
    # Initialize variables
    current_time = 0
    finish_times = [0] * len(processes)
    response_times = [0] * len(processes)
    turnaround_times = [0] * len(processes)
    ratios = [0] * len(processes)
    ready_queue = []
    io_queue = []

    # Helper function to find the process with the shortest remaining time
    def find_shortest_remaining_time(ready_queue):
        return min(ready_queue, key=lambda x: processes[x].remaining_time)

    # Main loop
    while sum([p.remaining_time for p in processes]) > 0 or ready_queue or io_queue:
        # Add arrived processes to the ready queue
        for i, p in enumerate(processes):
            if p.arrival_time == current_time and i not in ready_queue and i not in io_queue:
                ready_queue.append(i)

        # Handle Disk I/O
        for i in io_queue[:]:
            processes[i].remaining_io_time -= 1
            if processes[i].remaining_io_time == 0:
                if processes[i].remaining_io_activities:
                    processes[i].remaining_time += processes[i].remaining_io_activities.pop(0)
                io_queue.remove(i)
                if i not in ready_queue:
                    ready_queue.append(i)

        # Run the process with the shortest remaining time
        if ready_queue:
            current_process = find_shortest_remaining_time(ready_queue)
            ready_queue.remove(current_process)

            # Calculate response time
            if response_times[current_process] == 0:
                response_times[current_process] = current_time - processes[current_process].arrival_time

            # Execute process for one unit of time
            time_executed = min(1, processes[current_process].remaining_time)
            processes[current_process].remaining_time -= time_executed
            current_time += time_executed

            # Check if the current process needs to perform I/O
            if processes[current_process].io_time > 0 and processes[current_process].remaining_time in processes[current_process].io_activity:
                processes[current_process].remaining_io_time = processes[current_process].io_time
                io_queue.append(current_process)
            # If the process has not completed and is not going to the I/O queue, add it back to the ready queue
            elif processes[current_process].remaining_time > 0:
                ready_queue.append(current_process)
            # Check if the current process has finished
            else:
                finish_times[current_process] = current_time
                turnaround_times[current_process] = current_time - processes[current_process].arrival_time
                ratios[current_process] = turnaround_times[current_process] / processes[current_process].service_time

        else:
            if io_queue:
                min_io_time = min(processes[p].remaining_io_time for p in io_queue)
                current_time += min_io_time
                for p in io_queue:
                    processes[p].remaining_io_time -= min_io_time
            else:
                current_time += 1


    # Calculate throughput
    total_service_time = sum([p.service_time for p in processes])
    throughput = len(processes) / total_service_time

    # Write results to a CSV file
    with open('srt_results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Process', 'Finish Time', 'Response Time', 'Turnaround Time', 'Ratio', 'Throughput'])
        for i, p in enumerate(processes):
            writer.writerow([p.pid, finish_times[i], response_times[i], turnaround_times[i], ratios[i], throughput])