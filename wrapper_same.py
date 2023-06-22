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
        s1 = "NVI_data/20APR01XA/20APR01XA_V002_iGSFC_kall.wrp"
        s2 = "NVI_data/20APR01XAV2/20APR01XA_V002_iGSFC_kall.wrp"
        print(is_same_wrapper(s1, s2))

    else:
        print(is_same_wrapper(sys.argv[1], sys.argv[2]))