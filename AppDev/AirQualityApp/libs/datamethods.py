"""datamethods.py: Function-based versions of organize-logger-data.py and
read-logger-data.py for use in air quality app


"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from os.path import exists
import glob
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from csv import writer
import matplotlib.pyplot as plt

def refresh_data(data_directory):
    """Function equivalent of organize-logger-data.py. Checks the data directory
    for new data files and breaks up the data into day by day PKL files for easy
    and quick data reading by other functions.
    """

    # Set the directory where the data logs will be kept
    directory = data_directory
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
            styrene = []

            for i in range(len(rawdata)):
                rowstr = str(rawdata.loc[i])
                rowlist = rowstr.split(";")

                if any("VAL" in string for string in rowlist):      # Need to add triggers for other event types of interest
                    eventtype.append("VAL")
                    dtime  = dt.datetime.strptime(rowlist[1],"%Y%m%d%H%M%S")
                    datetime.append(dtime)

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
                before_end = measdata["DateTime"] < end_datetime
                between_times = after_start & before_end
                on_day = measdata.loc[between_times]    # DataFrame of only the current day's data

                # Generate the PKL name based on date
                pname = str(day) + "_Styrene.pkl"
                pfile = directory + "\\By Day\\" + pname        # Is this redundant?



                pklname = str(day) + "_Styrene.pkl"
                pklfile = directory + "\\By Day\\" + pklname

                # Look in By Day folder for duplicate files of pklfile. If a file already
                # exists, load its data and concatenate the new data with it. Then
                # remove any duplicates and save the complete file back to the same
                # name. This way each unique date we have data for should have a single
                # file assigned to it.
                if os.path.exists(pklfile):
                    print("Existing data found for {}".format(day))
                    existingdata = pd.read_pickle(pklfile)

                    # Concatenate the existing data and new data
                    # Use pd.concat([data1, data2], axis=0) and then df = df.drop_duplicates(subset="DateTime", keep="first")
                    complete_day = pd.concat([existingdata, on_day], axis=0, ignore_index=True)
                    complete_day = complete_day.drop_duplicates(subset="DateTime", keep="first")
                    complete_day = complete_day.reset_index(drop=True)
                    print("Data combined for {}".format(day))

                    # Save complete_day as a PKL file
                    complete_day.to_pickle(pklfile)

                else:
                    print("No existing data found for {}".format(day))
                    on_day = on_day.reset_index(drop=True)
                    on_day.to_pickle(pklfile) # Create the PKL file for the current data log file


            # Append the single day PKL file name to PROCESSED.csv
            # Append the datalog file name LOGGED.csv
            with open(processedfile, 'a', newline='') as f_object:
                writer_object = writer(f_object)    # Pass the CSV file object to the writer() function
                writer_object.writerow([base])      # Pass the datalog filename as an argument into the writerow() function
                f_object.close()                    # Close the file object

    print("All processed data .pkl files have been broken down by day.")

    os.chmod(processedfile, S_IREAD|S_IRGRP|S_IROTH)  # Make processedfile read-only after writing new processed filenames to list


def prepare_data(dstart, dend, tstart, tend, directory):
    """Function for gathering styrene data over chosen interval between dtstart
    and dtend.

            Parameters:
                    dstart: Datetime date object for starting date
                    dend: Datetime date object for ending date
                    tstart: Datetime time object for starting time
                    tend: Datetime time object for ending time
                    directory: Folder path to the folder that contains the raw
                        data .txt files, as well as the "By Day" folder and the
                        LOGGED.csv and PROCESSED.csv files.
    """

    dtstart = dt.datetime.combine(dstart, tstart)
    dtend = dt.datetime.combine(dend, tend)

    if dstart != dend:
        print("Calculating for multiple dates")
        alldates = [dstart+dt.timedelta(days=x) for x in range((dend-dstart).days)]
        alldates.append(dend)
        print(alldates)

        column_names = ["EventType","DateTime","Date","Time","Styrene"]
        measdata = pd.DataFrame(columns = column_names)

        for day in alldates:
            pklname = str(day) + "_Styrene.pkl"
            pklfile = directory + "\\By Day\\" + pklname

            # Check if the pklfile exists before trying to append to measdata
            if exists(pklfile):
                daydata = pd.read_pickle(pklfile)    # Read the PKL data in to a DataFrame

                measdata = pd.concat([measdata, daydata], axis=0, ignore_index=True)
                measdata = measdata.drop_duplicates(subset="DateTime", keep="first")
                measdata = measdata.reset_index(drop=True)

    else:
        print("Data is from a single day")

        pklname = str(dstart) + "_Styrene.pkl"
        pklfile = directory + "\\By Day\\" + pklname

        measdata = pd.read_pickle(pklfile)    # Read the PKL data in to a DataFrame


    # Filter data to show only readings between two datetimes
    after_start = measdata["DateTime"] >= dtstart
    before_end = measdata["DateTime"] <= dtend
    between_times = after_start & before_end
    measdata_window = measdata.loc[between_times]

    return measdata_window, dtstart, dtend


def plot_data(measdata_window, dtstart, dtend, valueannotations, lineannotations, directory):
    """Function for plotting styrene data over chosen interval between dtstart
    and dtend and showing or not showing annotations, and calculating relevant
    measures such as TWA.

            Parameters:
                    dstart: Datetime date object for starting date
                    dend: Datetime date object for ending date
                    tstart: Datetime time object for starting time
                    tend: Datetime time object for ending time
                    annotations: Boolean value to determine whether annotations
                        should be printed on the output chart.
                    directory: Folder path to the folder that contains the raw
                        data .txt files, as well as the "By Day" folder and the
                        LOGGED.csv and PROCESSED.csv files.
    """
    # Calculate the peak PPM in the time range
    peak = measdata_window["Styrene"].max()
    peakidx = measdata_window["Styrene"].idxmax()
    peaklabel = "Peak: {} ppm".format(peak)

    # Calculate the minimum value for plotting purposes
    min = measdata_window["Styrene"].min()

    # Calculate the time weighted average styrene value over the data
    twasum = measdata_window["Styrene"].sum()
    twatime = np.sum(measdata_window["Styrene"].count()) # This assumes the datalogger is always in seconds (don't change that!)
    twa = twasum/twatime
    twa = np.around(twa,1)
    twalabel = "TWA: {} ppm".format(twa)

    # Calculate maximum short term exposure (STE) over a range of 15 minutes
    npts = 15*60    # 15 minute window
    t0ind = 0
    t1ind = npts - 1
    ste = 0.0
    if len(measdata_window) > npts:
        while t1ind <= len(measdata_window):
            stetemp = measdata_window.iloc[t0ind:t1ind]["Styrene"].sum()
            if stetemp > ste:
                ste = stetemp
                steind0 = t0ind
                steind1 = t1ind
            t0ind += 1
            t1ind += 1

        ste = np.around(ste/npts,1)  # Time weight the STE value
        stelabel = "Max STE: {} ppm".format(ste)

        datalabel = twalabel + "\n" + peaklabel + "\n" + stelabel
        print(datalabel)
    else:
        datalabel = twalabel + "\n" + peaklabel
        print(datalabel)


    fig, ax = plt.subplots(figsize=(10,8))
    ax.plot(measdata_window["DateTime"], measdata_window["Styrene"], label="Measured Values")
    # Add if statement here to add annotations and the TWA line if annotations are True
    if lineannotations is True:
        # twaline = twa*np.ones(len(measdata_window["Styrene"]))
        # ax.plot(measdata_window["DateTime"], twaline, label="TWA")
        ax.axhline(y=twa, color='r', label="TWA")
        if ste > 0.0:
            ax.axvline(x=measdata_window.iloc[steind0]["DateTime"], color='m', label="Highest STE")
            ax.axvline(x=measdata_window.iloc[steind1]["DateTime"], color='m')

        ax.legend()

    if valueannotations is True:
        # Label the TWA value and the peak value
        ypos = (9/10)*(peak-min) + min
        ax.annotate(datalabel, (measdata_window.iloc[0]["DateTime"], ypos),
        (measdata_window.iloc[0]["DateTime"], ypos))

    ax.set_title("Measured Styrene Level")
    ax.set_xlabel("Date and Time")
    ax.set_ylabel("Styrene Concentration (ppm)")

    # Create image from plot
    i = 0
    while os.path.exists(directory + f"/plot{i}.png"):
        i += 1
    plotname = directory + "/plot{}.png".format(i)
    plt.savefig(plotname)
    plt.close()

    return twa, peak, ste, plotname
