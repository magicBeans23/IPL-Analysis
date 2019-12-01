import pandas as pd


def concatpds():
    df2010 = pd.read_excel('./Data/Processed/Summary/2010_Summary.xlsx')
    df2011 = pd.read_excel('./Data/Processed/Summary/2011_Summary.xlsx')
    df2012 = pd.read_excel('./Data/Processed/Summary/2012_Summary.xlsx')
    df2013 = pd.read_excel('./Data/Processed/Summary/2013_Summary.xlsx')
    df2015 = pd.read_excel('./Data/Processed/Summary/2015_Summary.xlsx')
    df2016 = pd.read_excel('./Data/Processed/Summary/2016_Summary.xlsx')
    df2017 = pd.read_excel('./Data/Processed/Summary/2017_Summary.xlsx')
    df2018 = pd.read_excel('./Data/Processed/Summary/2018_Summary.xlsx')
    df2019 = pd.read_excel('./Data/Processed/Summary/2019_Summary.xlsx')
    pd.concat([df2010, df2011, df2012, df2013, df2015, df2016, df2017, df2018, df2019], sort=False).to_excel('./Data/Processed/Summary/All_years_Summary.xlsx')


if __name__ == '__main__':
    concatpds()
