#!/usr/bin/python

import sys, re, datetime, urllib, socket

print
print "Analyzing experiment data."
print
print "Usage: <lang> <inputfile> <session threshold>"
print

inputFileName = sys.argv[1]

debug = False

print "Reading file" + inputFileName

inputFile = open(inputFileName, "r")

lines = 0

for line in inputFile:

  if debug:
    print "Line: " + line

  lines = lines + 1

print "Read " + str(lines) + " lines."
