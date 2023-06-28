import netCDF4 as nc
import sys
from vgos_db_equivalent import is_equivalent
import os

def extract_paths(lines):
    """
    Finds paths to files referenced in wrapper file

    Parameters:
    lines(list): List of lines read from wrapper file

    Returns:
    Returns a list of file paths to all files referenced in wrapper file
    """
    paths = []
    default_dir = []
    for line in lines: 
        if line[0] == "!" or line[0] == "#" or line[0] == "/":
            continue
        elif line[0:5].lower() == "begin":
            default_dir.append("")
        elif line[0:3].lower() == "end":
            default_dir.remove(default_dir[-1])
        elif line[0:11].lower() == 'default_dir':
            default_dir_tmp = line[12:-1]
            default_dir_tmp += '/'
            default_dir[-1] = default_dir_tmp
        elif '.nc' in line and " " not in line:
            line = line.strip("\n")
            paths.append("/".join(filter(lambda x: x, default_dir)) + line)
    return paths

def is_equivalent_wrapper(primary_file, secondary_file):
    """
    Answers if two wrapper files are vgosDB equivalent

    Checks if the wrappers have a one-to-one correspondence of vgosDB equivalent
    data files

    Parameters:
    primary_file (str): Path to one of the wrappers
    secondary_file (str): Path to the other wrapper

    Returns:
    True if the wrappers are equivalent, False if not
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

    # If there aren't the same number of files, the wrappers aren't equivalent
    if len(extracted_primary_paths) != len(extracted_secondary_paths):
        return False

    # Find each file from one DB in the other, otherwise not equivalent
    for path in extracted_primary_paths:
        nonFound = True
        for path2 in extracted_secondary_paths:

            # Found files also need to be equivalent
            if is_equivalent(primary_path+path, secondary_path+path2):
                nonFound = False
                # Need a one-to-one correspondence
                extracted_secondary_paths.remove(path2)
                break
        if nonFound:
            return False

    return True