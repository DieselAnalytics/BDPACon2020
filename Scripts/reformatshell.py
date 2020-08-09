# Import required libraries
import pandas as pd
import numpy as np
import os

# Set the working directory
os.chdir("C:/Users/ryanwade44/Documents/BDPACON2020/vscode/data")

# Reads the contents of ACS2018_Table_Shells.csv into 
# a pandas data frame
dfShellData = pd.read_csv("ACS2018_Table_Shells.csv")

# Finds all instances in the data frame that is populated with empty
# strings using a regular expression and replaces it with a NaN
dfShellData = dfShellData.replace(r"^\s*$", np.nan, regex = True)

# Define logic needed to get the category information and uses it
# in the where condition. When that condition is met the "Stub"
# field is used, otherwise NaN is used.
logic = dfShellData["Stub"].shift(periods =-1).str[0:8] == "Universe"
dfShellData["Category"] = np.where(logic, dfShellData["Stub"], np.nan)

# Use the ffill() method to replace the NaN with values from the
# preceding non-NaN cells
dfShellData["Category"] = dfShellData["Category"].ffill()

# Applies a filter that only keeps records that are not
# null in the "Line" field. The records that have null
# values in the "Line" field represent records that are
# not needed
dfShellData = dfShellData[dfShellData["Line"].notnull()]

# Subsets the data frame to only innclude the columns that are needed and 
# replacing the names with more meaningful names when needed.
dfShellData = dfShellData.loc[:,["Category", "Table ID", "UniqueID", "Stub"]]
dfShellData.columns = ["Category", "Table ID", "Variable", "Variable Description"]

# Reset the index
dfShellData.reset_index(inplace = True, drop = True)

# Save the contents in the data frame to a csv file
dfShellData.to_csv("ACS2018_Table_Shells_Reformatted.csv")