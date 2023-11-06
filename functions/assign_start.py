import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def assign_start(
    total_demand: np.array,
    n_workers: int,
    work_hours: int,
    tc: bool,
    lunch_hours: float = 0,
    week: bool= True
):
    if tc and week:
        work_stripes = int(work_hours * 4 + lunch_hours * 4)
        assignment_fact = 5
    elif week:
        work_stripes = work_hours * 4
        assignment_fact = 5
    else:
        work_stripes = work_hours * 4
        assignment_fact = 1
    start_schedule = []
    for _ in range(n_workers):
        windows = sliding_window_view(total_demand, work_stripes)
        assignment = np.array([assignment_fact] * work_stripes)
        windows_with_assignment = windows - assignment
        neg_values = np.sum(windows_with_assignment < 0, axis=1)
        remaining_hours = np.sum(windows_with_assignment, axis=1)
        min_neg_vals_idx = np.where(neg_values == min(neg_values))[0]
        candidates = remaining_hours[min_neg_vals_idx]
        start_day_idx = np.where(candidates == min(candidates))[0][0]
        start_day = min_neg_vals_idx[start_day_idx]
        total_demand[start_day:start_day + work_stripes] -= assignment_fact
        start_schedule.append(start_day)
    start_schedule = np.sort(start_schedule)
    return [start_schedule, total_demand]