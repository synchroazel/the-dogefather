import pandas as pd


def import_elon_tweets(path_to_dataset):
    '''
    Custom function to import Elon Musk's tweets from a given dataset.
    :param path_to_dataset: path to the .csv dataset with the tweets to import
    :return: pd.DataFrame with tweets and timestamps
    '''

    tmp = pd.read_csv(path_to_dataset)

    tweet_ids = tmp.id
    tweet_url = [f'https://twitter.com/elonmusk/status/{id}' for id in tweet_ids]

    df = pd.DataFrame({'tweet': tmp.tweet, 'timestamp': tmp.date, 'url': tweet_url})

    df['timestamp'] = pd.to_datetime(df.timestamp)

    return df


def import_crypto_prices(path_to_dataset):
    '''
    Custom function to import crypto market prices from a given dataset.
    :param path_to_dataset: path to the .csv dataset to import
    :return: pd.DataFrame with information from given dataset
    '''

    df = pd.read_csv(path_to_dataset)

    df['timestamp'] = pd.to_datetime(df.Date)

    df.timestamp = [dt_obj.strftime('%Y-%m-%d') for dt_obj in df.timestamp]

    return df
