from utility.vgos_db_equivalent import is_equivalent
from utility.vgos_db_plug_compatible import find_compatible
from utility.vgos_db_identical import is_identical
from utility.vgos_db_same import is_same
from utility.wrapper_equivalent import is_equivalent_wrapper
from utility.history_file_identical import is_identical_history_file
from utility.Directory import Directory
import shutil
import warnings
import glob
import datetime
import os
import tarfile
import argparse

VERSION = 1.0

def find_history_file_name(old_file_name, merge_directory):
    """
    Finds the correct name for a history file. This name should depend on the 
    version number of the other files in the directory.
    """
    history_file_names = "\t".join(os.listdir(f'{merge_directory}History'))
    file_name_stub = old_file_name.split('_')[0]

    # Sort out the flags (except version)
    flags = old_file_name.strip(".hist").split("_")[1:]
    flags_reduced = []
    for flag in flags:
        if flag[0].lower() != "v":
            flags_reduced.append(f"_{flag}")

    # Find the correct version number
    v = 0
    while f"_V{get_version_num(v)}" in history_file_names:
        v += 1

    # Return new name
    return f"{file_name_stub}_V{get_version_num(v)}{''.join(flags_reduced)}.hist"


def find_data_file_name(old_file_name, merge_directory):
    """
    Finds the correct name for a data file. This name should depend on the 
    version number of the other files in the directory.
    """
    file_name_stub = old_file_name.split("_")[0].split(".")[0]

    # Get the names of all plug-compatible files
    data_file_paths = glob.glob(f"{merge_directory}{file_name_stub}*.nc")
    data_file_names = []
    for path in data_file_paths:
        data_file_names.append(os.path.basename(path))

    # Sort out the flags (except version)
    flags = old_file_name.strip(".nc").split("_")[1:]
    flags_reduced = []
    for flag in flags:
        if flag[0].lower() != "v":
            flags_reduced.append(f"_{flag}")

    # Find the correct version number
    v = 1
    while f"_V{get_version_num(v)}" in data_file_names:
        v += 1

    # Return new name
    return f"{file_name_stub}_V{get_version_num(v)}{''.join(flags_reduced)}.nc"


def get_version_num(v):
    """
    Formats number to 3 digit string 
    """
    if v < 10:
        return f"00{v}"
    elif v < 100:
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
        history_lines = f"New directory: {directory_name} did not exist, now created."
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

    # If there is no history file with the given name, we can copy it over
    if history_file_name not in os.listdir(merge_directory+'/History'):
        shutil.copy2(f'{secondary_directory}History/{history_file_name}',
                     f'{merge_directory}History/{history_file_name}')
        history_lines = f'Copy history: {history_file_name} did not exist in merge directory, copied file.'

    else:
        new_history_file_name = is_identical_history_file(
            f'{secondary_directory}History/{history_file_name}', f'{merge_directory}History/')

        # If no identical history files exist, we copy the file with a different name
        if not new_history_file_name:
            # Finds a file name with correct version number
            new_file_name = find_history_file_name(
                history_file_name, merge_directory)
            shutil.copy2(f'{secondary_directory}History/{history_file_name}',
                         f'{merge_directory}History/{new_file_name}')
            line = line.strip(history_file_name) + new_file_name
            history_lines = f'Copy history: {history_file_name} did not exist in merge directory, but name was taken. Copied file with name {new_file_name}.'

        # If there exists a file with the same contents and a different name, we need to change the name
        elif new_history_file_name != history_file_name:
            line = line.strip(history_file_name) + new_history_file_name
            history_lines = f'Identical history: {history_file_name} changed name to {new_history_file_name}.'

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
    compatible_paths = find_compatible(
        secondary_directory+line, merge_directory[:-1])

    file_name = line
    file_path = secondary_directory+line

    # When no plug-compatible files are there, we can just copy over the data file
    if not compatible_paths:
        shutil.copy2(f'{secondary_directory}{file_name}',
                     f'{merge_directory}{file_name}')
        history_line = f'Copy file: No compatible files found for {current_dir}{file_name}, copied file.'
        return line, history_line

    # If there exists a file that is the same, we don't need to copy anything
    for compatible_line in compatible_paths:
        if is_same(file_path, compatible_line):
            return line, ''

    # If there exists a file that is the identical, we want that one instead
    for compatible_line in compatible_paths:
        if is_identical(file_path, compatible_line):
            new_file_name = compatible_line.split("/")[-1]
            history_line = f'Identical file found: {current_dir}{file_name} has been changed to {current_dir}{new_file_name}.'
            return new_file_name, history_line

    # If there exists a file that is equivalent, we want that one instead
    for compatible_line in compatible_paths:
        if is_equivalent(file_path, compatible_line):
            new_file_name = compatible_line.split("/")[-1]
            # Equivalent files might or might not have the same name
            if file_name == new_file_name:
                history_line = f'Equivalent file found: {current_dir}{file_name}, did not copy old file.'
            else:
                history_line = f'Equivalent file found: {current_dir}{file_name} has been substituted with {current_dir}{new_file_name}.'
            return new_file_name, history_line

    # If we reach this, our only option is to copy the file (as there is no
    # other file we can choose). If there is a file with the same name, we need
    # to change it.
    if file_name in os.listdir(merge_directory):
        old_file_name = file_name
        # Finds a file name with a correct version number
        file_name = find_data_file_name(old_file_name, merge_directory)
        shutil.copy2(f'{secondary_directory}{old_file_name}',
                     f'{merge_directory}{file_name}')
        history_line = f'Copy file: No file same, identical or equivalent for {current_dir}{old_file_name}, but name already existed. Updating name to {current_dir}{file_name}.'
        return file_name, history_line

    else:
        shutil.copy2(f'{secondary_directory}{file_name}',
                     f'{merge_directory}{file_name}')
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


