import pandas as pd

from get_players import get_players


def clean_games(player_url):
    """Removes unnecessary rows & columns.
    
    Removes columns with no useable data, and games which player was not 
    active (eg. Inactive, DND, DNP, etc.). 
    """
    file = f"../stats/{player_url.split('/')[-1].split('.')[0]}_games.csv"
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    df = df.drop(columns=['', '.1'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Season'] = [season_label(date) for date in df['Date']]
    df = df.sort_values('Date', ascending=True)
    df = df.reset_index(drop=True)
    return df


def season_label(date):
    """Creates season format for use as data label.
    
    Takes date input (eg. 2010-01-28) and returns output which represents season 
    the game occured (eg. 09-10). 
    """
    yr = date.year
    mon = date.month
    if yr == 2020:
        if int(mon) >= 11:
            date1 = date + pd.DateOffset(years=1)
            yr1 = date1.year
            return f"{str(yr)[-2:]}-{str(yr1)[-2:]}"
        else:
            date1 = date - pd.DateOffset(years=1)
            yr1 = date1.year
            return f"{str(yr1)[-2:]}-{str(yr)[-2:]}"
    else:
        if int(mon) >= 8:
            date1 = date + pd.DateOffset(years=1)
            yr1 = date1.year
            return f"{str(yr)[-2:]}-{str(yr1)[-2:]}"
        else:
            date1 = date - pd.DateOffset(years=1)
            yr1 = date1.year
            return f"{str(yr1)[-2:]}-{str(yr)[-2:]}"


if __name__ == '__main__':
    players = get_players(['Kobe Bryant', 'Lebron James', 'Stephen Curry',])
    for player, url in players.items():
        df_clean = clean_games(url)
        df_clean.to_csv(f"../stats/{url.split('/')[-1].split('.')[0]}_games.csv", 
                        index=False)
        print(f'{player} clean success')