####################
    Scripts needed
####################

Script which lists all plug-compatible files in a directory, should return a list
of .netCDF files which are plug compatible. 

Utility for finding: 
    vgosDB-same
    vgosDB-identical
    vgosDB-equivalent

same: Same file name and content, including meta content. 
identical: Same content including meta content (i.e. not necessarily same name). 
equivalent: Same content, excluding meta content, 
plug compatible: Same stub

Routine for merging vgosDB folder: 
1. Check if wrappers with same name are equivalent, if equivalent do nothing, if
   not equivalent give a warning, this should not happen. 
2. If wrappers do not share name, open both wrapper files, the destination file 
   should be in write mode and the secondary wrapper in read mode. Also open a 
   history file to document which changes have been made. Then follow the following 
    


Script for adding merged folder to data center (Do later)



################################
    Testing - coroutines
################################

Files needed:
    A: Original netCDF-file (Antenna.nc)
    B: A file that is identical to A, but with a different name (e.g. diff. v) (Antenna_V001.nc)
    C: A file that is equivalent to A, but with different meta data (1st vars) (Antenna_V002.nc)
    D: A file that is equivalent to A, but with different attributes (Antenna_V003.nc)
    E: A file that is plug compatible to A, but with different data (Antenna_V004.nc)
    F: Non-plug compatible netCDF-file to A (Eccentricity.nc)
    G: A vgosDB containing (DB_orig)
        i. A wrapper (wrap.wrp)
        ii. File A
    H: A vgosDB containing (DB_equiv1)
        i. A wrapper equivalent to wrapper in G
        ii. File B
    I: A vgosDB containing (DB_equiv2)
        i. A wrapper equivalent to wrapper in G
        ii. File C
    J: A vgosDB containing (DB_non_comp)
        i. A wrapper not equivalent to wrapper in G (maybe missing files)

Tests to be done:
    Plug compatible:
        1. Given file A, can you find files A-E without picking up F?
    Same:
        1. Check if file A is same to file A
        2. Check if file A is not same as files B-F
    Equivalent:
        1. Check if A is equivalent to files A-D
        2. Check if A is not equivalent to files E and F
    Identical:
        1. Check if A is identical to files A and B
        2. Check if A is not identical to files C-F
    Wrapper equivalent:
        1. Check if G is equivalent to G-I
        2. Check if G is not equivalent to J
    Wrapper same:
        1. Check if G is same as G
        2. Check if G is not same as H-J


################################
    Testing - full algorithm    
################################

Cases to test:
    1. Check that wrappers with same name which are equivalent do not copy over
    a new wrapper file. 
    
    2. Check that wrapper with same name which is not equivalent throws a
    warning message. 

    3. Check that lines of directory are written to new wrapper correct
        i. directories that exists in both DBs
        ii. directories that only exist in secondary DB

    4. Check that lines of history files are written to new wrapper correct 

    5. Check that lines of data files are written to new wrapper correct
        i. files in root folder
        ii. files in sub directories
        iii. with and without having started a section
        iv. same files, identical files, equivalent files and other files

    6. Check that other lines are written to new wrapper correct 


File structure
    test_primary/wrapper1.wrp is equivalent to test_secondary/wrapper1.wrp
    test_primary/file1.nc is same as test_secondary/file1.nc
    test_primary/Folder1/file2.nc is equivalent to test_secondary/Folder1/file2.nc

    test_primary/wrapper2.wrp is not same as test_secondary/wrapper2.wrp
    test_primary/Folder2/file3.nc doesn't exist in test_secondary
    

Tests: 
Test 1 23/6 13:45, Case 1:
    Expected result: As all wrappers in secondary folder have an equivalent wrapper
    in merge location, no files should be moved and no new wrapper should be created, 
    there should be print statement stating what happened. 

    Result: Test worked as expected, no files were created and print statement 
    described what happened.  
    
Test 2 23/6 13:52, Case 2:
    Expected result: As there will be wrappers with the same name which are not 
    equivalent there should be a warning message. 

    Result: Found issue with code where incorrect files were compared, issue was 
    fixed, test now performs as expected.

Test 3 23/6 14:11, Case 3:
    Expected result: New wrapper file created in merge folder, this file should include
    pointers to all .nc files in their correct locations.

    Result: Test worked as expected, the new wrapper was created, a folder that
    didn't exist was created and a file was placed in the folder.

Test 4 23/6 14:46, Case 3:
    Expected result: Creates a history file and notes down that a directory
    needed to be created.

    Result: History file was created with wrong name, bug fixed.