from merge_vgosDB import merge_vgosDB
import tarfile
import os
import shutil
import sys
        

def main(merge_directory, secondary_directory, who):
    with tarfile.open(merge_directory, 'r') as mergeZip: 
        mergeZip.extractall('merge_temp')
    with tarfile.open(secondary_directory, 'r') as secondaryZip:
        secondaryZip.extractall('secondary_temp')

    merge_folder_name = merge_directory.split('/')[-1].split('.')[0]
    secondary_folder_name = secondary_directory.split('/')[-1].split('.')[0]

    merge_vgosDB(f'merge_temp/{merge_folder_name}', f'secondary_temp/{secondary_folder_name}', who)

    # Make merge temp into a tar file
    with tarfile.open(merge_directory, 'w:xz') as mergeZip:
        mergeZip.add('merge_temp', arcname=os.path.basename(''))
    shutil.rmtree('merge_temp')
    shutil.rmtree('secondary_temp')


    


if __name__ == '__main__':
    if len(sys.argv) < 4:
        merge_directory = 'test_data/n_data/20230315-r41094.tar.xz'
        secondary_directory = 'test_data/g_data/20230315-r41094.tar.xz'
        who = 'NVI Inc. - Summer Swedes'
    else: 
        merge_directory = sys.argv[1]
        secondary_directory = sys.argv[2] 
        who = sys.argv[3]

    main(merge_directory, secondary_directory, who)