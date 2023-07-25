import dash
from dash import Dash, dcc, html, Input, Output ,dash_table        # pip install dash
import dash_bootstrap_components as dbc         # pip install dash_bootstrap_components
import pandas as pd
import numpy as np
import sqlite3
import time
import pickle
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from scrapy.settings import Settings
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapyfbref import  settings as fbrefsettings
from scrapytiles import  settings as trfmktsettings
from scrapymarkstats import  settings as mssettings
from scrapymarkstatsplayers import  settings as mspsettings
from sklearn.metrics.pairwise import cosine_similarity
from scrapymarkstats.spiders.markstats import MSSpider
from scrapymarkstatsplayers11.spiders.markstats import MSPSpider
from scrapyfbref.spiders.fbref import FbrefSpider,FbrefSCASpider,FbrefGKSpider,FbrefDEFSpider,FbrefSTDSpider,FbrefAGKSpider,FbrefGCASpider,FbrefMISSpider,FbrefPOSSpider,FbrefPSTSpider,FbrefPASSpider,FbrefSHTSpider
from scrapytiles.spiders.transferspider import TransferENGSpider,TransferESPSpider,TransferITASpider,TransferGERSpider,TransferFRASpider
import os

def valuesetter():
    if not os.path.isfile("fbref.db"):
        master_scrapper()





def update_gkstats():
    con = sqlite3.connect('fbref.db')
    cursor = con.cursor()
    cursor.execute("""UPDATE gkstats
    SET pid = (SELECT a.pid from astats AS a  where a.player=gkstats.player AND a.born=gkstats.born AND a.position="GK")
         """)
    cursor.execute("""UPDATE agkstats
        SET pid = (SELECT a.pid from astats AS a  where a.player=agkstats.player AND a.born=agkstats.born AND a.position="GK")
             """)
    # for zone domination
    sqdpossesionlink = 'https://fbref.com/en/comps/Big5/possession/squads/Big-5-European-Leagues-Stats'
    temp = pd.read_html(sqdpossesionlink, match='Squad Possession', flavor='bs4')

    for i in range(2):
        # to get rid of heirarchial cols
        temp[i].columns = temp[i].columns.to_flat_index()
        temp[i].columns = [x[1] for x in temp[i].columns]

        # removing null values
        temp[i].dropna(subset=['Squad', 'Comp'], inplace=True)
        temp[i] = temp[i].drop(temp[i][temp[i]['Squad'] == 'Squad'].index)
        temp[i].fillna(0, inplace=True)



    sqlcommand4 = """create table if not exists zonedomination( squad varchar(20),defpen real, def3rd real, mid3rd real,att3rd real,attpen real,totaltouches real,
            vsdefpen real,vsdef3rd real, vsmid3rd real,vsatt3rd real,vsattpen real,vstotaltouches real
                                    )"""

    cursor.execute(sqlcommand4)
    cursor.execute("delete from zonedomination")
    for i in range(len(temp[0])):
        insertcmd = 'insert into zonedomination values( :1, :2, :3, :4,:5,:6,:7, :8, :9,:10,:11,:12,:13)'
        cursor.execute(insertcmd, (
            temp[0].iloc[i, 1], int(temp[0].iloc[i, 7]), int(temp[0].iloc[i, 8]), int(temp[0].iloc[i, 9]),
            int(temp[0].iloc[i, 10]),
            int(temp[0].iloc[i, 11]), int(temp[0].iloc[i, 6]), int(temp[1].iloc[i, 7]), int(temp[1].iloc[i, 8]),
            int(temp[1].iloc[i, 9]),
            int(temp[1].iloc[i, 10]), int(temp[1].iloc[i, 11]), int(temp[1].iloc[i, 6])))
    print("gk stats are updated")
    con.commit()
    cursor.close()

