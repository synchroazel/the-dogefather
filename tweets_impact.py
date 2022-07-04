from datetime import timedelta

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def tweets_impact(tweets_df, crypto_df, days, non_doge=False):
    '''
    Custom function to produce a pd.DataFrame with information on tweets
    and the price diferences of a crypto on a given time window
    :param tweets_df: pd.DataFrame with tweets information
    :param crypto_df: pd.DataFrame with crypto prices information
    :param days: time window to consider the price difference in
    :param non_doge: False if the returned df should only contain info on Doge-tweets, True otherwise
    :return: a pd.DataFrame
    '''
    tweets = tweets_df.loc[~tweets_df.tweet.str.startswith('@')]

    if non_doge:
        tweets = tweets.loc[~tweets_df.tweet.str.contains('doge|Doge')]

    else:
        tweets = tweets.loc[tweets_df.tweet.str.contains('doge|Doge')]

    tweets = pd.DataFrame(tweets.reset_index(drop=True))

    tweet_times = tweets.loc[tweets.timestamp < pd.to_datetime('2021/12/28')].timestamp
    tweet_times = np.array([t.strftime('%Y-%m-%d') for t in tweet_times.tolist()])

    crypto_bf = crypto_df.loc[crypto_df['Date'].isin(tweet_times)].Open.array.to_numpy().squeeze()

    all = []

    for d in range(1, days + 1):
        tweet_times_af = pd.to_datetime(tweet_times) + timedelta(days=d)

        tweet_times_af = np.array([t.strftime('%Y-%m-%d') for t in tweet_times_af.tolist()])

        crypto_af_par = crypto_df.loc[crypto_df['Date'].isin(tweet_times_af)].Close.array.to_numpy().squeeze()

        all.append(crypto_af_par)

    crypto_af = np.matrix(all, dtype=object, copy=True).mean(axis=0)

    crypto_af = pd.Series(np.array(crypto_af).T.squeeze())

    scaler = StandardScaler()

    scaler.fit(crypto_df.Open.values.reshape(-1, 1))
    crypto_bf_sc = scaler.transform(crypto_bf.reshape(-1, 1)).squeeze()
    scaler.fit(crypto_df.Close.values.reshape(-1, 1))
    crypto_af_sc = scaler.transform(crypto_af.values.reshape(-1, 1)).squeeze()

    crypto_diff = crypto_af - crypto_bf
    crypto_diff_sc = crypto_af_sc - crypto_bf_sc

    crypto_diff_perc = (crypto_diff_sc * 100) / crypto_bf_sc

    crypto_diffs = pd.DataFrame({'before': crypto_bf,
                                 'after': crypto_af,
                                 'differ': crypto_diff,
                                 'before_sc': crypto_bf_sc,
                                 'after_sc': crypto_af_sc,
                                 'differ_sc': crypto_diff_sc,
                                 'differ_perc': crypto_diff_perc,
                                 'timestamp': pd.to_datetime(np.unique(tweet_times))})

    crypto_diffs = crypto_diffs.merge(tweets).sort_values(by='differ', ascending=False)

    return crypto_diffs
