import netCDF4 as nc

ds = nc.Dataset('test_data/DB_orig/Apriori/Antenna.nc', 'a')

# ds['CreateTime'][:] = ['2','0','2','3','/','0','6','/','2','2',' ','0','9',':','2','0',':','1','8',' ','U','T','C']

# ds['AntennaAxisType'].CreateTime = "2023/06/22 09:20:18 UTC"

# ds['AntennaAxisType'][:] = ['\\','x','9','9','\\','x','0','0','\\','x','0','3','\\','x','0','0','\\','x','0','4','\\','x','0','0','\\','x','0','3','\\','x','0','0','\\','x','0','3','\\','x','0','0']
# ds['AntennaStationList'][:] = [['H','E','J','H','E','J','H','E'],['H','E','J','H','E','J','H','E'],['H','E','J','H','E','J','H','E'],['H','E','J','H','E','J','H','E'],['H','E','J','H','E','J','H','E']]

ds['Stub'][:] = ['A','n','t','e','n','n','a']