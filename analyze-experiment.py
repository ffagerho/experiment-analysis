#!/usr/bin/python

import sys, re

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

print
print "Analyzing experiment data."
print
print "Usage: <lang> <inputfile> <session threshold>"
print
# cat event_dump2.txt | sed 's/[^ ]|/;/g' | sed 's/[ ]*|/|/g' | sed 's/|[ ]*/|/g' | sed 's/^ *//' | grep -v '^[-(]' | grep -v '^$' > event_dump2.csv

inputFileName = sys.argv[1]

print "Input file: " + inputFileName

#data = np.recfromcsv(inputFileName, delimiter='|')
#with open(inputFileName, 'rb') as csvFile:
#  csvReader = csv.reader(csvFile, delimiter='|')
#  for row in csvReader:
#    print ', '.join(row)

print "Read CSV file..."

df = pd.read_csv(inputFileName, parse_dates=['datetime'], sep='|')

print "Done."

print "There are {:.0f} rows in the data.".format(len(df))

# Clean

idx = df.target_email.str.contains('solita.fi$|stt.fi$|stt-lehtikuva.fi$|example.com$', flags=re.IGNORECASE, regex=True, na=False)
df = df[~idx]

print "After cleaning, there are {:.0f} rows in the data".format(len(df))

# Describe data set

print "Data set starts: {}".format(df['datetime'].min())
print "Data set ends: {}".format(df['datetime'].max())

# Calculate direct and report logins (absolute numbers and ratios)

num_logins = len(df[(df.event == "LOGIN")])
num_report_logins = len(df[(df.event == "LOGIN") & (df.event_target == "REPORT")])
num_direct_logins = len(df[(df.event == "LOGIN") & (df.event_target != "REPORT")])

ratio_report_logins = float(num_report_logins) / float(num_logins)
ratio_direct_logins = float(num_direct_logins) / float(num_logins)

print "Direct logins: {} ({} %)".format(num_direct_logins, round(ratio_direct_logins * 100, 4))
print "Report logins: {} ({} %)".format(num_report_logins, round(ratio_report_logins * 100, 4))
print "Total logins: {}".format(num_logins)

# Calculate opportunity ratio per user

opportunity_ratios = {}

for target_email in df.target_email.unique():
    reports_sent = df[(df.target_email == target_email) & (df.event == "EMAIL_SENT") & (df.event_target == "REPORT")]
    reports_opened = df[(df.target_email == target_email) & (df.event == "LOGIN") & (df.event_target == "REPORT") & (df.event_target_id.isin(reports_sent.event_target_id))].event_target_id.unique()
    
    num_reports_sent = len(reports_sent)
    num_reports_opened = len(reports_opened)
    
    if num_reports_sent == 0:
        this_or = 0
    else:
        this_or = float(num_reports_opened) / float(num_reports_sent)
    
    opportunity_ratios[target_email] = {
        'ao': num_reports_sent,
        'uo': num_reports_opened,
        'or': this_or
    }

ordata = pd.DataFrame.from_dict(opportunity_ratios, orient="index")

# Calculate overall opportunity ratio

print "Unique users considered for opportunity ratio: {}".format(len(ordata))
print "Mean opportunity ratio: {} %".format(round(ordata['or'].mean() * 100, 4))
print "Median opportunity ratio: {} %".format(ordata['or'].median())
print "Minimum opportunity ratio: {} %".format(ordata['or'].min() * 100, 4)
print "Maximum opportunity ratio: {} %".format(ordata['or'].max() * 100, 4)
print "Opportunity ratio standard deviation: {}".format(round(ordata['or'].std(), 5))

plt.figure()
ordata['or'].plot(kind="hist")
plt.show()
