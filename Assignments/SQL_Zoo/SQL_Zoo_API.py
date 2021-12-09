# main.py

from starlette.responses import HTMLResponse
from mysqlCnx import MysqlCnx
from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import json 

#open the config file, read it then connect to the database
with open('/var/www/html/api/sqlzoo/.sql_zoo_config.json') as f:
    config = json.loads(f.read())

cnx = MysqlCnx(**config)

#Create an item data model for adding new information to a table
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float

#Create an world data model for adding new information to a table
class world_class(BaseModel):
    name: str
    continent: str
    area: float
    population: float
    gdp: float
    capital: str
    tld: str
    flag: str

#Create an teacher data model for adding new information to a table
class teacher_class(BaseModel):
    id: int
    dept: int
    name: str
    phone: str
    mobile: str





#create dictionaries to hold the questions and sql queries.
world_dict = {
    1: {"question" :"Show the name, continent and population of all countries", "sql": "SELECT name, continent, population FROM world"},
    2: {"question":"Show the name for the countries that have a population of at least 200 million", "sql":"SELECT name FROM world WHERE population >= 200000000"},
    3: {"question":"Give the name and the per capita GDP for those countries with a population of at least 200 million" , "sql":"SELECT name, gdp/population FROM world WHERE population >= 200000000"},
    4: {"question":"Show the name and population (in millions) for the countries on the continent of South America ", "sql":"SELECT name, population/1000000 FROM world WHERE continent LIKE 'South America'"},
    5: {"question":"Show the name and population for France, Germany, Italy", "sql":"SELECT name, population FROM world WHERE name IN('France','Germany','Italy')"},
    6: {"question":"Show the countries which have a name that includes the word United", "sql":"SELECT name FROM world WHERE name LIKE '%United' or name like 'United%' or name like '%United%'"},
    7: {"question":"Show the name, population and area of countries that are big by area or big by population.", "sql":"SELECT name, population, area FROM world WHERE area > 3000000 OR population > 250000000"},
    8: {"question":"Show name population and area for the countries with an area more than 3 million or population more than 250 million but not both.", "sql":"SELECT name, population, area FROM world WHERE area > 3000000 XOR population > 250000000"},
    9: {"question":"Show the name and population in millions and the GDP in billions for the countries of the continent South America.", "sql":"SELECT name, ROUND(population/1000000,2), ROUND(gdp/1000000000, 2) FROM world WHERE  continent = 'South America'"},
    10: {"question":"Show per-capita GDP for the trillion dollar countries to the nearest $1000.", "sql":"SELECT name , ROUND(gdp/population, -3) FROM world WHERE gdp >= 1000000000000"},
    11: {"question":"Show the name and capital where the name and the capital have the same number of characters.", "sql":"SELECT name, capital FROM world WHERE LENGTH(name) = LENGTH(capital)"},
    12: {"question":"Show the name and the capital where the first letters of each match. Don't include countries where the name and the capital are the same word.", "sql":"SELECT name, capital FROM world WHERE LEFT(name,1) = LEFT(capital,1) AND name <> capital"},
    13: {"question":"Find the country that has all the vowels and no spaces in its name.", "sql":"SELECT name FROM world WHERE name LIKE '%a%' AND name LIKE '%e%' AND name LIKE '%i%' AND name LIKE '%o%' AND name LIKE '%u%' AND name NOT LIKE '% %'"}
}

