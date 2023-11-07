#%% Importing libraries
import pandas as pd
import os

#%% Loading data
class DataReader():
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
    def read_files(self):
        return pd.read_excel(self.file_path, sheet_name=None)

def sucursal_demand_data_separation(suc_cod, demand_data):
    try:
        if suc_cod in demand_data['suc_cod'].values:
            suc_demand_data = demand_data[demand_data['suc_cod'] == suc_cod]
            return suc_demand_data
        else:
            raise KeyError("El codigo de la sucursal ingresada no existe")
    except Exception as ex:
        print(ex)

def day_demand_data_separation(suc_demand_data):
    suc_demand_data['fecha'] = [row.date() for row in suc_demand_data['fecha_hora']]
    demand_per_day = []
    for date, group in suc_demand_data.groupby('fecha'):
        del group['fecha']
        demand_per_day.append(group)
    return demand_per_day

def load_data(folder:str, file_name: str):
    # Path to file
    path_to_file = os.path.join(folder, 'archive', file_name)
    data = DataReader(file_path=path_to_file).read_files()
    return data


def load_demand_data(data: dict, suc_code: int):
    demand_data = data['demand']
    suc_demand_data = sucursal_demand_data_separation(suc_code, demand_data)
    demand_per_day = day_demand_data_separation(suc_demand_data)
    return demand_per_day


def load_workers_data(data: dict, suc_code: int):
    workers_data = data['workers']
    workers = workers_data[workers_data['suc_cod'] == suc_code]
    n_tc_workers = workers_data[workers_data['suc_cod']
                                == suc_code]['contrato'].value_counts()['TC']
    n_mt_workers = workers_data[workers_data['suc_cod']
                                == suc_code]['contrato'].value_counts()['MT']
    return n_tc_workers, n_mt_workers, workers
# %%