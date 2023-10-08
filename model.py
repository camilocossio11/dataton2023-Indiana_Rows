#%% Loading libraries
import pandas as pd
import random
from load_data import DataReader

#%%
demand = DataReader(file_path = 'archive/Dataton 2023 Etapa 1.xlsx').read_file()
schedule = pd.DataFrame()