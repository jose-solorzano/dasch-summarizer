#
# This script tests some specific targets that produce extreme
# slopes, apparently due to magnitudes that are very large
# negative values.
#

import dasch_regression
import pandas as pd
import os
from dasch_aflags import *

DIR_NAME = 'D:\\opt\\data\\scrape-dasch'
FOUND_FILE = 'found.txt'
STORE_DIR = 'store'

AFLAGS_EXCLUDED = AFLAGS_BAD_BIN | AFLAGS_DEFECTIVE

BAD_TARGETS = [
    8259161,
    8248339,
    8259299,
    8248336,
    8248189,
    8259229,
    36210110,
]

store_path = os.path.join(DIR_NAME, STORE_DIR)
data_matrix = []
count = 0
for apassid in BAD_TARGETS:
    count += 1
    if count > 1000:
        break
    data_file_path = os.path.join(store_path, str(apassid % 100), str(apassid) + '.txt')
    if not os.path.exists(data_file_path):
        print('File does not exist: %s' % data_file_path)
        break
    else:
        row = dasch_regression.get_summarized_info(data_file_path, AFLAGS_EXCLUDED)
        if row is not None:
            data_matrix.append((apassid,) + row)

out_frame = pd.DataFrame(data_matrix, columns=['apassdr9_id', 'n_points',
                                               'n_reg', 'slope', 'slope_stderr',
                                               'mean_mag', 'mean_limiting_mag',
                                               'n_reg_pre_1960', 'slope_pre_1960', 'slope_stderr_pre_1960',
                                               'mean_mag_pre_1960', 'mean_limiting_mag_pre_1960'])
print('Summary: \r\n%s' % str(out_frame['slope'].describe()))
print(out_frame[['n_points', 'n_reg', 'mean_mag', 'mean_limiting_mag']])

