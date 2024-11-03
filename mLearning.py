import pandas as pd
import numpy as np

import pickle


def make_prediction(date, city):
    date = date + ' 12:00:00'

    cities = {'Apex': 'APdata.csv', 'Asheville': 'AVdata.csv', 'Burlington': 'BGdata.csv', 'Cary': 'CAdata.csv',
              'Concord': 'CCdata.csv', 'Chapel Hill': 'CHdata.csv', 'Charlotte': 'CLdata.csv', 'Durham': 'DHdata.csv',
              'Fayetteville': 'FYdata.csv', 'Greensboro': 'GBdata.csv', 'Gastonia': 'GTdata.csv', 'Greenville': 'GVdata.csv',
              'High Point': 'HPdata.csv', 'Huntersville': 'HVdata.csv', 'Jacksonville': 'JVdata.csv', 'Kannapolis': 'KPdata.csv',
              'Raleigh': 'RLdata.csv', 'Wake Forest': 'WFdata.csv', 'Wilmington': 'WLdata.csv', 'Winston-Salem': 'WSdata.csv'}

    filename = cities[city]

    df = pd.read_csv(filename)

    pred_df = df[df['Date'] == date].drop(['AQI', 'Date'], axis=1)

    # Convert boolean columns to numeric
    boolean_cols = pred_df.select_dtypes(include=['bool']).columns.tolist()
    pred_df[boolean_cols] = pred_df[boolean_cols].astype(int)

    reg_aqi = pickle.load(open('NCaqi.pkl', 'rb'))

    y_pred = reg_aqi.predict(pred_df)
    y_pred_aqi = np.clip(y_pred, 0, 5)

    reg_concern = pickle.load(open('NCconcern.pkl', 'rb'))

    y_pred = reg_concern.predict(pred_df)
    y_pred_concern = np.clip(y_pred, 0, 5)

    return [round(y_pred_aqi[0]), round(y_pred_concern[0])]
