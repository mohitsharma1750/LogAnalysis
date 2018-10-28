
import psycopg2 as psy

#Database Name

DBNAME = "news"

# Database queries. Most Popular article, Most popular Authors and Error Percent respectively.


# Query to get the Most popular articles of all the time. 
# Replace function is used to get the name of articles from Log.
query_articles = """select articles.title as most_popular_articles, count(*) as view_count
            from log, articles
            where log.status='200 OK'
            and articles.slug = REPLACE(log.path,'/article/','')
            group by articles.title
            order by view_count desc
            limit 3;"""

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

# Query to get the errors from error_percent_log_view to get the error percent more than one. 
# View is created to get the percentage Errors more than one. 
query_errors = """select date, error_percent
                from error_percent_log_view
                where error_percent > 1;
            """


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


# Function to GET the Popular three articles of all time
def popular_articles():
    top_three_articles = query_database(query_articles)
    print_title("Most Popular articles of all time, Top 3 are ")

    for most_popular_articles, view_count in top_three_articles:
        print(" \"{}\" Article has {} View Count".format(most_popular_articles, view_count))


#  Function to GET the top authors of all time
def popular_authors():
    top_authors = query_database(query_authors)
    print_title("Most Popular authors of all time")

    for most_popular_authors, view_count in top_authors:
        print(" Author \"{}\" has {} Popularity Votes".format(most_popular_authors, view_count))


# Function to see days with Failed Request more than one Percent.
def bad_request_days():
    error_request= query_database(query_errors)
    print_title("Days with more than one percentage of bad requests")
#Loop in result and print the result
    for day, percentagefailed in error_request:
        print("""{0:%B %d, %Y} -- {1:.2f} % Bad Requests""".format(day, percentagefailed))

# Main Function where execution starts.
if __name__ == '__main__':
    popular_articles()
    popular_authors()
    bad_request_days()