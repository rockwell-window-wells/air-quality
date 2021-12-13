"""read_logger_data.py: Take the raw data from the PAC-8000 data logger and
generate plots, relevant statistics, and allow event tagging by matching up a
tag/time list (a list of tags based on what was happening).

"""

# import the necessary packages
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import datetime as dt
# import seaborn as sns
import scipy.ndimage


# Read the file
filename = "ARPL-1307_PAC_8000_13_12_2021.txt"

rawdata = pd.read_csv(filename, sep=", ", header=None)

eventtype = []
datetime = []
date = []
time = []
styrene = []

npts = 50000    # Set this as len(rawdata) to process all the data
gausspts = 100  # Number of points to calculate smoothed data
sampling = "20T"   # Take a sample at this interval (S for seconds, T for minutes, H for hours)

for i in range(npts):
    rowstr = str(rawdata.loc[i])
    rowlist = rowstr.split(";")
    
    if any("VAL" in string for string in rowlist):
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

# Create new dataframe with only the sampled data
sampdata = measdata.set_index("DateTime")
sampdata = sampdata.resample(sampling, convention="start").median()
sampdata = sampdata.reset_index()

# measdata.plot(x="DateTime", y="Styrene")

fig, ax = plt.subplots()
ax.scatter(sampdata["DateTime"], sampdata["Styrene"], label="Measured Values")
ax.plot(sampdata["DateTime"], scipy.ndimage.gaussian_filter(sampdata["Styrene"], gausspts), label="Smoothed Values")
# plt.legend("Measured Values", "Smoothed Values")
ax.set_xlabel("Date and Time")
ax.set_ylabel("Styrene Level (ppm)")
plt.show()

# fig, ax = plt.subplots()
# ax.plot(measdata["DateTime"], measdata["Styrene"], label="Measured Values")
# ax.plot(measdata["DateTime"], scipy.ndimage.gaussian_filter(measdata["Styrene"], 500), label="Smoothed Values")
# # plt.legend("Measured Values", "Smoothed Values")
# ax.set_xlabel("Date and Time")
# ax.set_ylabel("Styrene Level (ppm)")
# plt.show()


# Calculate time-weighted average (using total time measured -- this will need to be changed for 8 hour measurements):
twasum = measdata["Styrene"].sum()
twatime = measdata["DateTime"].max() - measdata["DateTime"].min()
twatime = twatime.total_seconds()
twa = twasum/twatime