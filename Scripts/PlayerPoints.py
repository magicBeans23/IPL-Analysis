import pandas as pd
import unidecode
'''Calculating team strengths as per player performance in the last season'''


# calculate team scores based on lineups
def calc_scores(x, pts_type, df):
    print('==================================')
    x = unidecode.unidecode(x)
    sc = 0
    for y in x.split(','):
        t = 0
        try:
            t = df[df.PLAYER.str.strip().str.upper() == y.strip().upper()][pts_type].values[0]
        except IndexError:
            t = 0
        finally:
            sc += t
            print(y, t)
    print('total score', sc)
    return sc


def calculate_scores(years, attribute_weights={'Wkts': 3.5,'Dots': 1,'Fours': 2.5,'Sixes': 3.5,'Catches': 2.5,'Stumpings': 2.5}):
    for year in years:
        matches = pd.read_excel('./Data/Matches/' + str(year) + '.xlsx')
        playerpoints = pd.read_excel('./Data/Players/' + str(year - 1) + '.xlsx')
        playerpoints['battingPts'] = playerpoints['Fours'] * attribute_weights.get('Fours') + playerpoints[
            'Sixes'] * attribute_weights.get('Sixes')
        playerpoints['bowlingPts'] = playerpoints['Wkts'] * attribute_weights.get('Wkts') + playerpoints[
            'Dots'] * attribute_weights.get('Dots')
        playerpoints['fieldingPts'] = playerpoints['Catches'] * attribute_weights.get('Catches') + playerpoints[
            'Stumpings'] * attribute_weights.get('Stumpings')
        # calculating team scores:
        playerpoints['PLAYER'] = [unidecode.unidecode(x) for x in playerpoints['PLAYER']]
        print('Home Batting Points')
        matches['HBatting'] = [calc_scores(x, 'battingPts', playerpoints) for x in matches['HP11']]
        print('Home Bowling Points')
        matches['HBowling'] = [calc_scores(x, 'bowlingPts', playerpoints) for x in matches['HP11']]
        print('Home Fielding Points')
        matches['HFielding'] = [calc_scores(x, 'fieldingPts', playerpoints) for x in matches['HP11']]
        print('Away Batting Points')
        matches['ABatting'] = [calc_scores(x, 'battingPts', playerpoints) for x in matches['AP11']]
        print('Away Bowling Points')
        matches['ABowling'] = [calc_scores(x, 'bowlingPts', playerpoints) for x in matches['AP11']]
        print('Away Fielding Points')
        matches['AFielding'] = [calc_scores(x, 'fieldingPts', playerpoints) for x in matches['AP11']]
        matches.to_excel('./Data/Processed/' + str(year) + '.xlsx')


if __name__ == '__main__':
    years = [2010, 2011, 2012, 2013, 2015, 2016, 2017, 2018, 2019]
    calculate_scores(years)
