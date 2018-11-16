import pandas as pd

data_path = 'data/'
file_name = 'addresses.csv'
file2_name = 'backup-addresses.csv'

data_df = pd.read_csv(data_path+file_name, index_col='Location')
data2_df = pd.read_csv(data_path+file2_name, index_col='Location')

for i, row in data_df.iterrows():
    if i in data2_df.index:
        data_df.loc[i, :] = data2_df.loc[i, :]

data_df.to_csv(data_path+file_name)
print('done')