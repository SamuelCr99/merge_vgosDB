from vgos_db_equivalent import is_equivalent
from vgos_db_plug_compatible import find_compatible
from vgos_db_identical import is_identical
from vgos_db_same import is_same
from wrapper_equivalent import is_equivalent_wrapper
from history_file_identical import is_identical_history_file
from Directory import Directory
import os
import shutil
import sys
import warnings
import glob
import datetime


def find_history_file_name(old_file_name, merge_directory):
    """
    Finds the correct name for a history file. This name should depend on the 
    version number of the other files in the directory.
    """
    history_file_names = "\t".join(os.listdir(f'{merge_directory}History'))
    old_file_name_prefix = old_file_name.split('_')[0]
    flags = old_file_name.strip(".hist").split("_")[1:]
    flags_reduced = []
    for flag in flags:
        if flag[0].lower() != "v":
            flags_reduced.append(flag)
    v=0
    while f"_V{get_version_num(v)}" in history_file_names:
        v+=1
    return f"{old_file_name_prefix}_V{get_version_num(v)}_{'_'.join(flags_reduced)}.hist"


def find_data_file_name(old_file_name, merge_directory):
    """
    Finds the correct name for a data file. This name should depend on the 
    version number of the other files in the directory.
    """
    old_file_name_prefix = old_file_name.split("_")[0].split(".")[0]

    data_file_paths = glob.glob(f"{merge_directory}{old_file_name_prefix}*.nc")
    data_file_names = []
    for path in data_file_paths:
        data_file_names.append(os.path.basename(path))

    flags = old_file_name.strip(".nc").split("_")[1:]
    flags_reduced = []
    for flag in flags:
        if flag[0].lower() != "v":
            flags_reduced.append(f"_{flag}")
    
    v=1
    while f"_V{get_version_num(v)}" in data_file_names:
        v+=1
    
    return f"{old_file_name_prefix}_V{get_version_num(v)}{''.join(flags_reduced)}.nc"


def get_version_num(v):
    """
    Formats number to 3 digit string 
    """
    if v<10:
        return f"00{v}"
    elif v<100:
        return f"0{v}"
    else:
        return f"{v}"


# Is-methods are used to determine which type of information a line in the
# wrapper file is referring to
def is_beginning(line):
    return line.split(" ")[0].lower() == "begin"

def is_end(line):
    return line.split(" ")[0].lower() == "end"

def is_directory(line):
    return line.split(' ')[0].lower() == "default_dir"

def is_history_file(line):
    return ".hist" in line.split(' ')[-1] and line.split(' ')[0] == 'History'

def is_data_file(line):
    return '.nc' in line.split(' ')[-1]

def handle_directory(line, merge_directory):
    """
    Handles actions to be performed for lines which refer to a directory. 

    Steps: 
    Checks to see if referred to directory exists in merge_directory, if it does
    not then we create it. 

    Parameters: 
    line (str): Line from wrapper file containing name of history file. 
    merge_directory(string): File path of the target location for the merge.

    Return values:
    Returns the lines which should be written to the new wrapper file and history
    file.
    """
    directory_name = line.split(' ')[1]
    history_lines = ''
    if directory_name not in os.listdir(merge_directory):
        os.mkdir(f'{merge_directory}{directory_name}')
        history_lines = f"Directory: {directory_name} did not exist, now created."
    return line, history_lines

