import netCDF4 as nc

META_VARS = ["Stub", "CreateTime", "CreatedBy", "Program", "DataOrigin", "TimeTag",
             "TimeTagFile", "Session", "Band", "Station", "Subroutine", "History", "vgosDB_Version"]


def is_equivalent(file1, file2):
    """
    Checks if two netCDF files are vgosDB equivalent

    Checks if the files have the same variables, except meta variables

    Parameters:
    file1 (str): One of the files
    file2 (str): The other file

    Returns:
    True if the files are vgosDB equivalent, False otherwise
    """
    ds1 = nc.Dataset(file1)
    ds2 = nc.Dataset(file2)

    for var in ds1.variables:
        if var in META_VARS:
            continue
        if var not in ds2.variables:
            return False
        if ds1[var][:].tolist() != ds2[var][:].tolist():
            return False

    return True
