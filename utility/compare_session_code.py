def compare_session_code(merge_wrappers, secondary_wrappers):
    """
    Compares the session code from wrapper files, if session codes are not all the
    same error is thrown. This as vgosDB from different sessions should not be merged


    
    """
    wrappers = merge_wrappers + secondary_wrappers
    session_codes = []
    for wrapper in wrappers: 
        with open(wrapper, "r") as file: 
            lines = file.readlines()
        for line in lines:
            if "Session " in line: 
                session_codes.append(line.strip("Session "))
                break
    print(session_codes)
    
    if len(set(session_codes)) != 1:
        raise Exception("You cannot merge vgosDB from different sessions")