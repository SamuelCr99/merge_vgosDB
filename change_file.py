import netCDF4 as nc

ds = nc.Dataset('NVI_data/20APR01XA/Apriori/Antenna.nc', 'a')
ds2 = nc.Dataset('NVI_data/20APR01XA/Apriori2/Antenna.nc')

# ds['Stub'][:] = ['A', 'n', 't', 'e','n','n','a']
ds['Stub'][:] = ['A', 'a', 't', 'e','n','n','a']
x1 = (ds['Stub'][:])
x2 = (ds2['Stub'][:])
print(x1==x2)