def clustering():
    #collecting data from diff tables
    #normalize them
    #predict model
    #create a new table store the cluster and pid player
    con = sqlite3.connect('fbref.db')
    cursor = con.cursor()

    cursor.execute("""
    select a.pid,a.playedfull,mp.xthreat,mp.noncrossxt,mp.fieldsgainedpass,mp.fieldsgainedcarry, a.xnonpeng,a.xnonpencon,po.tdef,po.tdefpen,pt.ti,pt.crs,pt.sw,pt.tb,pt.fk,pt.dead,pt.live,pt.attemp,a.progp,p.crspa,p.ppa,p.xag,p.final3rdpasses,po.tattpen,p.axag,a.assist,po.tmid,po.tatt,po.tlive,
    po.dispos,m.recov,s.sotperm,s.shperm,po.cpa,po.attcarries,a.progc,po.miscon,a.assist+a.nonpen,po.carriesprgdist,
    a.assist+a.goals,po.carriestotdist,po.carries,po.dribtkldper,po.dribsuccper,po.dribatt,p.lpatt,p.kp,p.mpatt,p.mpcmp,g.scapasslive,
    d.tklint,d.interceptions,d.pass_blocked,d.shots_blocked,d.blocks,g.scapassdead,p.spatt,d.tklonatt
    from astats as a,dstats as d,gca as g,passing as p,passtypes as pt, possession as po ,shooting as s,misstats as m,markstatsplayers as mp
     where  a.position <> 'GK' and 	trim(a.squad) =(select trim(fbrefsquad) from squadkey where trim(markstatssquad)=trim(mp.squad)) and (trim(mp.player), trim(a.player)) in (select trim(markstatsplayer),trim(fbrefplayer) from playerkey)
	 and a.pid =d.pid and a.pid=g.pid and a.pid=p.pid and a.pid=pt.pid and a.pid=po.pid and a.pid=s.pid and m.pid=a.pid ;
     
    
     """)

    fbrefstats=cursor.fetchall()
    print(len(fbrefstats),fbrefstats[0])
    fbrefstats=np.array(fbrefstats)
    data=pd.DataFrame(data=fbrefstats)
    data.replace('',0,inplace=True)
    data=data.astype(float)
    testdata=data.iloc[:,2:].div(data.iloc[:,1],axis="index")
    print("starting to cluster data")
    sc = StandardScaler().fit(testdata)
    xtra = sc.transform(testdata)
    scaler = MinMaxScaler().fit(xtra)
    xtrain = scaler.transform(xtra)
    model = pickle.load(open('modelextv2.pkl', 'rb'))
    pred=[]
    for x in xtrain:

        pred.append(model.predict(x.reshape(1,-1))[0])
    data['pred']=pred

    cursor.execute("create table if not exists clusterinfo (pid integer primary key,cluster integer) ")
    cursor.execute("delete from clusterinfo;")
    for i in range(len(pred)):

        cursor.execute("insert into clusterinfo values(:1,:2)",(int(data.iloc[i,0]),int(pred[i])))
        con.commit()

    print("starting similarity calculation",len(pred))
    #series of pids
    cursor.execute(
        "create table if not exists similarplayers (pid integer primary key,sFirst integer,sSecond integer,sThird integer) ")
    cursor.execute("delete from similarplayers;")
    for q in range(0,20):

        dfindices=[x==q for x in pred]
        print(len(dfindices),q)
        tempdata=data[dfindices]

        pid=tempdata.iloc[:,0]
        sim = cosine_similarity(testdata[dfindices])
        arr = pid.tolist()

        #mapping
        map = {}
        j = 0
        for i in arr:
            map[i] = sim[j]
            j = j + 1
        similardata=[]
        for x in arr:
            vals = np.array(list(map[x]))
            indices=vals.argsort()
            temp=[x,arr[indices[-2]],arr[indices[-3]],arr[indices[-4]]]
            similardata.append(temp)

        print("At cluster:",q,len(arr),tempdata.shape[0],len(similardata))

        for i in similardata:
            cursor.execute("insert into similarplayers values(:1,:2,:3,:4)", (i[0],i[1],i[2],i[3]))
            con.commit()
    print("finished")
    con.close()
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
                    (squadvalues[int(i / 4)][0], squadvalues[int(i / 4)][1], squadvalues[int(i / 4)][2],
                     records[i][3], records[i][4], records[i][5],
                     records[i + 1][3], records[i + 1][4], records[i + 1][5], records[i + 2][3], records[i + 2][4],
                     records[i + 2][5],
                     records[i + 3][3], records[i + 3][4], records[i + 3][5]))
        con.commit()

    cur.execute("create table if not EXISTS squadkey (fbrefsquad varchar ,markstatssquad varchar)");
    cur.execute("DELETE from goalshotcreation where squad like ' vs %'");
    cur.execute("DELETE  from squadkey");
    cur.execute(
        """update goalshotcreation set squadsanaccent=replace(replace(replace(replace(replace(replace(replace(squad,'ö','o'),'é','e'),'í','i'),'á','a'),"'",'.'),'Manchester','Man'),'-','');""");


    cur.execute(
        "insert into squadkey SELECT s.squad as ss, m.squad as ms from markstats as m,goalshotcreation as s where trim(s.country)=trim(m.country)  and  m.squad like '%'|| s.squadsanaccent ||'%' or s.squadsanaccent like '%'|| m.squad ||'%' ");
    cur.execute(
        "insert into squadkey select s.squad as ss,m.squad as ms from markstats as m , goalshotcreation as s where trim(s.country)=trim(m.country) and s.squad not in (select fbrefsquad from squadkey ) and m.squad not in (select markstatssquad from squadkey) and (substr(trim(m.squad),1,instr(trim(m.squad),' ')-1)=substr(trim(s.squadsanaccent),1,instr(trim(s.squadsanaccent),' ')-1) or substr(trim(m.squad),instr(trim(m.squad),' ')+1)=substr(trim(s.squadsanaccent),instr(trim(s.squadsanaccent),' ')+1))");
    cur.execute(
        "insert into squadkey select s.squad as ss,m.squad as ms from markstats as m , goalshotcreation as s where trim(s.country)=trim(m.country) and s.squad not in (select fbrefsquad from squadkey ) and m.squad not in (select markstatssquad from squadkey)");


    #re arranging
    #totgk
    cur.execute("""create table if not exists totgk  (pid integer default 0 ,player varchar(38),born integer default 0,mp decima(5,2),goalsallowed integer default 0 , pkgallowed integer default 0, fkgallowed integer default 0,ckgallowed integer default 0,ogagainst integer default 0,psxg  decimal(5,2) default 0,psxg_sot decimal(5,2) default 0,
    psxgpn varchar(8),gklaunchper  decimal(5,2) default 0,crossstpper decimal(5,2) default 0,
    opa  decimal(5,2) default 0,avgdistswp decimal(5,2) default 0,saves integer default 0, savesper  decimal(5,2) default 0,pksv integer default 0)""")

    cur.execute("""insert into totgk select g.pid ,g.player ,g.born ,g.mp,g.goalsallowed , g.pkgallowed , g.fkgallowed ,g.ckgallowed ,g.ogagainst ,g.psxg  ,g.psxg_sot ,g.psxgpn ,g.gklaunchper  ,g.crossstpper ,g.opa  ,g.avgdistswp,p.saves ,
     p.savesper  ,p.pksv  from agkstats as g left join gkstats as p  on g.pid=p.pid""")
    #deleting
    cur.execute("drop table gkstats;")
    cur.execute("drop table agkstats;")
    #totatt
    cur.execute("""create table if not exists totatt (pid integer default 0 PRIMARY KEY,mp decima(5,2), sotper  decimal(5,2) default 0,shotconv decimal(5,2) default 0,sca integer default 0, recov integer default 0,aerialswon integer default 0,aerialswonper  decimal(5,2) default 0
    ,tb integer default 0,sw integer default 0,crs integer default 0,position varchar) """)
    cur.execute("""
    insert into totatt select a.pid ,b.mp , a.sotper  ,a.shotconv ,b.sca , m.recov ,m.aerialswon ,m.aerialswonper  
    ,pt.tb ,pt.sw ,pt.crs  ,n.position from shooting as a inner join gca as b on a.pid=b.pid
            inner join misstats as m on b.pid=m.pid
			inner join passtypes as pt on m.pid=pt.pid
             inner join astats as n  on pt.pid=n.pid
    
    """)
    #matching players
    cur.execute("create table if not EXISTS dummy (fbrefplayer varchar,playersanaccent varchar,league varchar,squad varchar,msquad varchar)")
    cur.execute("insert into dummy select a.player,a.player,a.league,a.squad ,m.markstatssquad from astats as a , squadkey as m where trim(m.fbrefsquad) like trim(a.squad)")
    cur.execute("create table if not EXISTS playerkey (fbrefplayer varchar ,markstatsplayer varchar)")

    cur.execute("DELETE  from playerkey")
    cur.execute("""update dummy set playersanaccent=replace(replace(replace(replace(replace(replace(replace(playersanaccent,'ö','o'),'é','e'),'í','i'),'á','a'),'ñ','n'),'ć','c'),'-','')""")
    cur.execute("""update dummy set playersanaccent=replace(replace(replace(replace(replace(replace(replace(playersanaccent,'ü','u'),'ë','e'),'š','s'),'ã','a'),'ń','n'),'č','c'),'ï','i');""")
    cur.execute(
        """update markstatsplayers set playersanaccent=replace(replace(replace(replace(replace(replace(replace(playersanaccent,'ü','u'),'ë','e'),'š','s'),'ã','a'),'ń','n'),'č','c'),'ï','i');""")

    cur.execute(
        """update markstatsplayers set playersanaccent=replace(replace(replace(replace(replace(replace(replace(playersanaccent,'ö','o'),'é','e'),'í','i'),'á','a'),'ñ','n'),'ć','c'),'-','')""")

    cur.execute(
        "insert into playerkey SELECT s.fbrefplayer as ss, m.player as ms from markstatsplayers as m,dummy as s where trim(s.msquad)=trim(m.squad)  and  (m.player like  s.playersanaccent or   s.playersanaccent like m.player )and m.player not in (select markstatsplayer from playerkey);")

    cur.execute(
        "insert into playerkey SELECT s.fbrefplayer as ss, m.player as ms from markstatsplayers as m,dummy as s where trim(s.msquad)=trim(m.squad)  and  (m.player like  s.fbrefplayer or   s.fbrefplayer like m.player )and m.player not in (select markstatsplayer from playerkey);")
    cur.execute(
        "insert into playerkey SELECT s.fbrefplayer as ss, m.player as ms from markstatsplayers as m,dummy as s where trim(s.msquad)=trim(m.squad)  and  (m.playersanaccent like  s.fbrefplayer or   s.fbrefplayer like m.playersanaccent )and m.player not in (select markstatsplayer from playerkey);")
    cur.execute("insert into playerkey SELECT s.fbrefplayer as ss, m.player as ms from markstatsplayers as m,dummy as s where trim(s.msquad)=trim(m.squad)  and  (m.playersanaccent like  s.playersanaccent or   s.playersanaccent like m.playersanaccent )and m.player not in (select markstatsplayer from playerkey);")
    cur.execute(
        "insert into squadkey select s.squad as ss,m.squad as ms from markstats as m , goalshotcreation as s where trim(s.country)=trim(m.country) and s.squad not in (select fbrefsquad from squadkey ) and m.squad not in (select markstatssquad from squadkey)")
    # deleting

    cur.execute("drop table goalshotcreation;")
    cur.execute("drop table dummy;")
    cur.execute("drop table rawtransferstats;")
    for x in ['astats','dstats','passing','possession','totatt']:
        cur.execute("update  '{}' set position='MFDF' where position='DF,MF' OR position='MF,DF'".format(x))
        cur.execute("update  '{}' set position='FWDF' where position='DF,FW' OR position='FW,DF'".format(x))
        cur.execute("update  '{}' set position='FWMF' where position='MF,FW' OR position='FW,MF'".format(x))
    con.commit()
    cur.close()
    #for clustering
    clustering()
