/*
    Name: Byron Dowling
    Class: 5303 Advanced Database Management
    Assignment: SQL Zoo queries

    Notes/Reminders
    * SELECT defines the table columns
    * '%some generic search term%' allows you to do partial name matching
    * OR works exactly how you would think
*/


-- SELECT Basics
-- https://sqlzoo.net/wiki/SELECT_basics


-- #1
-- The example uses a WHERE clause to show the population of 'France'. Note that strings (pieces of text that are data) should be in 'single quotes';
-- Modify it to show the population of Germany
SELECT population FROM world
WHERE name = 'Germany'

-- #2
-- Checking a list The word IN allows us to check if an item is in a list. The example shows the name and population for the countries 'Brazil', 'Russia', 'India' and 'China'.
-- Show the name and the population for 'Sweden', 'Norway' and 'Denmark'.
SELECT name, population FROM world
WHERE name IN ('Sweden', 'Norway', 'Denmark');

-- #3
-- Which countries are not too small and not too big? BETWEEN allows range checking (range specified is inclusive of boundary values). 
-- The example below shows countries with an area of 250,000-300,000 sq. km. 
-- Modify it to show the country and the area for countries with an area between 200,000 and 250,000.
SELECT name, area FROM world
WHERE area BETWEEN 200000 AND 250000



-- SELECT from WORLD Tutorials
--https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial


-- #1
-- Observe the result of running this SQL command to show the name, continent and population of all countries.
SELECT name, continenet, population FROM world

-- #2
-- Show the name for the countries that have a population of at least 200 million. 200 million is 200000000, there are eight zeros.
SELECT name FROM world
WHERE population = 64105700

-- #3
-- Give the name and the per capita GDP for those countries with a population of at least 200 million.
SELECT name, GDP/population FROM world
WHERE population > 200000000

-- #4
-- Show the name and population in millions for the countries of the continent 'South America'. Divide the population by 1000000 to get population in millions.
SELECT name, population/1000000 FROM world
WHERE continent = 'South America'

-- #5
-- Show the name and population for France, Germany, Italy
SELECT name, population FROM world
WHERE name in ('France', 'Germany', 'Italy')

-- #6
-- Show the countries which have a name that includes the word 'United'
SELECT name FROM world
WHERE name LIKE '%united%'

-- #7
-- Two ways to be big: A country is big if it has an area of more than 3 million sq km or it has a population of more than 250 million.
-- Show the countries that are big by area or big by population. Show name, population and area.
SELECT name, population, area FROM world
WHERE area > 3000000 OR population > 250000000

-- #8
-- Exclusive OR (XOR). Show the countries that are big by area (more than 3 million) or big by population (more than 250 million) but not both. Show name, population and area.
-- Australia has a big area but a small population, it should be included.
-- Indonesia has a big population but a small area, it should be included.
-- China has a big population and big area, it should be excluded.
-- United Kingdom has a small population and a small area, it should be excluded.
SELECT name, population, area FROM world
WHERE (area > 3000000 AND population < 250000000)
OR (area < 3000000 AND population > 250000000)

-- #9
-- Show the name and population in millions and the GDP in billions for the countries of the continent 'South America'. 
-- Use the ROUND function to show the values to two decimal places.
-- For South America show population in millions and GDP in billions both to 2 decimal places.
SELECT name, ROUND(population/1000000,2), ROUND(gdp/1000000000,2) FROM world
WHERE continent = 'South America'

-- #10
-- Show the name and per-capita GDP for those countries with a GDP of at least one trillion (1000000000000; that is 12 zeros). Round this value to the nearest 1000.
-- Show per-capita GDP for the trillion dollar countries to the nearest $1000.
SELECT name, ROUND(gdp/population, -3) FROM world
WHERE gdp > 1000000000000

-- #11
-- Greece has capital Athens.
-- Each of the strings 'Greece', and 'Athens' has 6 characters.
-- Show the name and capital where the name and the capital have the same number of characters.
-- You can use the LENGTH function to find the number of characters in a string
SELECT name, capital FROM world
WHERE LENGTH(capital) = LENGTH(name)

-- #12
-- The capital of Sweden is Stockholm. Both words start with the letter 'S'.
-- Show the name and the capital where the first letters of each match. Don't include countries where the name and the capital are the same word.
-- You can use the function LEFT to isolate the first character.
-- You can use <> as the NOT EQUALS operator.
SELECT name, capital FROM world
WHERE LEFT(name,1) = LEFT(capital,1) AND name <> capital

