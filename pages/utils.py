import plotly.graph_objects as go
import plotly.express as px


customscale=[[0, "rgb(0, 204, 0)"],[0.1, "rgb(0, 204, 0)"],
             [0.11, "rgb(128, 255, 0)"],[0.2, "rgb(128, 255, 0)"],
             [0.21, "rgb(230, 230, 0)"],[0.60, "rgb(230, 230, 0)"],
             [0.61, "rgb(255, 255, 77)"],[0.80, "rgb(255, 255, 77)"],
             [0.81, "rgb(230, 92, 0)"],[0.90, "rgb(255, 51, 0)"],
             [0.1, "rgb(255, 51, 0)"],[1.0, "rgb(230, 92, 0)"]]



def plotone(c,playerid,position):

    if position=='GK':
        c.execute(
            """ select p.psxg_sot,p.psxgpn,a.player,a.pid from astats as a ,totgk as p where a.playedfull>=25  and a.pid=p.pid   order by a.player""")
        d = c.fetchall()
        xval = []
        textval = []
        playerstats = [d[0][0], d[0][1], d[0][2].split()[-1]]
        yval=[]
        for t in d:
            if t[3] == playerid:
                playerstats = [t[0], t[1], t[2].split()[-1]]
            if t[1]=='':
                yval.append(0)
            elif t[1]=='-':
                yval.append(float(t[1]))
            else :
                yval.append(float(t[1]) )
            xval.append(t[0])

            textval.append(t[2].split()[-1])



        fig = px.scatter(title='Shot Stopping', labels={'x': 'Quality of shots', 'y': 'Psxg', 'text': 'Name'},
                         x=xval, y=yval, text=textval,

                         )
        fig.add_traces(
            go.Scatter(x=[playerstats[0]], y=[playerstats[1]], text=[playerstats[2]], textfont=fontdict2, name=""))
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='top center')
        return fig
    c.execute("select cluster from clusterinfo where pid= {} ".format(playerid))
    clusterid=c.fetchall()[0][0]
    print("cluster id for chosen player",clusterid)


    if clusterid in (1,14,9,19,3,16,10):
        c.execute(""" select (p.kp+p.crspa+p.ppa+pt.tb)/a.playedfull ,a.player,a.pid  from astats as a ,passing as p, passtypes as pt,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid=pt.pid and pt.pid= p.pid  order by a.player""".format(clusterid))
        d=c.fetchall()
        xval=[]
        textval=[]
        c.execute(
            """ select (p.cpa)/a.playedfull ,a.player  from astats as a ,possession as p,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid= p.pid  order by a.player""".format(
                clusterid))
        d2 = c.fetchall()
        playerstats=[d[0][0],d2[0][0],d[0][1].split()[-1]]
        yval = []
        for i in range(len(d)):
            if d[i][2]==playerid:
                playerstats=[d[i][0],d2[i][0],d[i][1].split()[-1]]
            xval.append(d[i][0])
            yval.append(d2[i][0])
            textval.append(d[i][1].split()[-1])
        fig=px.scatter(title='Type of Creativity',labels={'x':'Passing','y':'Carries','text':'Name'},
            x=xval,           y=yval, text=textval,


        )

        fig.add_traces(
            go.Scatter( x=[playerstats[0]], y=[playerstats[1]],text=[playerstats[2]],textfont=fontdict2,name=""))
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='top center')

    elif clusterid in (6,13):
        c.execute(
            """ select (p.final3rdpasses)/a.playedfull ,a.player,a.pid  from astats as a ,passing as p,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid=p.pid   order by a.player""".format(
                clusterid))
        d = c.fetchall()
        xval = []
        textval = []
        c.execute(
            """ select (p.attcarries)/a.playedfull ,a.player  from astats as a ,possession as p,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid= p.pid  order by a.player""".format(
                clusterid))
        d2 = c.fetchall()

        playerstats = [d[0][0], d2[0][0], d[0][1].split()[-1]]
        yval = []
        for i in range(len(d)):
            if d[i][2] == playerid:
                playerstats = [d[i][0], d2[i][0], d[i][1].split()[-1]]
            xval.append(d[i][0])
            yval.append(d2[i][0])
            textval.append(d[i][1].split()[-1])
        fig=px.scatter(title='Type of Attacking Contribution',labels={'x':'Passing','y':'Carries','text':'Name'},
            x=xval,           y=yval, text=textval,

           )
        fig.add_traces(
            go.Scatter(x=[playerstats[0]], y=[playerstats[1]], text=[playerstats[2]], textfont=fontdict2, name=""))
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='top center')
    elif clusterid in (7,11,12,17,18):
        c.execute(
            """ select (a.progp)/a.playedfull ,(a.progc)/a.playedfull ,a.player,a.pid  from astats as a ,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid   order by a.player""".format(
                clusterid))
        d = c.fetchall()
        xval = []
        textval = []


        playerstats = [d[0][0], d[0][1], d[0][2].split()[-1]]
        yval = []
        for i in range(len(d)):
            if d[i][3] == playerid:
                playerstats = [d[i][0], d[i][1], d[i][2].split()[-1]]
            xval.append(d[i][0])
            yval.append(d[i][1])
            textval.append(d[i][2].split()[-1])
        fig=px.scatter(labels={'x':'Passing','y':'Carries','text':'Name'},
            x=xval,title='Type of Attacking Contribution',
            y=yval, text=textval,
        )
        fig.add_traces(
            go.Scatter(x=[playerstats[0]], y=[playerstats[1]], text=[playerstats[2]], textfont=fontdict2, name=""))
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='top center')
    elif clusterid in (0,8):
        c.execute(
            """ select (p.kp+p.crspa+p.ppa+pt.tb)/a.playedfull ,a.player  from astats as a ,passing as p, passtypes as pt,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid=pt.pid and pt.pid= p.pid  order by a.player""".format(
                clusterid))
        d2 = c.fetchall()

        textval = []
        c.execute(
            """ select (a.progr+p.tatt+p.tattpen)/a.playedfull ,a.player ,a.pid from astats as a ,possession as p,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid= p.pid  order by a.player""".format(
                clusterid))
        d = c.fetchall()
        xval = []
        playerstats = [d[0][0], d2[0][0], d[0][1].split()[-1]]
        yval = []
        for i in range(len(d)):
            if d[i][2] == playerid:
                playerstats = [d[i][0], d2[i][0], d[i][1].split()[-1]]
            xval.append(d[i][0])
            yval.append(d2[i][0])
            textval.append(d[i][1].split()[-1])
        fig = px.scatter(title='Type of Forward', labels={'x': 'Involvement in attacking phase', 'y': 'creativity','text':'Name'},
                         x=xval, y=yval, text=textval,

                         )
        fig.add_traces(
            go.Scatter(x=[playerstats[0]], y=[playerstats[1]], text=[playerstats[2]], textfont=fontdict2, name=""))
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='top center')
    elif clusterid in (5,2):#ball playing capabilities
        d=[]
        for x in ['progp','progc']:
            c.execute(
                """select round(rnk,1),round(val,2) from (select pid,{}/playedfull as val,percent_rank()over( order by {}/playedfull asc )*100 as rnk from (select a.pid ,a.{} ,a.playedfull  from astats as a where a.playedfull>=10 and a.pid in (select c.pid from clusterinfo as c where cluster={}) ) ) where pid= '{}' ;""".format(
                    x,x, x,clusterid, playerid))
            d.append(c.fetchall())
        for x in ['lpatt','lpcmp']:
            c.execute(
                """select round(rnk,1),round(val,2) from (select pid,{}/mp as val,percent_rank()over(order by {}/mp asc )*100 as rnk from (select a.pid ,a.{} ,a.mp  from passing as a where a.mp>=10 and a.pid in (select c.pid from clusterinfo as c where cluster={})) ) where pid= '{}' ;""".format(
                   x, x, x,clusterid, playerid))

            d.append( c.fetchall())
        c.execute(
            """select round(rnk,1),round(val,2) from (select pid,{}/mp as val,percent_rank()over( order by {}/mp asc )*100 as rnk from (select a.pid ,a.{} ,a.mp  from totatt as a where a.mp>=10 and a.pid in (select c.pid from clusterinfo as c where cluster={}))  ) where pid= '{}' ;""".format(
                'sw', 'sw','sw', clusterid,playerid))


        d.append(c.fetchall())

        xval = [t[0][0] for t in d]
        textval = [t[0][1] for t in d]
        yval = ['Prog passes','Prog carries','Long pass attemp','Long pass comp ','Switches']
        fig = px.bar(title="Ball Playing Quality", x=xval, y=yval, orientation='h', color=xval,text=textval,labels={'x':'','y':'','color':'Percentile','text':'per 90'},
                      color_continuous_scale=px.colors.make_colorscale(
                [customscale[x][1] for x in range(len(customscale) - 2, -1, -2)])
                     , range_x=[0, 100], range_color=[0, 100])
    else:#cbs
        d = []
        for x in ['tklondef','tklonmid','pass_blocked','shots_blocked','interceptions']:
            c.execute(
                """select round(rnk,1),round(val,2) from (select pid,{}/mp as val,percent_rank()over(order by {}/mp asc )*100 as rnk from (select a.pid ,a.{} ,a.mp  from dstats as a where a.mp>=10 and a.pid in (select c.pid from clusterinfo as c where cluster={})) ) where pid= '{}' ;""".format(
                   x, x, x,clusterid, playerid))
            d.append(c.fetchall())


        xval = [t[0][0] for t in d]
        textval = [t[0][1] for t in d]
        yval = ['Tackles on def3rd', 'Tackles on mid3rd', 'Passes blocked', 'Shots blocked', 'Interceptions']
        fig = px.bar(title="Game Reading Quality", x=xval, y=yval, orientation='h', color=xval, text=textval,
                     labels={'x': '', 'y': '','color':'Percentile','text':'per 90'},
                     color_continuous_scale=px.colors.make_colorscale(
                         [customscale[x][1] for x in range(len(customscale) - 2, -1, -2)])
                     , range_x=[0, 100], range_color=[0, 100])

    return fig
