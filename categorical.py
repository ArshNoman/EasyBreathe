""" This file essentially does the same thing as main.py except it predicts the Air Quality concern levels
based on the U.S. Air Quality Index (https://www.airnow.gov/aqi/aqi-basics/). This makes for more relevant
predictions compared to main.py's model since it's more of a classifier prediction model for only 5 values and
gives more information on how the average citizen must react to a certain level of AQI."""


from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd
import numpy as np
import pickle

""" Loading and preparing the training dataset """

# removing the Date and the AQI columns because we don't want those interfering with the model's learning
df = pd.read_csv('datasets/trainingData.csv').drop(['AQI', 'Date'], axis=1)
# setting the x value to everything but the concern column since that's what we're trying to predict
x = df.drop('concern', axis=1).copy()
# setting the y value to the concern level column
y = df['concern'].copy()

# Converting boolean columns to integers because XGBoost (and most ML models really) can't handle boolean
# values and so we're essentially converting all the "True" to 1 and all the "False" to 0
boolean_cols = x.select_dtypes(include=['bool']).columns.tolist()
x[boolean_cols] = x[boolean_cols].astype(int)

""" Splitting the data and training the model """

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=7, stratify=y)

# Putting the data into a regressor model since we're trying to predict continuous and non-categorical values
# n_estimators is essentially the number of trees in the training

# P.S. I know this is a classifying task, but for some reason the Regressor model is more accurate!
reg = xgb.XGBRegressor(n_estimators=100)
# verbose is True to give us constant updates on the training process
reg.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=True)

importance = reg.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': x.columns, 'Importance': importance})

feature_importance_df = feature_importance_df.sort_values('Importance', ascending=True)

""" Saving the model and opening it to test the blind dataset """

filename = 'xgboost_classifier.pkl'
pickle.dump(reg, open(filename, 'wb'))

""" Running it with the blind dataset to test performance """

# Literally repeating the same process as the previous code, just this time with a different dataset and no training
pred_df = pd.read_csv('datasets/blindData.csv').drop(['AQI', 'Date'], axis=1)
x_pred = pred_df.drop('concern', axis=1).copy()
y_true = pred_df['concern'].copy()

# Convert boolean columns to integers once more but this time for the blind dataset
boolean_cols = x_pred.select_dtypes(include=['bool']).columns.tolist()
x_pred[boolean_cols] = x_pred[boolean_cols].astype(int)

""" Making predictions on the blind test dataset"""

y_pred = reg.predict(x_pred)
# Keeps the predictions restricted to 0 and 5.
y_pred = np.clip(y_pred, 0, 5)
y_pred = np.ceil(y_pred)

""" Calculating the percentage accuracy within a ±3 tolerance margin """

tolerance = 0.5
correct_predictions = np.abs(y_pred - y_true) <= tolerance
accuracy_percentage = (np.sum(correct_predictions) / len(y_true)) * 100
print('\n\nAccuracy Percentage:', str(accuracy_percentage) + '%')

# something fun I added for more prediction data accuracy analysis

epsilon = 1e-10
percentage_error = (np.abs(y_pred - y_true) / (y_true + epsilon)) * 100
print('\n\nPercentage Errors for each data row:\n', str(percentage_error) + '%')

""" Feature importance plotting, once more using Matplotlib """

plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance')
plt.show()

x = np.arange(len(y_true))

""" Plotting the actual vs predicted AQI values to visualize our data and its accuracy """

# Plot the true values and the predicted values
plt.plot(x, y_true, label='True Values')
plt.plot(x, y_pred, label='Predicted Values')
plt.xlabel('Samples')
plt.ylabel('Values')
plt.title('True vs Predicted Values')
plt.legend()
plt.show()
