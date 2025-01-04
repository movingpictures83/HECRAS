
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from postprocess.threshold import flood_threshold, drought_threshold, flood_threshold_t1, drought_threshold_t1
# from preprocess.helper import stage_series_to_supervised, series_to_supervised
from helper import series_to_supervised

class HECRASPlugin:
 def input(self, inputfile):
  self.inputfile = inputfile
 def run(self):
     pass
 def output(self, outputfile):
  # In[54]:
  t1=1

  error_ras = pd.read_csv(self.inputfile+'/ras_1920.csv', index_col=0)
  error_ras.reset_index(drop=True, inplace=True)

  ras_concat = pd.concat([error_ras.loc[:, 'S1_RAS'], error_ras.loc[:, 'S25A_TW_RAS'], error_ras.loc[:, 'S25B_TW_OBS'], error_ras.loc[:, 'S26_TW_RAS']], axis=1)
  ras_concat = pd.DataFrame(ras_concat)

  plt.rcParams["figure.figsize"] = (18, 6)
  plt.plot(ras_concat.iloc[:, 0], label='S1')
  plt.axhline(y = 3.5, color='r', linestyle='dashed', linewidth=2)
  plt.axhline(y = 0, color='r', linestyle='dashed', linewidth=2)
  plt.xlabel('Time', fontsize=18)
  plt.ylabel('S1 Water Stage', fontsize=18)
  plt.xticks(fontsize=14)
  plt.yticks(fontsize=14)
  plt.legend(fontsize=14)
  plt.show()

  ras_flood = ras_concat[ras_concat['S1_RAS'] > 3.5]

  plt.rcParams["figure.figsize"] = (18, 6)
  plt.plot(ras_concat.iloc[5873:5913, 0], label='S1')
  plt.axhline(y = 3.5, color='r', linestyle='dashed', linewidth=2)
  plt.axhline(y = 0, color='r', linestyle='dashed', linewidth=2)
  plt.xlabel('Time', fontsize=18)
  plt.ylabel('S1 Water Stage', fontsize=18)
  plt.xticks(fontsize=14)
  plt.yticks(fontsize=14)
  plt.legend(fontsize=14)
  plt.show()

  test_set = pd.read_csv(self.inputfile+'/test_data.csv')
  test_set.columns

  test_set_s1 = test_set.iloc[:, 0:2]
  test_set_s1.reset_index(drop=True, inplace=True)

  filter_flood = test_set_s1[test_set_s1['WS_S1'] > 3.5]

  plt.rcParams["figure.figsize"] = (18, 6)
  plt.plot(test_set_s1['WS_S1'], label='S1')
  plt.axhline(y = 3.5, color='r', linestyle='dashed', linewidth=2)
  plt.axhline(y = 0, color='r', linestyle='dashed', linewidth=2)
  plt.xlabel('Time', fontsize=18)
  plt.ylabel('S1 Water Stage', fontsize=18)
  plt.xticks(fontsize=14)
  plt.yticks(fontsize=14)
  plt.legend(fontsize=14)

  plt.rcParams["figure.figsize"] = (18, 6)
  plt.plot(test_set_s1.iloc[7640:7680, 1], label='S1')
  plt.axhline(y = 3.5, color='r', linestyle='dashed', linewidth=2)
  plt.axhline(y = 0, color='r', linestyle='dashed', linewidth=2)
  plt.xlabel('Time', fontsize=18)
  plt.ylabel('S1 Water Stage', fontsize=18)
  plt.xticks(fontsize=14)
  plt.yticks(fontsize=14)
  plt.legend(fontsize=14)

  test_set_s1.iloc[7640:7680, 0]

  n_hours = 72
  K = 24
  data_supervised = series_to_supervised(ras_concat, n_hours, K)

  col_names = ['S1_RAS', 'S25A_TW_RAS', 'S25B_TW_OBS', 'S26_TW_RAS'] * (n_hours+K)
    
  data_supervised.reset_index(drop=True, inplace=True)
  data_supervised.columns = [[i + '_' + j for i, j in zip(col_names, list(data_supervised.columns))]]

  data_supervised_array = data_supervised.to_numpy(dtype='float32')
  data_supervised_array = data_supervised_array.reshape((-1, 96, 4))
  data_supervised_array = data_supervised_array[:, -24:, :]

  upper_threshold = 3.5

  flood_threshold_t1(data_supervised_array, t1, upper_threshold)

  lower_threshold = 0

  drought_threshold_t1(data_supervised_array, t1, lower_threshold)

