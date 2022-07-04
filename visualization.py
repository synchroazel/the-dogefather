import numpy as np
import pandas as pd
from bokeh.models import Range1d
from bokeh.models import Title
from bokeh.plotting import figure
from sklearn.preprocessing import StandardScaler

palette = {'BTC': '#EE6055',
           'SOL': '#119DA4',
           'DOGE': '#FFC247',
           'non DOGE': '#808080'}


def plot_scaled_prices(df, name):
    '''
    Custom function to produce sparklines-like plot with scaled prices from a crypto_df
    :param df: pd.DataFrame with crypto's data
    :param name: the name of the crypto
    :return: a bokeh plot
    '''
    p = figure(title=f'{name}-USD in 2021',
               x_axis_type="datetime",
               plot_height=100,
               plot_width=320)

    scaled_prices = (df[['Open']] - df[['Open']].min()).Open.tolist()

    p.line(pd.to_datetime(df.timestamp),
           scaled_prices,
           color=palette[name],
           line_width=1.5)

    p.x_range = Range1d(pd.to_datetime('01/01/2021'), pd.to_datetime('01/01/2022'))

    # Graphic settings to create sparklines-like plot

    # grid settings
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = 'grey'
    p.ygrid.grid_line_alpha = 0.2

    # plot outline settings
    p.outline_line_color = None

    # x and y axis settings
    p.xaxis.axis_label = ''
    p.yaxis.axis_label = ''
    p.xaxis.visible = False
    p.yaxis.axis_line_width = 0

    # y axis ticks settings
    p.yaxis.major_label_text_color = 'grey'
    p.yaxis.major_label_text_font_size = '8px'
    p.yaxis.major_tick_line_color = 'grey'
    p.yaxis.major_tick_line_width = 0
    p.yaxis.minor_tick_line_width = 0

    # title settings
    p.title.text_font_size = '10px'

    return p


def plot_stdzed_prices(doge_df, sol_df, btc_df, subtitle=' ', from_date='01/01/2021', to_date='01/01/2022'):
    '''
    Custom function to plot standardized priced of 3 cryptos
    :param doge_df: previously assigned pd.DataFrame with Dogecoin data
    :param sol_df: previously assigned pd.DataFrame with Solana data
    :param btc_df: previously assigned pd.DataFrame with Bitcoin data
    :param subtitle: subtitle for the final plot
    :param from_date: [optional] starting date for the plot x axis
    :param to_date: [optional] ending date for the plot x axis
    :return: a bokeh plot
    '''
    scaler = StandardScaler()

    p = figure(title='Dogecoin, Solana and Bitcoin prices in 2021',
               x_axis_type="datetime",
               plot_height=400,
               plot_width=900)

    scaler.fit(doge_df[['High']])

    p.line(pd.to_datetime(doge_df.timestamp),
           scaler.transform(doge_df[['High']]).tolist(),
           color=palette['DOGE'],
           legend_label="DOGE",
           line_width=1.5)

    scaler.fit(sol_df[['High']])

    p.line(pd.to_datetime(sol_df.timestamp),
           scaler.transform(sol_df[['High']]).tolist(),
           color=palette['SOL'],
           legend_label="SOL",
           line_width=1.5)

    scaler.fit(btc_df[['High']])

    p.line(pd.to_datetime(btc_df.timestamp),
           scaler.transform(btc_df[['High']]).tolist(),
           color=palette['BTC'],
           legend_label="BTC",
           line_width=1.5)

    p.x_range = Range1d(pd.to_datetime(from_date), pd.to_datetime(to_date))
    p.y_range = Range1d(-2, 5)

    # subtitle settings
    p.add_layout(Title(text=subtitle, text_font_style="italic"), 'above')

    # legend box settings
    p.legend.border_line_width = 2

    # grid settings
    p.xgrid.grid_line_color = None
    p.xgrid.grid_line_alpha = 0.2
    p.ygrid.grid_line_color = 'grey'
    p.ygrid.grid_line_alpha = 0.2

    # x and y axis settings
    p.xaxis.axis_label = ''
    p.xaxis.axis_line_color = 'grey'
    p.xaxis.axis_line_alpha = 0.2

    p.yaxis.axis_label = 'standardized prices (DOGE-USD)'
    p.yaxis.axis_line_color = 'grey'
    p.yaxis.axis_line_alpha = 0.2

    # y axis ticks settings
    p.xaxis.major_label_text_color = 'grey'
    p.xaxis.major_tick_line_color = 'grey'
    p.xaxis.major_tick_line_alpha = 0.2

    p.yaxis.major_label_text_color = 'grey'
    p.yaxis.major_tick_line_color = 'grey'
    p.yaxis.major_tick_line_alpha = 0.2
    p.yaxis.minor_tick_line_width = 0

    # title settings
    p.title.text_font_size = '15px'

    return p


