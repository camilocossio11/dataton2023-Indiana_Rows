from functions.assign_start import assign_start
from functions.assign_lunch import assign_lunch
from functions.assign_breaks import assign_breaks, assign_breaks_mt
from functions.utils import create_schedule, total_demand_week, verify_start_end

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
                                        demand=total_demand,
                                        work_hours=work_hours,
                                        tc=True,
                                        week=True,
                                        lunch_schedule=lunch_schedule,
                                        lunch_hours=lunch_hours)
    schedule, total_demand = assign_breaks(start_day_schedule=start_day_schedule,
                                            lunch_schedule=lunch_schedule,
                                            demand=total_demand,
                                            schedule=general_schedule)
    start_of_day, end_of_day = verify_start_end(start_day_schedule=start_day_schedule,
                                                total_demand=total_demand,
                                                work_hours=work_hours,
                                                lunch_hours=lunch_hours)
    solution = {
        'schedule': schedule,
        'start_day_schedule': start_day_schedule,
        'total_demand': total_demand,
        'start_of_day': start_of_day,
        'end_of_day': end_of_day
    }
    return solution

def tc_schedule_weekend(n_workers: int, demand_saturday: list, work_hours: int):
    start_day_schedule, total_demand = assign_start(total_demand=demand_saturday,
                                                    n_workers=n_workers,
                                                    work_hours=work_hours,
                                                    tc=True,
                                                    week=False)
    general_schedule = create_schedule(start_day_schedule=start_day_schedule,
                                        demand=total_demand,
                                        work_hours=work_hours,
                                        tc=True,
                                        week=False)
    general_schedule, total_demand = assign_breaks_mt(start_day_schedule=start_day_schedule,
                                                        demand=total_demand,
                                                        schedule=general_schedule,
                                                        work_hours=work_hours,
                                                        week=False)
    start_of_day, end_of_day = verify_start_end(start_day_schedule=start_day_schedule,
                                                total_demand=total_demand,
                                                work_hours=work_hours,
                                                week=False)
    solution = {
        'schedule': general_schedule,
        'start_day_schedule': start_day_schedule,
        'total_demand': total_demand,
        'start_of_day': start_of_day,
        'end_of_day': end_of_day
    }
    return solution