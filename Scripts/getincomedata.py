# Imports required packages
import pandas as pd
import numpy as np
import censusdata
import os

os.chdir(r"C:\Users\ryanwade44\Documents\BDPACON2020X\vscode")

# Put the variables that represent variables you want to retrieve
# in a list
cns_vars = [
    "B19113_001E","B19113A_001E","B19113B_001E","B19113C_001E",
    "B19113D_001E","B19113E_001E","B19113F_001E","B19113G_001E",
    "B19113H_001E","B19113I_001E"
    ] 

# Define the names you want to use
new_names = {
    'index':'Geography',"B19113_001E":"ALL","B19113A_001E":"WHITE",
    "B19113B_001E":"BLACK","B19113C_001E":"INDIAN","B19113D_001E":"ASIAN",
    "B19113E_001E":"PACIFIC","B19113F_001E":"OTHER","B19113G_001E":"MIX",
    "B19113H_001E":"JUST WHITE","B19113I_001E":"HISPANIC"
}
#**********************************************************************************************************
#**********************************************************************************************************
#**********************************************************************************************************

# Define the geographies you want data on
geographies = [('us', '*')]

# Fetch the data from the census api using the 5 year estimates for 
# 2018 
MEDINC_BY_US_BY_RACE = censusdata.download(
    'acs5', 2018, censusdata.censusgeo(geographies), 
    cns_vars)

# Reest the index for the MEDINC_BY_STATE_BY_RACE data frame
MEDINC_BY_US_BY_RACE = MEDINC_BY_US_BY_RACE.reset_index()

# Rename the columns with more meaningful names
MEDINC_BY_US_BY_RACE = MEDINC_BY_US_BY_RACE.rename(columns=new_names)

# Create a function to get the location name
def getLocation(row):
    return row["Geography"].name

# Sets the location field based on thee getLocation() field. Sets the "Place" field to the "Location" field
MEDINC_BY_US_BY_RACE["Location"] = MEDINC_BY_US_BY_RACE.apply(lambda row:  getLocation(row),axis=1)
MEDINC_BY_US_BY_RACE["Place"] = MEDINC_BY_US_BY_RACE["Location"]

# Sets the Query field
MEDINC_BY_US_BY_RACE["Query Type"] = "Country"

#**********************************************************************************************************
#**********************************************************************************************************
#**********************************************************************************************************

# Define the geographies you want data on
geographies = [('state', '*')]

# Fetch the data from the census api using the 5 year estimates for 
# 2018 
MEDINC_BY_STATE_BY_RACE = censusdata.download(
    'acs5', 2018, censusdata.censusgeo(geographies), 
    cns_vars)

# Reest the index for the MEDINC_BY_STATE_BY_RACE data frame
MEDINC_BY_STATE_BY_RACE = MEDINC_BY_STATE_BY_RACE.reset_index()

# Rename the columns with more meaningful names
MEDINC_BY_STATE_BY_RACE = MEDINC_BY_STATE_BY_RACE.rename(columns=new_names)

# Create a function to get the location name
def getLocation(row):
    return row["Geography"].name

# Sets the location field based on thee getLocation() field. Sets the "Place" field to the "Location" field
MEDINC_BY_STATE_BY_RACE["Location"] = MEDINC_BY_STATE_BY_RACE.apply(lambda row:  getLocation(row),axis=1)
MEDINC_BY_STATE_BY_RACE["Place"] = MEDINC_BY_STATE_BY_RACE["Location"]

# Sets the Query field
MEDINC_BY_STATE_BY_RACE["Query Type"] = "State"

#**********************************************************************************************************
#**********************************************************************************************************
#**********************************************************************************************************

# Define a new set of geographies based on places
geographies = [('state', '*'),('place','*')]

# Fetch the data from the census api
MEDINC_BY_STATE_BY_PLACE_BY_RACE = censusdata.download(
    'acs5', 2018, censusdata.censusgeo(geographies), 
    cns_vars)

# Reset your index
MEDINC_BY_STATE_BY_PLACE_BY_RACE = MEDINC_BY_STATE_BY_PLACE_BY_RACE.reset_index()

# Give the columns more meaningful names
MEDINC_BY_STATE_BY_PLACE_BY_RACE = MEDINC_BY_STATE_BY_PLACE_BY_RACE.rename(columns=new_names)

# Sets the "Place" field using the getLocation() function
MEDINC_BY_STATE_BY_PLACE_BY_RACE["Place"] = MEDINC_BY_STATE_BY_PLACE_BY_RACE.apply(lambda row:  getLocation(row),axis=1)

# Create a function to get the State out of the "Place" field and uses it to set the "Location" field
def getState(place):
    return place.split(",",1)[1]
MEDINC_BY_STATE_BY_PLACE_BY_RACE["Location"] = MEDINC_BY_STATE_BY_PLACE_BY_RACE["Place"].apply(lambda place: getState(place))

# Sets the Query field
MEDINC_BY_STATE_BY_PLACE_BY_RACE["Query Type"] = "Place"

#**********************************************************************************************************
#**********************************************************************************************************
#**********************************************************************************************************

# Combines the contents from the MEDINC_BY_STATE_BY_PLACE_BY_RACE data frame and 
# MEDINC_BY_STATE_BY_RACE data frame into one data frame.

MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_US_BY_RACE
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE.append(MEDINC_BY_STATE_BY_RACE, ignore_index = True)
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE.append(MEDINC_BY_STATE_BY_PLACE_BY_RACE, ignore_index = True)

#**********************************************************************************************************
#**********************************************************************************************************
#**********************************************************************************************************

# Replaces -666666666 with NaN
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE.replace(-666666666, np.nan)

# Choose the columns that you want to keep in the order you want them
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE.loc[:,['Query Type', 'Location', 'Place', 'ALL', 'WHITE', 'BLACK', 'INDIAN', 'ASIAN', 'PACIFIC','OTHER', 'MIX', 'JUST WHITE', 'HISPANIC']]

# Creates a boolean series that returns true if all of the race fields are null and returns False otherwise.
# This series will be used to subset the MEDINC_BY_LOCATION_BY_PLACE_BY_RACE by removing all records 
# where the race fields are all nulls.
logic = \
    ~(
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["ALL"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["WHITE"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["BLACK"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["INDIAN"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["ASIAN"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["PACIFIC"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["OTHER"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["MIX"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["JUST WHITE"] .isnull() & \
        MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["HISPANIC"] .isnull()
    )
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE[logic]

#**********************************************************************************************************
#**********************************************************************************************************
#**********************************************************************************************************

# Saves the contents of the MEDINC_BY_LOCATION_BY_PLACE_BY_RACE data frame to the 
# MedIncomeData.csv csv file
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE.to_csv("./Data/MedIncomeData.csv")