import pandas as pd

# Load the data and print column names
data = pd.read_csv('network_data_log.csv')
print(data.columns)
