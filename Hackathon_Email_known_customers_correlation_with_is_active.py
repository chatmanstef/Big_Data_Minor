import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Directory containing CSV files
folder_path = "D:\\Programming\\Vekto Hackathon\\HappyHorizonsCleaned"

# List all CSV files in the directory
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Create a dataframe for each CSV file
for csv_file in csv_files:
    # Extract dataframe name from CSV filename and replace '-' with '_'
    dataframe_name = os.path.splitext(csv_file)[0].replace("-_", "_").replace("-", "_")
    
    # Read CSV file into dataframe
    df = pd.read_csv(os.path.join(folder_path, csv_file))
    
    # Assign dataframe to a variable with the modified name
    globals()[dataframe_name] = df

# Find the correlation between 'is_active' being 1 and all other columns
correlation = vekto_quote_has_customer_email.corr()['is_active'].sort_values(ascending=False)

print(correlation)