def create_new_wrapper(wrapper_file, merge_directory, secondary_directory, who):
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

    # If there is an equivalent wrapper already, we don't need to copy it
    wrapper_file_name = wrapper_file.split('/')[-1]
    if wrapper_file_name in os.listdir(merge_directory):
        if is_equivalent_wrapper(merge_directory+wrapper_file_name,
                                 secondary_directory+wrapper_file_name):
            return
        else:
            # Happens if there is a wrapper with the same name but not the same
            # content. Should not be possible.
            warnings.warn(
                f"Wrapper with the same name found, but they are not equivalent! Wrapper ignored: {wrapper_file_name}")
            return

    # When there is no equivalent wrapper, we need to write a new one
    lines_to_write_wrapper = []
    lines_to_write_history = []
    now = datetime.datetime.utcnow()
    lines_to_write_history.append(f"""
TIMETAG {now.strftime('%Y/%m/%d %H:%M:%S')} UTC

merge_vgosDB v{VERSION}
Merging  {wrapper_file_name} into  vgosdB {merge_directory.split('/')[-2]}
Run by {who}
""")
    current_dir = Directory()

    # Goes through each line and finds specific keywords which triggers events
    # that change the line in the wrapper and writes to the history file.
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
            return_values = handle_directory(
                line, merge_directory + current_dir.get_path())
            current_dir.go_in(line.split(" ")[1])
            lines_to_write_wrapper.append(return_values[0])
            if return_values[1]:
                lines_to_write_history.append(return_values[1])

        elif is_history_file(line):
            return_values = handle_history_file(
                line, merge_directory, secondary_directory)
            lines_to_write_wrapper.append(return_values[0])
            if return_values[1]:
                lines_to_write_history.append(return_values[1])

        elif is_data_file(line):
            return_values = handle_data_file(
                line,merge_directory + current_dir.get_path_with_slash(),
                secondary_directory + current_dir.get_path_with_slash(),
                current_dir.get_path_with_slash())
            lines_to_write_wrapper.append(return_values[0])
            if return_values[1]:
                lines_to_write_history.append(return_values[1])

        else:
            lines_to_write_wrapper.append(line)

    if len(lines_to_write_history) > 1:
        # Make the history directory if there isn't one
        if 'History' not in os.listdir(merge_directory):
            os.mkdir(f'{merge_directory}History')

        # Get a reasonable name for the history file
        history_file_names = "\t".join(os.listdir(f'{merge_directory}History'))
        v = 0
        while f"_V{get_version_num(v)}" in history_file_names:
            v += 1
        merge_history_file_name = f"{merge_directory.split('/')[-2]}_V{get_version_num(v)}_kvgosDBmerge.hist"

        # Add to the history section of the merged wrapper
        end_history_index = [i for i, elem in enumerate(
            lines_to_write_wrapper) if 'end history' in elem.lower()][0]
        now = datetime.datetime.utcnow()
        if lines_to_write_wrapper[end_history_index-1][0] != "!":
            lines_to_write_wrapper.insert(end_history_index-1, "!")
            end_history_index += 1
        process_text = f"""Begin Process merge_vgosDB
Version {VERSION}
CreatedBy {who}
Default_dir History
RunTimeTag {now.strftime('%Y/%m/%d %H:%M:%S')} UTC
{merge_history_file_name}
End Process merge_vgosDB
!"""
        lines_to_write_wrapper.insert(end_history_index, process_text)

        # Write the history file
        with open(f"{merge_directory}History/{merge_history_file_name}", 'x') as f:
            f.writelines("\n".join(lines_to_write_history))

    # Write the wrapper
    with open(merge_directory+wrapper_file_name, 'x') as f:
        f.writelines("\n".join(lines_to_write_wrapper))


