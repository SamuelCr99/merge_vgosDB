import netCDF4 as nc
import sys
from vgos_db_identical import is_identical


def is_same(primary_file, secondary_file):
    if primary_file.split('/')[-1] != secondary_file.split('/')[-1]:
        return False

    return is_identical(primary_file,secondary_file)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        s1 = "NVI_data/20APR01XA/Apriori/Antenna.nc"
        s2 = "NVI_data/20APR01XA/Apriori2/Antenna.nc"
        print(is_same(s1, s2))

    else:
        print(is_same(sys.argv[1], sys.argv[2]))
