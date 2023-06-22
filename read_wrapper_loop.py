from vgos_db_equivalent import is_equivalent
from vgos_db_plug_compatible import find_compatible
from vgos_db_identical import is_identical
from vgos_db_same import is_same
import os


def write_to_wrapper(line):
    pass

def write_history_file_to_wrapper(line):
    pass

def check_directory(line):
    # Does the directory exist in merged vgosDB?
    pass

def check_for_history_file(line):
    # Does the merged vgosDB contain a history file of the same name? 
    
    pass


def is_wrapper_info(line):
    return False

def is_directory(line):
    if "default_dir" in line.lower():
        return True
    return False

def is_history_file(line):
    if ".hist" in line.split(' ')[-1] and line.split(' ')[0] == 'History':
        return True
    return False

def is_data_file(line):
    if '.nc' in line.split(' ')[-1]:
        return True
    return False

def handle_wrapper_info(line):
    write_to_wrapper(line)

def handle_directory(line):
    if not check_directory(line):
        # Create directory in merged vgosDB and write this to the history file
        pass
    write_to_wrapper(line)

def handle_history_file(line):
    if not check_for_history_file(line):
        # Copy the secondary history file to the merged vgosDB area under new name
        # Indiciate operation in history file
        pass
    write_history_file_to_wrapper(line)


def handle_data_file(line):
    if find_compatible(line):
        # Copy vgosDB datafile to merged vgosDB
        pass
    elif is_same(line):
        # Return to top 
        pass
    elif is_identical(line):
        # Use name of vgosDB identical
        # Update history to indicate change of name
        pass
    elif is_equivalent(line):
        # Use name of vgosDB-equivalent
        # Update history file to indicate change of name
        pass
    else:
        if check_directory(line): # This might be wrong
            # Copy the secondary vgosDB datafile to the merged vgosDB with a unique name
            pass
        else: 
            # Copy the secondary vgosDB datafile 
            pass

def find_wrapper_files(directory):
    # if directory[-1] != '/': directory += '/'
    wrapper_files = []
    files = os.listdir(directory)
    for file in files:
        if file[-4:] == '.wrp':
            wrapper_files.append(directory + file)
    return wrapper_files




def main(wrapper_file, merge_directory):
    with open(wrapper_file) as file:
        lines = file.readlines()


    for line in lines: 
        if is_wrapper_info(line):
            print("It is a wrapper file!")
            # handle_wrapper_info(line)

        elif is_directory(line):
            line = line.strip('\n')
            print(f"Directory found: {line}")
            handle_directory(line)

        elif is_history_file(line):
            line = line.strip('\n')
            print(f"History found: {line}")
            handle_history_file(line)

        elif is_data_file(line):
            line = line.strip('\n')
            print(f"Datafile found: {line}")
            handle_history_file(line)

if __name__ == '__main__':
    file_location = 'NVI_data/20APR01XA/'
    wrapper_files = find_wrapper_files(file_location)
    wrapper_files.sort(reverse=True)
    for wrapper_file in wrapper_files: 
        main(wrapper_file, '')
        quit()