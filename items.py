# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NetflixcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    video_id = scrapy.Field()
    #pass

class ForeignDramaSeriesItem(scrapy.Item):
    pr_series_id = scrapy.Field()
    series_id = scrapy.Field()
    title = scrapy.Field()
    casts = scrapy.Field()
    genres = scrapy.Field()
    year = scrapy.Field()
    is_original = scrapy.Field()
    deleted = scrapy.Field()
    updated_date = scrapy.Field()

class ForeignDramaSeasonItem(scrapy.Item):
    pr_season_id = scrapy.Field()
    season_number = scrapy.Field()
    series_id = scrapy.Field()
    outline = scrapy.Field()

class ForeignDramaEpisodeItem(scrapy.Item):
    pr_episode_id = scrapy.Field()
    season_id = scrapy.Field()
    season_number = scrapy.Field()
    jacket_img_url = scrapy.Field()
    title = scrapy.Field()
    episode_number = scrapy.Field()
    play_time = scrapy.Field()
    outline = scrapy.Field()
