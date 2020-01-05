import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import files
uploaded = files.upload()

credits = pd.read_csv("tmdb_5000_credits.csv")

movies_incomplete = pd.read_csv("tmdb_5000_movies.csv")

# print("credits: ", credits.shape) (4803, 4)
# print("movies_incomplete", movies_incomplete.shape) (4803, 20)

V = movies_clean['vote_count'] # nr of votes for the movie
R = movies_clean['vote_average'] # for rating - averange for the movie as a number form 0 do 10
C = movies_clean['vote_average'].mean() # the mean vote across the whole report
m = movies_clean['vote_count'].quantile(0.70) # min. 70% votes

movies_clean['weighted_averange'] = (V/ (V+m) * R) + (m/(m + V) * C) # weighted ranking

wavg = movies_ranked.sort_values('weighted_averange', ascending=False)

plt.figure(figsize=(16, 6))

ax = sns.barplot(x=wavg['weighted_averange'].head(10). y=wavg['original_title'].head(10), data=wavg, palette='deep')
