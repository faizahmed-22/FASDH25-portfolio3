# Importing necessary libraries
import pandas as pd
import plotly.express as px

# Define path to your monthly CSV file
csv_path = ("data/dataframes/n-grams/1-gram/1-gram-year-month.csv")

# Read the CSV file
df = pd.read_csv(csv_path)

# Create 'date' column for monthly summaries
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Define fear and hope related word lists
Fear_related_filter_list = ['fear', 'grief', 'trauma', 'panic', 'death']
Hope_related_filter_list = ['hope', 'solidarity', 'resistance', 'faith', 'courage']
all_words = Fear_related_filter_list + Hope_related_filter_list

# Filter the DataFrame to include only relevant 1-grams
df = df[df['1-gram'].isin(all_words)]

# Categorize the 1-grams (AI help)
df['category'] = df['1-gram'].apply(
    lambda word: 'fear' if word in Fear_related_filter_list
    else 'hope'
)

# Define the time range 
start_date = '2023-01-01'
end_date = '2024-12-31'
df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
print(df)

# Frequency comparison (group by month and category) (AI)
df['month'] = df['date'].dt.to_period('M')
monthly_category_count = (
    df.groupby(['month', 'category'])['count-sum']
      .sum()
      .reset_index()
)

monthly_category_count['month'] = monthly_category_count['month'].astype(str)
print(df ['month'])

# Plot the bar chart
fig = px.bar(
    monthly_category_count,
    x='month',
    y='count-sum',
    color='category',
    barmode='group',
    text='count-sum',
    title='Fear vs Hope 1-gram Frequency by Month (2023–2024)',
    labels={'month': 'Month', 'count-sum': 'Total 1-gram Count'}
)

# Show the chart
fig.show()

# Saving the HTML file
fig.write_html("fear_vs_hope_script 1.html")
print("Plot saved as: fear_vs_hope_script 1.html")




