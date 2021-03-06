#
# Checks that all files that should exist do
#

import os

DIR_NAME = 'D:\\opt\\data\\scrape-dasch'
FOUND_FILE = 'found.txt'
STORE_DIR = 'store'

found_path = os.path.join(DIR_NAME, FOUND_FILE)
store_path = os.path.join(DIR_NAME, STORE_DIR)
file_count = 0
exists_count = 0
with open(found_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        file_count += 1
        apassid = int(line)
        data_file_path = os.path.join(store_path, str(apassid % 100), str(apassid) + '.txt')
        if not os.path.exists(data_file_path):
            print('File does not exist: %s' % data_file_path)
        else:
            exists_count += 1
print('Number of files: %d' % file_count)
print('Exists count: %d' % exists_count)
