import pandas as pd
import numpy as np

import pickle


def make_prediction(date, city):
    date = date + ' 12:00:00'

    cities = {'Apex': 'datasets/cities/APdata.csv', 'Asheville': 'datasets/cities/AVdata.csv', 'Burlington': 'datasets/cities/BGdata.csv', 'Cary': 'datasets/cities/CAdata.csv',
              'Concord': 'datasets/cities/CCdata.csv', 'Chapel Hill': 'datasets/cities/CHdata.csv', 'Charlotte': 'datasets/cities/CLdata.csv', 'Durham': 'datasets/cities/DHdata.csv',
              'Fayetteville': 'datasets/cities/FYdata.csv', 'Greensboro': 'datasets/cities/GBdata.csv', 'Gastonia': 'datasets/cities/GTdata.csv', 'Greenville': 'datasets/cities/GVdata.csv',
              'High Point': 'datasets/cities/HPdata.csv', 'Huntersville': 'datasets/cities/HVdata.csv', 'Jacksonville': 'datasets/cities/JVdata.csv', 'Kannapolis': 'datasets/cities/KPdata.csv',
              'Raleigh': 'datasets/cities/RLdata.csv', 'Wake Forest': 'datasets/cities/WFdata.csv', 'Wilmington': 'datasets/cities/WLdata.csv', 'Winston-Salem': 'datasets/cities/WSdata.csv'}

    filename = cities[city]

    df = pd.read_csv(filename)

    pred_df = df[df['Date'] == date].drop(['Date'], axis=1)

    # Convert boolean columns to numeric
    boolean_cols = pred_df.select_dtypes(include=['bool']).columns.tolist()
    pred_df[boolean_cols] = pred_df[boolean_cols].astype(int)

    reg_aqi = pickle.load(open('NCaqi.pkl', 'rb'))

    y_pred_aqi = reg_aqi.predict(pred_df)

    reg_concern = pickle.load(open('NCconcern.pkl', 'rb'))

    y_pred = reg_concern.predict(pred_df)
    y_pred_concern = np.clip(y_pred, 0, 5)

    return {'aqi': round(y_pred_aqi[0]), 'concern': round(y_pred_concern[0])}
