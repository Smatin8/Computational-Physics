# -*- coding: utf-8 -*-

import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, os
import datetime

begin_time = datetime.datetime.now()                # Track Processing Time

def RFIstats(df):                               # Create Function to Calculate Stats
    df = df[freqVal]                            # Set Index to freqval (frequency)
    skew = df.skew(axis= 0, skipna = True)      # Calculate Skewness
    kurt = df.kurtosis()                        # Calculate Kurtosis
    mean = df.mean()                            # Calculate Mean
    median = df.median()                        # Calculate Median
    std = df.std()                              # Calculate STD
    nine5 = df.quantile(0.95)                   # Calculate 95th percentile
    sigma5 = 5 * std                            # Calculate 5sigma
    maxVal = df.max()                           # Calculate Max Value
    minVal = df.min()                           # Calculate Min Value
    FreqEntry = {'{} MHz'.format(freqVal):{ 'Skewness': skew, 'Kurtosis': kurt, 'Mean': mean, 'Median': median, 'STD': std, '95th Percentile': nine5, '5 Sigma': sigma5, 'Max Val': maxVal, 'Min Val': minVal}}
    return FreqEntry                            # Make into Dictionary and Return

path = str(os.getcwd())                         # Path Where all the SH Folders are located
day = glob.glob(path + "/*")                    # Grab All Folder in Path


   
for f in day:
    if len(os.listdir(f) ) != 0:    # Check if the File is empty or not
        os.chdir(f)                 # Changes Directory
        daynum = str(os.getcwd())   # Make directory into string
        newpath = os.getcwd()       # Set new path for files
        date = daynum[-8:]          # Grab the date to name big files later
        print('Analyzing: {}'.format(date))
    
    
        files = glob.glob(newpath + "/*csv")    # New CSV file path
        placer = []                             # Set Empty List to Append data  
    

        for filename in files:                  # Grab Files from current Folder
            df = pd.read_csv(filename, usecols = ['Frequency (MHz)', 'Amplitude Max(mW)'],index_col=0, header = 0)      # Grab Frequency and Amplitude
            placer.append(df)                   # Append data to list

        df = pd.concat(placer, axis = 1, ignore_index=True)     # Concat list of frequencies for selected files

        all_Dict = {}                           # Create Dictionary to grab all stats for each frequency
        busy_Chan = []                          # Create List to gather Busy Channel and its Data for the day
        busy_List = []                          # Create List of busy channels for the day
    
        for i in range(len(df)):
            freqdf = df.iloc[[i]]              # Grab Each Row
            frequencyNum = freqdf.index        # Find the index
            freqVal = frequencyNum[0]          # grab the frequency value in MHz from index
            
            goodFreq = freqdf.transpose()   # Transpose the Frequency row to column to use in RFIstats function
            newDict = RFIstats(goodFreq)    # Apply RFIstats function to dataset
            all_Dict.update(newDict)        # Update Dictionary with RFIstat values
        
     
            if newDict['{} MHz'.format(freqVal)]['Skewness'] !=0 or newDict['{} MHz'.format(freqVal)]['Kurtosis'] !=0:
                busy_Chan.append(goodFreq)      # Append Day worth of data of busy frequency
                busy_List.append(freqVal)       # Append Busy Channel Frequency
        
        df2 = pd.concat(busy_Chan, axis = 1)
        np.savetxt("BusyList_{}.csv".format(date),busy_List, delimiter =",",  fmt ='% s')       # Save list of Busy Channels as csv
        df2.to_csv('BusyFrequencies_{}.csv'.format(date))                                       # Save list of all busy Frequency with that days data
    
        bigdata = pd.DataFrame(all_Dict)        # Convert Dictionary to Pandas Dataframe
        largedata = bigdata.T                   # Tranpose Dataset Back to have Stats vs Frequency
        largedata.index.names = ['Frequency']   # Set Index to Frequency
    
        largedata.to_csv('DataAnalysis_{}.csv'.format(date))                    # Save Dataframe as CSV
        print('{} Completed!'.format(date))                                       # Print Completed Day
        endtime = str(datetime.datetime.now() - begin_time)                        
        print('Time ELapsed: '+ endtime )                                        # Track Processing Time
        print()
    else:
        print('!!!{} is Empty!!!'.format(f[-8:]))      # If folder is Empty
        print()
    