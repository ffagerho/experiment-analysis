import sys, re
import pandas as pd

def import_and_clean_data(file_name):
    print "Parse CSV: " + file_name
    df = pd.read_csv(file_name, parse_dates=['datetime'], sep='|')
    print "Done."
    print "There are {:.0f} rows in the data.".format(len(df))

    idx = df.target_email.str.contains('solita.fi$|stt.fi$|stt-lehtikuva.fi$|example.com$', flags=re.IGNORECASE, regex=True, na=False)
    df = df[~idx]

    print "After cleaning, there are {:.0f} rows in the data".format(len(df))
    print

    return df
