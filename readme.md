# Merge vgosDB 

## Description

A utility for merging two vgosDBs together. The program was developed at NVI Inc. by Filip Herbertsson and Samuel Collier Ryder during a summer internship in 2023.

### Method

When run, the program goes through each of the wrappers in one database and creates a new wrapper in the other database, unless the same wrapper is already there. When it goes through each wrapper, all dependencies (i.e. netCDF files and history files) are identified. The history files are copied over as they are, unless the same history file already exists in the folder that the databases are merged into. In order to avoid overwriting files, the file name is sometimes changed. For the netCDF files, the process goes as follows:

1. If a file that is equivalent to the current file already exists in the folder that the databases merge into, it doesn't copy the file. Instead, it writes the file it found to the wrapper. That the files are equivalent means that all variables that contain measured data are the same, but not necessarily attributes or variables containing meta-data. All functions/programs using the data in the netCDF file should thus still give the same output.
2. If no equivalent file is found, it copies over the netCDF file. As before, the file name is sometimes changed to avoid overwriting files.

Each wrapper that is written gets a new history file assigned to it, which describes all the modifications that were necessary in order to merge the databases.

## How to install

You can clone the GitHub repository and install the required libraries manually with

```bash
$ git clone https://github.com/SamuelCr99/merge_vgosDB.git
$ pip -r requirements.txt
```

## How to use

Merge vgosDB is used by running the script `merge_vgosDB.py` with

```bash
$ python3 merge_vgosDB.py <filepath_merge_db> <filepath_secondary_db> <name_executer>
```

Write `python` instead of `python3` if running code on Windows. The filepaths can either be paths to directories or to files ending in .tgz or .tar.xz. These paths can be given as either relative or absolute. When specifying directories, the program will merge the secondary directory into the merge directory. When specifying zipped files, the program will overwrite the first file.

Example: 
```bash
$ python3 merge_vgosDB example/GSFC_data/20230315-r41094 example/BKG_data/20230315-r41094 "NVI Inc."
```

When merging databases using a script, include the method `merge_vgosDB()` with

```python
from merge_vgosDB.merge_vgosDB import merge_vgosDB
```

and supply the method with the same parameters as before.

## Acknowledgements

This project contains data supplied by the Federal Agency for Cartography and Geodesy of Germany and NASA Goddard Space Flight Center. The manual for vgosDB, as well as the general layout of this project, were both written by John Gipson.
