import pandas as pd
import numpy as np

def create_schedule(start_day_schedule:list, lunch_schedule:list, demand:pd.DataFrame):
    n_workers = len(start_day_schedule)
    schedule = np.zeros((n_workers,len(demand)))
    for i in range(n_workers):
        schedule[i,start_day_schedule[i]:lunch_schedule[i]] = 1
        schedule[i,lunch_schedule[i]:lunch_schedule[i]+6] = 3
        schedule[i,lunch_schedule[i]+6:start_day_schedule[i]+34] = 1
    return schedule

def update_demand(demand:np.array, schedule:np.array):
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
    assert matrix.shape[1] == len(demand), "Mismatch between matrix columns and demand vector length."
    # Calculate the number of workers working at each moment of time
    workers_working = (matrix == 1).sum(axis=0)  # Sum across rows for each column
    # Calculate the difference between demand and workers working
    difference = demand - workers_working
    # Sum only the positive differences
    total_shortfall = difference[difference > 0].sum()
    return total_shortfall