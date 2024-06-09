import os
import pandas as pd
import numpy as np
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

# Replace values in the 'customer_group_id' column
vekto_quote_no_empty_carts['customer_group_id'].replace({0: 'not logged in', 1: 'general', 2: 'wholesale'}, inplace=True)

# Get unique customer groups
unique_customer_groups = vekto_quote_no_empty_carts['customer_group_id'].unique()

# Create subplots for each customer group
fig, axes = plt.subplots(nrows=1, ncols=len(unique_customer_groups), figsize=(15, 5))

# Plot count plots for each customer group
for i, customer_group in enumerate(unique_customer_groups):
    # Filter dataframe for the specific customer group
    subset_df = vekto_quote_no_empty_carts[vekto_quote_no_empty_carts['customer_group_id'] == customer_group]
    
    # Create a count plot
    sns.countplot(data=subset_df, x='is_active', ax=axes[i])
    
    axes[i].set_title(f'Customer Group: {customer_group}')
    axes[i].set_xlabel('Shopping Cart Status')
    axes[i].set_ylabel('Amount of shopping carts')  # Replace y-axis label
    axes[i].set_xticklabels(['Closed', 'Open'])  # Replace x-axis labels
    
plt.tight_layout()
plt.show()