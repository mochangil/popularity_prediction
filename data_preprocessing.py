import pandas as pd

df = pd.read_csv('data.csv')

genres = {'acoustic': 0, 'dance': 1, 'hip-hop': 2, 'indie': 3, 'jazz': 4, 'k-pop': 5, 'pop-film': 6, 'pop': 7, 'r-n-b': 8, 'rock': 9, 'soul': 10}
df.iloc[:, 15] = df.iloc[:, 15].map(genres)

#df["duration_mins"] = df["duration_ms"]/60000

df.loc[((df.popularity >= 0) & (df.popularity <= 30)), "popularity_level" ] = 1
df.loc[((df.popularity > 30) & (df.popularity <= 60)), "popularity_level" ] = 2
df.loc[((df.popularity > 60) & (df.popularity <= 100)), "popularity_level" ] = 3
#df["popularity_level"] = df["popularity"].apply(lambda x: x // 10 * 10)
df["popularity_level"] = df["popularity_level"].astype("int")

#df=df.drop(columns=[''])
#df = df.reindex(sorted(df.columns), axis=1)
df.to_csv('new_data.csv',index=False)