import os
import sys
import glob
import pandas as pd
import csv
import tools_setting as conf

if __name__ == '__main__':

    try:
        print('START tools_merge_dir')
        # argv[1] -> output folder name
        # argv[2] -> input pattern
        output_folder = sys.argv[1]
        input_pattern = sys.argv[2]

        for merge_dir in conf.MERGE_ALL_DIR_PATH:
            output_dir = os.path.join(merge_dir, output_folder)
            print merge_dir + input_pattern + "*/*.csv"
            # get all file paths with .csv filename extension and pattern
            dir_list = glob.glob(merge_dir + input_pattern + "*/*.csv")
            # sort by modified time
            dir_list.sort(key=os.path.getmtime)

            # create set to avoid duplicates
            set_csv = set()

            # traverse the directories
            for path in dir_list:
                filename = os.path.basename(path)
                set_csv.add(filename)

            # convert back to list
            list_csv = list(set_csv)
            print list_csv

            # iterate through unique csv filenames
            for csv_output_file in list_csv:
                csv_merge = []
                print 'PATTERN: ' + csv_output_file
                # iterate through absolute paths dir_list
                for csv_input_file in dir_list:
                    if os.path.basename(csv_input_file) == csv_output_file:
                        print 'APPEND ' + os.path.basename(os.path.dirname(csv_input_file)) + \
                              ' FILE: ' + os.path.basename(csv_input_file)
                        df = pd.read_csv(csv_input_file, dtype='object')
                        csv_merge.append(df)

                # create output file
                df_output = pd.concat(csv_merge)
                df_output_path = os.path.join(output_dir, csv_output_file)
                df_output.to_csv(df_output_path, quoting=csv.QUOTE_ALL, index=False, encoding="utf_8_sig")
                print 'OUTPUT: ' + df_output_path

        print('END tools_merge_dir')
    except Exception as e:
        print e
    sys.exit(0)