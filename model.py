#%% Loading libraries
import pandas as pd
import random
import numpy as np
import os
import time
from functions.load_data import DataReader
from functions.best_TC import final_solution_per_day_TC
from functions.result_format import solution_format
from functions.load_data import sucursal_demand_data_separation, day_demand_data_separation

#%%

def main(iterations:int):
    # Folder where the script is located
    start = time.time()
    current_folder = os.path.dirname(os.path.abspath(__file__))
    # Path to file
    path_to_file = os.path.join(current_folder, 'archive', 'Dataton 2023 Etapa 2.xlsx')
    data = DataReader(file_path = path_to_file).read_files()
    demand_data = data['demand']
    workers_data =  data['workers']
    suc_code = 834
    suc_demand_data = sucursal_demand_data_separation(suc_code, demand_data)
    demand_per_day = day_demand_data_separation(suc_demand_data)
    TC_solution, total_shortfall = final_solution_per_day_TC(demand_per_day[0:5],4)
    return TC_solution,total_shortfall

# %%
if __name__=='__main__':
    TC_solution,total_shortfall = main(5_000)
    # df_solution = solution_format(demand, workers, best_schedule)
    # df_solution.to_csv('solucion.csv',index=False)
# %%
