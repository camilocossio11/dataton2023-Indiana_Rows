#%% Loading libraries
import pandas as pd
import random
from load_data import DataReader

#%%
data = DataReader(file_path = 'archive/Dataton 2023 Etapa 1.xlsx').read_files()
demand = data['demand']
workers =  data['workers']
schedule = pd.DataFrame()