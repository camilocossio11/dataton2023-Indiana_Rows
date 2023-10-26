#%%
import numpy as np
#%%

def exclude_lunch(breaks_index: np.array) -> np.array:
    try:
        exclude = None
        for i in range(len(breaks_index) - 5):
            if (breaks_index[i]+5) == (breaks_index[i+5]):
                exclude = np.arange(breaks_index[i]+1, breaks_index[i+5])
        brks = np.setdiff1d(breaks_index, exclude)
        return brks
    except Exception as e:
        print(f'Ocurrio un error: {e}')
    finally:
        del brks, exclude

def check_breaks(schedule: np.array) -> bool:
    try:
        breaks = np.insert(np.where(schedule != 1), 0, 0)
        breaks = exclude_lunch(breaks)
        dif = [breaks[i+1]-breaks[i] for i in range(len(breaks)-1)]
        if min(dif) < 4 or max(dif) > 8:
            return False
        else:
            return True
    except Exception as e:
        print(f'Ocurrio un error: {e}')
    finally:
        del breaks, dif

def check_lunch_time(schedule: np.array) -> bool:
    try:
        lunch_blocks = [i for i, elemento in enumerate(schedule) if elemento == 3]
        lunch_start = lunch_blocks[0]
        if len(lunch_blocks) != 6:
            print('El bloque de almuerzo no es de 1 h y 30 min')
            return False
        elif 17 <= lunch_start <= 25:
            print('El bloque de almuerzo se encuentra asignado correctamente')
            return True
        else:
            print('El bloque de almuerzo no se encuentra entre el horario permitido para almorzar')
            return False
    except Exception as e:
        print(f'Ocurrio un error: {e}')
    finally:
        del lunch_blocks, lunch_start

def check_solution(schedule: np.array) -> bool:
    try:
        check_1 = check_breaks(schedule)
        check_2 = check_breaks(schedule)
        if check_1 and check_2:
            return True
        else:
            return False
    except Exception as e:
        print(f'Ocurrio un error: {e}')

# %%
