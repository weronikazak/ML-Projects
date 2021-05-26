df.drop(["price", "currency"], axis=1, inplace=True)
df.dtypes

df.country.value_counts().plot(kind="pie")

plt.axis("equal")
plt.title("x")
plt.legend(labels=df.country.value_counts().index, loc="upper left")
df.mark.value_counts().to_frame()
df.head()

df.plot(kind='bar', figsize=(18, 6), title="idk")

df.groupby(["mark"]).mean().round(2)
plt.xticks(rotation=90)
sns.countplot(df.year).set_title("xd")

sns.heatmap(df.corr())

sns.distplot(df.mileage, kde=False)

sns.boxplot(y=df2.price_eur, x=df.country, data=df)