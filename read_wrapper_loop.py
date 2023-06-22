from vgos_db_equivalent import is_equivalent
from vgos_db_plug_compatible import find_compatible
from vgos_db_identical import is_identical
from vgos_db_same import is_same
import os


# def is_wrapper_info(line):
#     return False

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
    return line

def handle_directory(line, merge_directory):
    directory_name = line.split(' ')[-1]
    history_lines = ''

    if directory_name not in os.listdir(merge_directory):
        # Create a new directory
        history_lines = f"Directory: {directory_name} did not exist, now created"
    return line, history_lines

def handle_history_file(line, merge_directory, secondary_directory):
    history_file_name = line.split(' ')[-1]

    if history_file_name not in os.listdir(merge_directory+'/History'):
        # Copy the secondary history file to the merged vgosDB area under new name
        # Indiciate operation in history file
        pass
    # write_history_file_to_wrapper(line)
    return "History " + line

def handle_data_file(line, merge_directory, secondary_directory):
    compatible_station = find_compatible(secondary_directory+line, merge_directory)[0]
    compatible_station_folder = compatible_station.strip(merge_directory).strip(line)
    folder_name = ''

    if not compatible_station: 
        # Copy file to merged vgosDB  
        pass

    if is_same(line,compatible_station):
        # Return to top 
        pass
    elif is_identical(line, compatible_station):
        # Update history to indicate change of name
        return line
    elif is_equivalent(line, compatible_station):
        # Update history to indicate change of name
        return line
    else:
        if line in os.listdir(merge_directory+folder_name): 
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




def main(wrapper_file, merge_directory, secondary_directory):
    with open(wrapper_file) as file:
        lines = file.readlines()

    # if wrapper_file.split('/')[-1] in os.listdir(merge_directory):
    #     print('Same wrapper file found')

    lines_to_write_wrapper = []
    lines_to_write_history = []

    for line in lines: 
        line = line.strip('\n')

        if is_directory(line):
            return_values = handle_directory(line, merge_directory)
            lines_to_write_wrapper.append(return_values[0])
            if return_values[1]:
                lines_to_write_history.append(return_values[1])

        elif is_history_file(line):
            lines_to_write_wrapper.append(handle_history_file(line, merge_directory, secondary_directory))

        # elif is_data_file(line):
        #     # Line here will not work, we will need the whole path! 
        #     handle_data_file(line, merge_directory, secondary_directory)
        # else:
        #     lines_to_write_wrapper.append(handle_wrapper_info(line))
    for l in lines_to_write_history:
        print(l)

if __name__ == '__main__':
    secondary_directory = 'NVI_data/20APR01XA/'
    wrapper_files = find_wrapper_files(secondary_directory)
    wrapper_files.sort(reverse=True)
    for wrapper_file in wrapper_files: 
        main(wrapper_file, 'NVI_data/20APR01XA', secondary_directory)
        quit()