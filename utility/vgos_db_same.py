from utility.vgos_db_identical import is_identical


def is_same(primary_file, secondary_file):
    """
    Checks if two netCDF files are vgosDB same

    Checks if the files have the same name, same variables, same values and same
    attributes

    Parameters:
    primary_file (str): One of the files
    secondary_file (str): The other file

    Returns:
    True if the files are vgosDB same, False otherwise
    """
    if primary_file.split('/')[-1] != secondary_file.split('/')[-1]:
        return False

    return is_identical(primary_file, secondary_file)
