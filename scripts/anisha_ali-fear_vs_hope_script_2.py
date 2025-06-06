# Importing necessary libraries
import pandas as pd
import plotly.express as px

#  Define Path to the 1-gram year-month CSV
csv_path = "data/dataframes/n-grams/1-gram/1-gram-year-month.csv"

# Read the CSV file
df = pd.read_csv(csv_path)

# Create a 'date' column for filtering by month
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Define fear and hope related word lists (adding word variants)
Fear_related_filter_list = [
    'fear', 'fears', 'grief', 'trauma', 'panic', 'death', 'deaths', 'died'
]
Hope_related_filter_list = [
    'hope', 'hopes', 'hoped', 'hoping', 'solidarity', 'resistance', 'faith', 'courage'
]
all_words = Fear_related_filter_list + Hope_related_filter_list

# Filter the dataframe to include only relevant 1-grams only
df = df[df['1-gram'].isin(all_words)]

# Adding a category column: 'fear' or 'hope' (Chatgpt help)
df['category'] = df['1-gram'].apply(
    lambda word: 'fear' if word in Fear_related_filter_list else 'hope'
)

# Restrict to timeline: from September 1, 2023 onwards
start_date = '2023-09-01'
df = df[df['date'] >= start_date]

# Group by month and category to get total word counts (frequency comparision) (chatgpt help)
df['month'] = df['date'].dt.to_period('M')
monthly_counts = (
    df.groupby(['month', 'category'])['count-sum']
      .sum()
      .reset_index()
)
monthly_counts['month'] = monthly_counts['month'].astype(str)
print (df ['month'])

# Plot the grouped bar chart (using absolute counts)
fig = px.bar(
    monthly_counts,  
    x='month',
    y='count-sum',
    color='category',
    barmode='group',
    text='count-sum',  
    title='Fear vs Hope 1-gram Frequency by Month (Sep 2023 – Present)',
    labels={'month': 'Month', 'count-sum': 'Total Word Count'}
)

# Show the chart
fig.show()

# Saving the HTML file
fig.write_html("fear_vs_hope_script_2.html")
print("Plot saved as: fear_vs_hope_script_2.html")

