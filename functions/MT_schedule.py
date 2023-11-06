import numpy as np
from functions.assignments import assign_start, assign_breaks_mt
from functions.utils import create_schedule

def mt_schedule_week(total_demand: np.array, work_hours: int, n_workers: int, solution_tc: dict):
    start_day = []
    if (not solution_tc['start_of_day']) and (n_workers > 1):
        start_day.append(0)
        total_demand[0:work_hours * 4] -= 5
        n_workers -= 1
    if (not solution_tc['end_of_day']) and (n_workers > 1):
        end_day = len(total_demand) - int(work_hours * 4)
        start_day.append(end_day)
        total_demand[end_day:end_day + int(work_hours * 4)] -= 5
        n_workers -= 1
    if n_workers > 0:
        start_day_schedule, total_demand = assign_start(total_demand=total_demand,
                                                        n_workers=n_workers,
                                                        work_hours=work_hours,
                                                        tc=False)
        if start_day:
            start_day_schedule = np.concatenate((start_day_schedule, np.array(start_day)))
    else:
        start_day_schedule = np.array(start_day)
    general_schedule = create_schedule(start_day_schedule=start_day_schedule,
                               demand=total_demand,
                               work_hours=work_hours,
                               tc=False,
                               week=True)
    general_schedule, total_demand = assign_breaks_mt(start_day_schedule=start_day_schedule,
                                                        demand=total_demand,
                                                        schedule=general_schedule,
                                                        work_hours=work_hours)
    solution = {
        'schedule': general_schedule,
        'start_day_schedule': start_day_schedule,
        'total_demand': total_demand
    }
    return solution
