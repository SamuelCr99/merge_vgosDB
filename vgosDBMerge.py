import glob
from wrapper_equivalent import is_equivalent_wrapper
from vgos_db_plug_compatible import find_compatible
from vgos_db_same import is_same
import sys
import os


def merge(secondary_path,merged_path):
    # Path entries should not contain / at the end
    if secondary_path[-1] == '/': secondary_path = secondary_path[:-1]
    if merged_path[-1] == '/': merged_path = merged_path[:-1]

    secondary_wrappers = glob.glob(f"{secondary_path}/*.wrp")
    merged_wrappers = glob.glob(f"{merged_path}/*.wrp")

    for secondary_wrapper in secondary_wrappers:
        secondary_wrapper_name = secondary_wrapper.split('/')[-1]

        ignore_wrapper = False

        for merged_wrapper in merged_wrappers:
            merged_wrapper_name = merged_wrapper.split('/')[-1]
            if merged_wrapper_name == secondary_wrapper_name:
                ignore_wrapper = True
                if not is_equivalent_wrapper(merged_wrapper,secondary_wrapper):
                    print(f"-----------------------------\nWARNING: Two wrappers with same name are not equivalent!\n1: {merged_wrapper_name} in {merged_path}\n2: {secondary_wrapper_name} in {secondary_path}\nThe secondary wrapper will be ignored!\n-----------------------------")
                break
        
        if ignore_wrapper:
            continue

        with open(secondary_wrapper, "r") as file:
            secondary_wrapper_lines = file.readlines()
        
        merged_wrapper_file = open(merged_path + "/" + secondary_wrapper_name)

        prefix = ""
        program_prefix = ""
        for line in secondary_wrapper_lines:
            if ".nc" in line and not " " in line:
                file_name = line.strip("\n")
                file_path = secondary_path + "/" + program_prefix + prefix + "/" + file_name
                dir_path = merged_path + "/" + program_prefix + prefix
                compatible_files = find_compatible(file_path,dir_path)

                if not compatible_files:
                    pass
                    # Copy file from secondaryDB to mergeDB
                    
                else:
                    for compat_file in compatible_files:
                        if is_same(compat_file,file_path):
                            pass
                            # Tål att tänkas på
                            
                    
            
            elif "Default_dir" in line:
                prefix = line.strip('Default_Dir ').strip('\n')

                # Check if directory exists in mergedDB, otherwise create it
                if not os.path.exists(merged_path+"/"+prefix):
                    os.mkdir(merged_path+"/"+prefix)

            elif line[0] == "!" and len(line) == 2:
                prefix = ""

            elif "Begin Program" in line:
                program_prefix = line.strip("Begin Program ").strip('\n')
                program_prefix += "/"
            
            merged_wrapper_file.write(line)



if __name__ == '__main__':
    if len(sys.argv) < 3:
        s1 = "NVI_data/20APR01XA/20APR01XA_V005_iGSFC_kall.wrp"
        s2 = "NVI_data/20APR01XAV2/20APR01XA_V005_iGSFC_kall.wrp"
        print(is_same_wrapper(s1, s2))

    else:
        print(is_same(sys.argv[1], sys.argv[2]))