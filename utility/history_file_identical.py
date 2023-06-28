import os

# Maybe change this so that we check if each row is in both files, instead of checking
# that they are in the exact same place!


def is_identical_history_file(history_file, merge_history_directory):
    """
    Checks if there exists a history file in a directory which contains the same
    information as given history file

    Parameters: 
    history_file (str): Path to history file in secondary folder    
    f2 (str): Path to history directory in merge folder

    Returns:
    Returns path to file which is compatible, returns an empty string if no 
    compatible file is found
    """
    with open(history_file) as file1:
        history_file_lines = file1.readlines()

    for merge_history_file in os.listdir(merge_history_directory):
        with open(merge_history_directory+merge_history_file) as file2:
            merge_history_file_lines = file2.readlines()

        if history_file_lines == merge_history_file_lines:
            return merge_history_file

    return ""
