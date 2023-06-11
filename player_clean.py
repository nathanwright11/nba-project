import pandas as pd

from active_players import get_active_players


def clean_games(file):
    """Removes unnecessary rows & columns, adds regular/playoff label as column.
    
    1. Removes columns with no useable data. 
    2. Removes games which player was not active (eg. Inactive, DND, DNP, etc.). 
    3. Adds label for each game whether it was regular season or playoffs.
    """
    df = pd.read_csv(file)
    df.drop(columns=[' ', ' .1'], inplace=True)
    df.dropna(subset='MP', inplace=True)
    type = file.split('_')[1]
    df = df.assign(Type=type)
    return df


def date_sort(df):
    """Sorts games in order by date, then resets the df indexes"""
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def s_label(date):
    """Creates season format for use as data label.
    
    Takes date input (eg. 2010-01-28) and returns output which represents season 
    the game occured (eg. 09-10). Currently doesn't work for games in 1999/2000
    """
    yr, mon, _ = date.split("-")
    if int(mon) >= 8:
        return f"{yr[-2:]}-{int(yr[-2:])+1}"
    else:
        return f"{int(yr[-2:])-1:02d}-{yr[-2:]}"


if __name__ == '__main__':
    players = get_active_players()
    for player in players:
        first, last = player.lower().split()
        reg_games = f"./stats/{last[:5]}{first[:2]}_regular_games.csv"
        p_games = f"./stats/{last[:5]}{first[:2]}_playoff_games.csv"

        reg_games = clean_games(reg_games)
        p_games = clean_games(p_games)

        games = pd.concat([reg_games, p_games], ignore_index=True)
        games['Season'] = [s_label(date) for date in games['Date']]
        games = date_sort(games)

        games.to_csv(f"./stats/{last[:5]}{first[:2]}_games.csv")
        print(f"{last} clean: success")