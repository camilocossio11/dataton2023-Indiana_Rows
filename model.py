# %% Loading libraries
import pandas as pd
import random
import numpy as np
import os
import time
from functions.load_data import DataReader
from functions.result_format import solution_format
from functions.load_data import sucursal_demand_data_separation, day_demand_data_separation
from functions.TC_schedule import tc_schedule_week

# %%


def main():
    # Folder where the script is located
    start = time.time()
    current_folder = os.path.dirname(os.path.abspath(__file__))
    # Path to file
    path_to_file = os.path.join(
        current_folder, 'archive', 'Dataton 2023 Etapa 2.xlsx')
    data = DataReader(file_path=path_to_file).read_files()
    demand_data = data['demand']
    workers_data = data['workers']
    suc_code = 834
    suc_demand_data = sucursal_demand_data_separation(suc_code, demand_data)
    demand_per_day = day_demand_data_separation(suc_demand_data)
    schedule, total_demand, total_shortfall = tc_schedule_week(n_workers=4,
                                                               demand_per_day=demand_per_day[0:5],
                                                               lunch_hours=1.5,
                                                               work_hours=7)
    end = time.time()
    time_execution = end - start
    return schedule, total_demand, total_shortfall, time_execution


# %%
if __name__ == '__main__':
    schedule, total_demand, total_shortfall, time_execution = main()
    # df_solution = solution_format(demand, workers, best_schedule)
    # df_solution.to_csv('solucion.csv',index=False)
# %%
