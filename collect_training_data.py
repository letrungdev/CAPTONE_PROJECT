import pandas as pd


target_file = "Data/Train/restaurant_train.csv"
df1 = pd.read_csv("Data/Train/reviews.csv", index_col=False, usecols=["rate", "review"])[["review", "rate"]].values.tolist()
df2 = pd.read_csv("Data/Train/tripadvisor_hotel_reviews.csv", index_col=False, usecols=["Review", "Rating"])[["Review", "Rating"]].values.tolist()


data = df1
for i in df2:
    data.append(i)

df = pd.DataFrame(data, columns =["Review", "Rating"])
df['Rating'] = df["Rating"].astype('int')
print(df.head())
df.to_csv(target_file, index=False)