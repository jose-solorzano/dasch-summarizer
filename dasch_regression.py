#
# Routines that read DASCH short-format files, and calculate
# slopes and other summary statistics.
#

from scipy import stats
import numpy as np
import pandas as pd

MIN_N_PRE_1960 = 50
OUTLIER_SD = 3.0


def get_regression_info(data_frame: pd.DataFrame, remove_outliers=False):
    mag = data_frame['magcal_magdep']
    limiting_mag = data_frame['limiting_mag_local']
    mean_mag = np.mean(mag)
    mean_limiting_mag = np.mean(limiting_mag)
    x = data_frame['year'] - 1880
    slope, intercept, _, _, std_err = stats.linregress(x, mag)
    n_reg = len(x)
    if remove_outliers:
        residuals = mag - (x * slope + intercept)
        mean_res = np.mean(residuals)
        std_res = np.std(residuals)
        max_res = mean_res + OUTLIER_SD * std_res
        min_res = mean_res - OUTLIER_SD * std_res
        include = (residuals <= max_res) & (residuals >= min_res)
        x_trimmed = x[include]
        mag_trimmed = mag[include]
        slope, intercept, _, _, std_err = stats.linregress(x_trimmed, mag_trimmed)
        n_reg = len(x_trimmed)
    if np.isnan(slope):
        print('Unexpected: Got NaN slope!')
        return None
    slope_cent = slope * 100
    std_err_cent = std_err * 100
    return n_reg, slope_cent, std_err_cent, mean_mag, mean_limiting_mag,


def read_table(file_path: str, aflags_exclude: int):
    # Notes:
    # - Rows where the year is 'inf' are removed.
    # - Rows with certain AFLAGS values are removed.
    # - Rows with magcal_magdep < 0 are removed (important).
    raw_table = pd.read_table(file_path, skiprows=[0, 2], na_values=['inf'])
    is_defective = (raw_table['AFLAGS'] & aflags_exclude != 0) | raw_table['year'].isna() | \
                   (raw_table['magcal_magdep'] < 0)
    return len(raw_table), raw_table[~is_defective],


def get_summarized_info_for_frame(file_path: str, len_raw: int, corrected_table: pd.DataFrame, remove_outliers=False):
    corrected_table_pre_1960 = corrected_table[corrected_table['year'] <= 1960]
    if len(corrected_table_pre_1960) < MIN_N_PRE_1960:
        print('Less then %d data points pre-1960: %s' % (MIN_N_PRE_1960, file_path,))
        return None
    reg_info = get_regression_info(corrected_table, remove_outliers=remove_outliers)
    if reg_info is None:
        print('Invalid: %s' % file_path)
        return None
    reg_info_pre_1960 = get_regression_info(corrected_table_pre_1960, remove_outliers=remove_outliers)
    if reg_info_pre_1960 is None:
        print('Invalid: %s' % file_path)
        return None
    return (len_raw,) + reg_info + reg_info_pre_1960


def get_summarized_info(file_path: str, aflags_exclude: int, remove_outliers=False):
    len_raw, corrected_table = read_table(file_path, aflags_exclude)
    return get_summarized_info_for_frame(file_path, len_raw, corrected_table, remove_outliers=remove_outliers)