nobel_dict = {
    1: {"question":"Display Nobel prizes for 1950.", "sql":"SELECT yr, subject, winner FROM nobel WHERE yr = 1950"},
    2: {"question":"Who won the 1962 Nobel prize for Literature.", "sql":"SELECT winner FROM nobel WHERE yr = 1962 AND subject = 'Literature'"},
    3: {"question":"Show the year and subject that won 'Albert Einstein' his prize.", "sql":"SELECT yr, subject from nobel WHERE winner = 'Albert Einstein'"},
    4: {"question":"What are the names of the 'Peace' winners since the year 2000 inclusive.", "sql":"select winner from nobel WHERE subject like '%Peace%' and yr >= '2000'"},
    5: {"question":"Show all details (yr, subject, winner) of the Literature prize winners for 1980 to 1989 inclusive.", "sql":"SELECT yr, subject, winner FROM nobel WHERE subject = 'Literature' AND yr >= 1980 AND yr <= 1989"},
    6: {"question":"Show all details of the presidential winners: Theodore Roosevelt Woodrow Wilson Jimmy Carter Barack Obama ", "sql":"SELECT * FROM nobel WHERE winner IN ('Theodore Roosevelt','Woodrow Wilson','Jimmy Carter','Barack Obama')"},
    7: {"question":"Show the winners with first name John", "sql":"SELECT winner FROM nobel WHERE winner LIKE 'John%'"},
    8: {"question":"Show the year, subject, and name of Physics winners for 1980 together with the Chemistry winners for 1984.", "sql":"SELECT yr, subject, winner FROM nobel WHERE yr = 1980 AND subject = 'Physics' OR yr = 1984 AND subject = 'Chemistry'"},
    9: {"question":"Show the year, subject, and name of winners for 1980 excluding Chemistry and Medicine", "sql":"SELECT yr, subject, winner FROM nobel WHERE yr = 1980 AND subject <> 'Medicine' AND subject <> 'Chemistry'"},
    10: {"question":"Show year, subject, and name of people who won a 'Medicine' prize before 1910, not including 1910) and winners of a 'Literature' prize in or after 2004 inclusive.)", "sql":"SELECT yr, subject, winner FROM nobel WHERE subject = 'Medicine' AND yr < 1910 OR subject = 'Literature' AND yr >= 2004"},
    11: {"question":"Find all details of the prize won by PETER GRÜNBERG", "sql":"SELECT yr, subject, winner FROM nobel WHERE winner = 'PETER GRÜNBERG'"},
    12: {"question":"Find all details of the prize won by EUGENE O'NEILL", "sql":"SELECT yr, subject, winner FROM nobel WHERE winner LIKE 'EUGENE O%' and winner LIKE '%NEILL'"},
    13: {"question":"List the winners, year and subject where the winner starts with Sir. Show the the most recent first, then by name order.", "sql":"SELECT winner, yr, subject FROM nobel WHERE winner LIKE 'Sir%' ORDER BY yr DESC, winner ASC"},
    14: {"question":"Show the 1984 winners and subject ordered by subject and winner name; but list Chemistry and Physics last.", "sql":"SELECT winner, subject FROM nobel WHERE yr=1984 ORDER BY CASE WHEN subject IN ('Physics','Chemistry') THEN 1 ELSE 0 END, subject, winner"}
}

basic_dict = {
    1: {"question":"What is the population of Germany?","sql":"SELECT population FROM world WHERE name = 'France'"},
    2: {"question": "Show the population for Sweden, Norway and Denmark", "sql":"SELECT name, population FROM world WHERE name IN ('Sweden', 'Norway', 'Denmark')" },
    3: {"question": "Which countries have an area between 200 000 and 250 000 sq. km.", "sql":"SELECT name, area FROM world WHERE area BETWEEN 200000 AND 250000"}
}

