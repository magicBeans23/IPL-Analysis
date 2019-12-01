"""
Scrapy crawler calling from script using internal API and
Using multiple spiders.
Demo on cricinfo IPL data
"""
import scrapy
from scrapy.crawler import CrawlerProcess


class MySpider1(scrapy.Spider):
    name = '2018_match_data'
    allowed_domains = ['cricbuzz.com']
    # start_urls = ['https://www.cricbuzz.com/cricket-series/2676/indian-premier-league-2018/matches/']
    start_urls = ['https://www.cricbuzz.com/cricket-series/2330/indian-premier-league-2015/matches']

    team_names = {
        "MUMBAI INDIANS": "MI",
        "KINGS XI PUNJAB": "KP",
        "KOLKATA KNIGHT RIDERS": "KKR",
        "SUNRISERS HYDERABAD": "SRH",
        "CHENNAI SUPER KINGS": "CSK",
        "RAJASTHAN ROYALS": "RR",
        "DELHI CAPITALS": "DD",
        "DECCAN CHARGERS": "SRH",
        "ROYAL CHALLENGERS BANGALORE": "RCB",
        "PUNE WARRIORS": "PW"
    }

    def getTeamCode(self, teamFullName):
        teamcode = self.team_names.get(teamFullName.upper())

        if teamcode is None:
            return teamFullName
        else:
            return teamcode

    def parse(self, response):
        print('processing : ' + response.url)
        win_list = response.xpath(
            '//*[@id="series-matches"]//div[@class="cb-col-60 cb-col cb-srs-mtchs-tm"]/a[2]/text()').getall()
        home_away_list = response.xpath(
            '//*[@id="series-matches"]//div[@class="cb-col-60 cb-col cb-srs-mtchs-tm"]/a[1]/span/text()').getall()
        game_time_list = response.xpath(
            '//*[@id="series-matches"]//div[@class="cb-col-40 cb-col cb-srs-mtchs-tm"]/div/span[2]/text()').getall()
        rows = zip(home_away_list, win_list, game_time_list)
        for row in rows:
            home_team = self.getTeamCode(row[0].split('vs')[0].strip())
            away_team = self.getTeamCode(row[0].split('vs')[1].split(',')[0].strip())
            won = 0
            if self.getTeamCode(row[1].split('won')[0].strip()) == home_team:
                won = 1
            day = 1
            if int(row[2].split(':')[0].strip()) > 5:
                day = 0
            info = {
                "home": home_team,
                "away": away_team,
                "winner": won,
                "day_night": day,
            }
            yield info


class MySpider2(scrapy.Spider):
    name = 'match_data_urls'
    allowed_domains = ['cricbuzz.com']
    # start_urls = ['https://www.cricbuzz.com/cricket-series/2676/indian-premier-league-2018/matches/']
    start_urls = ['https://www.cricbuzz.com/cricket-series/2060/indian-premier-league-2010/matches']

    def getTeamCode(self, teamFullName):
        teamcode = self.team_names.get(teamFullName.upper())

        if teamcode is None:
            return teamFullName
        else:
            return teamcode

    def parse(self, response):
        print('processing : ' + response.url)
        home_away_list = response.xpath(
            '//*[@id="series-matches"]//div[@class="cb-col-60 cb-col cb-srs-mtchs-tm"]/a[1]/@href').getall()
        for home_away in home_away_list:
            url = response.urljoin(home_away)
            info = {
                "url": '\'' + url + '\''
            }
            yield info


process1 = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': './Data/downloads/cricbuzz.csv'
})
process2 = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': './Data/downloads/cricbuzzlinks.csv'
})

if __name__ == '__main__':
    process1.crawl(MySpider1)
    process2.crawl(MySpider2)
    process1.start()
    process2.start()