def master_scrapper():
    configure_logging()
    crawler_settings = Settings()
    crawler_settings.setmodule(trfmktsettings)
    runner = CrawlerRunner(settings=crawler_settings)
    crawler_settings2 = Settings()
    crawler_settings2.setmodule(fbrefsettings)
    runner2 = CrawlerRunner(settings=crawler_settings2)
    crawler_settings3 = Settings()
    crawler_settings3.setmodule(mssettings)
    runner3 = CrawlerRunner(settings=crawler_settings3)
    crawler_settings4 = Settings()
    crawler_settings4.setmodule(mspsettings)
    runner4 = CrawlerRunner(settings=crawler_settings4)

    @defer.inlineCallbacks
    def crawl():
        yield runner2.crawl(FbrefSTDSpider)
        yield runner2.crawl(FbrefSCASpider)
        yield runner2.crawl(FbrefDEFSpider)
        yield runner2.crawl(FbrefSpider)
        yield runner2.crawl(FbrefGKSpider)
        yield runner2.crawl(FbrefPASSpider)
        yield runner2.crawl(FbrefPSTSpider)
        yield runner2.crawl(FbrefPOSSpider)
        yield runner2.crawl(FbrefSHTSpider)
        yield runner2.crawl(FbrefAGKSpider)
        yield runner2.crawl(FbrefMISSpider)
        yield runner2.crawl(FbrefGCASpider)

        yield runner.crawl(TransferESPSpider)
        yield runner.crawl(TransferFRASpider)
        yield runner.crawl(TransferGERSpider)
        yield runner.crawl(TransferITASpider)
        yield runner.crawl(TransferENGSpider)

        yield runner3.crawl(MSSpider)
        yield runner4.crawl(MSPSpider)
        reactor.stop()

    crawl()
    reactor.run()
    time.sleep(3)
    update_gkstats()
    processing_raw()
valuesetter()

app = Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.VAPOR])

app.config.suppress_callback_exceptions = True

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2",style={"color":"black"})
                    ],

                    href=page["path"],
                    active="exact",

                )
                for page in dash.page_registry.values()
            ],
            vertical=False,
            pills=True,
            className="bg-light",
            style={"width":"100%","display":"flex","justify-content":"center"}

)


app.layout=html.Div(
    children=[
           html.H2("FOOTBALL STATISTICS APP",style={"text-align":"center","width":"100%","font-family":"High Tower Text","font-weight":"bold"})
        ,html.Div([sidebar],className='col-4',style={"width":"100%","font-family":"High Tower Text"}),dash.page_container




    ],style={"display":"flex","flex-direction":"column"})







if __name__ == "__main__":
    app.run_server(debug=True)





