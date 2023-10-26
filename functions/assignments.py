import random
import pandas as pd
import numpy as np

def assign_start(n_workers:int)->list:
    # Assign randomly te start hour
    start_day_schedule = []
    for i in range(n_workers):
        start_day_schedule.append(6-random.randint(-6,6))
    # To make sure that someone is available at the begining and the end of the day:
    if 0 not in start_day_schedule:
        index_min = start_day_schedule.index(min(start_day_schedule))
        start_day_schedule[index_min] = 0
    if 12 not in start_day_schedule:
        index_max = start_day_schedule.index(max(start_day_schedule))
        start_day_schedule[index_max] = 12
    return start_day_schedule

def assign_lunch(demand: pd.DataFrame,n_workers:int)->list:
    lunch_demand = demand[16:30].copy()
    # Movile window size (6 stripes = 1.5 hours)
    n = 6
    lunch_schedule = []
    for i in range(n_workers):
        # Compute the sume through moving windows
        lunch_demand['sumatoria_ventana'] = lunch_demand['demanda'][::-1].rolling(window=n).sum()
        lunch_demand['sumatoria_ventana'] = lunch_demand['sumatoria_ventana'][::-1]
        # Compute the start lunch
        start_lunch = lunch_demand['sumatoria_ventana'].idxmin()
        # Update the demand
        lunch_demand.loc[~lunch_demand.index.isin(range(start_lunch,start_lunch+n)),'demanda'] = lunch_demand.loc[~lunch_demand.index.isin(range(start_lunch,start_lunch+n)),'demanda'] - 1
        lunch_schedule.append(start_lunch)
    return lunch_schedule

def assign_break_intersection(candidates_1:set, candidates_2:set, demand:np.array, start_day:int):
    intersection = list(map(lambda x: x + start_day, list(candidates_1 & candidates_2)))
    index = list(demand[intersection]).index(min(list(demand[intersection])))
    return intersection[index]

def assign_break_no_intersection(
        candidates_1:set,
        candidates_2:set,
        demand:np.array,
        unavailable:set,
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
                breaks += [candidates[current_min_index],candidates[i]]
                new_unavailable = set(list(range(candidates[i]-4,candidates[i]+5)))\
                                .union(set(list(range(candidates[current_min_index]-4,candidates[current_min_index]+5))))
                unavailable = unavailable.union(new_unavailable)
                current_min_index = i
                i = current_min_index + 1
            else:
                i += 1
    return breaks

def assign_breaks(start_day_schedule:list, lunch_schedule:list, demand:np.array, schedule:np.array):
    for i in range(len(start_day_schedule)):
        breaks = []
        aux = lunch_schedule[i]-start_day_schedule[i]
        # Find the slots that cannot change due to the condition that employees must 
        # work minimum 1 hour (4 slots) at the beginning, at the end of the day, 
        # before and after lunch.
        unavailable = set(
                    list(range(0,4)) + # Beginning of the day
                    list(range(aux-4,aux+10)) + # Before, during and after lunch
                    list(range(30,34)) # End of the day
                    )
        # Find the candidate stripes to be active pause at the beginning of the day and 
        # exclude those that cannot change
        beginning_day = set(list(range(4,9))) - unavailable
        # Find the candidate stripes to be active pause before the lunch and exclude 
        # those that cannot change
        if aux - 9 >= 0:
            before_lunch = set(list(range(aux-9,aux-4))) - unavailable
        else:
            before_lunch = set(list(range(0,aux-4))) - unavailable
        # Find the candidate stripes to be active pause after the lunch and exclude 
        # those that cannot change
        if aux + 15 <= 34:
            after_lunch = set(list(range(aux+10,aux+15))) - unavailable
        else:
            after_lunch = set(list(range(aux+10,34))) - unavailable
        # Find the candidate stripes to be active pause at the end of the day and 
        # exclude those that cannot change
        ending_day = set(list(range(25,30))) - unavailable
        # Evaluate if there are common elements in beginning_day and before_lunch
        if beginning_day & before_lunch:
            brk = assign_break_intersection(beginning_day, before_lunch, demand, start_day_schedule[i])
            breaks = breaks + [brk]
        elif beginning_day.union(before_lunch):
            switch = set(list(range(0,lunch_schedule[i]-start_day_schedule[i])))
            brk = assign_break_no_intersection(beginning_day,
                                                before_lunch,
                                                demand,
                                                unavailable,
                                                switch,
                                                start_day_schedule[i])
            brk = list(map(lambda x: x + start_day_schedule[i], brk))
            breaks = breaks + brk
        else:
            pass
        # Evaluate if there are common elements in after_lunch and ending_day
        if after_lunch & ending_day:
            brk = assign_break_intersection(after_lunch, ending_day, demand, start_day_schedule[i])
            breaks = breaks + [brk]
        elif after_lunch.union(ending_day):
            switch = set(list(range(lunch_schedule[i]-start_day_schedule[i]+6,34)))
            brk = assign_break_no_intersection(after_lunch,
                                                ending_day,
                                                demand,
                                                unavailable,
                                                switch,
                                                start_day_schedule[i])
            breaks = breaks + brk
        else:
            pass
        schedule[i,breaks] = 2
        demand[breaks] = demand[breaks] + 1
    return schedule, demand