from vgos_db_equivalent import is_equivalent
from vgos_db_plug_compatible import find_compatible
from vgos_db_identical import is_identical
from vgos_db_same import is_same
from wrapper_equivalent import is_equivalent_wrapper
from history_file_identical import is_identical_history_file
import os
import shutil
from Directory import Directory

def get_version_num(v):
    if v<10:
        return f"00{v}"
    elif v<100:
        return f"0{v}"
    else:
        return f"{v}"

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
            v = 1
            while f"{history_file_name[:-5]}_v{get_version_num(v)}.hist" in os.listdir(merge_directory+'/History'):
                v+=1
            new_file_name = history_file_name.split('.')[0] + f"_v{get_version_num(v)}.hist"
            shutil.copyfile(f'{secondary_directory}History/{history_file_name}', f'{merge_directory}History/{new_file_name}') #Copies file
            line = line.strip(history_file_name) + new_file_name

    return line, history_lines

def handle_data_file(line, merge_directory, secondary_directory):
    compatible_lines = find_compatible(secondary_directory+line, merge_directory[:-1])

    file_name = line
    file_path = secondary_directory+line

    # CHECK THAT COMPATIBLE LINE ONLY IS FILE NAME, NO FOLDER!
    if not compatible_lines: 
        shutil.copyfile(f'{secondary_directory}{file_name}', f'{merge_directory}{file_name}') #Copies file
        history_line = f'No compatible files found for: {secondary_directory}{file_name}, creating new file' 
        return line, history_line


    for compatible_line in compatible_lines:
        if is_same(file_path,compatible_line):
            return line, ''

    
    for compatible_line in compatible_lines:
        if is_identical(file_path, compatible_line):
            history_line = f'{secondary_directory+file_name} has been changed to {secondary_directory+compatible_line}'
            return compatible_line.split("/")[-1], history_line

    
    for compatible_line in compatible_lines:
        if is_equivalent(file_path, compatible_line):
            history_line = f'{secondary_directory+file_name} has been changed to {secondary_directory+compatible_line}'
            return compatible_line.split("/")[-1], history_line


    if file_name in os.listdir(merge_directory):
        old_file_name = file_name
        v = 1
        while file_name[:-3] + f"_v{get_version_num(v)}.nc" in os.listdir(merge_directory):
            v+=1
        file_name = file_name[:-3] + f"_v{get_version_num(v)}.nc"
        shutil.copyfile(f'{secondary_directory}{file_name}', f'{merge_directory}{file_name}') #Copies file
        history_line = f'No file same, identical or equivalent for {old_file_name}, but name already existed, updating name to {file_name}'
        return file_name, history_line

    else: 
        shutil.copyfile(f'{secondary_directory}{file_name}', f'{merge_directory}{file_name}') #Copies file
        history_line = f'No file is same, identical or equivalent for {file_name}. Copied it over.'
        return file_name, history_line


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
        wrapper_lines = file.readlines()

    # # This is for case 1
    # wrapper_file_name = wrapper_file.split('/')[-1]
    # if wrapper_file_name in os.listdir(merge_directory):
    #     if is_equivalent_wrapper(merge_directory+wrapper_file_name, merge_directory+wrapper_file_name):
    #         print("Equivalent wrapper with same name found, no need to copy files")
    #         return
    #     else: 
    #         print("Wrapper with same name found, but they are not equivalent!")
    #         return

    # For case 2
    lines_to_write_wrapper = []
    lines_to_write_history = []
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
            return_values = handle_data_file(line, merge_directory + current_dir.get_path_with_slash(), secondary_directory + current_dir.get_path_with_slash())
            lines_to_write_wrapper.append(return_values[0])
            if return_values[1]:
                lines_to_write_history.append(return_values[1])

        else:
            lines_to_write_wrapper.append(handle_wrapper_info(line))

    for l in lines_to_write_wrapper:
        print(l)
    print('------')
    for l in lines_to_write_history:
        print(l)

if __name__ == '__main__':
    secondary_directory = 'test_data/DB_equiv_1/'
    merge_directory = 'test_data/DB_orig/'
    wrapper_files = find_wrapper_files(secondary_directory)
    wrapper_files.sort(reverse=True)
    for wrapper_file in wrapper_files: 
        main(wrapper_file, merge_directory, secondary_directory)
        quit()