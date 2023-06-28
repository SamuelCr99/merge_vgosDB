import netCDF4 as nc
import glob
import sys

def find_compatible(file_path,dir_path):
    """
    Finds all vgosDB plug compatible netCDF files in a directory

    Checks all files in a folder so they have the same stub (in their variables)
    as the reference file, and returns them
    
    Parameters:
    file_path (str): The file to check compatibility against
    dir_path (str): The folder with all files to check

    Returns:
    A list of the paths to all plug compatible files
    """
    ds1 = nc.Dataset(file_path)

    data_file_paths = glob.glob(f"{dir_path}/*.nc")

    # Needed if code is run on Windows
    data_file_paths_fixed = []
    for path in data_file_paths:
        data_file_paths_fixed.append(path.replace("\\","/"))

    plug_compatible_paths = []

    for data_file_path in data_file_paths_fixed:
        ds2 = nc.Dataset(data_file_path)
        
        if (ds1['Stub'][:].tobytes() != ds2['Stub'][:].tobytes()):
            continue

        plug_compatible_paths.append(data_file_path)

    return plug_compatible_paths