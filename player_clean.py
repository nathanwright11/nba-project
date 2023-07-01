import pandas as pd

from get_players import get_players


def clean_games(player_url):
    """Removes unnecessary rows & columns.
    
    Removes columns with no useable data, and games which player was not 
    active (eg. Inactive, DND, DNP, etc.). 
    """
    file = f"./stats/{player_url.split('/')[-1].split('.')[0]}_games.csv"
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df.drop(columns=['', '.1'], inplace=True)
    df.dropna(subset='MP', inplace=True)
    df['Season'] = [season_label(date) for date in df['Date']]
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def season_label(date):
    """Creates season format for use as data label.
    
    Takes date input (eg. 2010-01-28) and returns output which represents season 
    the game occured (eg. 09-10). Currently doesn't work for games in 1999/2000
    """
    yr, mon, _ = date.split("-")
    if int(mon) >= 8:
        return f'{yr[-2:]}-{int(yr[-2:])+1}'
    else:
        return f'{int(yr[-2:])-1:02d}-{yr[-2:]}'


if __name__ == '__main__':
    players = get_players(['Kobe Bryant', 'Lebron James', 'Stephen Curry'])
    for player, url in players.items():
        df_clean = clean_games(url)
        df_clean.to_csv(f"./stats/{url.split('/')[-1].split('.')[0]}_games.csv")
        print(f'{player} clean success')