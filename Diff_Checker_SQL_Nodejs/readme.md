# NodeJS replace for Sqlite3
Welcome!
This is an utility script used in the process of comparing two tables in a db with the same columns but with different values. In order to use the JOIN operator you'll need one column with the same data between to match two tables and this script does that with the value of the column containing the URL. 

It replace one value for other in a column for the whole table, that's it. 

It's pretty useful when you have two different URLs (i.e. production URLs vs staging URLs) and you need to compare some data.

There are different ways to compare two versions of the same site, custom scripts using any programming language, excel, sheets or using SQL. This NodeJS utility will help you matching one column of two tables in order to be able to compare the data from two tables.

## Use cases
When you submit a change to your site you can deploy a bug without knowking it breaking specific pages and it's always a good practice to do healthy checks (not onlye for SEO puposes). 

Below you'll find some of the most common use cases:
* Web migrations
* Changing mobile configuration (as a content parity checker)
* Adding AMP version
* Modifying the front-end of your application
* For QA purposes

## Installation & depencies
This is an utility so you'll need some extra things in order to use this utility.

First, download the repo and adapt it to your needs. 

In the `index.js` you'll find different variables that need to be adapted:
```js
  const dbPath = '../databaseName.db'; // Adapt

  const tableName = `"tableName"`; // Adapt

  volatileURL
  .replace('volatile-url-to-replace', '') // Adapt
  .replace('http://', 'https://') // Adapt
```
You'll need to change the name of the database, the table where you want to change the data using THIS utility script & the urls with the changed applied (I usually work with volatile URLs).

Second, install Sqlite3 & the SQL Client
* Install [Sqlite3](https://www.sqlite.org/download.html)
* Install [SQL Client](https://sqlitebrowser.org/)

## How it works
The process used to verify that everything is okay:
1. Install dependencies & adapt it to your needs
2. Crawl the legacy site & the new version (repo adapted to [Screaming Frog](https://www.screamingfrog.co.uk/seo-spider/)) & export the output in CSV
3. Create a database using your command line: ```sqlite3 databaseName.db```
4. Import the CSV into SQL tables using the SQL Client
5. Execute the script ```node index.js```
6. Run the queries in the SQL Client

## Promisified methods
Just for informational purposes, this repo promisified the callback methods from sqlite3 package in `db.js`.
More info [here](https://github.com/JoshuaWise/better-sqlite3/issues/262)

## Example queries
Here you'll find some useful queries to compare data with some SEO purposes:

### Check different status code
Query to extract which URLs have different status code between two versions.
```sql
  SELECT 
    p.Address,
    p.StatusCode AS StatusCodeProd,
    v2.StatusCode AS StatusCodeVolatile
  FROM "production" AS p
  LEFT JOIN   "volatile" as v 
    ON p.Address = v.canonURL 
    AND coalesce( p.StatusCode, "N/A") = coalesce(v.StatusCode, "N/A")
  LEFT JOIN  "volatile" as v2 
      on v2.canonURL = p.Address
  WHERE 
    v.canonURL IS NULL
```

### Check different titles
Query to extract which URLs have different titles between two versions.
```sql
  SELECT 
    p.Address,
    v2.Address,
    p.Title1 AS Prod,
    v2.Title1 AS Volatile
  FROM "production" AS p
  LEFT JOIN   "volatile" as v 
    ON p.Address = v.canonURL 
    AND coalesce( p.StatusCode, "N/A") = coalesce(v.StatusCode, "N/A")
    AND p.Title1 = v.Title1
    
  LEFT JOIN  "volatile" as v2 
      on v2.canonURL = p.Address
  WHERE 
    v.Title1 IS NULL
    AND v2.StatusCode = 200
```