import netCDF4 as nc
import sys
from vgos_db_same import is_same
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
    prefix = ""
    program_prefix = ""
    for line in lines: 
        if "Begin Program" in line:
            program_prefix = line.strip("Begin Program ").strip('\n')
            program_prefix += '/'
        elif line[0] == "!" and len(line) == 2:
            prefix = ""
        elif 'Default_Dir' in line:
            prefix = line.strip('Default_Dir ').strip('\n')
            prefix += '/'
        elif '.nc' in line and " " not in line:
            line = line.strip("\n")
            paths.append(program_prefix+prefix + line)
    return paths

def is_same_wrapper(primary_file, secondary_file):
    primary_path = '/'.join(primary_file.split('/')[0:-1]) + '/'
    secondary_path = '/'.join(secondary_file.split('/')[0:-1]) + '/'

    with open(primary_file) as file:
        primary_file_lines = file.readlines()
        
    with open(secondary_file) as file:
        secondary_file_lines = file.readlines()

    extracted_primary_paths = extract_paths(primary_file_lines)
    extracted_secondary_paths = extract_paths(secondary_file_lines)

    if len(extracted_primary_paths) != len(extracted_secondary_paths):
        return False

    for path in extracted_primary_paths:
        if path not in extracted_secondary_paths:
            return False
        
        if not is_same(primary_path+path, secondary_path+path):
            return False

    return True



if __name__ == '__main__':
    if len(sys.argv) < 3:
        s1 = "NVI_data/20APR01XA/20APR01XA_V005_iGSFC_kall.wrp"
        s2 = "NVI_data/20APR01XAV2/20APR01XA_V005_iGSFC_kall.wrp"
        print(is_same_wrapper(s1, s2))

    else:
        print(is_same_wrapper(sys.argv[1], sys.argv[2]))