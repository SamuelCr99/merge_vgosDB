import netCDF4 as nc
import glob
import sys

def find_compatible(file_path,dir_path):

    ds1 = nc.Dataset(file_path)

    data_file_paths = glob.glob(f"{dir_path}/*.nc")

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

if __name__ == '__main__':
    if len(sys.argv) < 3:
        s1 = "NVI_data/20APR01XA/Apriori/Antenna.nc"
        s2 = "NVI_data/20APR01XA/Apriori"
        print(find_compatible(s1, s2))

    else:
        print(find_compatible(sys.argv[1], sys.argv[2]))