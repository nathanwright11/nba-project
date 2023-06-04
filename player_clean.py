import pandas as pd

def clean_games(file):
    """Removes unnecessary rows & columns, adds regular/playoff label as column.
    
    Removes columns with no useable data. Removes games which player was not active
    (eg. Inactive, DND, DNP, etc.). Adds label for each game whether it was regular 
    season or playoffs.
    """
    df = pd.read_csv(file)
    df = df.drop(columns=[' ', ' .1'])
    df = df.dropna(subset='MP')
    type = file.split('_')[1]
    df = df.assign(Type=type)
    return df

def date_sort(df):
    """Sorts games in order by date, then resets the df indexes"""
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date', ascending=True)
    df = df.reset_index(drop=True)
    return df

def s_label(date):
    """Creates season format for use as data label.
    
    Takes date input (eg. 2010-01-28) and returns output which represents the season 
    that game occured in (eg. 09-10).
    """
    yr, mon, day = date.split("-")
    if int(mon) >= 8:
        return f"{yr[-2:]}-{int(yr[-2:])+1}"
    else:
        return f"{int(yr[-2:])-1:02d}-{yr[-2:]}"


players = ['stephen curry',
           'lebron james',
           'jayson tatum',
           'jimmy butler', 
           'nikola jokic',
           'kevin durant',
           'joel embiid',
           'giannis antetokounmpo']

for player in players:
    first, last = player.split()
    reg_games = f"./stats/{last[:5]}{first[:2]}_regular_games.csv"
    p_games = f"./stats/{last[:5]}{first[:2]}_playoff_games.csv"

    reg_games = clean_games(reg_games)
    p_games = clean_games(p_games)

    games = pd.concat([reg_games, p_games], ignore_index=True)
    games['Season'] = [s_label(date) for date in games['Date']]
    games = date_sort(games)

    games.to_csv(f"./stats/{last[:5]}{first[:2]}_games.csv")
    print(f"{last} clean: success")