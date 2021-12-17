# -*- coding: utf-8 -*-
"""
organize_logger_data.py: Specify a folder where raw data logs are kept. Make
Pandas DataFrames for each individual day covered by the data logs, and save
these as CSV files for quick access later.

Created on Thu Dec 16 13:43:59 2021

@author: Ryan.Larson
"""

import numpy as np
import pandas as pd
import datetime as dt
import os
import glob
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from csv import writer


# Set the directory where the data logs will be kept
directory = r"Z:\Safety\Inspections & Assessments\Air Samplings\PAC 8000 Data Logs"
namepattern = "ARPL-1307_PAC 8000*.txt"
filepattern = directory + "\\" + namepattern

### Check for new data files against a logged list ###
logfile = directory + "\\LOGGED.csv"    # NOTE: LATER THIS SHOULD VERIFY THAT THE EXPECTED FILE STRUCTURE EXISTS BEFORE PROCEEDING
os.chmod(logfile, S_IWUSR|S_IREAD)  # This makes the log file read/write

# Read the logfile data into dataframe
try:
    logged = pd.read_csv(logfile)
except pd.errors.EmptyDataError:
    print("LOGGED.csv is empty\n")

# Go through the files in the PAC 8000 Data Logs folder and see which ones are
# not listed in the logfile (the ones in that file have been processed and 
# prepared for easy usage)
for file in glob.glob(filepattern):
    base = os.path.basename(file)
    # print(base)
    
    # If the current file is not listed as logged, create a rawdata DataFrame
    # and clean the data. Then separate into more DataFrames based on date and
    # export them as CSV files. Finally, add the datalog .txt file name to the
    # list in LOGGED.csv.
    if not logged["DataLog"].str.contains(base).any():
        print("{} is not in the logged list".format(base))
        rawdata = pd.read_csv(file, sep=", ", header=None)
        
        eventtype = []
        datetime = []
        date = []
        time = []
        styrene = []

        for i in range(len(rawdata)):
            rowstr = str(rawdata.loc[i])
            rowlist = rowstr.split(";")
            
            if any("VAL" in string for string in rowlist):      # Need to add triggers for other event types of interest
                eventtype.append("VAL")
                dtime  = dt.datetime.strptime(rowlist[1],"%Y%m%d%H%M%S")        
                datetime.append(dtime)
                date.append(dtime.date())
                time.append(dtime.time())
                
                styrenestr = rowlist[2]
                split = styrenestr.split("\n")
                if "INV" in split[0]:
                    split[0] = float("NaN")
                else:
                    split[0] = float(split[0])
                    
                styrene.append(split[0])
                
        measdata = pd.DataFrame({"EventType":eventtype,
                                 "DateTime":datetime,
                                 "Date":date,
                                 "Time":time,
                                 "Styrene":styrene})
        
        pklname = os.path.splitext(base)[0] + ".pkl"
        pklfile = directory + "\\" + pklname
        
        measdata.to_pickle(pklfile)
        
        # csvname = os.path.splitext(base)[0] + ".csv"
        # csvfile = directory + "\\" + csvname
        
        # measdata.to_csv(csvfile, mode='a', index=False)  # Write measdata to csv
        
        # os.chmod(csvfile, S_IREAD|S_IRGRP|S_IROTH)  # Set the csvfile as read-only
        
        # # Append the datalog file name LOGGED.csv
        # with open(logfile, 'a', newline='') as f_object:
        #     writer_object = writer(f_object)    # Pass the CSV file object to the writer() function
        #     writer_object.writerow([base])      # Pass the datalog filename as an argument into the writerow() function
        #     f_object.close()                    # Close the file object


print("All remaining files have been logged.")

os.chmod(logfile, S_IREAD|S_IRGRP|S_IROTH)  # Make logfile read-only after writing new datalogger filenames to list


### Break down the CSV files by date for easy searching ###
processedfile = directory + "\\By Day\\PROCESSED.csv"
os.chmod(processedfile, S_IWUSR|S_IREAD)  # This makes the log file read/write

# Read the processedfile data into dataframe
try:
    processed = pd.read_csv(processedfile)
except pd.errors.EmptyDataError:
    print("PROCESSED.csv is empty\n")
    
pnamepattern = "ARPL-1307_PAC 8000*.csv"
pfilepattern = directory + "\\" + pnamepattern

for file in glob.glob(pfilepattern):
    base = os.path.basename(file)
    print(base)
    
    # If the CSV file isn't in the list, process it
    if not processed["ProcessedData"].str.contains(base).any():
        print("{} is not in the processed list".format(base))
        
        measdata = pd.read_csv(file, parse_dates=True)    # Read the CSV data in to a DataFrame
        measdata["Date"] = pd.to_datetime(measdata["Date"])
        measdata["Date"] = measdata["Date"].dt.date
        
        measdata["Time"] = pd.to_datetime(measdata["Time"])
        measdata["Time"] = measdata["Time"].dt.time
        
        measdata["DateTime"] = pd.to_datetime(measdata["DateTime"])
        
        # # daytimestr = 
        # daytimes = []
        for ind in measdata.index:
            measdata.loc[ind,"DateTime"] = measdata.loc[ind,"DateTime"].to_pydatetime()
        
        # Get list of unique dates in measdata
        uniquedates = pd.to_datetime(measdata["DateTime"]).dt.date.unique()
            
        
        # For each unique date, create a DataFrame with data only from that date
        for day in uniquedates:
            print(type(day))
            print(type(measdata["DateTime"][1]))
            dateindices = measdata["Date"] == day
            datedata = measdata.loc[dateindices]
            
            # Generate the CSV name based on date
            daystr = day.strftime("%Y-%m-%d")
            csvname = daystr + "_Styrene.csv"
            csvfile = directory + "\\By Day\\" + csvname
            
            # Check if a CSV file exists in the By Day folder with the same name
            dayfilepattern = directory + "\\By Day\\*_Styrene.csv"
            for dayfile in glob.glob(dayfilepattern):
                print(dayfile)
                
                if csvname == dayfile:
                    # If the generated CSV name has the same name as an existing CSV file,
                    # open the existing file and append any new values from the current
                    # CSV file, if any exist.
                    print("\nA file already exists with that name")
                else:
                    print("File {} is not in the processed list".format(dayfile))