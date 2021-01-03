import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set_style('darkgrid')
def hist_plot(column):
    df = pd.read_csv('../data/streamer_data.csv')
    df = df.drop(columns = ['game_name', 'login', 'broadcaster_type', 'language'])
    df.account_age = pd.to_timedelta(df.account_age).map(lambda x: x.days)
    
    fig, ax = plt.subplots(figsize = (16,8))
    ax.set_title(f'Unpartnered vs Partnered Distribution of {column}', fontsize = 24)
    sns.distplot(df.loc[df.target == 0][column], ax = ax)
    sns.distplot(df.loc[df.target == 1][column], ax = ax)
    ax.tick_params(labelsize=14)
    ax.set_xlabel(ax.get_xlabel(), fontsize = 16)
    ax.legend(['Unpartnered', 'Partnered'], fontsize = 16)
    return fig


def scatter_fig(var1, var2):
    df = pd.read_csv('../data/streamer_data.csv')
    df = df.drop(columns = ['game_name', 'login', 'broadcaster_type', 'language'])
    df.account_age = pd.to_timedelta(df.account_age).map(lambda x: x.days)
    fig, ax = plt.subplots(figsize = (16,8))
    ax.set_title(f'{var1} vs {var2}', fontsize = 24)
    ax.set_xlabel(ax.get_xlabel(), fontsize = 16)
    ax.set_ylabel(ax.get_ylabel(), fontsize = 16)
    ax.tick_params(labelsize = 14)
    sns.scatterplot(df.loc[df.target == 0][var1], df.loc[df.target == 0][var2], alpha=0.5);
    sns.scatterplot(df.loc[df.target == 1][var1], df.loc[df.target == 1][var2], alpha=0.5);
    ax.legend(['Unpartnered', 'Partnered'], fontsize = 16)
    return fig