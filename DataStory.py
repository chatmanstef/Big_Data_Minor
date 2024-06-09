import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from PIL import Image
from io import BytesIO

### DATA WRANGLING
# Load the dataset
file_path = 'D:\Programming\Spyder\SeychellesData.csv' # Change the path to correctly point to your SeychellesData.csv location
df = pd.read_csv(file_path) # Load the data into a pandas dataframe

df['Total protein servings'] = df['fishd'] * df['fish12meal'] + df['poultryd'] + df['meatfreshd'] + df['meatprocd']

### FUNCTIONS
# Function to add percentile groups as a new column to the dataframe
def add_percentile_group(df, column_name):
    # Calculate percentiles
    df['percentile_group'] = pd.qcut(df[column_name], q=groups, labels=False)
    # Increment by 1 to make percentile groups start from 1 instead of 0
    df['percentile_group'] += 1
    # Sort the dataframe by percentile group
    df.sort_values(by='percentile_group', inplace=True)
    return df

# Function to calculate the average of each percentile group for a selected column
def calculate_percentile_averages(df, column_name):
    percentile_averages = df.groupby('percentile_group')[column_name].mean()
    return percentile_averages

### TEXT
st.write("# Protein Leverage: The answer to the obesity crisis?")

st.write("The world has seen a shocking increase in obesity over the past few decades. In the animation below, we can see how most countries had obesity rates between 5% and 15% in 1975 and we can see how this quickly rose to 20%-30% with some countries even going above 30%.")

st.video("https://www.youtube.com/watch?v=jMqxTuoWqsQ")

st.write("How did this come to be? One of the more recent theories is called the Protein Leverage Hypothesis (PLH). This hypothesis states that lifeforms require a given amount of protein in their diet and they will eat until this requirement is met. If the protein density of their food is low, this means they have to eat more total food, which leads to overeating. The theory was coined by Professors Raubenheimer and Simpson, two insect biologists first noticed this while researching locusts. They proposed that other species could have similar mechanisms to drive their food preferences. After taking some time to gain traction, the theory was then tested on other animals and also humans.")

st.write("## Early doubts")

st.write("The theory was then tested on other animals and also humans. Gosby et al. (2011) first tested this with a randomised controlled trial and they found a weak link between protein intake and overeating, finding that the lower protein group became more hungry but not significantly increasing their energy intake.")

st.write("## Recent evidence")

st.write("More recently, stronger evidence was found. In the graph below, you can see the total energy intake compared to the protein intake. As the protein intake increases, the total energy intake clearly comes down. This data comes from over 40 different observational trials.")


# Fetching and displaying the image from the Gyazo link
st.write("### Protein intake VS. total energy intake")
response = requests.get("https://i.gyazo.com/06e0c58a8af055aa5bfcd2d29b306a63.png")
image = Image.open(BytesIO(response.content))
st.image(image)

### CUSTOM GRAPH
st.write("## Can we find the effect ourselves?")

st.write("In order to test the hypothesis, let's take a look at a nutritional intake dataset from the Seychelles. This dataset contains both health markers and dietary data, which should allow us to find out if the PLH holds true for the people of the Seychelles.")

st.write("Here you can see the dataset for yourself:")
st.write(df)

st.write("Let's add a column that combines the servings of protein rich foods into one score and make 5 percentile groups based on this score.")

### CUSTOM GRAPH MAKER
st.write("## Custom graph")

# Selector for user to select amount of groups
groups = st.slider("Select the amount of percentile groups", 2, 10)

# Selector for user to select column
selected_marker = 'bmi'

# Selector for user to select column
selected_column = 'Total protein servings'

# Age range filter
age_min, age_max = st.slider("Select an age range", int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))

# Filter the dataframe based on selected age range
df_filtered = df[(df['age'] >= age_min) & (df['age'] <= age_max)]

# Add percentile groups as a new column based on the selected column
df_filtered = add_percentile_group(df_filtered, selected_column)

# Calculate the average of each percentile group for the selected column
percentile_averages = calculate_percentile_averages(df_filtered, selected_marker)

# Plot the bar chart
fig, ax = plt.subplots()
ax.bar(percentile_averages.index, percentile_averages.values)
ax.set_xlabel(f'{selected_column} percentile Group')
ax.set_ylabel(f'Average {selected_marker}')
ax.set_title(f'Average {selected_marker} by {selected_column} percentile Group')
st.pyplot(fig)

st.write("# References:")
st.write("- Gosby AK, Conigrave AD, Lau NS, Iglesias MA, Hall RM, Jebb SA, Brand-Miller J, Caterson ID, Raubenheimer D, Simpson SJ. (2011). Testing protein leverage in lean humans: a randomised controlled experimental study. *PLoS One, 6*(10), e25929. [doi: 10.1371/journal.pone.0025929](https://doi.org/10.1371/journal.pone.0025929)")
st.write("- Raubenheimer, D., & Simpson, S. J. (1999). Integrative models of nutrient balancing: application to insects and vertebrates. Nutritional Ecology of Insects, Mites, Spiders, and Related Invertebrates, 67-100.")
st.write("- Raubenheimer, D., & Simpson, S. J. (2019). Protein Leverage: Theoretical Foundations and Ten Points of Clarification. *Obesity, 27*, 1225-1238. [doi: 10.1002/oby.22531](https://doi.org/10.1002/oby.22531)")
st.write("- Simpson, S. J., & Raubenheimer, D. (2012). The nature of nutrition: a unifying framework from animal adaptation to human obesity. Princeton University Press.")