def plot_did(crypto_dfs, crypto_names):
    '''
    Custom function to produce a DiD plot
    :param crypto_dfs: list of previously assigned pd.DataFrames for each crypto
    :param crypto_names: list of the names of the cryptos considered
    :return: a bokeh plot
    '''
    labels = ['before', 'after']

    p = figure(title='Prices before and after a Doge-referencing tweet\n',
               x_range=labels, plot_height=400, plot_width=600)

    for df, crypto in zip(crypto_dfs, crypto_names):
        p.line(labels, [np.mean(df.before_sc), np.mean(df.after_sc)],
               color=palette[crypto], line_width=1.5, legend_label=crypto)

    # legend box settings
    p.legend.border_line_width = 2

    # grid settings
    p.xgrid.grid_line_color = None
    p.xgrid.grid_line_alpha = 0.2
    p.ygrid.grid_line_color = 'grey'
    p.ygrid.grid_line_alpha = 0.2

    # x and y axis settings
    p.xaxis.axis_label = ''
    p.xaxis.axis_line_color = 'grey'
    p.xaxis.axis_line_alpha = 0.2

    p.yaxis.axis_label = 'standardized prices'
    p.yaxis.axis_line_color = 'grey'
    p.yaxis.axis_line_alpha = 0.2

    # y axis ticks settings
    p.xaxis.major_label_text_color = 'grey'
    p.xaxis.major_tick_line_color = 'grey'
    p.xaxis.major_tick_line_alpha = 0.2

    p.yaxis.major_label_text_color = 'grey'
    p.yaxis.major_tick_line_color = 'grey'
    p.yaxis.major_tick_line_alpha = 0.2
    p.yaxis.minor_tick_line_width = 0

    # title settings
    p.title.text_font_size = '15px'

    return p


def plot_did_differences(crypto_dfs, crypto_names):
    '''
    Custom function to produce a DiD plot, considering differences
    :param crypto_dfs: list of previously assigned pd.DataFrames for each crypto
    :param crypto_names: list of the names of the cryptos considered
    :return: a bokeh plot
    '''
    labels = ['before', 'after']

    p = figure(title='Price differences before and after a Doge-referencing tweet\n',
               x_range=labels, plot_height=400, plot_width=600)

    for df, crypto in zip(crypto_dfs, crypto_names):
        p.line(labels, [0, np.mean(df.differ_sc)],
               color=palette[crypto], line_width=1.5, legend_label=crypto)

    # legend box settings
    p.legend.border_line_width = 2

    # grid settings
    p.xgrid.grid_line_color = None
    p.xgrid.grid_line_alpha = 0.2
    p.ygrid.grid_line_color = 'grey'
    p.ygrid.grid_line_alpha = 0.2

    # x and y axis settings
    p.xaxis.axis_label = ''
    p.xaxis.axis_line_color = 'grey'
    p.xaxis.axis_line_alpha = 0.2

    p.yaxis.axis_label = 'standardized differences'
    p.yaxis.axis_line_color = 'grey'
    p.yaxis.axis_line_alpha = 0.2

    # y axis ticks settings
    p.xaxis.major_label_text_color = 'grey'
    p.xaxis.major_tick_line_color = 'grey'
    p.xaxis.major_tick_line_alpha = 0.2

    p.yaxis.major_label_text_color = 'grey'
    p.yaxis.major_tick_line_color = 'grey'
    p.yaxis.major_tick_line_alpha = 0.2
    p.yaxis.minor_tick_line_width = 0

    # title settings
    p.title.text_font_size = '15px'

    return p
