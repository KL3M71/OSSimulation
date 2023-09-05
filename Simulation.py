# Main Simulation, will simulate certain algorithm running 5 looped processes for 10 minutes
import csv
from process import Process
from fcfs import fcfs
from roundRobin import round_robin
from srt import srt
from hrrn import hrrn
from output import write_output_to_csv

# read input from CSV file
processes = []
with open('processes.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        pid = int(row['Process'])
        arrival_time = int(row['Arrival time'])
        service_time = int(row['Service time'])
        io_time = sum(int(x) for x in row['Disk I/O time (total)'].split(',') if x != 'na')
        io_activity_str = row['Disk I/O activity']
        if io_activity_str == 'na':
            io_activity = []
        else:
            if io_activity_str.startswith('[') or io_activity_str.endswith(']'):
                io_activity_str = io_activity_str.replace('[', '').replace(']', '')
            io_activity = [int(x) for x in io_activity_str.split(',') if x != '']
        processes.append(Process(pid, arrival_time, service_time, io_time, io_activity))



avg_finish_time = None
avg_response_time = None
avg_turn_around_time = None
avg_ratio_turn_around_service = None
avg_throughput = None

# Ask user for scheduling algorithm selection
print("Select a scheduling algorithm:")
print("1. First-Come, First-Served (FCFS)")
print("2. Round Robin (RR)")
print("3. Shortest Remaining Time (SRT)")
print("4. Highest Response Ratio Next (HRRN)")
selection = int(input("Enter your selection (1-4): "))

# Call the corresponding scheduling function based on user selection
if selection == 1:
    execution_order = fcfs(processes)
elif selection == 2:
    execution_order = round_robin(processes, 1)
elif selection == 3:
    execution_order = srt(processes)
elif selection == 4:
    completed_processes = hrrn(processes)
    total_time = completed_processes[-1].finish_time
    throughput = len(completed_processes) / total_time
    write_output_to_csv(completed_processes, throughput, 'hrrn_results.csv')
