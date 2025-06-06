#import libraries
import os
import re
import pandas as pd
import plotly.express as px

#Load CSV file, already manually preexplored lengths seems to be the best fit
df= pd.read_csv("data/dataframes/length/length.csv")
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

print(df.head(5000))

#there are 4341 articles in summation form 2021 to 2024
#what does it look like when displayed



#histogram visulaisation
article_counts = df['date'].value_counts().reset_index()
article_counts.columns = ['date', 'article_count']
article_counts = article_counts.sort_values(by='date')
fig_hist = px.bar(article_counts, x='date', y='article_count',
                  title=' Number of Articles Per Day (Post Oct 7, 2023)',
                  labels={'date': 'Date', 'article_count': 'Number of Articles'},color='article_count',  # different colors per bar
                  color_continuous_scale='Viridis')
fig_hist.show()

#bar visualisation
daily_article_counts = df.groupby('date').size().reset_index(name='article_count')
fig2 = px.bar(daily_article_counts, x='date', y='article_count',
              title='Number of Articles Published per Day',
              labels={'date': 'Date', 'article_count': 'Article Count'})
fig2.update_layout(xaxis=dict(tickformat="%Y-%m-%d"))
fig2.show()


#data set too wide cant see visualisation properly needs a filter
#possible choices for cut off date to shorten data set, OCt 7 2023
cutoff_date=pd.to_datetime("2023-10-07")
df=df[df['date']>= cutoff_date]

#now try visulaisation again
#histogram visulaisation
article_counts = df.groupby('date').size().reset_index(name='article_count')
fig_hist = px.bar(article_counts, x='date', y='article_count',
                  title=' Number of Articles Per Day (Post Oct 7, 2023)',
                  labels={'date': 'Date', 'article_count': 'Number of Articles'},color='article_count',  # different colors per bar
                  color_continuous_scale='Viridis')
fig_hist.show()

#bar visualisation
article_counts = df.groupby('date').size().reset_index(name='article_count')
fig2 = px.bar(daily_article_counts, x='date', y='article_count',
              title='Number of Articles Published per Day',
              labels={'date': 'Date', 'article_count': 'Article Count'})
fig2.update_layout(xaxis=dict(tickformat="%Y-%m-%d"))
fig2.show()

#visualisation is looking better but needs better filter
#what else can we do???
#maybe filter the amount of words around 200 or more words since WOrdCount says its around how many words is needed for articless to be meaningful

df = df[df['length'] >= 200]

#now try visualisation
#histogram visulaisation
article_counts = df.groupby('date').size().reset_index(name='article_count')
fig_hist = px.bar(article_counts, x='date', y='article_count',
                  title=' Number of Articles Per Day (Post Oct 7, 2023)',
                  labels={'date': 'Date', 'article_count': 'Number of Articles'},color='article_count',  # different colors per bar
                  color_continuous_scale='Viridis')
fig_hist.show()

#bar visualisation
fig2 = px.bar(daily_article_counts, x='date', y='article_count',
              title='Number of Articles Published per Day',
              labels={'date': 'Date', 'article_count': 'Article Count'})
fig2.update_layout(xaxis=dict(tickformat="%Y-%m-%d"))
fig2.show()
#okay better but now try with 100

df = df[df['length'] >= 100]

#now try visualisation
#histogram visulaisation
fig_hist = px.bar(article_counts, x='date', y='article_count',
                  title=' Number of Articles Per Day (Post Oct 7, 2023)',
                  labels={'date': 'Date', 'article_count': 'Number of Articles'},color='article_count',  # different colors per bar
                  color_continuous_scale='Viridis')
fig_hist.show()

#bar visualisation
fig2 = px.bar(daily_article_counts, x='date', y='article_count',
              title='Number of Articles Published per Day',
              labels={'date': 'Date', 'article_count': 'Article Count'})
fig2.update_layout(xaxis=dict(tickformat="%Y-%m-%d"))
fig2.show()

#histogram works best lets use that
#
