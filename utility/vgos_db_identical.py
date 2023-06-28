import netCDF4 as nc


def is_identical(primary_file, secondary_file):
    """
    Checks if two netCDF files are vgosDB identical

    Checks if the files have the same variables, same values and same
    attributes

    Parameters:
    primary_file (str): One of the files
    secondary_file (str): The other file

    Returns:
    True if the files are vgosDB identical, False otherwise
    """
    primary_ds = nc.Dataset(primary_file)
    secondary_ds = nc.Dataset(secondary_file)

    # Checks the names of the variables
    if str(primary_ds.variables) != str(secondary_ds.variables):
        return False

    # Checks values and attributes for each variable
    for variable in primary_ds.variables:
        if (primary_ds[variable][:] != secondary_ds[variable][:]).any():
            return False
        for attr in primary_ds[variable].ncattrs():
            if attr not in secondary_ds[variable].ncattrs():
                return False
            else:
                if getattr(primary_ds[variable], attr) != getattr(secondary_ds[variable], attr):
                    return False
        if primary_ds[variable].dimensions != secondary_ds[variable].dimensions:
            return False

    return True
