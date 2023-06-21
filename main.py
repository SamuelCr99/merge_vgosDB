import netCDF4 as nc

ds = nc.Dataset('data/20APR01XA/Apriori/Antenna.nc')

# print(ds['AntennaStationList'][:])

# for item in ds['AntennaStationList']:
#     print(item)


# for var in ds.variables:
#     print(var)
#     print(ds[var][::])

# print('------')

# for attr in ds.dimensions: 
#     print(attr)

# for dim in ds.dimensions.values():
#     print(dim)

# for var in ds.variables.values():
#     print(var)

# print(ds['Stub'][:].tobytes())

for variable in ds.variables:
    print(f'{variable}: {ds[variable][:].tobytes()}')