#!/usr/bin/python

import sys, re

import numpy as np
import pandas as pd

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
