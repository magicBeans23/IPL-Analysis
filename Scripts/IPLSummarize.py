import pandas as pd
'''summarize the season data team wise'''

def summarize(years):
    for year in years:
        df = pd.read_excel('./Data/Processed/' + str(year) + '.xlsx')
        df_home_summary = df[df['League Match'] == 1].groupby('Home Team').mean().drop(
            labels=['MatchNo', 'Chase', 'DayNight', 'Win',
                    'League Match', 'SO', 'DL', 'ABatting', 'ABowling', 'AFielding'], axis=1).rename(
            columns={'HTR': 'RunsScoredHome', 'HTO': 'OversPlayedHome', 'ATR': 'RunsConcededHome',
                     'ATO': 'OversBowledHome',
                     'HBatting': 'HomeBatting', 'HBowling': 'HomeBowling', 'HFielding': 'HomeFielding'})
        df_home_summary['HomeWins'] = df[df['League Match'] == 1].loc[:, ['Home Team', 'Win']].groupby('Home Team')\
        .sum()['Win']
        # Home team mean with No of victories in group stage
        df_home_summary.sort_values(by=['Top4', 'RunsScoredHome'], ascending=[False, False])
        # Away Teams
        df_away_summary = df[df['League Match'] == 1].groupby('Away Team').mean().drop(
            labels=['MatchNo', 'Chase', 'DayNight', 'Win',
                    'League Match', 'SO', 'DL', 'Top4', 'HBatting', 'HBowling', 'HFielding'], axis=1).rename(
            columns={'ATR': 'RunsScoredAway', 'ATO': 'OversPlayedAway', 'HTR': 'RunsConcededAway',
                     'HTO': 'OversBowledAway',
                     'ABatting': 'AwayBatting', 'ABowling': 'AwayBowling', 'AFielding': 'AwayFielding'})
        # No of away games played per team
        # 2019 --7, RR -6
        # 2018 --7
        # 2017 --7
        # 2016 --7
        # 2015 --7
        # 2013 --8
        # 2012 --8, CSK, SH -7
        # 2011 --7, PW, RR -6
        # 2010 --7
        n = 7
        if year in [2013, 2012]:
            n = 8
        df_away_summary['AwayWins'] = n - df[df['League Match'] == 1].loc[:, ['Away Team', 'Win']]\
            .groupby('Away Team').sum()
        df_away_summary.sort_values(by=['RunsScoredAway'], ascending=[False])
        df_summary = pd.concat([df_home_summary, df_away_summary.drop(labels=['Year'], axis=1)], axis=1)

        df_summary['RunsScored'] = (df_summary['RunsScoredHome'] + df_summary['RunsScoredAway']) / 2
        df_summary['RunsConceded'] = (df_summary['RunsConcededHome'] + df_summary['RunsConcededAway']) / 2
        df_summary['OversBowled'] = (df_summary['OversBowledHome'] + df_summary['OversBowledAway']) / 2
        df_summary['OversPlayed'] = (df_summary['OversPlayedHome'] + df_summary['OversPlayedAway']) / 2
        df_summary['Wins'] = df_summary['HomeWins'] + df_summary['AwayWins']
        df_summary['Batting'] = (df_summary['HomeBatting'] + df_summary['AwayBatting']) / 2
        df_summary['Bowling'] = (df_summary['HomeBowling'] + df_summary['AwayBowling']) / 2
        df_summary['Fielding'] = (df_summary['HomeFielding'] + df_summary['AwayFielding']) / 2

        df_summary.to_excel('./Data/Processed/Summary/' + str(year) +'_Summary.xlsx')


if __name__ == '__main__':
    years = [2010, 2011, 2012, 2013, 2015, 2016, 2017, 2018, 2019]
    summarize(years)


