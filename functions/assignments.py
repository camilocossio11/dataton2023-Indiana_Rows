# %%
import pandas as pd
import numpy as np
from functions.utils import verify_lunch
from numpy.lib.stride_tricks import sliding_window_view

# %%


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


def assign_start(
    total_demand: np.array,
    n_workers: int,
    work_hours: int,
    tc: bool,
    lunch_hours: float = 0
):
    if tc:
        work_stripes = int(work_hours * 4 + lunch_hours * 4)
    else:
        work_stripes = work_hours * 4
    start_schedule = []
    for _ in range(n_workers):
        windows = sliding_window_view(total_demand, work_stripes)
        assignment = np.array([5]*work_stripes)
        windows_with_assignment = windows - assignment
        neg_values = np.sum(windows_with_assignment < 0, axis=1)
        remaining_hours = np.sum(windows_with_assignment, axis=1)
        min_neg_vals_idx = np.where(neg_values == min(neg_values))[0]
        candidates = remaining_hours[min_neg_vals_idx]
        start_day_idx = np.where(candidates == min(candidates))[0][0]
        start_day = min_neg_vals_idx[start_day_idx]
        total_demand[start_day:start_day + work_stripes] -= 5
        start_schedule.append(start_day)
    start_schedule = np.sort(start_schedule)
    return [start_schedule, total_demand]


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


def assign_break_intersection(candidates_1: set, candidates_2: set, demand: np.array, start_day: int):
    intersection = list(map(lambda x: x + start_day,
                        list(candidates_1 & candidates_2)))
    index = list(demand[intersection]).index(min(list(demand[intersection])))
    return intersection[index]


def assign_break_no_intersection(
        candidates_1: set,
        candidates_2: set,
        demand: np.array,
        unavailable: set,
        switch: set,
        start_day: int
):
    breaks = []
    keys = list(candidates_1.union(candidates_2))
    values = demand[[list(map(lambda x: x + start_day, keys))]][0]
    aux = dict(zip(keys, values))
    ordered_dict = dict(sorted(aux.items(), key=lambda item: item[1]))
    candidates = list(ordered_dict.keys())
    current_min_index = 0
    i = 1
    while unavailable & switch != switch:
        if i >= len(candidates):
            current_min_index += 1
            i = current_min_index + 1
        else:
            aux = abs(candidates[i] - candidates[current_min_index])
            if (aux >= 5) and (aux <= 9):
                breaks += [candidates[current_min_index], candidates[i]]
                new_unavailable = set(list(range(candidates[i]-4, candidates[i]+5)))\
                    .union(set(list(range(candidates[current_min_index]-4, candidates[current_min_index]+5))))
                unavailable = unavailable.union(new_unavailable)
                current_min_index = i
                i = current_min_index + 1
            else:
                i += 1
    return breaks


def assign_breaks(start_day_schedule: list, lunch_schedule: list, demand: np.array, schedule: np.array):
    for i in range(len(start_day_schedule)):
        breaks = []
        aux = lunch_schedule[i]-start_day_schedule[i]
        # Find the slots that cannot change due to the condition that employees must
        # work minimum 1 hour (4 slots) at the beginning, at the end of the day,
        # before and after lunch.
        unavailable = set(
            list(range(0, 4)) +  # Beginning of the day
            list(range(aux-4, aux+10)) +  # Before, during and after lunch
            list(range(30, 34))  # End of the day
        )
        # Find the candidate stripes to be active pause at the beginning of the day and
        # exclude those that cannot change
        beginning_day = set(list(range(4, 9))) - unavailable
        # Find the candidate stripes to be active pause before the lunch and exclude
        # those that cannot change
        if aux - 9 >= 0:
            before_lunch = set(list(range(aux-9, aux-4))) - unavailable
        else:
            before_lunch = set(list(range(0, aux-4))) - unavailable
        # Find the candidate stripes to be active pause after the lunch and exclude
        # those that cannot change
        if aux + 15 <= 34:
            after_lunch = set(list(range(aux+10, aux+15))) - unavailable
        else:
            after_lunch = set(list(range(aux+10, 34))) - unavailable
        # Find the candidate stripes to be active pause at the end of the day and
        # exclude those that cannot change
        ending_day = set(list(range(25, 30))) - unavailable
        # Evaluate if there are common elements in beginning_day and before_lunch
        if beginning_day & before_lunch:
            brk = assign_break_intersection(
                beginning_day, before_lunch, demand, start_day_schedule[i])
            breaks = breaks + [brk]
        elif beginning_day.union(before_lunch):
            switch = set(
                list(range(0, lunch_schedule[i]-start_day_schedule[i])))
            brk = assign_break_no_intersection(beginning_day,
                                               before_lunch,
                                               demand,
                                               unavailable,
                                               switch,
                                               start_day_schedule[i])
            brk = list(map(lambda x: x + start_day_schedule[i], brk))
            breaks = breaks + brk
        # Evaluate if there are common elements in after_lunch and ending_day
        if after_lunch & ending_day:
            brk = assign_break_intersection(
                after_lunch, ending_day, demand, start_day_schedule[i])
            breaks = breaks + [brk]
        elif after_lunch.union(ending_day):
            switch = set(
                list(range(lunch_schedule[i]-start_day_schedule[i]+6, 34)))
            brk = assign_break_no_intersection(after_lunch,
                                               ending_day,
                                               demand,
                                               unavailable,
                                               switch,
                                               start_day_schedule[i])
            brk = list(map(lambda x: x + start_day_schedule[i], brk))
            breaks = breaks + brk
        schedule[i, breaks] = 2
        demand[breaks] = demand[breaks] + 1
    return [schedule, demand]
# %%
