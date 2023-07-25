import cx_Oracle
import time
import numpy as np
import requests
from bs4 import BeautifulSoup
import threading
import os
import pandas as pd
import scrapy
from scrapy.settings import Settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapyfbref import settings as fbrefsettings
from scrapymarkstats import settings as trfmktsettings
from scrapy.utils.project import get_project_settings
from scrapymarkstats.spiders.markstats import MSSpider
from fuzzywuzzy import process
from scrapyfbref.spiders.fbref import FbrefSpider, FbrefGKSpider, FbrefDEFSpider, FbrefSTDSpider
from scrapytiles.spiders.transferspider import TransferENGSpider, TransferESPSpider, TransferITASpider, \
    TransferGERSpider, TransferFRASpider

WETTBEWERB_GB_ = 'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1'
password = '/thiyagarajan'

import sqlite3


def update_gkstats():
    con = sqlite3.connect('fbref.db')
    cur = con.cursor()
    cur.execute("""UPDATE gkstats
SET pid = (SELECT a.pid from astats AS a  where a.player=gkstats.player AND a.born=gkstats.born AND a.position="GK")
 """)
    con.commit()
    cur.close()

def update_namekey():
    con = sqlite3.connect('fbref.db')
    cur = con.cursor()
    cur.execute("""select player,country from markstatsplayers where player not in (SELECT m.player from markstatsplayers m ,astats a where m.player == a.player)""")
    markstatsplayers = cur.fetchall()
    cur.execute(
        """select player from astats where player not in (SELECT a.player from markstatsplayers m ,astats a where m.player == a.player)""")
    fbrefplayers = cur.fetchall()
    matched =[" " for x in range(0,len(markstatsplayers))]
    fbrefplayers=[x[0] for x in fbrefplayers]
    cur.execute("create table if not exists namekey ( fbrefname varchar(30),league varchar(30) , markstatsname varchar(30) )")
    cur.execute(
        "insert into namekey select a.player,a.league,m.player from markstatsplayers m ,astats a where m.player == a.player")

    for i in range(0,len(markstatsplayers)):
        matched[i]=process.extractOne(markstatsplayers[i][0],fbrefplayers)
        print(matched[i],markstatsplayers[i][0])
        cur.execute(
            "insert into namekey values( :1 ,:2,:3)",(matched[i][0],markstatsplayers[i][1],markstatsplayers[i][0]))

    con.commit()
    cur.close()

def processing_raw():
    con = sqlite3.connect("fbref.db")
    cur = con.cursor()
    cur.execute("""create table if not exists transferstats( leaguernk integer ,squad varchar(20)
    ,league varchar(20),attage decimal(5,2),attval decimal(5,2),attavgval decimal(5,2),defage decimal(5,2),defval decimal(5,2)
    ,defavgval decimal(5,2),gkage decimal(5,2),gkval decimal(5,2),gkavgval decimal(5,2),
    totage decimal(5,2),totval decimal(5,2),totavgval decimal(5,2))

    """)
    cur.execute("delete from transferstats")
    cur.execute("select * from rawtransferstats order by league ,leaguernk ,position")
    records = cur.fetchall()
    cur.execute("select leaguernk,squad,country from lstanding order by country ,leaguernk ")
    squadvalues = cur.fetchall()

    for i in range(0, len(records), 4):
        cur.execute("insert into transferstats values( :1, :2, :3, :4,:5,:6,:7, :8, :9, :10, :11, :12,:13,:14,:15)",
                    (squadvalues[int(i / 4)][0], squadvalues[int(i / 4)][1], squadvalues[int(i / 4)][2], records[i][3],
                     records[i][4], records[i][5],
                     records[i + 1][3], records[i + 1][4], records[i + 1][5], records[i + 2][3], records[i + 2][4],
                     records[i + 2][5],
                     records[i + 3][3], records[i + 3][4], records[i + 3][5]))
        con.commit()
    cur.close()


if __name__ == "__main__":
    #configure_logging()
    #crawler_settings = Settings()
    #crawler_settings.setmodule(trfmktsettings)
    ##runner = CrawlerRunner(settings=crawler_settings)
    #runner.crawl(MSSpider)
    # runner.crawl(TransferFRASpider)
    # runner.crawl(TransferGERSpider)
    # runner.crawl(TransferITASpider)
    # runner.crawl(TransferENGSpider)
    #d = runner.join()
    #d.addBoth(lambda _: reactor.stop())
    update_namekey()
    #reactor.run()
    # processing_raw()










