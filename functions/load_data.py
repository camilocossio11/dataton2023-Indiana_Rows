#%% Importing libraries
import pandas as pd

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
            raise KeyError(f"El codigo de la sucursal ingresada no existe")
    except Exception as ex:
        print(ex)

def day_demand_data_separation(suc_demand_data):
    suc_demand_data['fecha'] = [row.date() for row in suc_demand_data['fecha_hora']]
    #suc_demand_data['hora'] = [row.time() for row in suc_demand_data['fecha_hora']]
    #del suc_demand_data['fecha_hora']
    demand_per_day = []
    for date, group in suc_demand_data.groupby('fecha'):
        del group['fecha']
        demand_per_day.append(group)
    return demand_per_day
# %%