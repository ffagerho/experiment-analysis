#!/usr/bin/python

import sys, re

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

import data_helper
import analyze_login
import analyze_opportunities
import analyze_polling
import analyze_clicks

# for data preprocessing:
# cat event_dump2.txt | sed 's/[^ ]|/;/g' | sed 's/[ ]*|/|/g' | sed 's/|[ ]*/|/g' | sed 's/^ *//' | grep -v '^[-(]' | grep -v '^$' > event_dump2.csv


def main():
    print "----------------------------------------------------"
    print "Analyzing experiment data."
    print
    print "Usage: <inputfile>"
    print "----------------------------------------------------"
    print

    inputFileName = sys.argv[1]

    print "Import data from: " + inputFileName
    df = data_helper.import_and_clean_data(inputFileName)

    describe_data(df)

    analyze_login.calculate_direct_and_report_logins(df)

    ordata = analyze_opportunities.calculate_ratios(df)

    plt.figure()
    ordata['or'].plot(kind="hist")
    plt.show()

    print ''
    polltimes = analyze_polling.calc_times(df)
    analyze_polling.largescale_values(polltimes)
    analyze_polling.show_histogram(polltimes)

    analyze_clicks.click_percentages(df)

    analyze_clicks.count_reportbased_clicks(df)
    analyze_clicks.count_userbased_clicks(df)

def describe_data(df):
    # Describe data set
    print "Data set starts: {}".format(df['datetime'].min())
    print "Data set ends: {}".format(df['datetime'].max())
    print

if __name__ == "__main__":
    main()