-- #13
-- Equatorial Guinea and Dominican Republic have all of the vowels (a e i o u) in the name. They don't count because they have more than one word in the name.
-- Find the country that has all the vowels and no spaces in its name.
-- You can use the phrase name NOT LIKE '%a%' to exclude characters from your results.
-- The query shown misses countries like Bahamas and Belarus because they contain at least one 'a'
SELECT name FROM world 
WHERE name LIKE '%A%' AND name LIKE '%E%' AND name LIKE '%I%' AND name LIKE '%O%' AND name LIKE '%U%' AND name NOT LIKE '% %'



-- SELECT from Nobel Tutorial
-- https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial


-- #1
-- Change the query shown so that it displays Nobel prizes for 1950.
SELECT yr, subject, winner FROM nobel
WHERE yr = 1950

-- #2
-- Show who won the 1962 prize for Literature
SELECT winner FROM nobel
WHERE yr = 1962 AND subject = 'Literature'

-- #3
-- Show the year and subject that won 'Albert Einstein' his prize.
SELECT yr, subject FROM nobel
WHERE winner = 'Albert Einstein'

-- #4
-- Give the name of the 'Peace' winners since the year 2000, including 2000.
SELECT winner FROM nobel
WHERE yr >= 2000 AND subject = 'Peace'

-- #5
-- Show all details (yr, subject, winner) of the Literature prize winners for 1980 to 1989 inclusive.
SELECT yr, subject, winner FROM nobel
WHERE yr >= 1980 AND yr <= 1989 AND subject = 'Literature'

-- #6
-- Show all details of the presidential winners:
        -- Theodore Roosevelt
        -- Woodrow Wilson
        -- Jimmy Carter
        -- Barack Obama
SELECT * FROM nobel
WHERE winner IN ('Theodore Roosevelt',
                  'Woodrow Wilson',
                  'Jimmy Carter', 
                  'Barack Obama')

-- #7
-- Show the winner with first name John
-- ***Notice the lack of first parentheses that inidcates string must start with John***
SELECT winner FROM nobel
WHERE winner LIKE 'John%'

-- #8
-- Show the year, subject, and name of Physics winners for 1980 together with the Chemistry winners for 1984.
SELECT yr, subject, winner FROM nobel
WHERE (yr = 1980 AND subject = 'Physics')
OR (yr = 1984 AND subject = 'Chemistry')

-- #9
-- Show the year, subject, and name of winners for 1980 excluding Chemistry and Medicine
SELECT yr, subject, winner FROM nobel
WHERE yr = 1980 AND subject != 'Chemistry' AND subject != 'Medicine'

-- #10
-- Show year, subject, and name of people who won a 'Medicine' prize in an early year 
-- (before 1910, not including 1910) together with winners of a 'Literature' prize in a later year (after 2004, including 2004)
SELECT yr, subject, winner FROM nobel
WHERE (subject = 'Medicine' AND yr < 1910)
OR (subject = 'Literature' AND yr >= 2004)

-- #11
-- Find all details of the prize won by PETER GRÜNBERG
-- Handling non-ascii umlaut
SELECT * FROM nobel
WHERE winner LIKE 'PETER GR%NBERG'

-- #12
-- Find all details of the prize won by EUGENE O'NEILL
-- Escaping single quotes
SELECT * FROM nobel
WHERE winner LIKE 'EUGENE O%NEILL'

-- #13
-- Knights in order
-- List the winners, year and subject where the winner starts with Sir. 
-- Show the the most recent first, then by name order.
-- DESC = order in Descending order
SELECT winner, yr, subject FROM nobel
WHERE winner LIKE 'Sir%'
ORDER BY yr DESC, winner

-- #14
-- The expression subject IN ('Chemistry','Physics') can be used as a value - it will be 0 or 1.
-- Show the 1984 winners and subject ordered by subject and winner name; but list Chemistry and Physics last.
SELECT winner, subject
FROM nobel
WHERE yr = 1984
ORDER BY subject IN ('Physics', 'Chemistry'), subject, winner



-- SELECT within SELECT SQL Zoo Tutorials
-- https://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial

-- #1
-- List each country name where the population is larger than that of 'Russia'.
SELECT name FROM world
WHERE population > (SELECT population FROM world WHERE name = 'Russia')

