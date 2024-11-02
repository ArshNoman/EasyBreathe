from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd
import numpy as np
import pickle

""" Loading and preparing the training dataset """

# removing the Date and the concern columns because we don't want those interfering with the model's learning
train_df = pd.read_csv('Bishkek.csv').drop(['Date', 'concern'], axis=1)
# setting the x value to everything but the AQI column since that's what we're trying to predict
X = train_df.drop('AQI', axis=1).copy()
# setting the y value to the AQI column
y = train_df['AQI'].copy()

# Converting boolean columns to integers because XGBoost (and most ML models really) can't handle boolean
# values and so we're essentially converting all the "True" to 1 and all the "False" to 0
boolean_cols = X.select_dtypes(include=['bool']).columns.tolist()
X[boolean_cols] = X[boolean_cols].astype(int)

""" Splitting the data and training the model """

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7)

# Putting the data into a regressor model since we're trying to predict continuous and non-categorical values
# n_estimators is essentially the number of trees in the training
reg = xgb.XGBRegressor(n_estimators=500, objective='reg:squarederror')
# verbose just gives us constant updates on the training process
reg.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=True)

importance = reg.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': importance})

feature_importance_df = feature_importance_df.sort_values('Importance', ascending=True)

""" Saving the model and opening it to test the blind dataset """

with open('xgboost.pkl', 'wb') as model_file:
    # Saving the model file with pickle for potential future usage
    pickle.dump(reg, model_file)

with open('xgboost.pkl', 'rb') as model_file:
    # Opening the model file with pickle
    reg = pickle.load(model_file)

""" Running it with the blind dataset to test performance """

# Literally repeating the same process as the previous code, just this time with a different dataset and no training
blind_test_df = pd.read_csv('blind.csv').drop(['Date', 'concern'], axis=1)
X_blind = blind_test_df.drop('AQI', axis=1)
y_blind_actual = blind_test_df['AQI']

# Convert boolean columns to integers once more but this time for the blind dataset
boolean_cols_blind = X_blind.select_dtypes(include=['bool']).columns.tolist()
X_blind[boolean_cols_blind] = X_blind[boolean_cols_blind].astype(int)

""" Making predictions on the blind test dataset"""

y_blind_pred = reg.predict(X_blind)

""" Calculating the percentage accuracy within a ±3 tolerance margin """
tolerance = 30
within_tolerance = (abs(y_blind_actual - y_blind_pred) <= tolerance).sum()
accuracy_percentage = (within_tolerance / len(y_blind_actual)) * 100
print(f"Percentage of predictions within ±{tolerance} tolerance: {accuracy_percentage:.2f}%")


""" Plotting the actual vs predicted AQI values to visualize our data and its accuracy """

# Using basic matplot lib for this process
plt.figure(figsize=(10, 6))
plt.plot(y_blind_actual.values, label='Actual AQI', marker='o', linestyle='-', markersize=4)
plt.plot(y_blind_pred, label='Predicted AQI', marker='x', linestyle='--', markersize=4)
plt.xlabel('Data Point Index')
plt.ylabel('AQI Value')
plt.title('Actual vs. Predicted AQI Values')
plt.legend()
plt.show()

""" Feature importance plotting, once more using Matplotlib """

plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance')
plt.show()
