# coding: UTF-8
# Read settings files, then delete files from settings file.
import sys
import os


if __name__ == '__main__':
    print 'Start delete_dir_files'

    return_code = 1
    if len(sys.argv) == 2:
        try:
            del_cnt = 0

            # Read settings file from parameter
            setting_file = sys.argv[1]
            f = open(setting_file, 'r')

            # Read settings file and iterate through each directory
            for dir_to_del in f:
                dir_to_del = dir_to_del.rstrip()
                print "Directory: " + dir_to_del

                # Check if directory exists, list each files in the directory, then delete
                if os.path.exists(dir_to_del):
                    for file_to_delete in os.listdir(dir_to_del):
                        file_to_delete_path = os.path.join(dir_to_del, file_to_delete)
                        os.remove(file_to_delete_path)
                        print 'Deleted: ' + file_to_delete
                        del_cnt += 1
                else:
                    print 'Error: path does not exist'

            # Display number of deleted files
            print ("Files deleted: %d", del_cnt)
            return_code = 0
            print 'End delete_dir_files'
        except Exception as e:
            print e
    else:
        print 'Error: Please input setting file path as parameter.'
    sys.exit(return_code)