-- #2
-- Show the countries in Europe with a per capita GDP greater than 'United Kingdom'.
SELECT name
FROM world
WHERE gdp/population >
    (SELECT gdp/population FROM world WHERE name = 'United Kingdom') AND continent = 'Europe'

-- #3
-- List the name and continent of countries in the continents containing either Argentina or Australia. 
-- Order by name of the country.
SELECT name, continent
FROM world
WHERE continent IN (SELECT continent FROM world WHERE name IN ('Argentina', 'Australia'))
ORDER BY name

-- #4
-- Which country has a population that is more than Canada but less than Poland? Show the name and the population.
SELECT name, population
FROM world
WHERE population >
    (SELECT population FROM world WHERE name = 'Canada')
AND population <
    (SELECT population FROM world WHERE name = 'Poland')

-- #5
-- Germany (population 80 million) has the largest population of the countries in Europe. Austria (population 8.5 million) has 11% of the population of Germany.
-- Show the name and the population of each country in Europe. Show the population as a percentage of the population of Germany.
-- The format should be Name, Percentage for example:
SELECT name, CONCAT(ROUND(population /(SELECT population FROM world WHERE name = 'Germany') * 100, 0), '%')
FROM world
WHERE continent = 'Europe'

-- #6
-- Which countries have a GDP greater than every country in Europe? 
-- [Give the name only.] 
-- (Some countries may have NULL gdp values)
SELECT name FROM world
WHERE gdp >= ALL(SELECT gdp FROM world WHERE gdp >=0 AND continent = 'Europe') AND continent != 'Europe'

-- #7
-- Find the largest country (by area) in each continent, show the continent, the name and the area:
SELECT continent, name, area FROM world x
  WHERE area >= ALL
    (SELECT area FROM world y
        WHERE y.continent = x.continent
          AND area > 0)

-- #8
-- List each continent and the name of the country that comes first alphabetically.
SELECT continent, name FROM world x
WHERE name <= ALL(SELECT name FROM world y WHERE y.continent = x.continent)

-- #9
-- Find the continents where all countries have a population <= 25000000. 
-- Then find the names of the countries associated with these continents. 
-- Show name, continent and population.
SELECT name, continent, population FROM world x
WHERE 25000000  > ALL(SELECT population FROM world y WHERE x.continent = y.continent AND y.population > 0)

-- #10
-- Some countries have populations more than three times that of any of their neighbours (in the same continent). 
-- Give the countries and continents.
SELECT name, continent FROM world x
WHERE population > ALL(SELECT population*3 FROM world y WHERE x.continent = y.continent AND population > 0 AND y.name != x.name)



-- SUM and COUNT tutorials
-- https://sqlzoo.net/wiki/SUM_and_COUNT

-- #1
-- Show the total population of the world.
SELECT SUM(population)
FROM world

-- #2
-- List all the continents - just once each.
SELECT DISTINCT(continent) FROM world

-- #3
-- Give the total sum GDP of Africa
SELECT SUM(gdp) FROM world
WHERE continent = 'Africa'

-- #4
-- How many countries have an area of at least 1000000
SELECT COUNT(name) FROM world
WHERE area >= 1000000

-- #5
-- What is the total population of ('Estonia', 'Latvia', 'Lithuania')
SELECT SUM(population) FROM world
WHERE name = 'Estonia' OR name = 'Latvia' OR name = 'Lithuania'

-- #6
-- For each continent show the continent and number of countries.
SELECT continent, COUNT(name) FROM world
GROUP BY continent

-- #7
-- For each continent show the continent and number of countries with populations of at least 10 million.
SELECT continent, COUNT(name) FROM world
WHERE population >= 10000000
GROUP BY continent

-- #8
-- List the continents that have a total population of at least 100 million.
SELECT continent FROM world
GROUP BY continent HAVING SUM(population) > 100000000


-- JOIN Operation Tutorial
-- https://sqlzoo.net/wiki/The_JOIN_operation

-- #1
-- The first example shows the goal scored by a player with the last name 'Bender'. The * says to list all the columns in the table - a shorter way of saying matchid, teamid, player, gtime
-- Modify it to show the matchid and player name for all goals scored by Germany. 
-- To identify German players, check for: teamid = 'GER'
SELECT matchid, player FROM goal 
WHERE teamid = 'GER'

