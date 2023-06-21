import netCDF4 as nc

def is_equivalent(file1,file2):

    ds1 = nc.Dataset(file1)
    ds2 = nc.Dataset(file2)

    if str(ds1.variables) != str(ds2.variables):
        return False

    return True

if __name__ == '__main__':
    print(is_equivalent('data/20APR01XA/Apriori/Antenna.nc','data/20APR01XA/Apriori/Antenna.nc'))