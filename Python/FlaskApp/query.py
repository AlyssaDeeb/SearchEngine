import nltk
import re
from nltk.corpus import stopwords
import mysql.connector
import textwrap

nltk.download('stopwords')
alphanumeric = re.compile('[^a-zA-Z0-9\'-]+')


def clean_input():
    raw_query = raw_input("Enter Query: ")
    cleaned_query_list = []

    for token in raw_query.split(' '):
        clean_token = alphanumeric.sub('', token.lower().strip())

        if clean_token and \
                clean_token not in stopwords.words("english"):
            cleaned_query_list.append(clean_token)

    return cleaned_query_list

def clean_input_NoPrompt(terms):
    cleaned_query_list = []

    for token in terms.split(' '):
        clean_token = alphanumeric.sub('', token.lower().strip())

        if clean_token and \
                clean_token not in stopwords.words("english"):
            cleaned_query_list.append(clean_token)

    return cleaned_query_list


def andQuery(cursor, terms, limit=20):
    numberTerms = len(terms)
    currentNumber = 0
    results = []

    if numberTerms < 1:
        return "No Results Found"

    query = "SELECT doc.name, doc.url FROM doc WHERE doc.id IN( SELECT DISTINCT term_in_doc.doc_id FROM term_in_doc, term WHERE term.name = %s AND term_in_doc.term_id = term.id ORDER BY `weighted_tf-idf` DESC) "

    currentNumber += 1

    while currentNumber < numberTerms:
        query += " AND doc.id IN (SELECT DISTINCT term_in_doc.doc_id FROM term_in_doc, term WHERE term.name = %s AND term_in_doc.term_id = term.id ORDER BY `weighted_tf-idf` DESC)"
        currentNumber += 1

    query += "LIMIT " + str(limit)
    cursor.execute(query, terms)

    for link in cursor:
        results.append(link)


    if cursor.rowcount == -1:
        print "No results found"

    print ""
    return results

def orQuery(cursor, terms, limit=20):
    numberTerms = len(terms)
    currentNumber = 0
    results = []

    if numberTerms < 1:
        return "No Results Found"

    query = "SELECT d.name, d.url FROM doc d INNER JOIN term_in_doc td on d.id = td.doc_id INNER JOIN term t on t.id = td.term_id WHERE t.name = %s"
    currentNumber += 1

    while currentNumber < numberTerms:
        query += "OR t.name = %s"
        currentNumber += 1

    query += "order by `weighted_tf-idf` desc LIMIT " + str(limit)
    cursor.execute(query, terms)

    for link in cursor:
        results.append(link)

    if cursor.rowcount == -1:
        print "No results found"

    print ""
    return results


def webDriver(searchInput):

    print searchInput
    if not searchInput:
        print "uh oh"
    connection = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='searchEngine')

    if not (connection.is_connected()):
        print "Connection Fails"
        return

    cursor = connection.cursor()

    results = []
    query_terms = clean_input_NoPrompt(searchInput)

    results = andQuery(cursor, query_terms)

    if len(results) > 20:
        results += orQuery(cursor, query_terms)

    #for name, url in results:
    #    print url
    connection.close()
    return results

def driver():
    print "Initializing Gago Search..."

    connection = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='searchEngine')

    if not (connection.is_connected()):
        print "Connection Fails"
        return

    cursor = connection.cursor()

    while 1:
        results = []
        query_terms = clean_input()

        results = andQuery(cursor, query_terms)

        if len(results > 20):
            results += orQuery(cursor, query_terms)

        for name, url in results:
            print url

#driver()