def merge_vgosDB(merge_directory, secondary_directory, who):
    """
    Finds all wrapper files in secondary directory and moves them over to the 
    merge directory

    Parameters: 
    merge_directory(str): File path to the directory where files should be 
    merged to. 

    secondary_directory(str): File path of the directory where files should be
    merged from.

    who(str): Person/Institution performing the merge.

    Returns: 
    No return values
    """
    merge_is_zip = "tgz" in merge_directory.split(
        ".")[-1] or "xz" in merge_directory.split(".")[-1]
    secondary_is_zip = "tgz" in secondary_directory.split(
        ".")[-1] or "xz" in secondary_directory.split(".")[-1]

    if merge_is_zip:
        # Unzip the files and update directory paths
        with tarfile.open(merge_directory, 'r') as mergeZip:
            mergeZip.extractall('merge_temp')
        merge_folder_name = merge_directory.split('/')[-1].split('.')[0]
        old_merge_directory = merge_directory
        merge_directory = f'merge_temp/{merge_folder_name}'

    if secondary_is_zip:
        with tarfile.open(secondary_directory, 'r') as secondaryZip:
            secondaryZip.extractall('secondary_temp')
        secondary_folder_name = secondary_directory.split('/')[-1].split('.')[0]
        secondary_directory = f'secondary_temp/{secondary_folder_name}'

    # Make sure paths always end with a /
    if merge_directory[-1] != '/':
        merge_directory += '/'
    if secondary_directory[-1] != '/':
        secondary_directory += '/'

    # Create a new wrapper for each wrapper in the second directory
    wrapper_files = find_wrapper_files(secondary_directory)
    wrapper_files.sort()
    for wrapper_file in wrapper_files:
        create_new_wrapper(wrapper_file, merge_directory,
                           secondary_directory, who)

    if merge_is_zip:
        # Zip up the merge directory
        with tarfile.open(old_merge_directory, 'w:xz') as mergeZip:
            mergeZip.add('merge_temp', arcname=os.path.basename(''))
        shutil.rmtree('merge_temp')

    if secondary_is_zip:
        shutil.rmtree('secondary_temp')


if __name__ == '__main__':
    help_text = """
    Merge vgosDB
    Merges a vgosDB (secondary database) into another (merged database).
    
    usage: merge_vgosDB filepath_merge_db filepath_secondary_db name_executer
    """
    parser = argparse.ArgumentParser(
                prog='Merge vgosDB',
                description='Utility for merging two vgosDB folders')

    parser.add_argument('merge_dir', type=str, help="session directory to merge into")
    parser.add_argument('secondary_dir', type=str, help="session directory to merge from")
    parser.add_argument('--who', default="unknown", help="name of the person/group running the script")
    args = parser.parse_args()
    merge_vgosDB(args.merge_dir, args.secondary_dir, args.who)
