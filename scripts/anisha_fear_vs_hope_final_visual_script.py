# Importing necessary libraries
import pandas as pd
import plotly.express as px

# Define path to the 1-gram year-month CSV file. This dataset includes monthly word frequencies and metadata like year and month.
csv_path = "data/dataframes/n-grams/1-gram/1-gram-year-month.csv"

# Loading the CSV file
df = pd.read_csv(csv_path)

# Create a 'date' column using year and month to help with time-based filtering
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Define fear and hope related word lists (including variants. These words will help identify and compare fear and hope-related language.
Fear_related_filter_list = [
    'fear', 'fears', 'grief', 'trauma', 'panic', 'death', 'deaths', 'died'
]
Hope_related_filter_list = [
    'hope', 'hopes', 'hoped', 'hoping', 'solidarity', 'resistance', 'faith', 'courage'
]
 
# Combine both lists into a single list for filtering
all_words = Fear_related_filter_list + Hope_related_filter_list

# # Filter the dataset to keep only rows where the 1-gram appears in our defined word lists (AI partial help)
df = df[df['1-gram'].isin(all_words)]

# Add a new column called 'category' that labels each 1-gram as either 'fear' or 'hope' (chatgpt help)
df['category'] = df['1-gram'].apply(
    lambda word: 'fear' if word in Fear_related_filter_list else 'hope'
)

# Restrict to timeline: from 7 September 2023 to 16 April 2024
start_date = '2023-09-07'
end_date = '2024-04-16'
df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Create 'month' column and group by month and category using count-mean
df['month'] = df['date'].dt.to_period('M')
monthly_means = (
    df.groupby(['month', 'category'])['count-mean']
      .mean()
      .reset_index()
)

# Convert 'month' column to string format so it can be used cleanly on the x-axis in Plotly
monthly_means['month'] = monthly_means['month'].astype(str)

# Plot using average mentions per article
fig = px.bar(
    monthly_means,
    x='month',            # x-axis: Month
    y='count-mean',       # y-axis: Avg mentions per article
    color='category',     # Different color for fear and hope
    barmode='group',      # Bars for fear and hope are side by side
    text='count-mean',    # Display numeric values above each bar
    title='Fear vs Hope – Avg Mentions per Article (Sep 7, 2023 – Apr 16, 2024)',
    labels={'month': 'Month', 'count-mean': 'Avg Mentions per Article'},
    color_discrete_map={'fear': 'red', 'hope': 'blue'}
    
)

# Format bar labels to show 2 decimal points and position them clearly above each bar (AI)
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

# Adjust layout to ensure labels don’t overlap and look consistent
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# Show the chart in the browser
fig.show()

# Save as an HTML file
fig.write_html("fear_vs_hope_final_visual_script.html")
print("Plot saved as: fear_vs_hope_final_visual_script.html")
