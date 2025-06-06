# Importing necessary libraries
# Pandas is used for data manipulation and plotly.express for interactive plotting
import pandas as pd
import plotly.express as px

# Loading the 1-gram dataset which contains word frequencies by year and month
df = pd.read_csv("data/dataframes/n-grams/1-gram/1-gram-year-month.csv")

# Looking at the structure
# Load the 1-gram dataset which contains word frequencies by year and month
print("Columns:", df.columns)

# Display the first few rows of the dataset to get an overview of the data
print(df.head())

# Create a new datetime column using year and month (day is set to 1)
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Print the earliest and latest dates in the dataset to understand the time covered
print("Date range in data:", df['date'].min(), "to", df['date'].max())

# Define fear/hope words (basic set)
fear_words = ['fear', 'grief', 'trauma']
hope_words = ['hope', 'faith', 'solidarity']

# Combine both lists into one for filtering
all_words = fear_words + hope_words

# Filter the dataset to include only rows where the 1-gram matches a fear or hope word
# Using .copy() to avoid a SettingWithCopyWarning later
df_filtered = df[df['1-gram'].isin(all_words)].copy()

# Add a new column called 'category' to label each word as either 'fear' or 'hope' (AI HELP)
df_filtered['category'] = df_filtered['1-gram'].apply(
    lambda w: 'fear' if w in fear_words else 'hope'
)

# Filter for for 2023–2024
df_filtered = df_filtered[(df_filtered['date'] >= '2023-09-01') & (df_filtered['date'] <= '2024-04-30')]

# Group by month and 1-gram
df_filtered['month'] = df_filtered['date'].dt.to_period('M')

# Group the filtered data by month and word
# Sum the total word counts to get overall frequency per month per word
test_group = df_filtered.groupby(['month', '1-gram'])['count-sum'].sum().reset_index()

# Convert the 'month' period to a string so it displays nicely on the x-axis in the chart
test_group['month'] = test_group['month'].astype(str)

# Trying a test line chart
fig = px.line(
    test_group,
    x='month',
    y='count-sum',
    color='1-gram',
    title='Exploration: Monthly Frequency of Selected Fear/Hope 1-grams',
    labels={'month': 'Month', 'count-sum': 'Total Word Count'}
)

# Display the interactive chart in a browser window
fig.show()

# Save the chart as an HTML file so it can be opened later
fig.write_html("exploration-script-1.html")
print("Exploration file saved as: exploration-script-1.html")
