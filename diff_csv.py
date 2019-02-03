import pandas as pd
import os
import csv
import sys
import glob

# Get deleted(old) and diff(new) data
# IMPORTANT NOTES: Before executing, the filenames of the files to be compared MUST BE THE SAME.
# Primary keys MUST BE DEFINED in tools_setting -> DIFF_CSV_KEY
# If there are no matching keys are found in DIFF_CSV_KEY, the input file will be skipped.

# Set MERGE_DIRNAME and INPUT_DIR_PREFIX only if there are subdirectories
#     inside DIFF_CSV_DIR_OLD and DIFF_CSV_DIR_NEW
# MERGE_DIRNAME - output directory of the merged files of DIFF_CSV_DIR_OLD and DIFF_CSV_DIR_NEW
# INPUT_DIR_PREFIX - prefix used by the subdirectories of DIFF_CSV_DIR_OLD and DIFF_CSV_DIR_NEW

MERGE_DIRNAME = ''
INPUT_DIR_PREFIX = 'File_'

DIFF_CSV_DIR_OUT = "D:/Diff CSV/diff/"
DIFF_CSV_DIR_OLD = "D:/Diff CSV/old/"
DIFF_CSV_DIR_NEW = "D:/Diff CSV/new/"


def compare_old_new(df1, df2, primary_keys):

    print 'Primary Keys', primary_keys
    df1_index = df1.set_index(primary_keys).index
    df2_index = df2.set_index(primary_keys).index

    df1_mask = ~df1_index.isin(df2_index)
    df2_mask = ~df2_index.isin(df1_index)

    diff_old = df1.loc[df1_mask]
    diff_new = df2.loc[df2_mask]

    return diff_old, diff_new


def scan_dir():

    # output directory is optional.
    csv_dir_new = os.path.join(DIFF_CSV_DIR_NEW, MERGE_DIRNAME)

    for csv_output in os.listdir(csv_dir_new):
        input_csv_new = os.path.join(csv_dir_new, csv_output)

        if csv_output.endswith('.csv'):
            csv_output_base = os.path.splitext(csv_output)[0]
            # primary_keys = DIFF_CSV_KEY.get(csv_output_base, None)

            # if primary_keys is not None:
            # new and old csv files of each directories
            input_csv_old = os.path.join(DIFF_CSV_DIR_OLD, MERGE_DIRNAME, csv_output)
            df_diff_path = os.path.join(DIFF_CSV_DIR_OUT, 'diff_' + csv_output)
            df_del_path = os.path.join(DIFF_CSV_DIR_OUT, 'deleted_' + csv_output)

            if os.path.exists(input_csv_old):

                print 'INPUT (Old): ' + input_csv_old
                print 'INPUT (New): ' + input_csv_new

                # read, the two csv files
                df_old = pd.read_csv(input_csv_old, dtype='object')
                df_new = pd.read_csv(input_csv_new, dtype='object')

                drop_col = list(df_old.columns.values)

                df_old.drop_duplicates(keep='first', inplace=True)
                df_new.drop_duplicates(keep='first', inplace=True)

                df_old["source"] = "old"
                df_new["source"] = "new"

                df_diff = pd.concat([df_old, df_new])
                df_diff.drop_duplicates(subset=drop_col, keep=False,inplace=True)
                df_diff = df_diff[df_diff["source"] == "new"].copy()
                df_diff.drop(columns=["source"], inplace=True)
                df_diff.to_csv(df_diff_path, quoting=csv.QUOTE_ALL, index=False, encoding="utf_8_sig")

                print 'DIFF OUTPUT: ' + df_diff_path


def merge_csv_with_subdir(input_mergedir):
    output_mergedir = os.path.join(input_mergedir, MERGE_DIRNAME)

    dir_list = glob.glob(input_mergedir + INPUT_DIR_PREFIX + "*/*.csv")
    dir_list.sort(key=os.path.getmtime)  # sort by modified time

    # create set to avoid duplicates
    set_csv = set()

    # traverse the directories
    for path in dir_list:
        filename = os.path.basename(path)
        set_csv.add(filename)

    # convert back to list
    list_csv = list(set_csv)

    # iterate through unique csv filenames
    for csv_output_file in list_csv:
        csv_merge = []
        print 'PATTERN: ' + csv_output_file
        # iterate through absolute paths dir_list
        for csv_input_file in dir_list:
            if os.path.basename(csv_input_file) == csv_output_file:
                print 'APPEND ' + os.path.basename(os.path.dirname(csv_input_file)) + \
                      ' FILE: ' + os.path.basename(csv_input_file)
                # append each input file to csv_merge
                df = pd.read_csv(csv_input_file, dtype='object')
                csv_merge.append(df)

        # create output file
        df_output = pd.concat(csv_merge)
        df_output_path = os.path.join(output_mergedir, csv_output_file)
        df_output.to_csv(df_output_path, quoting=csv.QUOTE_ALL, index=False, encoding="utf_8_sig")
        print 'OUTPUT: ' + df_output_path


if __name__ == '__main__':

    return_code = 1
    try:
        print 'START tools_diff_csv'
        # Merge CSV input files with sub directories
        # If the input files are already merged, set MERGE_DIRNAME to '' and comment out merge_csv_with_subdir below
        # merge_csv_with_subdir(conf.DIFF_CSV_DIR_OLD)
        # merge_csv_with_subdir(conf.DIFF_CSV_DIR_NEW)

        # Scan directory and get deleted and diff files
        scan_dir()
        return_code = 0
        print 'END tools_diff_csv'
    except Exception as e:
        print e
    sys.exit(return_code)