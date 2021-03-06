#
# This script is used to test the best combinations of excluded
# AFLAGS to reduce the standard deviation of slopes.
#

import dasch_regression
import numpy as np
import pandas as pd
import os
from dasch_aflags import *

DIR_NAME = 'D:\\opt\\data\\scrape-dasch'
FOUND_FILE = 'found.txt'
STORE_DIR = 'store'

# Note:
# AFLAGS_BAD_PLATE_QUALITY is not recommended, as it removes
# too much information. What it does can be better achieved
# by removing magnitudes that are less than zero.

AFLAGS_EXCLUDED = AFLAGS_BAD_BIN | AFLAGS_DEFECTIVE

# Individual improvements with:
# AFLAGS_UNKNOWN_DRAD
# AFLAGS_BAD_BIN
# AFLAGS_3TIMES
# AFLAGS_ISOTROPIC
# AFLAGS_MAXIMUM

# Should 3-sigma outliers be removed?
# It does improve the slope standard deviation and mean standard error.
TRIM_OUTLIERS = True

found_path = os.path.join(DIR_NAME, FOUND_FILE)
store_path = os.path.join(DIR_NAME, STORE_DIR)
data_matrix = []
with open(found_path, 'r') as file:
    lines = file.readlines()
    no_file_count = 0
    count = 0
    for line in lines:
        count += 1
        if count > 1000:
            break
        apassid = int(line)
        data_file_path = os.path.join(store_path, str(apassid % 100), str(apassid) + '.txt')
        if not os.path.exists(data_file_path):
            no_file_count += 1
            print('File does not exist: %s' % data_file_path)
        else:
            row = dasch_regression.get_summarized_info(data_file_path, AFLAGS_EXCLUDED, remove_outliers=TRIM_OUTLIERS)
            if row is not None:
                data_matrix.append((apassid,) + row)
    if no_file_count > 0:
        print('WARN: %d files not found!' % no_file_count)

out_frame = pd.DataFrame(data_matrix, columns=['apassdr9_id', 'n_points',
                                               'n_reg', 'slope', 'slope_stderr',
                                               'mean_mag', 'mean_limiting_mag',
                                               'n_reg_pre_1960', 'slope_pre_1960', 'slope_stderr_pre_1960',
                                               'mean_mag_pre_1960', 'mean_limiting_mag_pre_1960'])
print('Slope stdev: %.4f' % np.std(out_frame['slope']))
print('Mean stderr: %.4f' % np.std(out_frame['slope_stderr']))
