
import psycopg2 as psy

# Class to Analyse the Logs, There are three queries which serves the purpose, Queries are written
# first to get the basic idea what they are doing and later on used in functions, If there is any change required
# it can be directly done in the queries rather than going in different files.
# Functionality is divided into different functions , which are referring the query String, and there is a util function
# where we connect the DB, then fetch all rows corresponding to query then display them with proper formatting.

#Database Name
DBNAME = "news"

# Util Function to open and close the connection of DB.Take Sql_Request as param and execute it.
def query_database(sql_request):
    conn = psy.connect(database=DBNAME)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    results = cursor.fetchall()
    conn.close()
    return results


# A Util Function to Format the Title
def print_title(title):
    print ("\n\t\t\t" + "#"*30 + " "+title + "#"*30+ "\n")


# Query to get the Most popular articles of all the time. 
# Replace function is used to get the name of articles from Log.
query_articles = """select articles.title as most_popular_articles, count(*) as view_count
            from log, articles
            where log.status='200 OK'
            and articles.slug = REPLACE(log.path,'/article/','')
            group by articles.title
            order by view_count desc
            limit 3;"""


# Function to GET the Popular three articles of all time
def popular_articles():
    print_title("Most Popular articles of all time, Top 3 are ")

    for most_popular_articles, view_count in query_database(query_articles):
        print(" \"{}\" Article has {} View Count".format(most_popular_articles, view_count))


# Query to get the most popular authors of all time. Sorted by desc , means from most popular to least.
# log.status='200 OK' is added in condition to count only successful views. Can be refined or changed.
query_authors = """select authors.name as most_popular_authors, count(*) as view_count
            from articles, authors, log
            where log.status='200 OK'
            and authors.id = articles.author
            and articles.slug = REPLACE(log.path,'/article/','')
            group by authors.name
            order by view_count desc;
            """
            
#  Function to GET the top authors of all time
def popular_authors():
    print_title("Most Popular authors of all time")

    for most_popular_authors, view_count in query_database(query_authors):
        print(" Author \"{}\" has {} Popularity Votes".format(most_popular_authors, view_count))

# Query to get the errors from error_percent_log_view to get the error percent more than one. 
# View is created to get the percentage Errors more than one. 
query_errors = """select date, error_percent
                from error_percent_log_view
                where error_percent > 1;
            """

# Function to see days with Failed Request more than one Percent.
def bad_request_days():
    print_title("Days with more than one percentage of bad requests")
#Loop in result and print the result
    for day, percentagefailed in query_database(query_errors):
        print(""" On  {0:%d - %B - %Y} there are  {1:.2f} % Bad Requests""".format(day, percentagefailed))

# Main Function where execution starts.
if __name__ == '__main__':
    popular_articles()
    popular_authors()
    bad_request_days()