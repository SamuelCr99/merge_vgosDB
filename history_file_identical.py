# Maybe change this so that we check if each row is in both files, instead of checking
# that they are in the exact same place!
def is_identical_history_file(f1, f2):
    with open(f1) as file1:
        lines_file_1 = file1.readlines()

    with open(f2) as file2:
        lines_file_2 = file2.readlines()

    return lines_file_1 == lines_file_2