import netCDF4 as nc

ds = nc.Dataset('NVI_data/20APR01XA/Apriori/Antenna_V001.nc', 'a')
ds2 = nc.Dataset('NVI_data/20APR01XAV2/Apriori/Antenna_V001.nc')

ds['Stub'][:] = ['A', 'n', 't', 'e','n','n','a']
# ds['Stub'][:] = ['A', 'a', 't', 'e','n','n','a']
ds["AntennaAxisTilt"][:] = [0, 0]
print(ds["AntennaAxisTilt"][:] == ds2["AntennaAxisTilt"][:])
