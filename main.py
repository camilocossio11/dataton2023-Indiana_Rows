#%%
import pandas as pd
import time
from initial_solutions import initial_solution

#%%
def main(tc_work_hours:dict, mt_work_hours:dict, suc_codes:list, lunch_hours:float, export:bool = False):
    start = time.time()
    solutions_week = []
    solutions_weekend = []
    initial_solutions = []
    total_shortfall = 0
    for suc in suc_codes:
        solution_week,solution_weekend,initial_solution_formated = initial_solution(suc_code=suc,
                                                                                    tc_work_hours=tc_work_hours,
                                                                                    mt_work_hours=mt_work_hours,
                                                                                    lunch_hours=lunch_hours)
        solutions_week.append(solution_week)
        solutions_weekend.append(solution_week)
        initial_solutions.append(initial_solution_formated)
        total_shortfall += solution_week['total_shortfall'] + solution_weekend['total_shortfall']
    solution = pd.concat(initial_solutions, ignore_index=True)
    end = time.time()
    time_execution = end - start
    if export:
        solution.to_csv('solucion.csv',index=False)
    return solution, total_shortfall, time_execution

#%%
if __name__ == '__main__':
    tc_work_hours = {
        'week':7,
        'weekend':5
    }
    mt_work_hours = {
        'week':4,
        'weekend':4
    }
    suc_codes = [60,311,487,569,834]
    lunch_hours = 1.5
    solution, total_shortfall, time_execution = main(tc_work_hours=tc_work_hours,
                                                    mt_work_hours=mt_work_hours,
                                                    suc_codes=suc_codes,
                                                    lunch_hours=lunch_hours,
                                                    export=True)
# %%
