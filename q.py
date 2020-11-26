import twint
import time
import os

c = twint.Config()

twitter_user = input('Twitter username: ')

should_download = True

if os.path.isfile('{}.csv'.format(twitter_user)):
    skip_scraping = input('Tweet dump file exists. Use it (y) or overwrite (n)? \n')
    if skip_scraping == 'y':
        should_download = False

if should_download:
    c.Username = twitter_user
    c.Store_csv = True
    c.Output = '{}.csv'.format(twitter_user)
    c.Timeline = True
    twint.run.Search(c)

    print('Finished scraping tweets. Processing...')
    time.sleep(1)

else:
    print('Processing...')


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('qposts.csv', parse_dates=True)
df['hour'] = pd.to_datetime(df.date).dt.hour
df['date'] = pd.to_datetime(df.date)

tweets = pd.read_csv('{}.csv'.format(twitter_user), usecols=['created_at'],  parse_dates=['created_at'])
tweets['date'] = pd.to_datetime(tweets.created_at)
tweets['hour'] = pd.to_datetime(tweets.date).dt.hour

tweets_clipped = tweets[tweets.date < df.date.max()]
tweets_clipped = tweets_clipped[tweets_clipped.date > df.date.min()]
posts_since_pad_data = df[df.date > tweets.date.min()]
posts_since_pad_data = posts_since_pad_data[posts_since_pad_data.date < tweets.date.max()]
combined = pd.concat([posts_since_pad_data.date, tweets_clipped.date])
combined['date'] = pd.to_datetime(combined)
combined['hour'] = pd.to_datetime(combined.date).dt.hour

plt.figure(figsize=(6,6))
sns.histplot(data=posts_since_pad_data, x='date', y='hour', bins=24).set_title('Q Posts', size=20)
plt.xticks(rotation=45)
plt.xlabel("Date", size=12)
plt.ylabel("Hour", size=12)

plt.figure(figsize=(6,6))
sns.histplot(data=tweets_clipped, x='date', y='hour', bins=24).set_title('@{} Tweets'.format(twitter_user), size=20)
plt.xticks(rotation=45)
plt.xlabel("Date", size=12)
plt.ylabel("Hour", size=12)

plt.figure(figsize=(6,6))
sns.histplot(data=combined, x='date', y='hour', bins=24).set_title('Combined', size=20)
plt.xticks(rotation=45)
plt.xlabel("Date", size=12)
plt.ylabel("Hour", size=12)
plt.show()
