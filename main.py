import netCDF4 as nc

ds = nc.Dataset('test_data/g_data/20230616-i23167/KOKEE/Dis-OceanLoad.nc')
ds2 = nc.Dataset('test_data/g_data/20230616-i23167/KOKEE/Dis-OceanLoad_V001.nc')
print(ds.variables['CreatedBy'][:])

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

# for variable in ds.variables:
#     print(f'{variable}: {ds[variable][:].tobytes()}')

# for variable in ds.variables:
#     if variable == "AntennaAxisType":
#         print(f'{variable}: {ds[variable].CreateTime}')

# print(ds.variables)