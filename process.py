class Process:
    def __init__(self, pid, arrival_time, service_time, io_time, io_activity):
        self.pid = pid
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.io_time = io_time
        if isinstance(io_activity, list):
            self.io_activity = io_activity
        elif io_activity.strip():  # check if io_activity is not an empty string
            self.io_activity = [int(x) for x in io_activity.split(
                ",")] if "," in io_activity else [int(io_activity)]
        else:
            self.io_activity = []  # set to empty list if io_activity is empty string
        self.remaining_time = service_time
        self.remaining_io_time = io_time
        self.remaining_io_activities = self.io_activity.copy()
        self.response_time = -1
        self.finish_time = -1
        self.turnaround_time = -1
        self.ratio = -1
        self.start_time = -1

        
    def __str__(self):
        return f"PID: {self.pid} | Arrival Time: {self.arrival_time} | Service Time: {self.service_time} | I/O Time: {self.io_time} | I/O Activity: {self.io_activity} | Start Time: {self.start_time} | Completion Time: {self.completion_time} | Response Time: {self.response_time}"

    def response_ratio(self, current_time):
        waiting_time = current_time - self.arrival_time
        return 1 + (waiting_time / self.service_time)
