#%% Loading libraries
import pandas as pd
import random
import numpy as np
import os
from load_data import DataReader

#%%
def assign_start(n_workers:int)->list:
    # Assign randomly te start hour
    start_day_schedule = []
    for i in range(n_workers):
        start_day_schedule.append(4-random.randint(-4,4))
    # To make sure that someone is available at the begining and the end of the day:
    if 0 not in start_day_schedule:
        index_min = start_day_schedule.index(min(start_day_schedule))
        start_day_schedule[index_min] = 0
    if 8 not in start_day_schedule:
        index_max = start_day_schedule.index(max(start_day_schedule))
        start_day_schedule[index_max] = 8
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

def create_schedule(start_day_schedule:list, lunch_schedule:list, demand:pd.DataFrame):
    n_workers = len(start_day_schedule)
    schedule = np.zeros((n_workers,len(demand)))
    for i in range(n_workers):
        schedule[i,start_day_schedule[i]:lunch_schedule[i]] = 1
        schedule[i,lunch_schedule[i]:lunch_schedule[i]+6] = 3
        schedule[i,lunch_schedule[i]+6:start_day_schedule[i]+38] = 1
    return schedule

def update_demand(demand:np.array, schedule:np.array):
    return demand - np.sum(schedule.T == 1, axis=1)

def assign_break_intersection(candidates_1:set, candidates_2:set, demand:np.array, start_day:int):
    intersection = list(map(lambda x: x + start_day, list(candidates_1 & candidates_2)))
    index = list(demand[intersection]).index(min(list(demand[intersection])))
    return intersection[index]

def assign_break_no_intersection(
        candidates_1:set,
        candidates_2:set,
        demand:np.array,
        unavailable:set,
        before_lunch:bool,
        start_lunch:int,
        start_day:int
        ):
    if before_lunch:
        switch = set(list(range(0,start_lunch-start_day)))
    else:
        switch = set(list(range(start_lunch-start_day+6,38)))
    breaks = []
    keys = list(candidates_1.union(candidates_2))
    values = demand[[list(map(lambda x: x + start_day, keys))]][0]
    aux = dict(zip(keys, values))
    ordered_dict = dict(sorted(aux.items(), key=lambda item: item[1]))
    candidates = list(ordered_dict.keys())
    breaks.append(candidates[0])
    unavailable = unavailable.union(set(list(range(candidates[0]-4,candidates[0]+5))))
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
                    list(range(34,38)) # End of the day
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
        if aux + 15 <= 38:
            after_lunch = set(list(range(aux+10,aux+15))) - unavailable
        else:
            after_lunch = set(list(range(aux+10,38))) - unavailable
        # Find the candidate stripes to be active pause at the end of the day and 
        # exclude those that cannot change
        ending_day = set(list(range(29,34))) - unavailable
        # Evaluate if there are common elements in beginning_day and before_lunch
        if beginning_day & before_lunch:
            brk = assign_break_intersection(beginning_day, before_lunch, demand, start_day_schedule[i])
            breaks = breaks + [brk]
        elif beginning_day.union(before_lunch):
            brk = assign_break_no_intersection(beginning_day,
                                                before_lunch,
                                                demand,
                                                unavailable,
                                                True,
                                                lunch_schedule[i],
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
            brk = assign_break_no_intersection(after_lunch,
                                                ending_day,
                                                demand,
                                                unavailable,
                                                False,
                                                lunch_schedule[i],
                                                start_day_schedule[i])
            breaks = breaks + brk
        else:
            pass
        schedule[i,breaks] = 2
        demand[breaks] = demand[breaks] + 1
    return schedule, demand

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

def main():
    # Folder where the script is located
    current_folder = os.path.dirname(os.path.abspath(__file__))
    # Path to file
    path_to_file = os.path.join(current_folder, 'archive', 'Dataton 2023 Etapa 1.xlsx')
    data = DataReader(file_path = path_to_file).read_files()
    original_demand = data['demand']
    workers =  data['workers']
    n_workers = 8
    best_schedule = None
    best_result = 1000000
    for i in range(10000):
        # print(i)
        schedule = pd.DataFrame()
        start_day_schedule = assign_start(n_workers)
        # start_day_schedule[0] = 1
        # start_day_schedule = [3,8,0,2,1,4,6,5]
        lunch_schedule = assign_lunch(original_demand, n_workers)
        lunch_schedule[0] = 24
        schedule = create_schedule(start_day_schedule,lunch_schedule,original_demand)
        demand = update_demand(np.array(original_demand['demanda']),schedule)
        schedule, demand = assign_breaks(start_day_schedule,lunch_schedule,demand,schedule)
        total_shortfall = calculate_shortfall(schedule,list(original_demand['demanda']))
        if total_shortfall < best_result:
            best_schedule = schedule
            best_result = total_shortfall
    return best_schedule,best_result

# %%
if __name__=='__main__':
    best_schedule,best_result= main()
# %%
