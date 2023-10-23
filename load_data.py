#%% Importing libraries
import pandas as pd

#%% Loading data
class DataReader():
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
    def read_files(self):
        return pd.read_excel(self.file_path, sheet_name=None)
# %%