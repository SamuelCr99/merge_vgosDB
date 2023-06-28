from merge_vgosDB import merge_vgosDB


merge_directory = 'example/GSFC_data/20230315-r41094/'
secondary_directory = 'example/BKG_data/20230315-r41094/'
who = 'NVI Inc. - Summer Swedes'

merge_vgosDB(merge_directory, secondary_directory, who)