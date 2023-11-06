import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from functions.utils import verify_lunch

def fix_assign_lunch(
    total_demand: np.array,
    start_day_schedule: np.array,
    lunch_schedule: np.array,
    not_feasible_idx: np.array,
    lunch_stripes: int,
    max_end_lunch: int
):
    # Restaurar la demanda, dejarla como estaba sin la asignacion del almuerzo
    for idx in not_feasible_idx:
        str_lunch = lunch_schedule[idx]
        total_demand[str_lunch:str_lunch+lunch_stripes] -= 5
    # Reasignar en los factibles
    for idx in not_feasible_idx:
        min_start_lunch = start_day_schedule[idx] + 4
        candidates = list(range(min_start_lunch, max_end_lunch))
        lunch_windows = sliding_window_view(
            total_demand[min_start_lunch:max_end_lunch], lunch_stripes)
        sum_windows = np.sum(lunch_windows, axis=1)
        best_idx = np.where(sum_windows == min(sum_windows))[0][0]
        start_lunch = candidates[best_idx]
        lunch_schedule[idx] = start_lunch
        total_demand[start_lunch:start_lunch + lunch_stripes] += 5
    return [start_lunch, total_demand]

def assign_lunch(
    total_demand: pd.DataFrame,
    n_workers: int,
    lunch_hours: float,
    start_day_schedule: np.array,
    min_start_lunch: int = 16,  # Stripe corresponding 11:30
    max_start_lunch: int = 24  # Stripe corresponding 13:30
) -> list:
    lunch_stripes = int(lunch_hours * 4)
    candidates = list(range(min_start_lunch, max_start_lunch + 1))
    lunch_schedule = []
    max_end_lunch = max_start_lunch + lunch_stripes
    for _ in range(n_workers):
        lunch_windows = sliding_window_view(
            total_demand[min_start_lunch:max_end_lunch], lunch_stripes)
        sum_windows = np.sum(lunch_windows, axis=1)
        best_idx = np.where(sum_windows == min(sum_windows))[0][0]
        start_lunch = candidates[best_idx]
        lunch_schedule.append(start_lunch)
        total_demand[start_lunch:start_lunch + lunch_stripes] += 5
    lunch_schedule = np.sort(lunch_schedule)
    feasible, not_feasible_idx = verify_lunch(start_day_schedule=start_day_schedule,
                                              lunch_schedule=lunch_schedule)
    if not feasible:
        lunch_schedule, total_demand = fix_assign_lunch(total_demand=total_demand,
                                                        start_day_schedule=start_day_schedule,
                                                        lunch_schedule=lunch_schedule,
                                                        not_feasible_idx=not_feasible_idx,
                                                        lunch_stripes=lunch_stripes,
                                                        max_end_lunch=max_end_lunch)
    return [lunch_schedule, total_demand]