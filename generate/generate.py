# for every parameter set create the corresponding directory
# then copy the templates for the 'clean' and 'avx2' implementations inside that directory
# then substitute the actual parameters (listed in parameter_sets.csv)
# finally remove dead code (#if, #ifdef, #elif, etc.) and run astyle

import os
import csv
import shutil
import datetime

import utility

# move to the directory where the script is located
base_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(base_directory)

# output here
TARGET_DIR = './crypto_sign'

# check that the unifdef package is installed
# unifded is used to remove dead code
if os.system('which unifdef > /dev/null 2>&1') != 0:
    raise Exception('unifdef package not found, please install it')

astyle_config_file = './astyle/liboqs_astyle.ini'

# delete output directory if it already exists
if os.path.exists(TARGET_DIR):
    shutil.rmtree(TARGET_DIR)

# csv file
# the column '__dir__' constains the directory name for a given set of parameters
# the other columns contain the values to replace (e.g. replace "__random-bytes__" with "16")
csv_filename = './parameter_sets.csv'

# files and directories to copy
meta_file = '/META.yml'
clean_dir = '/clean'
avx2_dir = '/avx2'

with open(csv_filename, 'r') as csvfile:

    csv_reader = csv.DictReader(csvfile)
    columns = csv_reader.fieldnames

    for row in csv_reader:

        print('.', end='', flush=True)
        
        # create the directory for a given set of parameters 
        dir = row['__dir__']
        dir = os.path.join(TARGET_DIR, dir)
        if(not os.path.isdir(dir)):
            os.makedirs(dir)
            # copy META.yml
            shutil.copyfile('..' + meta_file, dir + meta_file)
            # copy the reference (clean) implementation template
            shutil.copytree('..' + clean_dir, dir + clean_dir)
            # copy the optimized (avx2) implementation template
            shutil.copytree('..' + clean_dir, dir + avx2_dir)
            shutil.copytree('..' + avx2_dir, dir + avx2_dir, dirs_exist_ok=True)
            # replace 'column_name' with 'column_value' in META.yml
            for column_name in columns:
                column_value = row[column_name]
                utility.replace_in_file(dir + meta_file, column_name, column_value)

        dir = dir + '/' + row['__implementation__']

        # replace 'column_name' with 'column_value' in the files
        for column_name in columns:
            column_value = row[column_name]
            utility.replace_in_dir(dir, column_name, column_value)

        utility.remove_dead_code(dir)

        utility.run_astyle(dir, astyle_config_file)

current_time = datetime.datetime.now().strftime("%H:%M")
print("\nImplementations placed in", TARGET_DIR, "@", current_time)