#%%
import numpy as np
from functions.TC_schedule import TC_schedule
from functions.utils import calculate_shortfall
from functions.assignments import assign_breaks
from functions.utils import update_demand

def search_best_schedule_per_day(demand_per_day, n_workers_TC):
    solutions = []
    for i in range(len(demand_per_day)):
        solution = TC_schedule(n_workers_TC,demand_per_day[i].reset_index(drop=True),5_000)
        solutions.append(solution)
    return solutions

def search_best_schedule(demand_per_day, n_workers_TC):
    solutions = search_best_schedule_per_day(demand_per_day, n_workers_TC)
    total_shortfalls = []
    for solution in solutions:
        shortfall = 0
        for demand in demand_per_day:
            shortfall += calculate_shortfall(solution['schedule'], list(demand['demanda']))
        total_shortfalls.append(shortfall)
    best_index = total_shortfalls.index(min(total_shortfalls))
    return solutions[best_index], total_shortfalls

def final_solution_per_day_TC(demand_per_day, n_workers_TC):
    best_solution, total_shortfalls = search_best_schedule(demand_per_day, n_workers_TC)
    solution_per_day = []
    final_demands = []
    total_shortfall = 0
    for demand in demand_per_day:
        demand_updated = update_demand(np.array(demand['demanda']),best_solution['schedule'])
        solution, f_demand = assign_breaks(best_solution['start_day_schedule'], best_solution['lunch_schedule'], demand_updated, best_solution['schedule'].copy())
        total_shortfall += calculate_shortfall(solution,list(demand['demanda']))
        solution_per_day.append(solution)
        final_demands.append(f_demand)
    return solution_per_day, total_shortfall, final_demands