select_dict = {
    1: {"question":"List each country name where the population is larger than that of 'Russia'.", "sql":"SELECT name FROM world WHERE population > (SELECT population FROM world WHERE name='Russia')"},
    2: {"question":"Show the countries in Europe with a per capita GDP greater than 'United Kingdom'.", "sql":"SELECT name FROM world WHERE  (gdp/population) > (SELECT (gdp/population) FROM world WHERE name = 'United Kingdom') AND continent = 'Europe'"},
    3: {"question":"List the name and continent of countries in the continents containing either Argentina or Australia. Order by name of the country.", "sql":"SELECT name, continent FROM world WHERE continent IN (SELECT continent FROM world WHERE name IN ('Argentina', 'Australia')) ORDER BY name"},
    4: {"question":" Which country has a population that is more than Canada but less than Poland? Show the name and the population.", "sql":"SELECT name, population FROM world WHERE population > (SELECT population FROM world WHERE name = 'Canada') AND population < (SELECT population FROM world WHERE name = 'Poland')"},
    5: {"question":"Show the name and the population of each country in Europe. Show the population as a percentage of the population of Germany.", "sql":"SELECT name, CONCAT(ROUND(population/(SELECT population FROM world WHERE name = 'Germany')*100), '%') FROM world WHERE continent = 'Europe"},
    6: {"question":"Which countries have a GDP greater than every country in Europe? ", "sql":"SELECT name FROM world WHERE gdp > ALL(SELECT gdp FROM world WHERE gdp > 0 AND continent = 'Europe')"},
    7: {"question":"Find the largest country (by area) in each continent, show the continent, the name and the area", "sql":"SELECT continent, name, area FROM world x WHERE area >= ALL(SELECT area FROM world y WHERE x.continent = y.continent AND y.area>0)"},
    8: {"question":"List each continent and the name of the country that comes first alphabetically.", "sql":"SELECT continent, name, area FROM world x WHERE area >= ALL(SELECT area FROM world y WHERE x.continent = y.continent AND y.area>0)"},
    9: {"question":"Find the continents where all countries have a population <= 25000000. Then find the names of the countries associated with these continents. Show name, continent and population.", "sql":"SELECT name, continent, population FROM world WHERE continent IN (SELECT continent FROM world x WHERE 25000000 >= (SELECT MAX(population) FROM world y WHERE x.continent = y.continent))"},
    10:{"question":"Give the countries and continents that have populations more than three times that of any of their neighbours (in the same continent).", "sql":"SELECT name, continent FROM world x WHERE population > ALL(SELECT 3*population FROM world y WHERE x.continent = y.continent AND x.name <> y.name)"}
}

count_dict = {
    1: {"question":"Show the total population of the world.", "sql":"SELECT SUM(population) FROM world"},
    2: {"question":"List all the continents - just once each.", "sql":"SELECT DISTINCT continent FROM world"},
    3: {"question":"Give the total GDP of Africa", "sql":"SELECT SUM(gdp) FROM world WHERE continent = 'Africa'"},
    4: {"question":"How many countries have an area of at least 1000000", "sql":"SELECT COUNT(*) FROM world WHERE area >= 1000000"},
    5: {"question":"What is the total population of ('Estonia', 'Latvia', 'Lithuania')", "sql":"SELECT SUM(population) FROM world WHERE name IN ('Estonia','Latvia','Lithuania')"},
    6: {"question":"For each continent show the continent and number of countries.", "sql":"SELECT continent, COUNT(*) FROM world GROUP BY continent"},
    7: {"question":"For each continent show the continent and number of countries with populations of at least 10 million.", "sql":"SELECT continent, COUNT(*) FROM world WHERE population >= 10000000 GROUP BY continent"},
    8: {"question":"List the continents that have a total population of at least 100 million", "sql":"SELECT continent FROM world x WHERE (SELECT SUM(population) FROM world y WHERE x.continent = y.continent) >= 100000000 GROUP BY continent"}
}

