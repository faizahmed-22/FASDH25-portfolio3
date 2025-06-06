#before running this script make sure to take it out of the scripts folder and put it into the FASDH25-portfolio 3 folder otherwise the script will not run
#import libraries
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


# Step 4: Create new data for article counts, taken from the slides and ChatGPT Entry #1
article_counts = df.groupby('date').size().reset_index(name='article_count') # group data by date and count how many articles appear on each date

article_counts['day'] = article_counts['date'].dt.day_name() # add new column that shows the name of the day for each date

article_counts['date_day'] = article_counts['date'].dt.strftime('%b %d, %Y') + ' (' + article_counts['day'] + ')' #  new column that combines the date with the day name 

#Step 5: Create histogram and save it took help from chat gpt entry #2
fig_hist = px.bar(
    article_counts,
    x='date_day',
    y='article_count',
    title='Number of Articles Per Day :)',
    labels={'date_day': 'Date (Day)', 'article_count': 'Number of Articles'},
    color='article_count', #this in particular was taken from chatgpt
    color_continuous_scale='Viridis'
)
fig_hist.show()
#Step 6: Get weekday number and count, partial help from ChatGPT entry #3
df['weekday'] = df['date'].dt.weekday # new column that stores the weekday number for each date

weekday_counts = df['weekday'].value_counts().sort_index().reset_index() # count how many articles fall on each weekday number

weekday_counts.columns = ['Weekday Number', 'Article Count'] # rename the columns to make them more readable


# Step 7: Replace weekday numbers with names
weekday_counts['Weekday'] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Step 8: Plot bar chart between  article count and day
fig_bar = px.bar(
    weekday_counts,
    x='Weekday',
    y='Article Count',
    title=' Articles Published Per Day of the Week',)
fig_bar.show()

#Step 9: Create bar graph between article length sum and month
# Create the month_label for the sorted, filtered data
df2 = df2.sort_values(by='date')
df2['month_label'] = df2['date'].dt.strftime('%b %Y')

fig_length = px.bar(
    df2,  
    x='month_label',
    y='length-sum',
    title='Article Sum Length by Month (Sep 2023 Onwards)',
    labels={'month_label': 'Month', 'length-mean': 'Average Length (words)'},
 
)
fig_length.show()

#Step 10: create graph between article word count mean and month
fig_mean = px.bar(
    df2,  
    x='month_label',
    y='length-mean',
    title=' Average Article Length by Month (Sep 2023 Onwards)',
    labels={'month_label': 'Month', 'length-mean': 'Average Length (words)'},
)
fig_mean.show()

#Step 11: Save histogram and bars as an HTML file
fig_hist.write_html("faiz_article_count_histogram.html")
print("Histogram saved to 'faiz_article_count_histogram.html")
fig_bar.write_html("faiz_weekday_bar_chart.html")
print("Bar chart saved to 'faiz_weekday_bar_chart.html'")
fig_length.write_html("faiz_date_article_length.html")
print("Bar chart saved to 'faiz_monthly_article_length_chart.html'")
fig_mean.write_html("faiz_date_article_mean.html")
print("Bar chart saved to 'faiz_monthly_article_mean_chart.html'")







