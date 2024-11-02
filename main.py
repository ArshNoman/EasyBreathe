from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import xgboost as xgb
import pandas as pd
import numpy as np
import pickle

# THIS IS A TEST TO SEE IF GIT COMMITS WORK

df = pd.read_csv('Bishkek.csv').drop(['AQI', 'Date'], axis=1)

x = df.drop('concern', axis=1).copy()
y = df['concern'].copy()

boolean_cols = x.select_dtypes(include=['bool']).columns.tolist()
# Convert boolean columns to numeric
x[boolean_cols] = x[boolean_cols].astype(int)

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=7, stratify=y)

reg = xgb.XGBRegressor(n_estimators=10)
reg.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=True)

importance = reg.feature_importances_
feature_importance_df = pd.DataFrame({'Feature': x.columns, 'Importance': importance})

feature_importance_df = feature_importance_df.sort_values('Importance', ascending=True)

filename = 'xgboost.pkl'
pickle.dump(reg, open(filename, 'wb'))

pred_df = pd.read_csv('blind.csv').drop(['AQI', 'Date'], axis=1)

x_pred = pred_df.drop('concern', axis=1).copy()
y_true = pred_df['concern'].copy()

boolean_cols = x_pred.select_dtypes(include=['bool']).columns.tolist()
# Convert boolean columns to numeric
x_pred[boolean_cols] = x_pred[boolean_cols].astype(int)


y_pred = reg.predict(x_pred)
y_pred = np.clip(y_pred, 0, 5)
y_pred = np.ceil(y_pred)
mse = mean_squared_error(y_true, y_pred)
print('\n\nMean Squared Error (MSE):', mse)

tolerance = 0.5
correct_predictions = np.abs(y_pred - y_true) <= tolerance
accuracy_percentage = (np.sum(correct_predictions) / len(y_true)) * 100
print('\n\nAccuracy Percentage:', str(accuracy_percentage) + '%')

epsilon = 1e-10
percentage_error = (np.abs(y_pred - y_true) / (y_true + epsilon)) * 100
print('\n\nPercentage Errors for each data row:\n', str(percentage_error) + '%')

median_error = np.median(percentage_error)
mean_error = np.mean(percentage_error)

print("\n\nMedian Percentage Error:", median_error)
# print("Mean Percentage Error:", mean_error)

plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance')
plt.show()

x = np.arange(len(y_true))

# Plot the true values and the predicted values
plt.plot(x, y_true, label='True Values')
plt.plot(x, y_pred, label='Predicted Values')
plt.xlabel('Samples')
plt.ylabel('Values')
plt.title('True vs Predicted Values')
plt.legend()
plt.show()
