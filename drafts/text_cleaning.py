import re

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud


# %% remove regular expression

def rm_regex(text, pattern_regex):
    r = re.findall(pattern_regex, text)
    for i in r:
        text = re.sub(i, '', text)

    return text


# %% compute sentiment intensity

def compute_si(tweet):
    sia = SentimentIntensityAnalyzer()

    score = sia.polarity_scores(str(tweet))

    if score['neg'] > score['pos']:
        return ('neg', score['neg'])
    else:
        return ('pos', score['pos'])


# %% hashtag extraction

def extract_hastags(tweets):
    hashtags = []

    for text in tweets:
        h = re.findall(r"#(\w+)", text)
        if h != []:
            hashtags.extend(h)

    return hashtags


# %% make a wordcloud

def wordcloud(tweets, size=8, custom_font=None):
    stopwords = set(nltk.corpus.stopwords.words("english") + nltk.corpus.stopwords.words("french"))

    wordcloud = WordCloud(font_path=custom_font,
                          width=1000, height=1000,
                          background_color='white',
                          stopwords=stopwords,
                          collocations=False,
                          min_font_size=10)

    wordcloud.generate(' '.join(tweets))

    plt.figure(figsize=(size, size), dpi=80)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


# %% main cleaning pipeline

def cleaning_pipeline(tweets):
    df = pd.DataFrame({'tweets': tweets})

    # Removing '@username'

    df['tidy_tweets'] = np.vectorize(rm_regex)(df['tweets'], "@[\w]*: | *RT*")
    df.head(10)

    # Removing links (http/https)

    cleaned_tweets = []

    for index, row in df.iterrows():
        # Here we are filtering out all the words that contains link
        words_without_links = [word for word in row.tidy_tweets.split() if 'http' not in word]
        cleaned_tweets.append(' '.join(words_without_links))

    df['tidy_tweets'] = cleaned_tweets

    # Removing empty tweets

    df = df[df['tidy_tweets'] != '']

    # Removing duplicates

    df.drop_duplicates(subset=['tidy_tweets'], keep=False)

    # Resetting indexes

    df = df.reset_index(drop=True)

    # Remove punctuations

    df['tidier_tweets'] = df['tidy_tweets'].str.replace("[^a-zA-Z# ]", "", regex=True)

    # Removing stopwords

    stopwords = set(nltk.corpus.stopwords.words("english") + nltk.corpus.stopwords.words("french"))

    stopwords_set = set(stopwords)
    cleaned_tweets = []

    for index, row in df.iterrows():
        # filerting out all the stopwords
        words_without_stopwords = [word for word in row.tidier_tweets.split() if
                                   not word in stopwords_set and '#' not in word.lower()]

        # finally creating tweets list of tuples containing stopwords(list) and sentimentType
        cleaned_tweets.append(' '.join(words_without_stopwords))

    df['tidier_tweets'] = cleaned_tweets

    return df
