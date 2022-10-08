import os
import pandas as pd
from datetime import datetime

data_set = "Kindle_Store_5.json"
directory = "../datasets"
path = os.path.join(directory, data_set)

df = pd.read_json(path, lines=True) #read dataset

# df.isna().any() use this to check if any variables are Na

df = df.fillna("Unnamed Reviewer") # fill the single Na in reviewer name

len_before = len(df.index)
df.loc[df.astype(str).drop_duplicates().index] # complicated code because of "helpful" being a list
len_now = len(df.index)

print("Removed duplicated lines") if len_now != len_before else print("Found no duplicated lines")

print("Finished cleaning Reviews dataset")




# Date histogram code

df_dates = df.copy()
# df_dates = pd.to_datetime(df['unixReviewTime'],unit='s')
df_dates['unixReviewTime'] = pd.to_datetime(df_dates['unixReviewTime'],unit='s')
df_dates['unixReviewTime'] = df_dates['unixReviewTime'].dt.year
df_dates["unixReviewTime"]

# year of review ordered for graph
graph = df_dates["unixReviewTime"].value_counts().sort_index()
graph

# year of review graph (histogram kinda)
ax= graph.plot(kind='bar', title="Review number through the years", y='freq', x = 'Years')
ax.set_xlabel("Year")
ax.set_ylabel("Frequency")

# overall graph stuff
overall_graph = df["overall"].value_counts().sort_index()
overall_graph

overall_plot= overall_graph.plot(kind='bar', title="Overall", y='freq', x = 'Years')
overall_plot.set_ylabel("Frequency")
overall_plot.set_xlabel("Review Grade")

overal_mean = df["overall"].mean() # mean of overall of reviews
print("average review grade:", overal_mean)

# text size graph
df["reviewText_size"] = df["reviewText"].str.len()
word_number_plot = df["reviewText_size"].value_counts().sort_index().plot()
word_number_plot.set_xlabel("Review text word count")

#check average of text size
df["reviewText_size"].mean()