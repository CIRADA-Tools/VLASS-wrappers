import pandas as pd
import os

if os.path.exists(os.getenv('PIPE1')+'/components_out_som.csv'):
	catalog=os.getenv('PIPE1')+'/components_out_som.csv'
elif os.path.exists(os.getenv('PIPE3_2') + '/components_out_som.csv'):
	catalog=os.getenv('PIPE3_2') + '/components_out_som.csv'





# Removing QL_cutout column due to lack of stable URLs
data_catalog=pd.read_csv(catalog)
data_catalog.drop(columns=['QL_cutout'], inplace=True)
# 
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the provided file
file_path = '2d_prob.txt'
data = np.loadtxt(file_path)

if imagetype=='se':
    for index, row in data_catalog.iterrows():
        x, y = int(row['Best_neuron_x']), int(row['Best_neuron_y'])
        data_catalog.at[index, 'P_sidelobe'] = data[x, y]



data_catalog.to_csv(catalog,index=False)