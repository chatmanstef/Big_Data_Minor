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

# Count the number of logins for each customer_email
login_counts = vekto_quote_has_customer_email['customer_email'].value_counts()

# Categorize customers based on login counts
single_login_customers = login_counts[login_counts == 1].index
two_logins_customers = login_counts[login_counts == 2].index
three_logins_customers = login_counts[login_counts == 3].index
four_logins_customers = login_counts[login_counts == 4].index
more_than_four_logins_customers = login_counts[login_counts > 4].index

# Create subplots for each login count
fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(20, 5))

# Plot count plots for each login count
sns.countplot(data=vekto_quote_has_customer_email[vekto_quote_has_customer_email['customer_email'].isin(single_login_customers)],
              x='is_active', ax=axes[0])
axes[0].set_title('Single Login Customers')
axes[0].set_xlabel('Shopping Cart Status')
axes[0].set_ylabel('Amount of shopping carts')
axes[0].set_xticklabels(['Closed', 'Open'])

sns.countplot(data=vekto_quote_has_customer_email[vekto_quote_has_customer_email['customer_email'].isin(two_logins_customers)],
              x='is_active', ax=axes[1])
axes[1].set_title('Two Logins Customers')
axes[1].set_xlabel('Shopping Cart Status')
axes[1].set_ylabel('Amount of shopping carts')
axes[1].set_xticklabels(['Closed', 'Open'])

sns.countplot(data=vekto_quote_has_customer_email[vekto_quote_has_customer_email['customer_email'].isin(three_logins_customers)],
              x='is_active', ax=axes[2])
axes[2].set_title('Three Logins Customers')
axes[2].set_xlabel('Shopping Cart Status')
axes[2].set_ylabel('Amount of shopping carts')
axes[2].set_xticklabels(['Closed', 'Open'])

sns.countplot(data=vekto_quote_has_customer_email[vekto_quote_has_customer_email['customer_email'].isin(four_logins_customers)],
              x='is_active', ax=axes[3])
axes[3].set_title('Four Logins Customers')
axes[3].set_xlabel('Shopping Cart Status')
axes[3].set_ylabel('Amount of shopping carts')
axes[3].set_xticklabels(['Closed', 'Open'])

sns.countplot(data=vekto_quote_has_customer_email[vekto_quote_has_customer_email['customer_email'].isin(more_than_four_logins_customers)],
              x='is_active', ax=axes[4])
axes[4].set_title('More Than Four Logins Customers')
axes[4].set_xlabel('Shopping Cart Status')
axes[4].set_ylabel('Amount of shopping carts')
axes[4].set_xticklabels(['Closed', 'Open'])

plt.tight_layout()
plt.show()
