import pandas as pd 
import numpy as np 
import censusdata
import os

search_criteria = "median family income"

income_variables = censusdata.search('acs5', 2018,'concept', search_criteria)
dfIV = pd.DataFrame(income_variables, columns=["Variable","Concepts","Labels"])
dfIV = dfIV[dfIV["Variable"] != "GEO_ID"]