def plottwo(c,playerid,position):
    if position == 'GK':
        c.execute(
            """ select (p.tdef+p.tmid+p.carries)/p.mp,g.gklaunchper ,a.player,a.pid  from astats as a ,totgk as g,possession as p where a.position='GK' and a.playedfull>=25  and a.pid=p.pid and p.pid=g.pid  order by a.player""")
        d = c.fetchall()
        xval = []
        textval = []

        playerstats = [d[0][0], d[0][1], d[0][2].split()[-1]]
        yval = []
        for i in range(len(d)):
            if d[i][3] == playerid:
                playerstats = [d[i][0], d[i][1], d[i][2].split()[-1]]
            xval.append(d[i][0])
            yval.append(d[i][1])
            textval.append(d[i][2].split()[-1])
        fig = px.scatter(title='Contribution in Buildup', labels={'x': 'Short', 'y': 'Long', 'text': 'Name'},
                         x=xval, y=yval, text=textval,

                         )
        fig.add_traces(
            go.Scatter(x=[playerstats[0]], y=[playerstats[1]], text=[playerstats[2]], textfont=fontdict2, name=""))
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition='top center')
        return fig
    c.execute("select cluster from clusterinfo where pid= {} ".format(playerid))
    clusterid = c.fetchall()[0][0]


    if clusterid in ( 19, 3, 16):
        d=[]
        for x in ['miscon','dispos','dribtkldper']:
         if x !='dribtkldper':
          c.execute(
            """select round(rnk,1),round(val,2)  from (select pid,{}/mp as val,percent_rank()over( order by {}/mp asc )*100 as rnk from (select a.pid ,a.{} ,a.mp  from possession as a where a.mp>=10 and a.pid in (select c.pid from clusterinfo as c where cluster={})) ) where pid= '{}' ;""".format(
                x,x,x,clusterid, playerid))
         else:
             c.execute(
                 """select round(rnk,1),round(val,2)  from (select pid,{} as val,percent_rank()over( order by {} asc )*100 as rnk from (select a.pid ,a.{} ,a.mp  from possession as a where a.mp>=10 and a.pid in (select c.pid from clusterinfo as c where cluster={})) ) where pid= '{}' ;""".format(
                    x, x,x, clusterid,playerid))
         d.append( c.fetchall())
        c.execute(
            """select round(rnk,1),round(val,2)  from (select pid,100-{} as val,percent_rank()over( order by 100-{} asc )*100 as rnk from (select a.pid ,a.{} ,a.mp  from passing as a where a.mp>=10 and a.pid in (select c.pid from clusterinfo as c where cluster={})) ) where pid= '{}' ;""".format(
                'spcmpper', 'spcmpper', 'spcmpper',clusterid, playerid))
        d.append(c.fetchall())

        xval = [t[0][0] for t in d]
        textval = [t[0][1] for t in d]
        yval = ['Miscontrols','Dispossessed','Dribbles lost%','Shortpass failed%']
        fig = px.bar(title="Efficiency ", x=xval, y=yval, orientation='h', color=xval,text=textval,labels={'x':'','y':'','color':'Percentile','text':'per 90'},
                      color_continuous_scale=px.colors.make_colorscale(
                [customscale[x][1] for x in range(0, len(customscale), 2)])
                     , range_x=[0, 100], range_color=[0, 100])
    elif clusterid in (6, 13):
        c.execute(
            """ select (d.tklonmid+d.tklonatt)/a.playedfull ,(d.blocks+d.interceptions+m.recov)/a.playedfull,d.tacklewon*100/d.tackles, a.player  from astats as a ,dstats as d,misstats as m ,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid=d.pid and d.pid=m.pid  order by a.player""".format(
                clusterid))
        d = c.fetchall()
        xval = [t[0] for t in d]
        textval = [t[3].split()[-1] for t in d]


        yval = [t[1] for t in d]
        colval=[t[2] for t in d]

        fig = px.scatter(
            x=xval, y=yval,labels={'x':'Tackling','y':'Game Reading','color':'Tackle succ%','text':'Name'},title='Defensive Actions', text=textval,color=colval,color_continuous_scale=px.colors.make_colorscale(
                [customscale[x][1] for x in range(len(customscale) - 2, -1, -2)])


        )
        fig.update_traces(textposition='top center')
    elif clusterid in (7, 11, 12, 17):
        c.execute(
            """ select (d.tklonmid+d.tklondef)/a.playedfull ,(d.blocks+d.interceptions+m.recov)/a.playedfull,d.tacklewon*100/d.tackles, a.player  from astats as a ,dstats as d,misstats as m ,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid=d.pid and d.pid=m.pid  order by a.player""".format(
                clusterid))
        d = c.fetchall()
        xval = [t[0] for t in d]
        textval = [t[3].split()[-1] for t in d]

        yval = [t[1] for t in d]
        colval = [t[2] for t in d]

        fig = px.scatter(
            x=xval, y=yval,labels={'x':'Tackling','y':'Game Reading','color':'Tackle succ%','text':'Name'}, text=textval, title='Defensive Actions',color=colval, color_continuous_scale=px.colors.make_colorscale(
                [customscale[x][1] for x in range(len(customscale) - 2, -1, -2)])


        )
        fig.update_traces(textposition='top center')
    elif clusterid in (1, 10, 18):
        c.execute(
            """ select (d.tacklewon)/a.playedfull ,(d.blocks+d.interceptions+m.recov)/a.playedfull,d.duelsucc, a.player  from astats as a ,dstats as d,misstats as m ,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid=d.pid and d.pid=m.pid  order by a.player""".format(
                clusterid))
        d = c.fetchall()
        xval = [t[0] for t in d]
        textval = [t[3].split()[-1] for t in d]

        yval = [t[1] for t in d]
        colval = [t[2] for t in d]

        fig = px.scatter(
            x=xval, y=yval,labels={'x':'Tackling','y':'Game Reading','color':'GroundDuels succ%','text':'Name'}, text=textval,title='Defensive Actions', color=colval, color_continuous_scale=px.colors.make_colorscale(
                [customscale[x][1] for x in range(len(customscale) - 2, -1, -2)])


        )
        fig.update_traces(textposition='top center')
    elif clusterid in (0, 8,9,14):
        c.execute(
            """ select (a.xnonpeng)/a.playedfull ,s.shotconv,s.npgnpxg ,a.player  from astats as a ,shooting as s,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}' and a.pid=c.pid and c.pid=s.pid  order by a.player""".format(
                clusterid))
        d = c.fetchall()
        xval = [t[0] for t in d]
        textval = [t[3].split()[-1] for t in d]
        colval = [t[2] for t in d]
        yval = [t[1] for t in d]
        fig = px.scatter(
            x=xval, color=colval, y=yval, text=textval,title='Clinical Nature',labels={'x':'Quality of chances','y':'Shot conversion','color':'NpXG-NpG','text':'Name'},
            color_continuous_scale=px.colors.make_colorscale(
                [customscale[x][1] for x in range(len(customscale) - 2, -1, -2)])

        )
        fig.update_traces(textposition='top center')

    else:
        c.execute(
            """ select d.duelsucc ,(m.aerialswon)/a.playedfull,m.aerialswonper, a.player  from astats as a ,dstats as d,misstats as m ,clusterinfo as c where a.playedfull>=10 and c.cluster= '{}'and  a.pid=c.pid and c.pid=d.pid and d.pid=m.pid  order by a.player""".format(
                clusterid))
        d = c.fetchall()
        xval = [t[0] for t in d]
        textval = [t[3].split()[-1] for t in d]

        yval = [t[1] for t in d]
        colval = [t[2] for t in d]
        fig = px.scatter(title='Defensive Duels',labels={'x':'Dribblers takld%','y':'Aerials Won Per 90','color':'Aerials succ%','text':'Name'},
            x=xval, y=yval, text=textval, color=colval, color_continuous_scale=px.colors.make_colorscale(
                [customscale[x][1] for x in range( len(customscale)-2,-1,- 2)])


        )
        fig.update_traces(textposition='top center')

    return fig

