#%%
from load_data import DataReader
import pandas as pd
from datetime import date

#%%
def read_data():
    DR = DataReader(r'/Users/mariajosefranco/Documents/python_codes/dataton2023/dataton2023-Indiana_Rows/archive/Dataton 2023 Etapa 2.xlsx')
    demand_data = DR.read_files()['demand']
    workers_data = DR.read_files()['workers']
    return demand_data, workers_data

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
    suc_demand_data['hora'] = [row.time() for row in suc_demand_data['fecha_hora']]
    del suc_demand_data['fecha_hora']
    df_per_date = {}
    for date, group in suc_demand_data.groupby('fecha'):
        df_per_date[date] = group
    return df_per_date

#%%
suc_cod = 834
demand_data, workers_data = read_data()
suc_demand_data = sucursal_demand_data_separation(suc_cod, demand_data)

demand_data_per_day = day_demand_data_separation(suc_demand_data)
dia1 =  demand_data_per_day[date(2023, 12, 11)]
dia2 =  demand_data_per_day[date(2023, 12, 12)]
dia3 =  demand_data_per_day[date(2023, 12, 13)]
dia4 =  demand_data_per_day[date(2023, 12, 14)]
dia5 =  demand_data_per_day[date(2023, 12, 15)]
dia6 =  demand_data_per_day[date(2023, 12, 16)]
# %%
