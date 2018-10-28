# LogAnalysis
Log Analysis Project for Udacity Full Stack Program.


# Requirement
You are provided with a dump of News agency DB, You have to create a report which serves the following purpose.

1. Which articles are the topmost three articles in term of popularity.
2. Which authors have the most viewed articles.
3. On which days did more than 1% of requests lead to errors.


Your Output should be dumped in a output.txt to see expected output after running LogsAnalysisService.py.

# Setup
Software
Make sure the software listed beneath is installed on your computer. You can use latest versions also.

Python 3.6.x

PostgreSQL 9.5.x

# Test data
Download and unzip https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip. Build the database by running psql -d news -f newsdata.sql

# Views
A database view allows you to simplify complex queries: a database view is defined by an SQL statement that associates with many underlying tables. You can use database view to hide the complexity of underlying tables to the end-users and external applications.

In Order to create the views. First run : 
psql -d news
Then start loading the views by running the commands listed under.

# View Created
There is only one view create in order to see the Percentage of error.
View Creation Command.

  create view error_percent_log_view 
  as select date(time),round(100.0*sum(case log.status when '200 OK' 
  then 0 else 1 end)/count(log.status),2) as "error_percent" from log group by date(time) 
  order by "error_percent" desc;


# How to run the application

Using command prompt
1. Navigate to the project Folder of Log Analysis Project.
2. Check the content of the Folder (Run 'ls' in case of linux and 'dir' in case of windows).
3. Make sure you have file LogsAnalysisService.py in the directory.
3. Check your python environment and run python/python3(In case of python 3).

Run the application
Type

python LogsAnalysisService.py



