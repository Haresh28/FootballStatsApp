<br/>
<p align="center">
  
  <h2 align="center">Football Stats App   </h2>

  
</p>



## About The Project
 The aim of this project is to gain useful insights  and player patters from  real time data .Users can also assess the quality and compare similarites and differences between the players and as well as clubs. This app is built using Dash and Plotly which are powerful framework for visualization .

### Prerequisites
```sh
pip install diskcache
pip install scrapy
pip install tqdm
```

### Working
**Web scrapping:**

* The data is gathered from three different sites by web scrapping using scrapy.
* Scrapy uses pipeline and multiprocessing for processing data and it is the go to  library for scrapping large tabular data.
* Once scrapped the data is stored in a sql database . Thus making it possible to access data offline.
* User can  update data by pressing the update button on the top left corner.

**Players:**
* A classification model is used to classify player based on their roles. This helps in visualizing certain abilities of a specific set of players .
* The players are not only classified on their roles but also on their quality
* By using this ,a list of 3 players  who are closer to the player  chosen   in terms of style is displayed

**Squad:**

* Squad page hosts variety of graphs that helps in assessing the squad valuation , squad balance, squad  playing style
* Feel free to check out *About* page for detailed information regarding the graphs


**Acknowledgements:**

* [Fbref](https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats)
* [Markstats](https://markstats.club/)
* [Transfermarkt](https://www.transfermarkt.com/)