join_dict = {
    1: {"question":"Show the matchid and player name for all goals scored by Germany.", "sql":"SELECT matchid, player FROM goal WHERE teamid = 'GER'"},
    2: {"question":"Show id, stadium, team1, team2 for just game 1012", "sql":"SELECT id, stadium, team1, team2 FROM game WHERE id = 1012"},
    3: {"question":"Show the player, teamid, stadium and mdate for every German goal.", "sql":"SELECT player, teamid, stadium, mdate FROM game JOIN goal ON game.id = goal.matchid WHERE teamid='GER'"},
    4: {"question":"Show the team1, team2 and player for every goal scored by a player called Mario player LIKE 'Mario%'", "sql":"SELECT game.team1, game.team2, goal.player FROM goal JOIN game ON game.id = goal.matchid WHERE goal.player LIKE 'Mario%'"},
    5: {"question":"Show player, teamid, coach, gtime for all goals scored in the first 10 minutes gtime<=10", "sql":"SELECT player, teamid, coach, gtime FROM goal JOIN eteam ON goal.teamid = eteam.id WHERE gtime <= 10"},
    6: {"question":"List the dates of the matches and the name of the team in which 'Fernando Santos' was the team1 coach.", "sql":"SELECT mdate, teamname FROM eteam JOIN game ON (eteam.id = game.team1) WHERE coach = 'Fernando Santos'"},
    7: {"question":"List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'", "sql":"SELECT player FROM game JOIN goal ON id = matchid WHERE stadium = 'National Stadium, Warsaw'"},
    8: {"question":"Show the name of all players who scored a goal against Germany.", "sql":"SELECT DISTINCT player FROM game JOIN goal ON matchid = id WHERE (team1='GER' OR team2='GER') AND teamid != 'GER'"},
    9: {"question":"Show teamname and the total number of goals scored.", "sql":"SELECT teamname, COUNT(*) FROM goal JOIN eteam ON eteam.id = goal.teamid GROUP BY teamname"},
    10: {"question":"Show the stadium and the number of goals scored in each stadium.", "sql":"SELECT stadium, COUNT(*) FROM goal JOIN game ON matchid = id GROUP BY stadium"},
    11: {"question":"For every match involving 'POL', show the matchid, date and the number of goals scored.", "sql":"SELECT matchid,mdate, COUNT(teamid) FROM game JOIN goal ON matchid = id WHERE (team1 = 'POL' OR team2 = 'POL') GROUP BY gisq.goal.matchid, gisq.game.mdate"},
    12: {"question":"For every match where 'GER' scored, show matchid, match date and the number of goals scored by 'GER'", "sql":"SELECT matchid, mdate, COUNT(*) FROM goal JOIN game ON id = matchid WHERE (team1 = 'GER' OR team2 = 'GER') AND teamid = 'GER' GROUP BY matchid, gisq.game.mdate"},
    13: {"question":"List every match with the goals scored by each team as shown. This will use 'CASE WHEN' which has not been explained in any previous exercises.", "sql":"SELECT game.mdate, game.team1, SUM(CASE WHEN goal.teamid = game.team1 THEN 1 ELSE 0 END) AS score1,game.team2,SUM(CASE WHEN goal.teamid = game.team2 THEN 1 ELSE 0 END) AS score2 FROM game LEFT JOIN goal ON matchid = id GROUP BY game.id,game.mdate, game.team1, game.team2 ORDER BY mdate,matchid,team1,team2"}
}




#app is a variable used to create a FASTAPI instance
app = FastAPI()

@app.get("/")
async def root(request: Request):
    return {
        "Listing of all routes": request.url_for("routes"),
        "URL for 'world'": request.url_for("world"),
        "URL for ''world' with number 1-13": request.url_for("get_world_item_by_id", **{"world_id":1}),
        "URL for ''nobel'": request.url_for("nobel"),
        "URL for ''nobel' with number 1-14": request.url_for("get_nobel_item_by_id", **{"nobel_id":1}),
        "URL for ''select' with number 1-10": request.url_for("get_select_by_id", **{"select_id":1}),
        "URL for ''count' with number 1-8": request.url_for("get_count_by_id", **{"count_id":1}),
        "URL for ''join' with number 1-13": request.url_for("get_join_by_id", **{"join_id":1}),
    }

# @app.get("/routes/", response_class=HTMLResponse)
# async def all_routes():
#     sample= """
#         '<a href= /basics>basics</a>'
#         <a href= /basics/1>basics individual</a><br>
        
#     """
#     return HTMLResponse(content=sample, status_code=200)


@app.get("/routes/", name="routes")
async def route_names():
    get_routes = ['basics', 'world', 'nobel', 'within', 'count', 'joins', 'all']
    put_route = ['world']
    post_route = ['teacher']
    return {'GetRoutes': get_routes, 'PostRoute': post_route, 'PutRoute': put_route}
    


@app.get("/basic/{basic_id}")
async def get_basic(basic_id:int):
    question = basic_dict[basic_id]['question']
    query = basic_dict[basic_id]['sql']
    result = cnx.query(query)

    response = {
        "Question": question,
        "Query": query,
        "Results": result
    }

    return response


#Create deflaut decorator that return everything from the worlds table
@app.get("/world", name= "world")
async def get_world_item():
    sql = "SELECT * FROM world;"
    result = cnx.query(sql)
    
    return result   

