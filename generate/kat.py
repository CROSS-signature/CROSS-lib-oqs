import os
import csv
import shutil
import datetime

import utility

# move to the directory where the script is located
base_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(base_directory)

replace_list = []

for i, elem in enumerate(replace_list):
    if i % 2 == 0:
        utility.replace_in_file('./parameter_sets.csv', replace_list[i+1], replace_list[i])