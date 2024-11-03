import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# # Load your CSV file
# data = pd.read_csv('./datasets/cities/DHdata.csv')
#
# # Convert the "Date" column to datetime format
# data['Date'] = pd.to_datetime(data['Date'])
#
# # Set the starting date
# start_date = datetime(2024, 11, 3)
#
# # Generate a range of dates starting from the specified start date, incrementing by one hour
# data['Date'] = [start_date + timedelta(hours=i) for i in range(len(data))]
#
# # Save the modified data back to CSV
# data.to_csv('./datasets/cities/DHdata.csv', index=False)

# Load the dataset
data = pd.read_csv('./datasets/cities/DHdata.csv')

# Round all numeric values to the nearest integer
data = data.map(lambda x: round(x) if np.issubdtype(type(x), np.number) else x)

# Save the modified dataset
data.to_csv('./datasets/cities/DHdata.csv', index=False)

