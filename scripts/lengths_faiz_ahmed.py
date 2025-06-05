import os
import re
import pandas as pd
import plotly.express as px

# Load the CSV file
df = pd.read_csv("data/dataframes/length/length.csv")
df2= pd.read_csv("data/dataframes/length/length-year-month.csv")

# Step 1: Filter by word count (100 or more words)
df = df[df['length'] >= 100]

# Step 2: Convert year, month, day to datetime
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
# Also convert year and month to datetime objects for filtering and sorting df2
df2['date'] = pd.to_datetime(df2[['year', 'month',]].assign(day=1))


# Step 3: Filter by date (Sep 7, 2023 or later)
cutoff_date = pd.to_datetime("2023-9-7")
df = df[df['date'] >= cutoff_date]

# Filter df2 to include data from September 2023 onwards
cutoff_date_df2 = pd.to_datetime("2023-9-7")
df2 = df2[df2['date'] >= cutoff_date_df2]


# Step 4: Create new data for article counts, taken from Amnas code in excercise 14.2 and ChatGPT Entry #1
article_counts = df.groupby('date').size().reset_index(name='article_count')
article_counts['day'] = article_counts['date'].dt.day_name()
article_counts['date_day'] = article_counts['date'].dt.strftime('%b %d, %Y') + ' (' + article_counts['day'] + ')'

#Step 5: Create histogram and save it took help from chat gpt entry #2
fig_hist = px.bar(
    article_counts,
    x='date_day',
    y='article_count',
    title='Number of Articles Per Day :)',
    labels={'date_day': 'Date (Day)', 'article_count': 'Number of Articles'},
    color='article_count',
    color_continuous_scale='Viridis'
)
fig_hist.show()
#Step 6: Get weekday number and count, partial help from ChatGPT entry #3
df['weekday'] = df['date'].dt.weekday
weekday_counts = df['weekday'].value_counts().sort_index().reset_index()
weekday_counts.columns = ['Weekday Number', 'Article Count']

# Step 7: Replace weekday numbers with names
weekday_counts['Weekday'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Step 8: Plot bar chart between  article count and day
fig_bar = px.bar(
    weekday_counts,
    x='Weekday',
    y='Article Count',
    title=' Articles Published Per Day of the Week',
    color='Article Count',
    color_continuous_scale='Blues')
fig_bar.show()

#Step 9: Create bar graph between article length and month
# Create the month_label for the sorted, filtered data
df2 = df2.sort_values(by='date')
df2['month_label'] = df2['date'].dt.strftime('%b %Y')

fig_length = px.bar(
    df2,  
    x='month_label',
    y='length-sum',
    title='Average Article Length by Month (Sep 2023 Onwards)',
    labels={'month_label': 'Month', 'length-mean': 'Average Length (words)'},
    color='length-mean',
    color_continuous_scale='Greens'
)
fig_length.show()

#Step 10: Save histogram and bar as an HTML file
fig_hist.write_html("faiz_article_count_histogram.html")
print("Histogram saved to 'faiz_article_count_histogram.html")
fig_bar.write_html("faiz_weekday_bar_chart.html")
print("Bar chart saved to 'faiz_weekday_bar_chart.html'")
fig_length.write_html("faiz_date_article_length.html")
print("Bar chart saved to 'faiz_monthly_article_length_chart.html'")






