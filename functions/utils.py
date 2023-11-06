import pandas as pd
import numpy as np


def create_schedule(
        start_day_schedule: list,
        demand: np.array,
        work_hours: int,
        tc: bool,
        week: bool,
        lunch_schedule: list = None,
        lunch_hours: float = 0):
    n_workers = len(start_day_schedule)
    schedule = np.zeros((n_workers, len(demand)))
    if week and tc:
        work_stripes = int(work_hours * 4)
        lunch_stripes = int(lunch_hours * 4)
        total_stripes = work_stripes + lunch_stripes
        for i in range(n_workers):
            schedule[i, start_day_schedule[i]:lunch_schedule[i]] = 1
            schedule[i, lunch_schedule[i]:lunch_schedule[i] + lunch_stripes] = 3
            schedule[i, lunch_schedule[i] + lunch_stripes:start_day_schedule[i]+total_stripes] = 1
    else:
        total_stripes = int(work_hours * 4)
        for i in range(n_workers):
            schedule[i, start_day_schedule[i]:start_day_schedule[i]+total_stripes] = 1
    return schedule


def update_demand(demand: np.array, schedule: np.array):
    return demand - np.sum(schedule.T == 1, axis=1)


def calculate_shortfall(matrix, demand):
    """
    Calculate the shortfall based on the difference between demand and workers working.

    Parameters:
    - matrix (numpy.ndarray): Matrix representing workers and time. 1s indicate working, 0s resting, and 3s lunch.
    - demand (list or numpy.ndarray): Vector of company's demand.

    Returns:
    - int: Total shortfall.
    """
    # Ensure that the demand vector length matches the number of columns in the matrix
    assert matrix.shape[1] == len(
        demand), "Mismatch between matrix columns and demand vector length."
    # Calculate the number of workers working at each moment of time
    # Sum across rows for each column
    workers_working = (matrix == 1).sum(axis=0)
    # Calculate the difference between demand and workers working
    difference = demand - workers_working
    # Sum only the positive differences
    total_shortfall = difference[difference > 0].sum()
    return total_shortfall


def total_demand_week(demand_per_day: list) -> np.array:
    # Take the column 'demanda' of each daily demand, from monday to friday and store it
    # in demands list
    demands = [demand['demanda'].tolist() for demand in demand_per_day]
    # Array containing the total demand per stripe (from monday to friday)
    week_total_demand = np.array([sum(x) for x in zip(*demands)])
    return week_total_demand


def verify_lunch(start_day_schedule: np.array, lunch_schedule: np.array):
    dif = lunch_schedule - start_day_schedule
    not_feasible_idx = np.where(dif < 4)[0]
    if not_feasible_idx.size == 0:
        feasible = True
    else:
        feasible = False
    return feasible, not_feasible_idx


def verify_start_end(
        start_day_schedule: np.array,
        total_demand: np.array,
        work_hours: int,
        lunch_hours: float):
    max_start_day = len(total_demand) - int(work_hours * 4 + lunch_hours * 4)
    start_of_day = True if 0 in start_day_schedule else False
    end_of_day = True if max_start_day in start_day_schedule else False
    return start_of_day, end_of_day
