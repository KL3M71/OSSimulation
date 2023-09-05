import csv

def round_robin(processes, time_slice):
    ready_queue = []
    io_queue = []
    current_process = None
    current_time = 0
    completed_processes = []

    while len(completed_processes) < len(processes):
        # add new jobs to the ready queue
        for p in processes:
            if p.arrival_time == current_time and p not in ready_queue and p not in io_queue:
                ready_queue.append(p)
                print(f"Time {current_time}: Process {p.pid} added to ready_queue")

        # handle disk io
        for p in io_queue[:]:
            p.remaining_io_time -= 1
            if p.remaining_io_time == 0:
                if p.remaining_io_activities:
                    p.remaining_time += p.remaining_io_activities.pop(0)
                io_queue.remove(p)
                if p not in ready_queue:
                    ready_queue.append(p)
                    
        # add current process back to ready queue if it has not finished
        if current_process is not None and current_process.remaining_time > 0:
            ready_queue.append(current_process)

        # process the next job in the ready queue
        if len(ready_queue) > 0:
            current_process = ready_queue.pop(0)
            print(f"Time {current_time}: Executing process {current_process.pid}")

            # if this is the first time this process is being executed, calculate its response time
            if current_process.start_time == -1:
                current_process.start_time = current_time
                current_process.response_time = current_time - current_process.arrival_time

            # execute process for one time slice
            time_executed = min(time_slice, current_process.remaining_time)
            current_process.remaining_time -= time_executed
            current_time += time_executed

            # check if the current process needs to perform I/O
            if current_process.io_time > 0 and current_process.remaining_time in current_process.io_activity:
                current_process.remaining_io_time = current_process.io_time
                io_queue.append(current_process)
                current_process = None
            # determine if process has completed or needs to be added to the I/O queue
            elif current_process.remaining_time == 0:
                current_process.finish_time = current_time
                current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                current_process.ratio = current_process.turnaround_time / current_process.service_time
                completed_processes.append(current_process)
                print(f"Time {current_time}: Process {current_process.pid} completed")
        else:
            if io_queue:
                min_io_time = min(p.remaining_io_time for p in io_queue)
                current_time += min_io_time
                for p in io_queue:
                    processes[p].remaining_io_time -= min_io_time
            else:
                current_time += 1


    # collect results
    response_times = [p.response_time for p in processes]
    finish_times = [p.finish_time for p in processes]
    turnaround_times = [p.turnaround_time for p in processes]
    ratios = [p.ratio for p in processes]

    # calculate throughput
    total_time = sum(turnaround_times)
    throughput = len(turnaround_times) / total_time if total_time > 0 else 0

    # write results to CSV
    with open("round_robin_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["PID", "Response Time", "Finish Time", "Turnaround Time", "Ratio", "Throughput"])
        for p in processes:
            writer.writerow([p.pid, p.response_time, p.finish_time, p.turnaround_time, p.ratio, throughput])

    print("All processes have completed.")
