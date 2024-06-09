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

# Replace values in the 'customer_group_id' column
vekto_quote_has_customer_email['customer_group_id'].replace({0: 'not logged in', 1: 'general', 2: 'wholesale'}, inplace=True)

# Define bins for order size ranges
bins = [0, .01, 10, 50, 150, 300, float('inf')]
labels = ['€0', '€0-€10', '€10-€50', '€50-€150', '€150-€300', '€300>']

# Create a new column for order size range
vekto_quote_has_customer_email['order_size_range'] = pd.cut(vekto_quote_has_customer_email['subtotal'], bins=bins, labels=labels, right=False)

# Create subplots for each order size range
fig, axes = plt.subplots(nrows=1, ncols=len(labels), figsize=(15, 5))

# Plot count plots for each order size range
for i, order_size_range in enumerate(labels):
    # Filter dataframe for the specific order size range
    subset_df = vekto_quote_has_customer_email[vekto_quote_has_customer_email['order_size_range'] == order_size_range]
    
    # Create a count plot
    sns.countplot(data=subset_df, x='is_active', ax=axes[i])
    
    axes[i].set_title(f'Order Size Range: {order_size_range}')
    axes[i].set_xlabel('Shopping Cart Status')
    axes[i].set_ylabel('Amount of shopping carts')
    axes[i].set_xticklabels(['Closed', 'Open'])

plt.tight_layout()
plt.show()
