import pandas as pd
from datetime import datetime, timedelta

# Load your CSV file
data = pd.read_csv('testdataCH.csv')

# Convert the "Date" column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Set the starting date
start_date = datetime(2024, 11, 3)

# Generate a range of dates starting from the specified start date, incrementing by one hour
data['Date'] = [start_date + timedelta(hours=i) for i in range(len(data))]

# Save the modified data back to CSV
data.to_csv('testdataCH.csv', index=False)
