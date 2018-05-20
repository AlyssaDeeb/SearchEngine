import mysql.connector
import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
import re


def query_index(cursor, terms, limit=10):

    query = ("SELECT  d.name, d.url FROM doc d INNER JOIN term_in_doc td on d.id = td.doc_id INNER JOIN term t on t.id = td.term_id WHERE t.name = %s LIMIT %s")
    cursor.execute(query,(terms,limit))

    for (id, url) in cursor:
        print url

    if cursor.rowcount == -1:
        print "No results found"

    print ""


def driver():
    print "Initializing Gago Search..."

    connection = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='searchEngine')

    if not (connection.is_connected()):
        print "Connection Fails"
        return

    cursor = connection.cursor()

    while 1:
        query_string = raw_input("Search term: ").lower()
        query_index(cursor, query_string)


driver()