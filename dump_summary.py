#
# Script that produces the summary data files.
#

import os
import pandas as pd

from dasch_aflags import *
import dasch_regression

# These flags minimize the overall slope standard deviation
# and mean standard error.
AFLAGS_EXCLUDED = AFLAGS_BAD_BIN | AFLAGS_DEFECTIVE

DIR_NAME = 'D:\\opt\\data\\scrape-dasch'
FOUND_FILE = 'found.txt'
STORE_DIR = 'store'

found_path = os.path.join(DIR_NAME, FOUND_FILE)
store_path = os.path.join(DIR_NAME, STORE_DIR)
data_matrix = []
wor_data_matrix = []
with open(found_path, 'r') as file:
    lines = file.readlines()
    no_file_count = 0
    count = 0
    for line in lines:
        count += 1
        if count % 1000 == 0:
            print('Processed %d files.' % count)
        apassid = int(line)
        data_file_path = os.path.join(store_path, str(apassid % 100), str(apassid) + '.txt')
        if not os.path.exists(data_file_path):
            no_file_count += 1
            print('File does not exist: %s' % data_file_path)
        else:
            len_raw, corrected_table = dasch_regression.read_table(data_file_path, AFLAGS_EXCLUDED)
            row = dasch_regression.get_summarized_info_for_frame(data_file_path,
                                                                 len_raw, corrected_table,
                                                                 remove_outliers=False)
            if row is not None:
                data_matrix.append((apassid,) + row)
            wor_row = dasch_regression.get_summarized_info_for_frame(data_file_path,
                                                                     len_raw, corrected_table,
                                                                     remove_outliers=True)
            if wor_row is not None:
                wor_data_matrix.append((apassid,) + wor_row)
    if no_file_count > 0:
        print('WARN: %d files not found!' % no_file_count)


def write_results(_data_matrix: [], with_outlier_removal: bool):
    out_frame = pd.DataFrame(_data_matrix, columns=['apassdr9_id', 'n_points',
                                                   'n_reg', 'slope', 'slope_stderr',
                                                   'mean_mag', 'mean_limiting_mag',
                                                   'n_reg_pre_1960', 'slope_pre_1960', 'slope_stderr_pre_1960',
                                                   'mean_mag_pre_1960', 'mean_limiting_mag_pre_1960'])
    suffix = '-wor' if with_outlier_removal else ''
    out_file_path = os.path.join(DIR_NAME, 'summarized-dasch-trends%s.csv' % suffix)
    out_frame.round(4).to_csv(out_file_path, index=False)
    print('Wrote %s' % out_file_path)


write_results(data_matrix, False)
write_results(wor_data_matrix, True)
