import pandas as pd
import numpy as np
from functions.assignments import assign_start,assign_lunch
from functions.utils import create_schedule, calculate_shortfall

def TC_schedule(n_workers,original_demand,iterations):
    solution = {
        'schedule': None,
        'shortfall': 100_000,
        'start_day_schedule': None,
        'lunch_schedule': None
    }
    for i in range(iterations):
        schedule = pd.DataFrame()
        lunch_schedule = assign_lunch(original_demand, n_workers)
        start_day_schedule = assign_start(lunch_schedule)
        schedule = create_schedule(start_day_schedule,lunch_schedule,original_demand)
        total_shortfall = calculate_shortfall(schedule,list(original_demand['demanda']))
        if total_shortfall < solution['shortfall']:
            solution['schedule'] = schedule
            solution['shortfall'] = total_shortfall
            solution['start_day_schedule'] = start_day_schedule
            solution['lunch_schedule'] = lunch_schedule
    return solution