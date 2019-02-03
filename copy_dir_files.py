# coding: UTF-8
# Bulk copy files to another directories by reading from a settings file.
import sys
import os
from shutil import copy


if __name__ == '__main__':
    print 'Start copy_dir_files'

    return_code = 1
    if len(sys.argv) == 2:
        try:
            copy_cnt = 0
            line_num = 1

            # Read settings file from parameter
            setting_file = sys.argv[1]
            f = open(setting_file, 'r')

            # Read settings file and iterate through each directory
            for line in f:
                line_split = line.rstrip().split(',')
                if len(line_split) != 3:
                    print 'Line: ', line_num, ' Invalid input. Skipping.'
                    line_num += 1
                    continue

                copy_from_file = line_split[0]
                copy_to_dir = line_split[1]
                to_copy_flag = bool(int(line_split[2]))

                print 'Line: ', line_num, ' Copy: ',to_copy_flag
                # Check if directory exists, list each files in the directory, then delete
                if to_copy_flag:
                    if os.path.exists(copy_from_file):
                        if os.path.exists(copy_to_dir):
                            print 'Copying ' + copy_from_file + ' to: ' + copy_to_dir + '...'
                            copy(copy_from_file, copy_to_dir)
                            print 'Copy successful.'
                            copy_cnt += 1
                        else:
                            print 'Error: Destination directory ' + copy_to_dir + ' does not exist'
                    else:
                        print 'Error: Source file: ' + copy_from_file + ' does not exist'
                line_num += 1

            # Display number of deleted files
            print "Files copied: ", copy_cnt
            return_code = 0
            print 'End copy_dir_files'
        except Exception as e:
            print e
    else:
        print 'Error: Please input setting file path as parameter.'
    sys.exit(return_code)