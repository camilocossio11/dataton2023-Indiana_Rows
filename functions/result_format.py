import pandas as pd
import numpy as np

def solution_format(demand_per_day:list, workers:pd.DataFrame, schedule:np.array, suc_code:int, week:bool = True):
    workers = workers.sort_values(by='contrato', ascending=False)
    df_solution = pd.DataFrame(columns=['suc_cod','documento','fecha','hora','estado','hora_franja'])
    for demand in demand_per_day:
        df_schedule = pd.DataFrame(schedule.T,columns=workers['documento'])
        df_schedule.replace(0,'Nada',inplace=True)
        df_schedule.replace(1,'Trabaja',inplace=True)
        df_schedule.replace(2,'Pausa Activa',inplace=True)
        df_schedule.replace(3,'Almuerza',inplace=True)
        df_schedule['fecha'] = list(pd.to_datetime(demand['fecha_hora']).dt.strftime('%d/%m/%Y'))
        df_schedule['hora'] = list(pd.to_datetime(demand['fecha_hora']).apply(lambda x: x.strftime('%H:%M')))
        if week:
            df_schedule['hora_franja'] = list(range(30,79))
        else:
            df_schedule['hora_franja'] = list(range(30,59))
        for i in workers['documento']:
            df_aux = df_schedule[[i,'fecha','hora','hora_franja']].rename(columns={i:'estado'})
            df_aux['documento'] = i
            df_aux['suc_cod'] = suc_code
            df_solution = pd.concat([df_solution,df_aux],ignore_index=True)
    return df_solution