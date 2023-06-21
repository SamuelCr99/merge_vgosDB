import netCDF4 as nc
import sys

# Is "Stub" necessarily meta?
META_VARS = ["Stub", "CreateTime","CreatedBy","Program","DataOrigin","TimeTag","TimeTagFile","Session","Band","Station","Subroutine","History","vgosDB_Version"]

def is_equivalent(file1,file2):

    ds1 = nc.Dataset(file1)
    ds2 = nc.Dataset(file2)

    if str(ds1.variables) != str(ds2.variables):
        return False
    
    for var in ds1.variables:
        if var in META_VARS:
            continue
        if (ds1[var][:] != ds2[var][:]).any():
            return False

    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        s1 = "NVI_data/20APR01XA/Apriori/Antenna.nc"
        s2 = "NVI_data/20APR01XA/Apriori2/Antenna.nc"
        print(is_equivalent(s1, s2))

    else:
        print(is_equivalent(sys.argv[1], sys.argv[2]))