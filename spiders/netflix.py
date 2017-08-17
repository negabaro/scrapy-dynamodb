# -*- coding: utf-8 -*-
import scrapy
from netflixcrawler.items import  NetflixcrawlerItem
from scrapy.http.request import Request
from netflixcrawler.items import ForeignDramaSeriesItem
from netflixcrawler.items import ForeignDramaSeasonItem
from netflixcrawler.items import ForeignDramaEpisodeItem
import re


class NetflixSpider(scrapy.Spider):
    name = 'netflix'
    allowed_domains = ['www.netflix.com','157.7.198.205']
    start_urls = ['http://157.7.198.205']
    #def __init__(self):
    #  print("init!!!!!!!!!!!!!!!!!!!")
    #  self.item = None

    def parse(self, response):
      print("parse!!!!!!!!!!!!!!!!!!!")
      item = []
      #item2 = NetflixcrawlerItem()
      #for sel in response.css("div.title-card-container"):
      #  item2['video_id'] = sel.css("div.ptrack-content").xpath('@data-ui-tracking-context').re_first('22video_id%22:(.+),%22image_key%22:%22sdp')
      #  yield item2 
      #  print(item2)
      #item = response.meta['item']
      #request = scrapy.Request("http://157.7.198.205",callback=self.parseList)
      #request.meta['item'] =item
      #return request
      #request.meta['item'] = item
      #request = Request("http://157.7.198.205", callback=self.parseList, meta={'item': item})
      #yield request
      #item = NetflixcrawlerItem()
      #yield scrapy.Request("https://www.netflix.com/jp/title/70177057", callback=self.parseSeries)
      #request =  scrapy.Request("https://www.netflix.com/jp/title/70177057", callback=self.parseSeason,meta={'item': item})
      items = []
      #request = scrapy.Request("https://www.netflix.com/jp/title/70177057", callback=self.parseSeries,meta={'item': item})
      #request.meta['item'] =item
      #return request 

      #request = scrapy.Request("https://www.netflix.com/jp/title/70177057", callback=self.parseEpisode,meta={'item': item})
      yield  scrapy.Request("https://www.netflix.com/jp/title/70177057", callback=self.parseDetail,meta={'item': item})
      #yield  scrapy.Request("https://www.netflix.com/jp/title/70177057", callback=self.parseSeries,meta={'item': item})
      #yield  scrapy.Request("https://www.netflix.com/jp/title/70177057", callback=self.parseSeason,meta={'item': item})

      #request.meta['item'] =item
      #yield request 

    ## 詳細ページをscrapyするロジックをコントールするメソッド
    def parseDetail(self,response):
        print("parseDeatil!!!!!!!!!!!!!!!!!!!")
        #item = response.meta['item']
        
        #self.logger.info("*******parseDetail Called %s", response.headers['Last-Modified'])
        #video_id = self.getVideoId(response)
        #item = response.meta['item']
        #item['header'] = self.parseSeason(response)
        #item['body'] =  self.parseSeries(response)
        #return self.parseEpisode(response)
        #yield item
        for sel2 in response.css("p.title-episodes-season-synopsis"):
          yield self.parseSeason2(response,sel2)
       
      
     
    def parseList(self, response):
      print("parseList!!!!!!!!!!!!!!!!!!!")
      #item = response.meta['item']
      item = NetflixcrawlerItem()
      #item = response.meta['item']
      for sel in response.css("div.title-card-container"):
#        item = NetflixcrawlerItem()
        item['video_id'] = sel.css("div.ptrack-content").xpath('@data-ui-tracking-context').re_first('22video_id%22:(.+),%22image_key%22:%22sdp')
        yield item
        #yield item2

  ## 詳細ページ中Series部分をScrapyするメソッド
    def parseSeries(self,response):
        video_id = self.getVideoId(response)
        self.logger.info("!!!!!!!!!!! parseSeries Called %s", response.url)
        series = ForeignDramaSeriesItem()

        for sel2 in response.css("div.metadata"):

            series['pr_series_id'] = video_id 
            series['title'] = sel2.css("h1.show-title::text").extract_first()
            series['casts'] = sel2.css("div.actors").css('span.actors-list::text').extract_first()
            series['genres'] = sel2.css("div.genres").css("span.genre-list::text").extract_first()
            series['year'] = sel2.css("p.year-and-duration").css("span.year::text").extract_first()
        if "Netflixオリジナル作品" == response.css('div.title-logo').css('img').xpath("@alt").re_first(': (.+)'):
           series['is_original'] = 1
        else:
           series['is_original'] = 0
        return series
        self.logger.info("zzzzzzzzzzzzzzz parseSeries End %s", response.url) 

    ## 詳細ページ中Season部分をScrapyするメソッド
    def parseSeason(self, response):
        video_id = self.getVideoId(response)
        self.logger.info("parseSeason Called %s", response.url)
        num=0

        for sel2 in response.css("p.title-episodes-season-synopsis"):
            num+=1

            season = ForeignDramaSeasonItem()
            season['outline'] = sel2.css("::text").extract_first()
            season['season_number'] = num
            season['series_id'] = video_id
            season['pr_season_id'] = video_id + "_" + str(season['season_number'])
            return season

    def parseSeason2(self, response,sel2):
        video_id = self.getVideoId(response)
        self.logger.info("parseSeason Called %s", response.url)
        num=0

        #for sel2 in response.css("p.title-episodes-season-synopsis"):
        num+=1

        season = ForeignDramaSeasonItem()
        season['outline'] = sel2.css("::text").extract_first()
        season['season_number'] = num
        season['series_id'] = video_id
        season['pr_season_id'] = video_id + "_" + str(season['season_number'])
        return season


    ## 詳細ページ中Episode部分をScrapyするメソッド
    def parseEpisode(self, response):
        video_id = self.getVideoId(response)
        self.logger.info("parseEpisode Called %s", response.url)
        for sel2 in response.css("div.title-episode"):
            episode = ForeignDramaEpisodeItem()
            self.logger.info("111e Called %s", video_id)

            episode['title'] = sel2.css("h3.title-episode-name::text").extract_first()
            episode['play_time'] = sel2.css("span.title-episode-runtime::text").extract_first()
            episode['outline'] = sel2.css("p.title-episode-synopsis::text").extract_first()
            #episode['episode_number'] = sel2.css("span.title-episode-number::text").extract_first()
            #title-episode-numberというタグがなくなった..
            episode['episode_number'] = sel2.css("h3.title-episode-name::text").re_first('([0-9]+). ')
            self.logger.info("222 Called %s", episode['episode_number'])
            episode['season_number'] = sel2.css("img.title-episode-img").xpath('@alt').re_first("シーズン(.+)の")
            self.logger.info("333 Called %s", episode['season_number'])
            episode['jacket_img_url'] = sel2.css("img.title-episode-img").xpath('@src').extract_first()
            episode['pr_episode_id'] = video_id + "_" + episode['season_number'] + "_" + episode['episode_number']
            episode['season_id'] = video_id + "_" + episode['season_number']
            yield episode

    ## 各詳細ページを識別する値(video_id)を取得
    def getVideoId(self,response):
        p = re.compile("([0-9]+)")
        m = p.search(response.url)
        if m != None:
          video_id = m.group(0)
        else:
          self.logger.info("Not Matched %s", response.url)
        return video_id
