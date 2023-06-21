import netCDF4 as nc

META_VARS = ["Stub","CreateTime","CreatedBy","Program","Subroutine","vgosDB_Version","DataOrigin","Session"]

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
    print(is_equivalent('data/20APR01XA/Apriori/Antenna.nc','data/20APR01XA/Apriori/Antenna.nc'))