#Use the GET method to return a json response with information from the worlds table
@app.get("/world/{world_id}")
async def get_world_item_by_id(world_id: int ):
    question = world_dict[world_id]['question']
    query = world_dict[world_id]['sql']
    result = cnx.query(query)
#Response is a dictionary made up of the QUESTION and QUERY from the world_dict variable and the queried information the worlds table
    response = {
        "Question": question,
        "Query": query,
        "Results": result
    }
    return response


#Defualt path decorator for the nobel route return everything from the nobel table
@app.get("/nobel/", name="nobel")
async def get_item():
    sql = "SELECT * FROM nobel;"
    result = cnx.query(sql)

    return result

#Use the GET method to return a json response with information from the nobel table
@app.get("/nobel/{nobel_id}")
async def get_nobel_item_by_id(nobel_id: int):
    question = nobel_dict[nobel_id]['question']
    query = nobel_dict[nobel_id]['sql']
    result = cnx.query(query)

#Response is a dictionary made up of the QUESTION and QUERY from the noble_dict variable and the queried information the worlds table
    response = {
        "Question": question,
        "Query": query,
        "Results":result
    }

    return response

#Use the GET method to return a json response with information from the select table
@app.get("/select/{select_id}")
async def get_select_by_id(select_id:int):
    question = select_dict[select_id]['question']
    query = select_dict[select_id]['sql']
    result = cnx.query(query)

    response = {
        "Question": question,
        "Query": query,
        "Results": result
    }

    return response


@app.get("/count/{count_id}")
async def get_count_by_id(count_id:int):
    question = count_dict[count_id]['question']
    query = count_dict[count_id]['sql']
    result = cnx.query(query)

    response = {
        "Question": question,
        "Query": query,
        "Results": result
    }

    return response


@app.get("/join/{join_id}")
async def get_join_by_id(join_id:int):
    question = join_dict[join_id]['question']
    query = join_dict[join_id]['sql']
    result = cnx.query(query)

    response = {
        "Question": question,
        "Query": query,
        "Results": result
    }

    return response

########POST routes

@app.post("/world/")
async def post_item(world_item: world_class):
    world_query = f"""
    INSERT INTO `world`(`name`, `continent`, `area`, `population`, `gdp`, `capital`, `tld`, `flag`) 
    VALUES ('{world_item.name}','{world_item.continent}','{world_item.area}','{world_item.population}','{world_item.gdp}','{world_item.capital}','{world_item.tld}','{world_item.flag}')
    """
    result = cnx.query(world_query)
    
    return result

####Adds new row into teachers table by using the teacher_class data model to create the query subset then use postman to insert the information
@app.post("/teacher/")
async def post_item(teacher_item: teacher_class):
    teacher_query = f"""
    INSERT INTO `teacher`(`id`, `dept`, `name`, `phone`, `mobile`) 
    VALUES ({teacher_item.id},{teacher_item.dept},'{teacher_item.name}','{teacher_item.phone}','{teacher_item.mobile}')
    """
    result = cnx.query(teacher_query)

    return result

# PUT route for worlds

@app.put("/world/")
async def update_world(world_item: world_class):
    sql = "UPDATE `world` SET "
    
    if world_item.name != None:
        sql += f"`name`=`{world_item.name}`, "
    
    if world_item.continent !=None: 
        sql += f"`continent`=`{world_item.continent}`, "
    
    if world_item.area !=None: 
        sql += f"`area`=`{world_item.area}`, "
    
    if world_item.population !=None: 
        sql += f"`population`=`{world_item.population}`, "

    if world_item.gdp != None: 
        sql += f"`gdp`= `{world_item.gdp}`, "
    
    if world_item.capital != None: 
        sql += f"`capital`=`{world_item.capital}`, "
    
    if world_item.tld != None: 
        sql += f"`tld`=`{world_item.tld}`, "

    if world_item.flag != None: 
        sql += f"`flag`=`{world_item.flag}` "

    sql+= "WHERE `name`=`Afghanistan"

   
    print(sql)
    res = cnx.query(sql)
    return res
    #return world_class

if __name__ == "__main__":
  uvicorn.run(app, host="143.244.188.178", port=8001, log_level="info")
