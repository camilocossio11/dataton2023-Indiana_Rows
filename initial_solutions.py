import pandas as pd
import numpy as np
import os
from functions.result_format import solution_format
from functions.load_data import load_data, load_demand_data, load_workers_data
from functions.TC_schedule import tc_schedule_week, tc_schedule_weekend
from functions.MT_schedule import mt_schedule
from functions.utils import calculate_shortfall

def initial_solution(suc_code: int, tc_work_hours: dict, mt_work_hours: dict,lunch_hours: float):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    data = load_data(current_folder,file_name='Dataton 2023 Etapa 2.xlsx')
    demand_per_day = load_demand_data(data=data, suc_code=suc_code)
    n_tc_workers, n_mt_workers, workers = load_workers_data(data=data,
                                                    suc_code=suc_code)
    # Week
    week_demand = demand_per_day[0:5]
    solution_week = initial_solution_week(tc_work_hours=tc_work_hours,
                                            mt_work_hours=mt_work_hours,
                                            lunch_hours=lunch_hours,
                                            n_tc_workers=n_tc_workers,
                                            n_mt_workers=n_mt_workers,
                                            week_demand=week_demand)
    solution_formated_week = solution_format(demand_per_day=week_demand,
                                            workers=workers,
                                            schedule=solution_week['schedule'],
                                            suc_code=suc_code)
    # Weekend
    weekend_demand = np.array(demand_per_day[-1]['demanda'].tolist())
    solution_weekend = initial_solution_weekend(tc_work_hours=tc_work_hours,
                                                mt_work_hours=mt_work_hours,
                                                n_tc_workers=n_tc_workers,
                                                n_mt_workers=n_mt_workers,
                                                weekend_demand=weekend_demand)
    solution_formated_weekend = solution_format(demand_per_day=[demand_per_day[-1]],
                                                workers=workers,
                                                schedule=solution_weekend['schedule'],
                                                suc_code=suc_code,
                                                week = False)
    initial_solution_formated = pd.concat([solution_formated_week, solution_formated_weekend], ignore_index=True)
    return solution_week,solution_weekend,initial_solution_formated

def initial_solution_week(
    tc_work_hours: dict,
    mt_work_hours: dict,
    lunch_hours: float,
    n_tc_workers: int,
    n_mt_workers: int,
    week_demand: list
):
    solution_tc = tc_schedule_week(n_workers=n_tc_workers,
                                    demand_per_day=week_demand,
                                    lunch_hours=lunch_hours,
                                    work_hours=tc_work_hours['week'])
    solution_mt = mt_schedule(total_demand=solution_tc['total_demand'],
                                work_hours=mt_work_hours['week'],
                                n_workers=n_mt_workers,
                                solution_tc=solution_tc)
    general_schedule_week = np.concatenate((solution_tc['schedule'], solution_mt['schedule']))
    total_shortfall_week = 0
    for demand in week_demand:
        total_shortfall_week += calculate_shortfall(general_schedule_week, list(demand['demanda']))
    initial_solution_week = {
        'schedule': general_schedule_week,
        'total_demand': solution_mt['total_demand'],
        'total_shortfall': total_shortfall_week
    }
    return initial_solution_week

def initial_solution_weekend(
    tc_work_hours: dict,
    mt_work_hours: dict,
    n_tc_workers: int,
    n_mt_workers: int,
    weekend_demand: np.array
):
    solution_tc_weekend = tc_schedule_weekend(n_workers=n_tc_workers,
                                                demand_saturday=weekend_demand,
                                                work_hours=tc_work_hours['weekend'])
    solution_mt_weekend = mt_schedule(total_demand=solution_tc_weekend['total_demand'],
                                        work_hours=mt_work_hours['weekend'],
                                        n_workers=n_mt_workers,
                                        solution_tc=solution_tc_weekend,
                                        week=False)
    general_schedule_weekend = np.concatenate((solution_tc_weekend['schedule'], solution_mt_weekend['schedule']))
    total_shortfall_weekend = calculate_shortfall(general_schedule_weekend, list(weekend_demand))
    solution_weekend = {
        'schedule': general_schedule_weekend,
        'total_demand': solution_mt_weekend['total_demand'],
        'total_shortfall': total_shortfall_weekend
    }
    return solution_weekend
