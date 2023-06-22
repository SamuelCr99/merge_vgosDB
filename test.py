from vgos_db_same import is_same
from vgos_db_identical import is_identical
from vgos_db_equivalent import is_equivalent
from vgos_db_plug_compatible import find_compatible
from wrapper_same import is_same_wrapper
from wrapper_equivalent import is_equivalent_wrapper

path = "test_data/netCDF_files/"
A_path = "test_data/netCDF_files/Antenna.nc"

same_files = ["Antenna"]
not_same_files = ["Antenna_V001","Antenna_V002","Antenna_V003","Antenna_V004","Eccentricity"]

identical_files = ["Antenna","Antenna_V001"]
not_identical_files = ["Antenna_V002","Antenna_V003","Antenna_V004","Eccentricity"]

equivalent_files = ["Antenna","Antenna_V001","Antenna_V002","Antenna_V003"]
not_equivalent_files = ["Antenna_V004","Eccentricity"]

plug_compatible_files = ["Antenna","Antenna_V001","Antenna_V002","Antenna_V003","Antenna_V004"]
not_plug_compatible_files = ["Eccentricity"]

# Same file checks
for file in same_files:
    if not is_same(A_path, f"{path}{file}.nc"):
        print(f"Same file fail: {file}")

for file in not_same_files:
    if is_same(A_path, f"{path}{file}.nc"):
        print(f"Not same file fail: {file}")

# Identical file checks
for file in identical_files:
    if not is_identical(A_path, f"{path}{file}.nc"):
        print(f"Identical file fail: {file}")

for file in not_identical_files:
    if is_identical(A_path, f"{path}{file}.nc"):
        print(f"Not identical file fail: {file}")

# Equivalent file checks
for file in equivalent_files:
    if not is_equivalent(A_path, f"{path}{file}.nc"):
        print(f"Equivalent file fail: {file}")

for file in not_equivalent_files:
    if is_equivalent(A_path, f"{path}{file}.nc"):
        print(f"Not equivalent file fail: {file}")

# Plug compatible file checks
found_plug_compatible_files_raw = find_compatible(A_path,path[0:-1])
found_plug_compatible_files = []
for file in found_plug_compatible_files_raw:
    found_plug_compatible_files.append(file.split("\\")[-1][0:-3])

for file in plug_compatible_files:
    if file not in found_plug_compatible_files:
        print(f"Plug compatible file fail: {file}")
for file in not_plug_compatible_files:
    if file in found_plug_compatible_files:
        print(f"Not plug compatible file fail: {file}")
if len(found_plug_compatible_files) != len(plug_compatible_files):
    print("Plug compatible file error: Different length of lists")