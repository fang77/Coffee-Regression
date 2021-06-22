import pandas as pd
import numpy as np
import statsmodels.api as sm
import math
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
# Filename to be used
filename = 'merged_data_cleaned.csv'

# Main operation, Analysis of picked coffee sources.
def main():
    df = clean(filename)
    df = df.fillna(0, inplace=False)
    analysis_taste(df)

def clean(filename):  
    nca = pd.read_csv(filename)
    print(nca.head())
    print(nca.columns)
    return nca

def regress(x, y):
    model = sm.OLS(x,y).fit()
    predictions = model.predict(y)

    print(model.summary())
    print(predictions)
    plt.scatter(y,x)
    plt.plot(y, predictions, color = 'red')
    plt.show()

def analysis_taste(df):
    print(df)
    taste_altitude = pd.DataFrame()
    taste_altitude = df.iloc[:, 18:31]
    taste_altitude['species'] =df.iloc[:, 1]
    taste_altitude['owner'] =df.iloc[:, 2]
    taste_altitude['country'] = df.iloc[:,3]

    altitude_range = pd.DataFrame(columns =["altitude", "low", "high" , "mean", "range"])

    altitude_range.low = df.altitude_low_meters
    altitude_range.high = df.altitude_high_meters
    altitude_range.mean = df.altitude_mean_meters
    altitude_range.range = altitude_range.high - altitude_range.low
    altitude_range.altitude = df.Altitude

    print(altitude_range.head())
    print(taste_altitude.head())

    #regression altitude vs height
    
    print(altitude_range.mean)

    x = altitude_range.high
    y = taste_altitude.Flavor

    classify_range = []

    for i in altitude_range.high:
        if i >= np.mean(altitude_range.high):
            classify_range.append("Above 1799m")
        else:
            classify_range.append("Below 1799m")

    temp_count = 0
    below = []
    above = []
    for x in classify_range:
        if x == "Above 1799m":
            above.append(y[temp_count])
        else:
            below.append(y[temp_count])
        temp_count = temp_count + 1
    

    test = f_oneway(below, above)
    print(test)
    
    regression_taste_altitude = pd.DataFrame(columns=["altitude", "taste"])
    regression_taste_altitude.altitude = x
    regression_taste_altitude.taste = y
    regression_taste_altitude = regression_taste_altitude[(regression_taste_altitude != 0).all(1)]
    regression_taste_altitude = regression_taste_altitude[(regression_taste_altitude < 5000).all(1)]

    regress(regression_taste_altitude.altitude,regression_taste_altitude.taste)
    



#run script
main()