def  gkdata(c,playerid):
    passingd = []
    c.execute("""update passing set spcmp = 0 where spcmp="";""")
    c.execute(
        "select round(rnk,1) from (select pid,spcmp,percent_rank()over(PARTITION by position order by spcmp/mp)*100 as rnk from passing  where mp>=10 and position='GK' ) where pid='{}';".format(
            playerid))
    passingd.append(c.fetchall()[0][0])
    c.execute("""update passing set mpcmpper = 0 where mpcmpper="";""")
    c.execute("select round(mpcmpper,1) from passing where pid= '{}'".format(playerid))
    passingd.append(c.fetchall()[0][0])
    c.execute("""update passing set mpcmp = 0 where mpcmp="";""")
    c.execute(
        "select round(rnk,1) from (select pid,mpcmp,percent_rank()over(PARTITION by position order by mpcmp/mp)*100 as rnk from passing  where mp>=10 and position='GK' ) where pid='{}';".format(
            playerid))
    passingd.append(c.fetchall()[0][0])

    gk = ['Shrtcmp', 'Midrangecmp%', 'Midrange_passes', 'GKicksLaunch%', 'Saves', 'Saves%', 'Pen_saved', 'Psxg+/-',
          'Psxg_Sot', 'Crs_stop%', '#OPA', 'AVGDist']

    gklist = ['gklaunchper', 'saves', 'savesper', 'pksv', 'psxgpn', 'psxg_sot', 'crossstpper', 'opa', 'avgdistswp']
    for x in gklist:
        c.execute("""update totgk set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['saves','opa']:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(order by {} /mp asc )*100 as rnk from totgk where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        else:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(order by {}  asc )*100 as rnk from totgk where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        passingd.append(c.fetchall()[0][0])


    return passingd,gk
def dfdata(c,playerid):

    df = ['Tkl', 'Tklw', 'DuelW%', 'Touches in mid', 'Aerials', 'AerialW%','Recoveries', 'Blocks', 'Int',
          'Passes_Att', 'Passes_cmp%', 'Errors']
    passingd=[]
    for x in ['tackles','tacklewon','duelsucc','blocks','interceptions','errors']:
        c.execute("""update dstats set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['duelsucc']:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from dstats where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        else:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from dstats where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['aerialswon','aerialswonper','recov']:
        c.execute("""update totatt set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['aerialswonper']:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        else:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} /mp asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['att','compper']:
        c.execute("""update passing set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['compper']:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from passing where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        else:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from passing where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        passingd.append(c.fetchall()[0][0])
    c.execute("""update possession set '{}' = 0 where '{}'="";""".format('tmid', 'tmid'))
    c.execute("""update possession set '{}' = 0 where '{}'="";""".format('tatt', 'tatt'))
    c.execute(
        """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by tmid+tatt asc )*100 as rnk from possession where mp>=10) where pid= '{}' ;""".format( playerid))
    passingd.append(c.fetchall()[0][0])

    return passingd[0:3]+[passingd[-1]]+passingd[6:9]+passingd[3:5]+passingd[9:11]+passingd[5:6],df

def mfdfdata(c,playerid):
    mfdf = ['Tkl', 'Tklw', 'AerialW%', 'Blocks', 'Int', 'Recoveries', 'Sw', 'Passes_Att', 'Passes_cmp%', 'LongpassCmp',
            'Prog P', 'Prog C']
    passingd = []
    for x in ['tackles', 'tacklewon', 'blocks', 'interceptions']:
        c.execute("""update dstats set '{}' = 0 where '{}'="";""".format(x, x))

        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from dstats where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in [  'recov','aerialswonper','sw']:
        c.execute("""update totatt set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['aerialswonper']:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        else:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} /mp asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['att', 'compper','lpcmp']:
        c.execute("""update passing set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['compper','lpcmp']:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from passing where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        else:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from passing where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['progp', 'progc']:
        c.execute("""update astats set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/playedfull asc )*100 as rnk from astats where min>1000) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])

    return passingd[0:2]+[passingd[5]]+passingd[2:5]+passingd[6:],mfdf
def mfdata(c,playerid):
    mf = [ 'Tackles','TacklesWon','Int', 'Recoveries', 'TB',  'Keypasses', 'XA', 'Prog P', 'Prog C', 'Prog R', 'XT', 'NoncrossXT']
    passingd = []
    for x in ['tackles', 'tacklewon', 'interceptions']:
        c.execute("""update dstats set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from dstats where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['recov','tb']:
        c.execute("""update totatt set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['kp','xa']:
        c.execute("""update passing set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from passing where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['progp', 'progc','progr']:
        c.execute("""update astats set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/playedfull asc )*100 as rnk from astats where min>1000) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    c.execute("""select  round(rnk,1) from (select player,squad, percent_rank()over( order by noncrossxt asc )*100 as rnk from markstatsplayers where player in (SELECT m.markstatsplayer from  playerkey as m where m.fbrefplayer in  (select player from astats where position='MF' )))where player = (select markstatsplayer  from playerkey where fbrefplayer= (SELECT player from astats where pid= '{}' )) and squad=(SELECT markstatssquad from squadkey where trim(fbrefsquad)=trim((select squad from astats where pid= '{}' )));
""".format(playerid,playerid))
    x=c.fetchall()

    passingd.append(x[0][0])
    c.execute("""select  round(rnk,1) from (select player,squad, percent_rank()over( order by noncrossxt asc )*100 as rnk from markstatsplayers where player in (SELECT m.markstatsplayer from  playerkey as m where m.fbrefplayer in  (select player from astats where position='MF' )))where player = (select markstatsplayer  from playerkey where fbrefplayer= (SELECT player from astats where pid= '{}' )) and squad=(SELECT markstatssquad from squadkey where trim(fbrefsquad)=trim((select squad from astats where pid= '{}' )));
""".format(playerid,playerid))
    passingd.append(c.fetchall()[0][0])
    return passingd,mf
def fwmfdata(c,playerid):
    fwmf = [ 'Dribsucc', 'Dribsucc%', 'TB', 'Keypasses', 'XA','PPA', 'XT','NoncrossXT', 'XnonpenG', 'Prog P', 'Prog C',
            'Prog R']
    passingd=[]
    for x in ['dribsucc','dribsuccper']:
        c.execute("""update possession set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['dribsuccper']:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from possession where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        else:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from possession where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['tb']:
        c.execute("""update totatt set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['kp','xa','ppa']:
        c.execute("""update passing set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from passing where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    c.execute("""select  round(rnk,1) from (select player,squad, percent_rank()over( order by xthreat asc )*100 as rnk from markstatsplayers where player in (SELECT m.markstatsplayer from  playerkey as m where m.fbrefplayer in  (select player from astats where position='FWMF' )))where player = (select markstatsplayer  from playerkey where fbrefplayer= (SELECT player from astats where pid= '{}' )) and squad=(SELECT markstatssquad from squadkey where trim(fbrefsquad)=trim((select squad from astats where pid= '{}' )));
        """.format(playerid,playerid))
    passingd.append(c.fetchall()[0][0])
    c.execute("""select  round(rnk,1) from (select player,squad, percent_rank()over( order by noncrossxt asc )*100 as rnk from markstatsplayers where player in (SELECT m.markstatsplayer from  playerkey as m where m.fbrefplayer in  (select player from astats where position='FWMF' )))where player = (select markstatsplayer  from playerkey where fbrefplayer= (SELECT player from astats where pid= '{}' )) and squad=(SELECT markstatssquad from squadkey where trim(fbrefsquad)=trim((select squad from astats where pid= '{}' )));
        """.format(playerid,playerid))
    passingd.append(c.fetchall()[0][0])

    for x in ['xnonpeng','progp', 'progc','progr']:
        c.execute("""update astats set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/playedfull asc )*100 as rnk from astats where min>1000) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])

    return passingd,fwmf
def fwdata(c,playerid):
    fw = ['Dribsucc', 'Dribsucc%', 'Miscontrols', 'Dispossessed','CPA', 'Final3rdC', 'Keypasses', 'XA', 'Prog R', 'nonpenG', 'XnonpenG', 'G/ShConv'          ]
    passingd = []
    for x in ['dribsucc', 'dribsuccper','miscon','dispos','cpa','attcarries']:
        c.execute("""update possession set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['dribsuccper']:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from possession where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        else:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from possession where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])

    for x in ['kp', 'xa']:
        c.execute("""update passing set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from passing where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['progr','nonpen','xnonpeng']:
        c.execute("""update astats set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/playedfull asc )*100 as rnk from astats where min>1000) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['shotconv']:
        c.execute("""update totatt set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    return passingd,fw

def fwdfdata(c,playerid):

    fwdf = ['Tkl', 'Tklw', 'DuelW%', 'AerialW%', 'Recoveries', 'Blocks', 'Int','SCA','KeyPasses', 'XA', 'PPA', 'CrossesPA']
    passingd = []
    for x in ['tackles', 'tacklewon', 'duelsucc', 'blocks', 'interceptions']:
        c.execute("""update dstats set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['duelsucc']:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from dstats where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        else:
            c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from dstats where mp>=10) where pid= '{}' ;""".format(
                x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in [ 'aerialswonper', 'recov','sca']:
        c.execute("""update totatt set '{}' = 0 where '{}'="";""".format(x, x))
        if x in ['aerialswonper']:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        else:
            c.execute(
                """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {} /mp asc )*100 as rnk from totatt where mp>=10) where pid= '{}' ;""".format(
                    x, playerid))
        passingd.append(c.fetchall()[0][0])
    for x in ['kp','xa','ppa','crspa']:
        c.execute("""update passing set '{}' = 0 where '{}'="";""".format(x, x))
        c.execute(
            """select round(rnk,1) from (select pid,percent_rank()over(partition by position order by {}/mp asc )*100 as rnk from passing where mp>=10) where pid= '{}' ;""".format(
                x, playerid))

        passingd.append(c.fetchall()[0][0])

    return passingd,fwdf
def graph_matcher(c,playerid,position):
    if position=='GK':
        return gkdata(c,playerid)
    elif position=='DF':
        return dfdata(c, playerid)
    elif position == 'MF':
        return mfdata(c, playerid)
    elif position == 'FW':
        return fwdata(c, playerid)
    elif position == 'FWMF':
        return fwmfdata(c, playerid)
    elif position == 'FWDF':
        return fwdfdata(c, playerid)
    else:
        return mfdfdata(c, playerid)

sqlcommands=["""select squad,round(rnk,1) from (select trim(squad) as squad ,percent_rank()over( order by gkprogression  asc)*100 as rnk from markstats ) 
 where trim(squad)=(select trim(markstatssquad) from squadkey where trim(fbrefsquad)=trim('{}'));""",
             """select squad,round(rnk,1) from (select trim(squad) as squad ,percent_rank()over( order by fieldtilt  asc)*100 as rnk from markstats ) 
              where trim(squad)=(select trim(markstatssquad) from squadkey where trim(fbrefsquad)=trim('{}'));""",
             """select squad,round(rnk,1) from (select trim(squad) as squad ,percent_rank()over( order by directness  asc)*100 as rnk from markstats ) 
              where trim(squad)=(select trim(markstatssquad) from squadkey where trim(fbrefsquad)=trim('{}'));""",
"""select squad,round(rnk,1) from (select squad,percent_rank()over(order by progp asc)*100 as rnk from (select squad,sum(progp) as progp from astats  group by squad)  ) where trim(squad)=trim('{}');""",
"""select squad,round(rnk,1) from (select squad,percent_rank()over(order by progp asc)*100 as rnk from (select squad,sum(x) as progp from (select a.squad,t.dribsucc as x from possession as t ,astats as a where t.pid=a.pid) group by squad)  ) where trim(squad)=trim('{}');
""",
"""select squad,round(rnk,1) from (select squad,percent_rank()over(order by progp asc)*100 as rnk from (select squad,sum(x) as progp from (select a.squad,(t.crs + t.fk) as x from passtypes as t ,astats as a where t.pid=a.pid) group by squad)  ) where trim(squad)=trim('{}');
             """,
"""select squad,round(rnk,1) from (select squad,percent_rank()over(order by progp asc)*100 as rnk from (select squad,sum(x) as progp from (select a.squad,t.npgnpxg as x from shooting as t ,astats as a where t.pid=a.pid) group by squad)  ) where trim(squad)=trim('{}');
""",

             """select squad,round(rnk,1) from (select trim(squad) as squad ,percent_rank()over( order by defline  asc)*100 as rnk from markstats ) 
              where trim(squad)=(select trim(markstatssquad) from squadkey where trim(fbrefsquad)=trim('{}'));""",
"""select squad,round(rnk,1) from (select squad,percent_rank()over(order by progp asc)*100 as rnk from (select squad,sum(x) as progp from (select a.squad,(t.tklint + t.blocks+ t.clearances) as x from dstats as t ,astats as a where t.pid=a.pid) group by squad)  ) where trim(squad)=trim('{}');
""",
             """select squad,round(rnk,1) from (select trim(squad) as squad ,percent_rank()over( order by oppnbuidup  desc)*100 as rnk from markstats ) 
              where trim(squad)=(select trim(markstatssquad) from squadkey where trim(fbrefsquad)=trim('{}'));""",
         ]

#for team page
def squadwheelhelper(c,value):

    totatt=['sw','sca']

    finalvalues=[]
    for x in sqlcommands:
        c.execute(x.format(value))

        rec=c.fetchall()[0]
        print(rec)
        finalvalues.append(rec[1])
    for x in totatt:
        c.execute(
            """select squad,round(rnk,1) from (select squad,percent_rank()over(order by progp asc)*100 as rnk from (select squad,sum(x) as progp from (select a.squad,t.'{}' as x from totatt as t ,astats as a where t.pid=a.pid) group by squad)  ) where trim(squad)=trim('{}');
""".format(x,value))
        rec = c.fetchall()[0]
        print(rec)
        finalvalues.append(rec[1])



    return finalvalues[0:4]+[finalvalues[10]]+finalvalues[4:6]+[finalvalues[11]]+finalvalues[6:10]

##important theme and color settings
legenddict=dict(
                               x=0,
                               y=1,
                               traceorder="reversed",
                               title_font_family="chela",
                               font=dict(
                                   family="chela",
                                   size=12,
                                   #color="black"
                               ),bgcolor="black",
                               bordercolor="darkorange",
                               borderwidth=1.5
                           )
fontdict=dict(
                               family="Consolas",
                               size=15,
                               #color="black"
                           )
fontdict2=dict(
                               family="Rockwell",
                               size=15,
                               color="red"
                           )

