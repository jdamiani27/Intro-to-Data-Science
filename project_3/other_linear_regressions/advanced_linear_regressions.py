import numpy as np
import pandas as pd
import scipy
import statsmodels
from datetime import datetime


def predictions(weather_turnstile):

    f = lambda x: datetime.strptime(x, "%Y-%m-%d").weekday()

    # Select Features (try different features!)
    features = weather_turnstile[['rain', 'fog', 'precipi', 'Hour', 'mintempi', 'maxtempi']]
    features['weekday'] = weather_turnstile['DATEn'].apply(f)

    # Add UNIT to features using dummy variables
    dummy_units = pd.get_dummies(weather_turnstile['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Create polynomial features
    #features['precipi'] = features['precipi']**3
    
    # Values
    values = weather_turnstile[['ENTRIESn_hourly']]
    m = len(values)

    features['ones'] = np.ones(m) # Add a column of 1s (y intercept)
    
    #print features.tail()
    
    # Convert features and values to numpy arrays
    features_array = np.array(features)
    values_array = np.array(values).flatten()
    features_array_transpose = features_array.transpose()
    
    theta = np.dot(np.dot(np.linalg.pinv(np.dot(features_array_transpose, features_array)), features_array_transpose), values_array)
    prediction = np.dot(features_array, theta)

    return prediction



def compute_r_squared(data, predictions):
    SST = ((data-np.mean(data))**2).sum()
    SSReg = ((predictions-np.mean(data))**2).sum()
    r_squared = SSReg / SST

    return r_squared

if __name__ == "__main__":
    input_filename = "turnstile_data_master_with_weather.csv"
    turnstile_master = pd.read_csv("turnstile_data_master_with_weather.csv")
    predicted_values = predictions(turnstile_master)
    r_squared = compute_r_squared(turnstile_master['ENTRIESn_hourly'], predicted_values) 

    print r_squared