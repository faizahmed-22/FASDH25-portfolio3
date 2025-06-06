# Loading the necessary libraries
import pandas as pd
import plotly.express as px

# Loading original topic model dataset
df = pd.read_csv("data/dataframes/topic-model/topic-model.csv")

# Applying date filter to keep articles between 7 September 2023 and 16 April 2024
df = df[
    (df["year"] > 2023) |
    ((df["year"] == 2023) & (df["month"] > 9)) |
    ((df["year"] == 2023) & (df["month"] == 9) & (df["day"] > 7))
]

# Creating a 'month_year' column for grouping
df["month_year"] = df["year"].astype(str) + "-" + df["month"].astype(str) # learnt previously in exploration (ChatGPT (1))

# Removing rows where the topic label is -1 (unclassified rows)
df = df[df["Topic"] != -1]

# Creating a more descriptive label for each topic by combining four keyword columns (helps us identify and differentiate topics in the graph)
df["Topic_Label"] = (
    df["topic_1"] + ", " +
    df["topic_2"] + ", " +
    df["topic_3"] + ", " +
    df["topic_4"]
) # learnet previously in exploration (ChatGPT (2))
 
# Grouping the data by topic label and month year, then counting number of articles in each group
grouped = df.groupby(["Topic_Label", "month_year"]).size().reset_index(name="Article_Count") # learnt previously in exploration (ChatGPT (3))

# Selecting 5 meaningful topics after reviewing top 20
selected_labels = [
    "captives, hamas, release, hostages",
    "gaza, people, killed, younis",
    "hospital, patients, medical, hospitals",
    "iran, iranian, syria, us",
    "bank, west, israeli, palestinian"  # replaced the vague topic
]

# Filter for only selected topic labels
df = df[
    (df["Topic_Label"] == "captives, hamas, release, hostages") |
    (df["Topic_Label"] == "gaza, people, killed, younis") |
    (df["Topic_Label"] == "hospital, patients, medical, hospitals") |
    (df["Topic_Label"] == "iran, iranian, syria, us") |
    (df["Topic_Label"] == "bank, west, israeli, palestinian")
]

# Group by topic and month-year
grouped = df.groupby(["Topic_Label", "month_year"]).size().reset_index(name="Article_Count")


# Plotting a bar chart showing article count per year for each top topic
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
    title="Top 5 Topics from Sept 2023 to Apr 2024 (by Month)"
)

# Showing and saving chart
fig.show()
fig.write_html("topic-visualisation-top5_SaraBaig.html")


# Visualised the top 5 topics (based on keywords) in articles published between 7 Sept 2023 and 16 April 2024
