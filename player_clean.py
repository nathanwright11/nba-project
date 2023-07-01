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
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


if __name__ == '__main__':
    players = get_players(['Kobe Bryant', 'Lebron James', 'Stephen Curry'])
    for player, url in players.items():
        df_clean = clean_games(url)
        df_clean.to_csv(f"./stats/{url.split('/')[-1].split('.')[0]}_games.csv")
        print(f'{player} clean success')