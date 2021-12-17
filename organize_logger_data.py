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
        # date = []
        # time = []
        styrene = []

        for i in range(len(rawdata)):
            rowstr = str(rawdata.loc[i])
            rowlist = rowstr.split(";")
            
            if any("VAL" in string for string in rowlist):      # Need to add triggers for other event types of interest
                eventtype.append("VAL")
                dtime  = dt.datetime.strptime(rowlist[1],"%Y%m%d%H%M%S")        
                datetime.append(dtime)
                # date.append(dtime.date())
                # time.append(dtime.time())
                
                styrenestr = rowlist[2]
                split = styrenestr.split("\n")
                if "INV" in split[0]:
                    split[0] = float("NaN")
                else:
                    split[0] = float(split[0])
                    
                styrene.append(split[0])
                
        measdata = pd.DataFrame({"EventType":eventtype,
                                 "DateTime":datetime,
                                 # "Date":date,
                                 # "Time":time,
                                 "Styrene":styrene})
        
        pklname = os.path.splitext(base)[0] + ".pkl"
        pklfile = directory + "\\" + pklname
        
        measdata.to_pickle(pklfile) # Create the PKL file for the current data log file
        
        # Append the datalog file name LOGGED.csv
        with open(logfile, 'a', newline='') as f_object:
            writer_object = writer(f_object)    # Pass the CSV file object to the writer() function
            writer_object.writerow([base])      # Pass the datalog filename as an argument into the writerow() function
            f_object.close()                    # Close the file object


print("All raw data .txt files have been logged.")

os.chmod(logfile, S_IREAD|S_IRGRP|S_IROTH)  # Make logfile read-only after writing new datalogger filenames to list


### Break down the CSV files by date for easy searching ###
processedfile = directory + "\\PROCESSED.csv"
os.chmod(processedfile, S_IWUSR|S_IREAD)  # This makes the processed file read/write

# Read the processedfile data into dataframe
try:
    processed = pd.read_csv(processedfile)
except pd.errors.EmptyDataError:
    print("PROCESSED.csv is empty\n")
    
pnamepattern = "ARPL-1307_PAC 8000*.pkl"
pfilepattern = directory + "\\" + pnamepattern

for file in glob.glob(pfilepattern):
    base = os.path.basename(file)
    print("Checking for {}....".format(base))
    
    # If the PKL file isn't in the list, process it
    if not processed["ProcessedData"].str.contains(base).any():
        print("{} is not in the processed list".format(base))
        
        measdata = pd.read_pickle(file)    # Read the PKL data in to a DataFrame
        
        uniquedates = pd.to_datetime(measdata["DateTime"]).dt.date.unique()
        # print(uniquedates)
        
        # For each unique date, create a DataFrame with data only from that date
        for day in uniquedates:
            midnight = dt.time(0,0,0)
            start_datetime = dt.datetime.combine(day,midnight)
            endday = day + dt.timedelta(days=1)
            end_datetime = dt.datetime.combine(endday,midnight)
            
            after_start = measdata["DateTime"] >= start_datetime
            before_end = measdata["DateTime"] <= end_datetime
            between_times = after_start & before_end
            on_day = measdata.loc[between_times]    # DataFrame of only the current day's data
            
            # Generate the PKL name based on date
            pname = str(day) + "_Styrene.pkl"
            pfile = directory + "\\By Day\\" + pname
            
            
            
            pklname = str(day) + "_Styrene.pkl"
            pklfile = directory + "\\By Day\\" + pklname
            
            # Look in By Day folder for duplicate files of pklfile. If a file already
            # exists, load its data and concatenate the new data with it. Then
            # remove any duplicates and save the complete file back to the same
            # name. This way each unique date we have data for should have a single
            # file assigned to it.
            
            
            
            
            
            
            
            on_day.to_pickle(pklfile) # Create the PKL file for the current data log file
            
        # Append the single day PKL file name to PROCESSED.csv
        # Append the datalog file name LOGGED.csv
        with open(processedfile, 'a', newline='') as f_object:
            writer_object = writer(f_object)    # Pass the CSV file object to the writer() function
            writer_object.writerow([base])      # Pass the datalog filename as an argument into the writerow() function
            f_object.close()                    # Close the file object
            
print("All processed data .pkl files have been broken down by day.")

os.chmod(processedfile, S_IREAD|S_IRGRP|S_IROTH)  # Make processedfile read-only after writing new processed filenames to list
