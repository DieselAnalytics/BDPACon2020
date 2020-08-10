# 
import pandas as pd
import numpy as np
import censusdata

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

MEDINC_BY_STATE_BY_RACE["Location"] = MEDINC_BY_STATE_BY_RACE.apply(lambda row:  getLocation(row),axis=1)
MEDINC_BY_STATE_BY_RACE["Place"] = MEDINC_BY_STATE_BY_RACE["Location"]

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

MEDINC_BY_STATE_BY_PLACE_BY_RACE["Place"] = MEDINC_BY_STATE_BY_PLACE_BY_RACE.apply(lambda row:  getLocation(row),axis=1)

# Create a function to get the location name
def getState(place):
    return place.split(",",1)[1]

MEDINC_BY_STATE_BY_PLACE_BY_RACE["Location"] = MEDINC_BY_STATE_BY_PLACE_BY_RACE["Place"].apply(lambda place: getState(place))

MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_STATE_BY_PLACE_BY_RACE
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_STATE_BY_RACE.append(MEDINC_BY_STATE_BY_PLACE_BY_RACE, ignore_index = True)

# Replaced -666666666.0 with NAN
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["ALL"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["ALL"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["WHITE"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["WHITE"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["BLACK"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["BLACK"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["INDIAN"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["INDIAN"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["ASIAN"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["ASIAN"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["PACIFIC"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["PACIFIC"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["OTHER"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["OTHER"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["MIX"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["MIX"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["JUST WHITE"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["JUST WHITE"].replace(-666666666.0, np.nan)
# MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["HISPANIC"] = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["HISPANIC"].replace(-666666666.0, np.nan)

MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE.loc[:,['Location', 'Place', 'ALL', 'WHITE', 'BLACK', 'INDIAN', 'ASIAN', 'PACIFIC','OTHER', 'MIX', 'JUST WHITE', 'HISPANIC']]
logic = ~(MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["ALL"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["WHITE"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["BLACK"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["INDIAN"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["ASIAN"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["PACIFIC"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["OTHER"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["MIX"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["JUST WHITE"] .isnull() & MEDINC_BY_LOCATION_BY_PLACE_BY_RACE["HISPANIC"] .isnull())
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE = MEDINC_BY_LOCATION_BY_PLACE_BY_RACE[logic]
MEDINC_BY_LOCATION_BY_PLACE_BY_RACE.to_csv("MedIncomeData.csv")

# MEDINC_BY_STATE_BY_RACE["Geography"][0].name
# geographies = censusdata.geographies(censusdata.censusgeo([('state','50'),('place','*')]), 'acs5', 2018)
# geographies