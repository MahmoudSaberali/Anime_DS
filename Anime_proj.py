# import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

pd.set_option("display.max_columns", None)

# import dataset
anime_df = pd.read_csv("anime.csv")

# Check the head of the DataFrame
print(anime_df.head())

# Check the tail of the DataFrame
print(anime_df.tail())

# rows-cols
print(anime_df.shape)

# Details
print(anime_df.info())

# dataset Statistics
print(anime_df.describe())  # for numbers
print(anime_df.describe(include=object))  # for object

# Column names
print(anime_df.columns)

# Check Null values and handle it
print(anime_df.isna().sum().sort_values(ascending=False))
print("-"*75)
print(anime_df['Demographic'].value_counts().sum()/1000*100 -100)  # %47.9 of the col is null
print("-"*75)
print(anime_df["Demographic"].value_counts())
# Made two function to reasonably treat with null values


def get_percentage(series: pd.Series):
    number_of_each_cat = int(series.value_counts().sum())  # number of non-null
    dict_ = series.value_counts().to_dict()  # change the series to dict
    dict_of_percentage = {}
    for key_, values_ in zip(dict_.keys(), dict_.values()):
        dict_of_percentage[key_] = float(int(values_) / number_of_each_cat)
    return dict_of_percentage


def fill_na_by_percentages(dict_of_percentages, series: pd.Series, name_of_column):
    fill_values = []
    for category, percent in dict_of_percentages.items():
        num_fill = round(percent / 100 * series.isna().sum())
        fill_values.extend([category] * num_fill)  # num_fill have integer number so multiply this number by str
        # its repeat this str depending on the multiplication factor and put them in list

    # Fill NaNs with sampled values to match the required amount
    fill_values = np.random.choice(fill_values, series.isna().sum(), replace=True)
    # anime_df['Demographic'].isna().sum() this will be integer
    anime_df.loc[series.isna(), name_of_column] = fill_values


print("_"*75)
# handle "Demographic"
percentages = get_percentage(anime_df['Demographic'])
fill_na_by_percentages(percentages, anime_df["Demographic"], "Demographic")  # Now it's time to fill the nulls

# handle "Broadcast", "Genres", "English"
print(anime_df["Broadcast"].value_counts())
anime_df["Broadcast"] = anime_df["Broadcast"].replace("Unknown", np.nan)  # replace string by nan to handle all nulls once
anime_df = anime_df.dropna(subset=["Broadcast", "Genres", "English"])  # drop null rows
# handle "Synonyms"
anime_df = anime_df.drop(columns="Synonyms")  # Drop column
print("_"*75)
# check for duplications
print(anime_df[anime_df.duplicated()])  # no duplicates
print("_"*75)

anime_df_top = anime_df[:10].sort_values("Popularity", ascending=True)
print(anime_df_top[["Popularity", "Score", "Rank", "English"]])
# 1) Top 10 Anime by Popularity

ax = anime_df_top[:10].plot(kind="bar", x="English", y="Popularity",
                       figsize=(10, 7), style='-b', fontsize=8)
ax.set_yticks([x for x in range(0, 1000, 50)])
plt.xticks(rotation=15, ha='right')
plt.title("Top 10 Anime by Popularity Where 1 is better then 10")
plt.show()
print("_"*75)
# 2)Score distribution
anime_df["Score"].plot(kind="hist")
plt.title("Score distribution")
plt.show()

######## 3) Yearwise Members ############
# TOP 7 years by total numbers
print(anime_df.columns)

# get year from premiered
year_list = []
for year in anime_df["Premiered"]:
    year_list.append(year.split(" ")[1])
anime_df["Year"] = year_list  # create Year column to easily calculate
print(anime_df.groupby(["Year"])["Members"].sum().sort_values(ascending=False) [:7])

print("_"*75)
# 4)Type
print(anime_df["Type"].value_counts())  # there is 354 TV as I dropped nulls

print("_"*75)
# 5) Genres
print(anime_df.groupby("Genres")["Genres"].count().sort_values(ascending=False)[:5].plot(kind="bar", figsize=(10, 7), fontsize=7))
plt.xticks(rotation=15, ha='right')
plt.title("Top 5 Genre")
plt.show()

print("_"*75)
# 6) Top Studios
top_7_studios = anime_df.groupby("Studios")["Studios"].count().sort_values(ascending=False)
top_7_studios[:7].plot(kind="bar", figsize=(10, 7), fontsize=7)
plt.title("Top 7 Studios")
plt.xticks(rotation=15, ha='center')
plt.show()

print("_"*75)
# 7)Source
top_Source = anime_df.groupby("Source")["Source"].count().sort_values(ascending=False)
top_Source.plot(kind="pie", figsize=(10, 7), fontsize=7)
plt.title("top_Source")
plt.xticks(rotation=15, ha='center')
plt.show()