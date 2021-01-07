import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set_style('darkgrid')
def hist_plot(column):
    df = pd.read_csv('../data/streamer_data.csv')
    df = df.drop(columns = ['game_name', 'login', 'broadcaster_type', 'language'])
    df.account_age = pd.to_timedelta(df.account_age).map(lambda x: x.days)
    column_title = column.replace('_', ' ').title()
    fig, ax = plt.subplots(figsize = (16,8))
    ax.set_title(f'Unpartnered vs Partnered Distribution of {column_title}', fontsize = 32)
    sns.distplot(df.loc[df.target == 0][column], ax = ax)
    sns.distplot(df.loc[df.target == 1][column], ax = ax)
    ax.tick_params(labelsize=18)
    ax.set_xlabel(column_title, fontsize = 24)
    ax.set_ylabel('Frequency', fontsize = 24)
    ax.legend(['Unpartnered', 'Partnered'], fontsize = 24)
    return fig


def scatter_fig(var1, var2):
    df = pd.read_csv('../data/streamer_data.csv')
    df = df.drop(columns = ['game_name', 'login', 'broadcaster_type', 'language'])
    df.account_age = pd.to_timedelta(df.account_age).map(lambda x: x.days)
    fig, ax = plt.subplots(figsize = (16,8))
    var1_title = var1.replace('_', ' ').title()
    var2_title = var2.replace('_', ' ').title()
    ax.set_title(f'{var1_title} vs {var2_title}', fontsize = 32)
    ax.tick_params(labelsize = 18)
    sns.scatterplot(df.loc[df.target == 0][var1], df.loc[df.target == 0][var2], alpha=0.5);
    sns.scatterplot(df.loc[df.target == 1][var1], df.loc[df.target == 1][var2], alpha=0.5);
    ax.set_xlabel(var1_title, fontsize = 24)
    ax.set_ylabel(var2_title, fontsize = 24)
    ax.legend(['Unpartnered', 'Partnered'], fontsize = 24)
    return fig