"""read_logger_data.py: Take the raw data from the PAC-8000 data logger and
generate plots, relevant statistics, and allow event tagging by matching up a
tag/time list (a list of tags based on what was happening).

"""

# import the necessary packages
import numpy as np
import pandas as pd
# import argparse
import matplotlib.pyplot as plt
import datetime as dt
# import seaborn as sns
import scipy.ndimage


# Read the file
filename = "ARPL-1307_PAC_8000_16_12_2021.txt"

# Set the start and end datetimes for closer analysis
syear = 2021
smonth = 12
sday = 15
shour = 14
sminute = 0

eyear = 2021
emonth = 12
eday = 15
ehour = 22
eminute = 0

start_datetime = dt.datetime(syear, smonth, sday, shour, sminute)   # Starting datetime for assessment
end_datetime = dt.datetime(eyear, emonth, eday, ehour, eminute)     # Ending datetime for assessment

rawdata = pd.read_csv(filename, sep=", ", header=None)

# Turn on the desired plots
sampleplot = False
allplot = False
windowplot = True

eventtype = []
datetime = []
date = []
time = []
styrene = []

npts = len(rawdata)    # Set this as len(rawdata) to process all the data
gausspts = 15  # Number of points to calculate smoothed data
sampling = "1T"   # Take a sample at this interval (S for seconds, T for minutes, H for hours)

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

# Filter data to show only readings between two datetimes
after_start = measdata["DateTime"] >= start_datetime
before_end = measdata["DateTime"] <= end_datetime
between_times = after_start & before_end
measdata_window = measdata.loc[between_times]


# Create new dataframe with only the sampled data
sampdata = measdata.set_index("DateTime")
sampdata = sampdata.resample(sampling, convention="start").median()
sampdata = sampdata.reset_index()

# measdata.plot(x="DateTime", y="Styrene")

if sampleplot is True:
    fig1, ax1 = plt.subplots()
    ax1.plot(sampdata["DateTime"], sampdata["Styrene"], label="Measured Values")
    # ax.scatter(sampdata["DateTime"], sampdata["Styrene"], label="Measured Values")
    ax1.plot(sampdata["DateTime"], scipy.ndimage.gaussian_filter(sampdata["Styrene"], gausspts), label="Smoothed Values")
    # plt.legend("Measured Values", "Smoothed Values")
    ax1.set_xlabel("Date and Time")
    ax1.tick_params(axis="x", labelrotation = 45)
    ax1.set_ylabel("Styrene Level (ppm)")
    # plt.show()

if allplot is True:
    fig2, ax2 = plt.subplots()
    ax2.plot(measdata["DateTime"], measdata["Styrene"], label="Measured Values")
    ax2.plot(measdata["DateTime"], scipy.ndimage.gaussian_filter(measdata["Styrene"], gausspts), label="Smoothed Values")
    # plt.legend("Measured Values", "Smoothed Values")
    ax2.set_xlabel("Date and Time")
    ax2.set_ylabel("Styrene Level (ppm)")
    # plt.show()

if windowplot is True:
    fig3, ax3 = plt.subplots(figsize=(10,8))
    ax3.plot(measdata_window["DateTime"], measdata_window["Styrene"], label="Measured Values")
    # ax3.plot(measdata_window["DateTime"], scipy.ndimage.gaussian_filter(measdata_window["Styrene"], gausspts), label="Smoothed Values")
    # plt.legend("Measured Values", "Smoothed Values")
    ax3.set_xlabel("Date and Time")
    ax3.set_ylabel("Styrene Level (ppm)")
    # plt.show()

plt.show()

# Calculate time-weighted average (using total time measured -- this will need to be changed for 8 hour measurements):
# for ind in measdata.index:

#     time = df["Time"][ind]
#     if time > shifts.loc["Day","Start"] and time < shifts.loc["Day","End"]:


peakval = measdata_window["Styrene"].max()

twasum = measdata_window["Styrene"].sum()
twatime = measdata_window["DateTime"].max() - measdata_window["DateTime"].min()
twatime = twatime.total_seconds()
twa = twasum/twatime
twa = np.around(twa,1)
