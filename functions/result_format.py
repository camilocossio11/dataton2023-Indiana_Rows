import pandas as pd
import numpy as np

def solution_format(demand:pd.DataFrame, workers:pd.DateOffset, best_schedule:np.array):
    df_schedule = pd.DataFrame(best_schedule.T,columns=workers['documento'])
    df_schedule.replace(0,'Nada',inplace=True)
    df_schedule.replace(1,'Trabaja',inplace=True)
    df_schedule.replace(2,'Pausa Activa',inplace=True)
    df_schedule.replace(3,'Almuerza',inplace=True)
    df_schedule['fecha'] = pd.to_datetime(demand['fecha_hora']).dt.strftime('%d/%m/%Y')
    df_schedule['hora'] = pd.to_datetime(demand['fecha_hora']).apply(lambda x: x.strftime('%H:%M'))
    df_schedule['hora_franja'] = list(range(30,76))
    df_solution = pd.DataFrame(columns=['suc_cod','documento','fecha','hora','estado','hora_franja'])
    for i in workers['documento']:
        df_aux = df_schedule[[i,'fecha','hora','hora_franja']].rename(columns={i:'estado'})
        df_aux['documento'] = i
        df_aux['suc_cod'] = workers[workers['documento'] == i]['suc_cod'].reset_index(drop=True)[0]
        df_solution = pd.concat([df_solution,df_aux],ignore_index=True)
    return df_solution