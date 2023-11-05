import numpy as np
from functions.assignments import assign_start, assign_lunch, assign_breaks
from functions.utils import create_schedule, calculate_shortfall, total_demand_week, verify_start_end


def tc_schedule_week(n_workers: int, demand_per_day: list, lunch_hours: float, work_hours: int):
    total_demand = total_demand_week(demand_per_day=demand_per_day)
    start_day_schedule, total_demand = assign_start(total_demand=total_demand,
                                                    n_workers=n_workers,
                                                    work_hours=work_hours,
                                                    lunch_hours=lunch_hours,
                                                    tc=True)
    lunch_schedule, total_demand = assign_lunch(total_demand=total_demand,
                                                n_workers=n_workers,
                                                lunch_hours=lunch_hours,
                                                start_day_schedule=start_day_schedule)
    general_schedule = create_schedule(start_day_schedule=start_day_schedule,
                                       lunch_schedule=lunch_schedule,
                                       demand=total_demand)
    schedule, total_demand = assign_breaks(start_day_schedule=start_day_schedule,
                                           lunch_schedule=lunch_schedule,
                                           demand=total_demand,
                                           schedule=general_schedule)
    start_of_day, end_of_day = verify_start_end(start_day_schedule=start_day_schedule,
                                                total_demand=total_demand,
                                                work_hours=work_hours,
                                                lunch_hours=lunch_hours)
    total_shortfall = 0
    for demand in demand_per_day:
        total_shortfall += calculate_shortfall(schedule,
                                               list(demand['demanda']))
    solution = {
        'schedule': schedule,
        'start_day_schedule': start_day_schedule,
        'total_demand': total_demand,
        'total_shortfall': total_shortfall,
        'start_of_day': start_of_day,
        'end_of_day': end_of_day
    }
    return solution


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
            start_day_schedule = np.concatenate(
                start_day_schedule, np.array(start_day))
    else:
        start_day_schedule = np.array(start_day)
    # Assign breaks
    # Create schedule
    return start_day_schedule
