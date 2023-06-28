import netCDF4 as nc
import sys
from utility.vgos_db_same import is_same
from utility.Directory import Directory


def extract_paths(lines):
    """
    Finds paths to files referenced in wrapper file

    Parameters:
    lines(list): List of lines read from wrapper file

    Returns:
    Returns a list of file paths to all files referenced in wrapper file
    """
    paths = []
    dir = Directory()
    for line in lines:
        if line[0] == "!" or line[0] == "#" or line[0] == "/":
            continue
        elif line[0:5].lower() == "begin":
            dir.go_in("")
        elif line[0:3].lower() == "end":
            dir.go_out()
        elif line[0:11].lower() == 'default_dir':
            dir.go_out()
            dir.go_in(line[12:-1])
        elif '.nc' in line and " " not in line:
            paths.append(dir.get_path_with_slash() + line.strip("\n"))
    return paths


def is_same_wrapper(primary_file, secondary_file):
    """
    Answers if two wrapper files are vgosDB same

    Checks if they contain the same files, and of those files are vgosDB same

    Parameters:
    primary_file (str): Path to one of the wrappers
    secondary_file (str): Path to the other wrapper

    Returns:
    True if the wrappers are the same, False if not
    """
    primary_path = '/'.join(primary_file.split('/')[0:-1]) + '/'
    secondary_path = '/'.join(secondary_file.split('/')[0:-1]) + '/'

    with open(primary_file) as file:
        primary_file_lines = file.readlines()

    with open(secondary_file) as file:
        secondary_file_lines = file.readlines()

    # Get the paths to all files in the wrappers
    extracted_primary_paths = extract_paths(primary_file_lines)
    extracted_secondary_paths = extract_paths(secondary_file_lines)

    # If there aren't the same number of files, the wrappers aren't the same
    if len(extracted_primary_paths) != len(extracted_secondary_paths):
        return False

    # Find each file from one DB in the other, otherwise not same
    for path in extracted_primary_paths:
        if path not in extracted_secondary_paths:
            return False

        # Found files also need to be the same
        if not is_same(primary_path+path, secondary_path+path):
            return False

    return True
