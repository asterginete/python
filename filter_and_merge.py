# Get only the files in MERGE_DIR that has value FILTER_VALUE
# in column FILTER_COLUMN, then merge it to MERGE_OUTPUT
import os
import sys
import pandas as pd
import csv


MERGE_DIR = "D:/Merge/"
MERGE_OUTPUT = "D:/Output/output.csv"
MERGE_PATTERN = "Prefix_"
FILTER_COLUMN = "Column"
FILTER_VALUE = "Value"


if __name__ == '__main__':

    try:
        print('START filter_and_merge')

        df_list = []
        for csv_file in os.listdir(MERGE_DIR):
            if not csv_file.startswith(MERGE_PATTERN):
                continue

            csv_path = os.path.join(MERGE_DIR, csv_file)
            if not os.path.exists(csv_path):
                continue

            try:
                df = pd.read_csv(csv_path, dtype='object')
            except:
                continue

            if not df.shape[0] > 0:
                continue

            df_out = df[df[FILTER_COLUMN] == FILTER_VALUE].copy()
            if not df_out.shape[0] > 0:
                continue

            df_list.append(df_out)
            print "File: " + csv_file + " Count: " + str(df_out.shape[0])

        if df_list:
            df_out = pd.concat(df_list)
            df_out.to_csv(MERGE_OUTPUT, quoting=csv.QUOTE_ALL, index=False, encoding="utf_8_sig")

        print('END filter_and_merge')
    except Exception as e:
        print e
    sys.exit(0)