def handle_history_file(line, merge_directory, secondary_directory):
    """
    Handles actions to be performed for lines which refer to a history file. 

    Steps: 
    Check if there is a history file with the same name. If there is then check
    if these history files are identical, if they are don't copy. If they are not
    create a new copy of the history file from secondary_directory but change name. 
    If there was no file with the same name copy over the file without a name 
    change. 

    Parameters: 
    line (str): Line from wrapper file containing name of history file. 
    merge_directory(string): File path of the target location for the merge.
    secondary_directory(string): File path of folder which contains wrapper file.

    Return values:
    Returns the lines which should be written to the new wrapper file and history
    file.
    """
    history_file_name = line.split(' ')[-1]
    history_lines = ''

    if history_file_name not in os.listdir(merge_directory+'/History'):
        shutil.copyfile(f'{secondary_directory}History/{history_file_name}', f'{merge_directory}History/{history_file_name}') #Copies file
        history_lines = f'Copy history: {history_file_name} did not exist in merge directory, copied file.'
    
    else:
        if not is_identical_history_file(f'{secondary_directory}History/{history_file_name}', f'{merge_directory}History/{history_file_name}'):
            new_file_name = find_history_file_name(history_file_name,merge_directory)
            shutil.copyfile(f'{secondary_directory}History/{history_file_name}', f'{merge_directory}History/{new_file_name}') #Copies file
            line = line.strip(history_file_name) + new_file_name
            history_lines = f'Copy history: {history_file_name} did not exist in merge directory, but name was taken. Copied file with name {new_file_name}.'

    return line, history_lines

def handle_data_file(line, merge_directory, secondary_directory, current_dir):
    """
    Handles actions to be performed for lines which refer to a data file. 

    Steps: 
    Check if there are any compatible files in the merge directory: 
        Y: Check if any of these files are same, identical or equivalent. If 
            they are copy over the name which corresponds with the file in the 
            merge dictionary. If same or identical write this to the history file. 
            If none of these are correct then we should copy over file, check if 
            there is a file with the same name. If yes rename, otherwise not. 
        N: Copy file and write to history file.  

    Parameters: 
    line (str): Line from wrapper file containing name of data file. 
    merge_directory(string): File path of the target location for the merge.
    secondary_directory(string): File path of folder which contains wrapper file.

    Return values:
    Returns the lines which should be written to the new wrapper file and history
    file.
    """
    compatible_paths = find_compatible(secondary_directory+line, merge_directory[:-1])

    file_name = line
    file_path = secondary_directory+line

    if not compatible_paths: 
        shutil.copyfile(f'{secondary_directory}{file_name}', f'{merge_directory}{file_name}') #Copies file
        history_line = f'Copy file: No compatible files found for {current_dir}{file_name}, copied file.' 
        return line, history_line


    for compatible_line in compatible_paths:
        if is_same(file_path,compatible_line):
            return line, ''


    for compatible_line in compatible_paths:
        if is_identical(file_path, compatible_line):
            history_line = f'Identical file found: {current_dir+file_name} has been changed to {current_dir}{compatible_line.split("/")[-1]}.'
            return compatible_line.split("/")[-1], history_line

    
    for compatible_line in compatible_paths:
        if is_equivalent(file_path, compatible_line):
            history_line = f'Equivalent file found: {current_dir+file_name} has been changed to {current_dir}{compatible_line.split("/")[-1]}.'
            return compatible_line.split("/")[-1], history_line


    if file_name in os.listdir(merge_directory):
        old_file_name = file_name
        file_name = find_data_file_name(old_file_name,merge_directory)

        shutil.copyfile(f'{secondary_directory}{old_file_name}', f'{merge_directory}{file_name}') #Copies file
        history_line = f'Copy file: No file same, identical or equivalent for {current_dir}{old_file_name}, but name already existed. Updating name to {current_dir}{file_name}.'
        return file_name, history_line

    else: 
        shutil.copyfile(f'{secondary_directory}{file_name}', f'{merge_directory}{file_name}') #Copies file
        history_line = f'Copy file: No file is same, identical or equivalent for {current_dir}{file_name}. Copied it over.'
        return file_name, history_line


def find_wrapper_files(directory):
    """
    Finds all wrapper files for a given directory
    """
    wrapper_files = []
    files = os.listdir(directory)
    for file in files:
        if file[-4:] == '.wrp':
            wrapper_files.append(directory + file)
    return wrapper_files



