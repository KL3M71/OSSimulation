import csv

def write_output_to_csv(completed_processes, throughput, filename):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['PID', 'Finish Time', 'Response Time', 'Turnaround Time', 'TAT/ST Ratio', 'Throughput']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for process in completed_processes:
            turnaround_time = process.finish_time - process.arrival_time
            response_time = process.start_time - process.arrival_time
            tat_st_ratio = turnaround_time / process.service_time

            writer.writerow({
                'PID': process.pid,
                'Finish Time': process.finish_time,
                'Response Time': response_time,
                'Turnaround Time': turnaround_time,
                'TAT/ST Ratio': tat_st_ratio,
                'Throughput': throughput
            })