-- #2
-- From the previous query you can see that Lars Bender's scored a goal in game 1012. Now we want to know what teams were playing in that match.
-- Notice in the that the column matchid in the goal table corresponds to the id column in the game table. We can look up information about game 1012 by finding that row in the game table.
-- Show id, stadium, team1, team2 for just game 1012
SELECT id,stadium,team1,team2 FROM game
WHERE id = 1012

-- #3
-- You can combine the two steps into a single query with a JOIN.
-- SELECT * FROM game JOIN goal ON (id=matchid)
-- The FROM clause says to merge data from the goal table with that from the game table. 
-- The ON says how to figure out which rows in game go with which rows in goal - the matchid from goal must match id from game. 
-- (If we wanted to be more clear/specific we could say ON (game.id=goal.matchid)
-- The code below shows the player (from the goal) and stadium name (from the game table) for every goal scored.
-- Modify it to show the player, teamid, stadium and mdate for every German goal.
SELECT player, teamid, stadium, mdate FROM game
JOIN goal ON (id=matchid AND teamid='GER')

-- #4
-- Use the same JOIN as in the previous question.
-- Show the team1, team2 and player for every goal scored by a player called Mario player LIKE 'Mario%'
SELECT team1, team2, player FROM game
JOIN goal ON (id=matchid AND player LIKE 'Mario%')

-- #5
-- The table eteam gives details of every national team including the coach. 
-- You can JOIN goal to eteam using the phrase goal JOIN eteam on teamid=id
-- Show player, teamid, coach, gtime for all goals scored in the first 10 minutes gtime<=10
SELECT player, teamid, coach, gtime FROM goal
JOIN eteam ON (teamid=id AND gtime <= 10)

-- #6
-- To JOIN game with eteam you could use either game JOIN eteam ON (team1=eteam.id) or game JOIN eteam ON (team2=eteam.id)
-- Notice that because id is a column name in both game and eteam you must specify eteam.id instead of just id
-- List the dates of the matches and the name of the team in which 'Fernando Santos' was the team1 coach.
SELECT mdate, teamname FROM game
JOIN eteam ON (team1=eteam.id AND coach LIKE '%Santos')

-- #7
-- List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'
SELECT player FROM goal
JOIN game ON (id=matchid AND stadium = 'National Stadium, Warsaw')

-- #8
-- The example query shows all goals scored in the Germany-Greece quarterfinal.
-- Instead show the name of all players who scored a goal against Germany.
SELECT DISTINCT(player) FROM game
JOIN goal ON matchid = id
WHERE ((team1='GER' OR team2='GER') AND teamid != 'GER')

-- #9
-- Show teamname and the total number of goals scored.
-- COUNT and GROUP BY
SELECT teamname, COUNT(player) FROM eteam
JOIN goal ON id=teamid
GROUP BY teamname

-- #10
-- Show the stadium and the number of goals scored in each stadium.
SELECT stadium, COUNT(player) AS goals FROM game
JOIN goal ON (id=matchid)
GROUP BY stadium

-- #11
-- For every match involving 'POL', show the matchid, date and the number of goals scored.
SELECT matchid, mdate, COUNT(player) AS goals FROM game
JOIN goal ON (matchid=id AND (team1 = 'POL' OR team2 = 'POL'))
GROUP BY matchid, mdate

-- #12
-- For every match where 'GER' scored, show matchid, match date and the number of goals scored by 'GER'
SELECT id, mdate, COUNT(player) FROM game
JOIN goal ON (id=matchid AND (team1 = 'GER' OR team2 = 'GER') AND teamid='GER')
GROUP BY id, mdate

-- #13
-- List every match with the goals scored by each team as shown. This will use "CASE WHEN" which has not been explained in any previous exercises.
-- mdate	team1	score1	team2	score2
-- 1 July 2012	ESP	4	ITA	0
-- 10 June 2012	ESP	1	ITA	1
-- 10 June 2012	IRL	1	CRO	3
-- Notice in the query given every goal is listed. If it was a team1 goal then a 1 appears in score1, otherwise there is a 0. 
-- You could SUM this column to get a count of the goals scored by team1. Sort your result by mdate, matchid, team1 and team2.
SELECT mdate,
       team1,
       SUM(CASE WHEN teamid = team1 THEN 1 ELSE 0 END) AS score1,
       team2,
       SUM(CASE WHEN teamid = team2 THEN 1 ELSE 0 END) AS score2 FROM
    game LEFT JOIN goal ON (id = matchid)
    GROUP BY mdate,team1,team2
    ORDER BY mdate, matchid, team1, team2