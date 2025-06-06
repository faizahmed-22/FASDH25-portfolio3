# Loading the pandas library
import pandas as pd

# Loading the topic modeling dataset into the pandas DataFrame
df = pd.read_csv("data/dataframes/topic-model/topic-model.csv")

# Displaying first five rows to look at the data structure and values
print("FIRST 5 ROWS:")
print(df.head())

# Printing the column names to look if fields are available for analysis
print("\nCOLUMN NAMES:")
print(df.columns)

# Checking data types of each column to look how they are stored
print("\nDATA TYPES:")
print(df.dtypes)

# Understanding the shape of dataset, i.e., the number of rows and columns
print("\nSHAPE OF DATAFRAME:")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Printing unique publication years found in dataset to understand time coverage
print("\nUNIQUE YEARS:")
print(df["year"].unique())

# Applying a filter to isolate only articles which were published between 7 Sept 2023 and 16 April 2024
# based on a combination of year, month, and day columns)
df_filtered = df[
    (df["year"] > 2023) |
    ((df["year"] == 2023) & (df["month"] > 9)) |
    ((df["year"] == 2023) & (df["month"] == 9) & (df["day"] > 7)) |
    (df["year"] == 2024) & ((df["month"] < 4) | ((df["month"] == 4) & (df["day"] <= 16)))
].copy() #.copy() - took help from ChatGPT(0) to avoid SettingWithCopyWarning in output


# Displaying the filtered dataset to check the result of the date-based filter
print("\nFILTERED ARTICLES AFTER 7 SEPTEMBER 2023:")
print(df_filtered.head())
print("Number of articles after 2023-09-07:", len(df_filtered))

# Looking at the values in 'Topic' column
print("\nTOPIC VALUE COUNTS:")
print(df_filtered["Topic"].value_counts())

# Showing the 20 most frequent topics to give a broader view before selecting top 5 for visualisation
print("\nTOP 20 TOPICS (with article counts):")
print(df_filtered["Topic"].value_counts().head(20))

# Showing example keywords for each of the top 20 topic numbers
top_20_topic_nums = df_filtered["Topic"].value_counts().head(20).index

# After reviewing the top 20 topic keywords, we decided to exclude Topic 2 (my, her, she, we) because it was vague and unclear
# We chose to replace it with Topic 0 (bank, west, israeli, palestinian) for its clearer thematic focus

print("\nEXAMPLE TOPIC KEYWORDS FOR TOP 20 TOPICS:")
for topic_num in top_20_topic_nums:
    sample_row = df_filtered[df_filtered["Topic"] == topic_num].head(1)
    print(f"Topic {topic_num}:",
          sample_row["topic_1"].values[0],
          sample_row["topic_2"].values[0],
          sample_row["topic_3"].values[0],
          sample_row["topic_4"].values[0])

# Printing keywords assigned to each article under topic_1 to topic_4 (helps evaluate whether the topics carry meaningful information)
# One topic includes pronouns like 'my, her, she, we' — these are less self-explanatory, so I read those articles to interpret their theme.
print("\nSAMPLE TOPIC KEYWORDS (topic_1 to topic_4):")
print(df_filtered[["topic_1", "topic_2", "topic_3", "topic_4"]].head())

# Applied an initial filter, and examined topic and keyword patterns

# Importing the necessary library
import plotly.express as px

# Creating a month-year column
df_filtered["month_year"] = df_filtered["year"].astype(str) + "-" + df_filtered["month"].astype(str)
# help from ChatGPT (1) to create a new column that combines year and month into a single string (like '2023-10').
# This made it easier to group and visualize topics by month later on.
# I understood that we can convert integers to strings using .astype(str), and combine them with '+'.


# Removing unclassified topics
df_filtered = df_filtered[df_filtered["Topic"] != -1]

# Creating Topic_Label from keywords #help  from ChatGPT (2)
# I used AI to figure out how to combine four keyword columns into one readable topic label.
# This helped me understand how to create custom text-based categories in a dataset.
# I learned that using '+' with commas is a simple way to join multiple columns into one.
df_filtered["Topic_Label"] = (
    df_filtered["topic_1"] + ", " +
    df_filtered["topic_2"] + ", " +
    df_filtered["topic_3"] + ", " +
    df_filtered["topic_4"]
)

# Grouping by Topic_Label and month_year
grouped = df_filtered.groupby(["Topic_Label", "month_year"]).size().reset_index(name="Article_Count") #help from ChatGPT (3)
# AI helped me understand how to group my data by topic and month, and count how many articles fall under each.
# This allowed me to prepare the data for a grouped bar chart.
# I now understand how .groupby() with .size() works, and how reset_index gives a cleaner DataFrame.

# Selecting top 20 topics overall (by total count)
top_20_labels = grouped.groupby("Topic_Label")["Article_Count"].sum().sort_values(ascending=False).head(20).index #help from ChatGPT (4)
# AI helped me to find the most common topics across the dataset.
# This code helped me select the top 20 topics by total article count.
# I learned that grouping and summing values, then sorting and selecting with .head() is a clear way to rank categories.


# Getting the list of top 20 topic labels
top_20_labels = grouped.groupby("Topic_Label")["Article_Count"].sum().sort_values(ascending=False).head(20).index.tolist()
# Filtering grouped data using OR conditions
grouped = grouped[
    (grouped["Topic_Label"] == top_20_labels[0]) |
    (grouped["Topic_Label"] == top_20_labels[1]) |
    (grouped["Topic_Label"] == top_20_labels[2]) |
    (grouped["Topic_Label"] == top_20_labels[3]) |
    (grouped["Topic_Label"] == top_20_labels[4]) |
    (grouped["Topic_Label"] == top_20_labels[5]) |
    (grouped["Topic_Label"] == top_20_labels[6]) |
    (grouped["Topic_Label"] == top_20_labels[7]) |
    (grouped["Topic_Label"] == top_20_labels[8]) |
    (grouped["Topic_Label"] == top_20_labels[9]) |
    (grouped["Topic_Label"] == top_20_labels[10]) |
    (grouped["Topic_Label"] == top_20_labels[11]) |
    (grouped["Topic_Label"] == top_20_labels[12]) |
    (grouped["Topic_Label"] == top_20_labels[13]) |
    (grouped["Topic_Label"] == top_20_labels[14]) |
    (grouped["Topic_Label"] == top_20_labels[15]) |
    (grouped["Topic_Label"] == top_20_labels[16]) |
    (grouped["Topic_Label"] == top_20_labels[17]) |
    (grouped["Topic_Label"] == top_20_labels[18]) |
    (grouped["Topic_Label"] == top_20_labels[19])
]

# Ploting the grouped bar chart
fig = px.bar(
    grouped,
    x="month_year",
    y="Article_Count",
    color="Topic_Label",
    barmode="group",
    labels={
        "month_year": "Month-Year",
        "Article_Count": "Number of Articles",
        "Topic_Label": "Topic"
    },
    title="Top 20 Topics from Sept 2023 to Apr 2024 (by Month)"
)

fig.show()
fig.write_html("topic-exploration-top20_SaraBaig.html")

# End of exploration

