import fileinput
import re
import os

def replace_in_file(path, text_to_search, replacement_text):
  with fileinput.FileInput(path, inplace=True) as file:
    for line in file:
        print(re.sub(text_to_search, replacement_text, line), end='')

def replace_in_dir(dir, text_to_search, replacement_text):
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                replace_in_file(file_path, text_to_search, replacement_text)

def run_astyle(dir, astyle_config_file):
    for file in os.listdir(dir):
        if file.endswith('.c') or file.endswith('.h'):
            astyle_command = 'astyle --options='+astyle_config_file+' '+dir+'/'+file+' > /dev/null 2>&1'
            os.system(astyle_command)

# use the unifdef utility to remove #if, #ifdef, #elif, etc.
# unifdef has a few quirks, some additional processing is needed
# (e.g. it does not recognize multiline #define statements)
def remove_dead_code(dir):
    # comment out preprocessor directives that can confuse unifdef
    replace_in_dir(dir, '#pragma', '//#pragma')
    replace_in_dir(dir, '#include', '//#include')
    # remove dead code from set.h and parameters.h, wich contain all useful definitions
    unifdef_command = 'unifdefall '+dir+'/set.h > tmp.unifdef ; mv tmp.unifdef '+dir+'/set.h'
    os.system(unifdef_command)
    unifdef_command = 'unifdef -m -f '+dir+'/set.h '+dir+'/parameters.h'
    os.system(unifdef_command)
    # create a temporary parameters.h with just the first few lines, the rest breaks unifdef
    unifdef_command = 'head -60 '+dir+'/parameters.h > '+dir+'/tmp_parameters.h'
    os.system(unifdef_command)
    # remove parentheses from the temporary parameters.h, unifdef does not like them
    replace_in_file(dir+'/tmp_parameters.h', '\(', '')
    replace_in_file(dir+'/tmp_parameters.h', '\)', '')
    # use the definitions in set.h and parameters.h to remove dead code from the rest of the files
    for file in os.listdir(dir):
        if file.endswith('.c') or file.endswith('.h'):
            unifdef_command = 'unifdef -m -f '+dir+'/set.h -f '+dir+'/tmp_parameters.h '+dir+'/'+file
            os.system(unifdef_command)
    # restore the preprocessor directives
    replace_in_dir(dir, "//#pragma once", "#pragma once")
    replace_in_dir(dir, '//#include', '#include')
    # remove the temporary parameters.h
    os.system('rm '+dir+'/tmp_parameters.h')