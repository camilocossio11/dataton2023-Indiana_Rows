# %% Loading libraries
import pandas as pd
import random
import numpy as np
import os
import time
from functions.load_data import DataReader
from functions.result_format import solution_format
from functions.load_data import sucursal_demand_data_separation, day_demand_data_separation
from functions.TC_schedule import tc_schedule_week, mt_schedule_week

# %%


def load_data(file_name: str):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    # Path to file
    path_to_file = os.path.join(current_folder, 'archive', file_name)
    data = DataReader(file_path=path_to_file).read_files()
    return data


def load_demand_data(data: dict, suc_code: int):
    demand_data = data['demand']
    suc_demand_data = sucursal_demand_data_separation(suc_code, demand_data)
    demand_per_day = day_demand_data_separation(suc_demand_data)
    return demand_per_day


def load_workers_data(data: dict, suc_code: int):
    workers_data = data['workers']
    n_tc_workers = workers_data[workers_data['suc_cod']
                                == suc_code]['contrato'].value_counts()['TC']
    n_mt_workers = workers_data[workers_data['suc_cod']
                                == suc_code]['contrato'].value_counts()['MT']
    return n_tc_workers, n_mt_workers


def initial_solution(suc_code: int, tc_work_hours: int, mt_work_hours: int, lunch_hours: float):
    # Folder where the script is located
    start = time.time()
    data = load_data(file_name='Dataton 2023 Etapa 2.xlsx')
    demand_per_day = load_demand_data(data=data, suc_code=suc_code)
    n_tc_workers, n_mt_workers = load_workers_data(data=data,
                                                   suc_code=suc_code)
    week_demand = demand_per_day[0:5]
    solution_tc = tc_schedule_week(n_workers=n_tc_workers,
                                   demand_per_day=week_demand,
                                   lunch_hours=lunch_hours,
                                   work_hours=tc_work_hours)
    start_day_schedule, total_demand = mt_schedule_week(total_demand=solution_tc['total_demand'],
                                                        work_hours=mt_work_hours,
                                                        n_workers=n_mt_workers,
                                                        solution_tc=solution_tc)
    end = time.time()
    time_execution = end - start
    return solution_tc, time_execution


# %%
if __name__ == '__main__':
    schedule, total_demand, total_shortfall, time_execution = initial_solution(
        suc_code=834, tc_work_hours=7, mt_work_hours=4, lunch_hours=1.5)
    # df_solution = solution_format(demand, workers, best_schedule)
    # df_solution.to_csv('solucion.csv',index=False)
# %%