def create_new_wrapper(wrapper_file, merge_directory, secondary_directory):
    """
    Checks if there is an equivalent wrapper with same name in merge directory
    if not it creates a new wrapper file, writes all the correct lines to it and
    performs the actions needed for wrapper file to work in new directory. 

    Parameters: 
    wrapper_file(string): File path of wrapper file.
    merge_directory(string): File path of the target location for the merge.
    secondary_directory(string): File path of folder which contains wrapper file.

    Returns: 
    No return values!  
    """
    with open(wrapper_file) as file:
        wrapper_lines = file.readlines()

    # This is for case 1
    wrapper_file_name = wrapper_file.split('/')[-1]
    if wrapper_file_name in os.listdir(merge_directory):
        if is_equivalent_wrapper(merge_directory+wrapper_file_name, secondary_directory+wrapper_file_name):
            return
        else: 
            warnings.warn("Wrapper with the same name found, but they are not equivalent!")
            return

    # For case 2
    lines_to_write_wrapper = []
    lines_to_write_history = []
    now = datetime.datetime.utcnow()
    lines_to_write_history.append(f"\nTIMETAG {now.strftime('%Y/%m/%d %H:%M:%S')} UTC")
    current_dir = Directory()
    
    for line in wrapper_lines: 
        line = line.strip('\n')

        if is_beginning(line):
            current_dir.go_in("")
            lines_to_write_wrapper.append(line)

        elif is_end(line):
            current_dir.go_out()
            lines_to_write_wrapper.append(line)

        elif is_directory(line):
            current_dir.go_out()
            return_values = handle_directory(line, merge_directory + current_dir.get_path())
            current_dir.go_in(line.split(" ")[1])
            lines_to_write_wrapper.append(return_values[0])
            if return_values[1]:
                lines_to_write_history.append(return_values[1])

        elif is_history_file(line):
            return_values = handle_history_file(line, merge_directory, secondary_directory)
            lines_to_write_wrapper.append(return_values[0])
            if return_values[1]:
                lines_to_write_history.append(return_values[1])

        elif is_data_file(line):
            return_values = handle_data_file(line, merge_directory + current_dir.get_path_with_slash(), secondary_directory + current_dir.get_path_with_slash(), current_dir.get_path_with_slash())
            lines_to_write_wrapper.append(return_values[0])
            if return_values[1]:
                lines_to_write_history.append(return_values[1])

        else:
            lines_to_write_wrapper.append(line)

    with open(merge_directory+wrapper_file_name, 'x') as f: 
        f.writelines("\n".join(lines_to_write_wrapper))

    if len(lines_to_write_history) > 1:
        if 'History' not in os.listdir(merge_directory):
            os.mkdir(f'{merge_directory}History')
        history_file_names = "\t".join(os.listdir(f'{merge_directory}History'))
        v=0
        while f"_V{get_version_num(v)}" in history_file_names:
            v+=1
        merge_history_file_name = f"{merge_directory.split('/')[-2]}_V{get_version_num(v)}_kvgosDBmerge.hist" 

        with open(f"{merge_directory}History/{merge_history_file_name}", 'x') as f: 
            f.writelines("\n".join(lines_to_write_history))
        

def main(merge_directory, secondary_directory):
    """
    Finds all wrapper files in secondary directory and moves them over to the 
    merge directory

    Parameters: 
    merge_directory(str): File path to the directory where files should be 
    merged to. 

    secondary_directory(str): File path of the directory where files should be
    merged from. 

    Returns: 
    No return values
    """
    if merge_directory[-1] != '/': merge_directory += '/'
    if secondary_directory[-1] != '/': secondary_directory += '/'

    wrapper_files = find_wrapper_files(secondary_directory)
    wrapper_files.sort()
    for wrapper_file in wrapper_files: 
        create_new_wrapper(wrapper_file, merge_directory, secondary_directory)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        merge_directory = 'test_data/n_data/20230616-i23167/'
        secondary_directory = 'test_data/g_data/20230616-i23167/'
    else: 
        merge_directory = sys.argv[1]
        secondary_directory = sys.argv[2] 

    main(merge_directory, secondary_directory)