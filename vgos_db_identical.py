import netCDF4 as nc
import sys


def is_identical(primary_file, secondary_file):
    primary_ds = nc.Dataset(primary_file)
    secondary_ds = nc.Dataset(secondary_file)

    if str(primary_ds.variables) != str(secondary_ds.variables):
        return False

    for variable in primary_ds.variables: 
        if (primary_ds[variable][:] != secondary_ds[variable][:]).any():
            return False

    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        s1 = "NVI_data/20APR01XA/Apriori/Antenna.nc"
        s2 = "NVI_data/20APR01XA/Apriori2/Antenna.nc"
        print(is_identical(s1, s2))

    else:
        print(is_identical(sys.argv[1], sys.argv[2]))