import os
import csv
import pandas as pd
import codecs

# break_file() - Break large files into multiple files.
# merge_file() - Merge multiple files into one file.

BREAK_INPUT_CSV = "D:/Break/large_file.csv"
BREAK_OUTPUT_FILE = "D:/Break/output_file"
BREAK_COUNTER_INIT = 1
BREAK_MAX_RECORDS = 100000

MERGE_DIR = "D:/Merge/"
MERGE_PATTERN = "Merge_"
MERGE_OUTPUT_FILE = os.path.join(MERGE_DIR, "MergedFiles.csv")


def break_file():
    # This function breaks down a file by grouping them based on Global Sample Code. The data is read up to the value of
    # MAX_RECORDS.

    df_input = pd.read_csv(BREAK_INPUT_CSV, dtype='object')
    list_sample_code = list(set(df_input["Global Sample Code"]))

    record_count = 0
    break_counter = BREAK_COUNTER_INIT
    list_df_breakdown = []
    for sample_code in list_sample_code:

        df_breakdown = df_input[df_input["Global Sample Code"] == sample_code].copy()
        cnt = df_breakdown.shape[0]
        record_count += cnt

        list_df_breakdown.append(df_breakdown)

        if record_count >= BREAK_MAX_RECORDS:
            print 'output file. record_count: ' + str(record_count) + ' COUNTER: ' + str(break_counter)
            df_output = pd.concat(list_df_breakdown)
            df_output.to_csv(os.path.join(BREAK_OUTPUT_FILE + '_' + str(break_counter) + '.csv'), quoting=csv.QUOTE_ALL,
                             index=False, encoding="utf_8_sig")
            break_counter += 1
            record_count = 0
            list_df_breakdown = []

    if record_count > 0:
        print 'output file. record_count: ' + str(record_count) + ' COUNTER: ' + str(break_counter)
        df_output = pd.concat(list_df_breakdown)
        df_output.to_csv(os.path.join(BREAK_OUTPUT_FILE + '_' + str(break_counter) + '.csv'), quoting=csv.QUOTE_ALL,
                         index=False, encoding="utf_8_sig")


def merge_file():
    # This function merges the CSV files inside MERGE_DIR that matches MERGE_PATTERN

    if os.path.exists(MERGE_DIR):
        list_df_merge = []
        for csv_file in os.listdir(MERGE_DIR):

            # Merge only csv files
            if not csv_file.endswith('.csv'):
                continue
            # Should match pattern
            if not csv_file.startswith(MERGE_PATTERN):
                continue
            # Check if path exists
            input_csv_path = os.path.join(MERGE_DIR, csv_file)

            if not os.path.exists(input_csv_path):
                continue
            print 'Merging: ' + csv_file
            with codecs.open(input_csv_path, "r", encoding='utf-8', errors='ignore') as f_csv:
                df_to_merge = pd.read_csv(f_csv, dtype='object')

            list_df_merge.append(df_to_merge)

        if list_df_merge:
            df_output = pd.concat(list_df_merge)
            df_output.to_csv(MERGE_OUTPUT_FILE, quoting=csv.QUOTE_ALL, index=False, encoding="utf_8_sig")
    else:
        print MERGE_DIR + " does not exist."


if __name__ == '__main__':
    merge_file()
    # break_file()
