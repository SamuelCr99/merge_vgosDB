from vgos_db_equivalent import is_equivalent
from vgos_db_plug_compatible import find_compatible
from vgos_db_identical import is_identical
from vgos_db_same import is_same
from wrapper_equivalent import is_equivalent_wrapper
from history_file_identical import is_identical_history_file
import os
import shutil
from Directory import Directory


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

def handle_wrapper_info(line):
    return line

def handle_directory(line, merge_directory):
    directory_name = line.split(' ')[1]
    history_lines = ''
    if directory_name not in os.listdir(merge_directory):
        os.mkdir(f'{merge_directory}{directory_name}')
        history_lines = f"Directory: {directory_name} did not exist, now created"
    return line, history_lines

def handle_history_file(line, merge_directory, secondary_directory):
    history_file_name = line.split(' ')[-1]
    history_lines = ''
    if history_file_name not in os.listdir(merge_directory+'/History'):
        shutil.copyfile(f'{secondary_directory}History/{history_file_name}', f'{merge_directory}History/{history_file_name}') #Copies file
        history_lines = f'{history_file_name} did not exist in merge directory, copied file to correct location'
    
    else:
        if not is_identical_history_file(f'{secondary_directory}History/{history_file_name}', f'{merge_directory}History/{history_file_name}'):
            new_file_name = history_file_name.split('.')[0] + '_merged' + '.hist'
            shutil.copyfile(f'{secondary_directory}History/{history_file_name}', f'{merge_directory}History/{new_file_name}') #Copies file
            line = line.strip(history_file_name) + new_file_name

    return line, history_lines

def handle_data_file(line, merge_directory, secondary_directory):
    compatible_line = find_compatible(secondary_directory+line, merge_directory)[0] # Remember to add the function so more than 1 compatible file can be used
    compatible_line_folder = compatible_line.strip(merge_directory).strip(line)
    folder_name = ''

    # CHECK THAT COMPATIBLE LINE ONLY IS FILE NAME, NO FOLDER!

    if not compatible_line: 
        # Copy file to merged vgosDB  
        pass

    if is_same(line,compatible_line):
        # Return to top 
        return line
    elif is_identical(line, compatible_line):
        # Update history to indicate change of name
        return compatible_line
    elif is_equivalent(line, compatible_line):
        # Update history to indicate change of name
        return compatible_line
    else:
        if line in os.listdir(merge_directory+folder_name): 
            # Copy the secondary vgosDB datafile to the merged vgosDB with a unique name
            # Add to wrapper
            # Update history
            pass
        else: 
            # Copy the secondary vgosDB datafile 
            # Write to wrapper
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

    ## This is for case 1
    # wrapper_file_name = wrapper_file.split('/')[-1]
    # if wrapper_file_name in os.listdir(merge_directory):
    #     if is_equivalent_wrapper(merge_directory+wrapper_file_name, merge_directory+wrapper_file_name):
    #         print("Equivalent wrapper found")
    #         return
    #     else: 
    #         print("Wrapper with same name found, but they are not equivalent!")
    #         return

    # For case 2
    lines_to_write_wrapper = []
    lines_to_write_history = []
    current_dir = Directory()
    
    for line in lines: 
        line = line.strip('\n')

        if is_beginning(line):
            current_dir.go_in("")

        elif is_end(line):
            current_dir.go_out()

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

        # elif is_data_file(line):
        #     # Line here will not work, we will need the whole path! 
        #     handle_data_file(line, merge_root_directory, secondary_root_directory)

        else:
            lines_to_write_wrapper.append(handle_wrapper_info(line))

if __name__ == '__main__':
    secondary_directory = 'NVI_data/20APR01XA/'
    merge_directory = 'NVI_data/20APR01XA/'
    wrapper_files = find_wrapper_files(secondary_directory)
    wrapper_files.sort(reverse=True)
    for wrapper_file in wrapper_files: 
        main(wrapper_file, merge_directory, secondary_directory)
        quit()