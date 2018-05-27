import nltk
import re
from nltk.corpus import stopwords
import mysql.connector
from collections import defaultdict

nltk.download('stopwords')
alphanumeric = re.compile('[^a-zA-Z0-9\'-]+')

"""
Prompts the user for a query and results the tokens of the user input
"""
def clean_input():
    raw_query = raw_input("Enter Query: ")
    cleaned_query_list = []

    for token in raw_query.split(' '):
        clean_token = alphanumeric.sub('', token.lower().strip())

        if clean_token and \
                clean_token not in stopwords.words("english"):
            cleaned_query_list.append(clean_token)

    return cleaned_query_list


"""
Takes the input query and tokenizes the query into terms and removes stopwords
"""
def clean_input_NoPrompt(terms):
    cleaned_query_list = []

    for token in terms.split(' '):
        clean_token = alphanumeric.sub('', token.lower().strip())

        if clean_token and \
                clean_token not in stopwords.words("english"):
            cleaned_query_list.append(clean_token)

    return cleaned_query_list


"""
Queries database for AND query with weighted results
"""
def weightedAndQuery(cursor, terms, limit):
    numberTerms = len(terms)
    currentNumber = 0
    results = []

    if numberTerms < 1:
        return "No Results Found"

    query = "SELECT doc.name, doc.url FROM doc WHERE doc.id IN( SELECT DISTINCT term_in_doc.doc_id FROM term_in_doc, term WHERE term.name = %s AND term_in_doc.term_id = term.id) "

    currentNumber += 1

    while currentNumber < numberTerms:
        query += " AND doc.id IN (SELECT DISTINCT term_in_doc.doc_id FROM term_in_doc, term WHERE term.name = %s AND term_in_doc.term_id = term.id)"
        currentNumber += 1

    currentNumber = 0

    query += "ORDER BY ((SELECT `weighted_tf-idf` from term_in_doc, term WHERE doc_id = doc.id AND term.name = %s AND term_in_doc.term_id = term.id)"

    currentNumber += 1

    while currentNumber < numberTerms:
        query += " + (SELECT `weighted_tf-idf` from term_in_doc, term WHERE doc_id = doc.id AND term.name = %s AND term_in_doc.term_id = term.id)"
        currentNumber += 1

    query += ") DESC "
    query += "LIMIT " + str(limit)
    cursor.execute(query, terms + terms)

    for link in cursor:
        results.append(link)


    if cursor.rowcount == -1:
        print "No results found"

    print ""
    return results


"""
Queries database for OR query with weighted results
"""
def weightedOrQuery(cursor, terms, limit):
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


"""
Queries database for AND query with regular tf-idf results
"""
def andQuery(cursor, terms, limit):
    numberTerms = len(terms)
    currentNumber = 0
    results = []

    if numberTerms < 1:
        return "No Results Found"

    query = "SELECT doc.name, doc.url FROM doc WHERE doc.id IN( SELECT DISTINCT term_in_doc.doc_id FROM term_in_doc, term WHERE term.name = %s AND term_in_doc.term_id = term.id) "

    currentNumber += 1

    while currentNumber < numberTerms:
        query += " AND doc.id IN (SELECT DISTINCT term_in_doc.doc_id FROM term_in_doc, term WHERE term.name = %s AND term_in_doc.term_id = term.id)"
        currentNumber += 1

    currentNumber = 0

    query += "ORDER BY ((SELECT `weighted_tf-idf` from term_in_doc, term WHERE doc_id = doc.id AND term.name = %s AND term_in_doc.term_id = term.id)"

    currentNumber += 1

    while currentNumber < numberTerms:
        query += " + (SELECT `weighted_tf-idf` from term_in_doc, term WHERE doc_id = doc.id AND term.name = %s AND term_in_doc.term_id = term.id)"
        currentNumber += 1

    query += ") DESC "
    query += "LIMIT " + str(limit)
    cursor.execute(query, terms + terms)

    for link in cursor:
        results.append(link)

    if cursor.rowcount == -1:
        print "No results found"

    return results


"""
Queries database for OR query with regular tf-idf results
"""
def orQuery(cursor, terms, limit):
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

    query += "order by `tf-idf` desc LIMIT " + str(limit)
    cursor.execute(query, terms)

    for link in cursor:
        results.append(link)

    if cursor.rowcount == -1:
        print "No results found"

    return results


"""
Given search input, returns list of weighted results
"""
def weighted_tf_idf_Results(searchInput):

    print searchInput
    if not searchInput:
        print "uh oh"
    connection = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='searchEngine')

    if not (connection.is_connected()):
        print "Connection Fails"
        return

    cursor = connection.cursor()

    results = []
    limit = 20

    if "k=" in searchInput:
        limitIndex = searchInput.index("k=")
        print limitIndex
        limit = int(searchInput[limitIndex + 2:])
        searchInput = searchInput[:limitIndex]

    query_terms = clean_input_NoPrompt(searchInput)

    results = weightedAndQuery(cursor, query_terms, limit)

    if len(results) < limit:
        otherResults = weightedOrQuery(cursor, query_terms, limit - len(results))
        for newResult in otherResults:
            if newResult not in results:
                results += newResult

    connection.close()
    return results


"""
Given search input, returns list of regular tf-idf results
"""
def tf_idf_Results(searchInput):

    print searchInput
    if not searchInput:
        print "uh oh"
    connection = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='searchEngine')

    if not (connection.is_connected()):
        print "Connection Fails"
        return

    cursor = connection.cursor()

    results = []
    limit = 20

    if "k=" in searchInput:
        limitIndex = searchInput.index("k=")
        limit = int(searchInput[limitIndex + 2:])
        searchInput = searchInput[ :limitIndex]


    query_terms = clean_input_NoPrompt(searchInput)

    results = andQuery(cursor, query_terms, limit)

    if len(results) < limit:
        otherResults = weightedOrQuery(cursor, query_terms, limit - len(results))
        for newResult in otherResults:
            if newResult not in results:
                results += newResult

    connection.close()
    return results

"""
Given search input, returns list of weighted results with the lowest minimum window size
"""
def position_Results(searchInput):

    print searchInput
    if not searchInput:
        print "uh oh"
    connection = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='searchEngine')

    if not (connection.is_connected()):
        print "Connection Fails"
        return

    cursor = connection.cursor()

    results = []
    limit = 20

    if "k=" in searchInput:
        limitIndex = searchInput.index("k=")
        print limitIndex
        limit = int(searchInput[limitIndex + 2:])
        searchInput = searchInput[:limitIndex]

    query_terms = clean_input_NoPrompt(searchInput)

    limit *= 10

    results = weightedAndQuery(cursor, query_terms, limit)

    if len(results) < limit:
        otherResults = weightedOrQuery(cursor, query_terms, limit - len(results))
        for newResult in otherResults:
            if newResult not in results:
                results += newResult

    positionWindowDict = defaultdict(int)
    resultsDict = defaultdict(str)

    for name, url in results:
        resultsDict[name] = url
        positionWindowDict[name] = getMinWindow(cursor, query_terms, name)

    limit /= 10
    currentIndex = 0
    positionResults = []
    for key, value in sorted(positionWindowDict.items(), key=lambda(k,v): v):

        if currentIndex < limit:
            positionResults.append((key, resultsDict[key]))
            currentIndex += 1
        else:
            break

    results = positionResults

    connection.close()
    return results

"""
Query for positions 
"""
def getPositionList(cursor, term, docID):
    results = []

    query = "SELECT position FROM position_list WHERE doc_id = (SELECT id FROM doc WHERE doc.name = %s) AND term_id = (SELECT id FROM term WHERE term.name = %s)"
    cursor.execute(query,(docID, term))

    for position in cursor:
        results.append(position[0])

    return results


"""
Gets smallest position window
"""
def getMinWindow(cursor, queryTerms, docID):
    if len(queryTerms) == 1:
        return 1

    positionLists = []         #list of position lists
    currentPosition = []
    allFull = True
    windowSize = float("inf")

    for terms in queryTerms:
        positionLists.append(getPositionList(cursor, terms, docID))


    for index, termPosition in enumerate(queryTerms):
        if len(positionLists[index]) != 0:
            currentPosition.append(positionLists[index].pop(0))

    if (max(currentPosition) - min(currentPosition)) < windowSize:
        windowSize = (max(currentPosition) - min(currentPosition)) + 1

    while allFull:

        if (min(currentPosition) == max(currentPosition)):
            currentPosition[currentPosition.index(max(currentPosition))] += 1

        gotNext = False
        replacementOptions = list(currentPosition)


        while not gotNext:

            lowest = min(replacementOptions)
            replaceIndex = currentPosition.index(lowest)

            if len(positionLists[replaceIndex]) > 0:
                currentPosition[replaceIndex] = positionLists[replaceIndex].pop(0)
                gotNext = True
            else:
                replacementOptions[replaceIndex] = float("inf")

            if(min(replacementOptions) == float("inf")):
                gotNext = True
                allFull = False

        if (max(currentPosition) - min(currentPosition)) < windowSize:
            windowSize = (max(currentPosition) - min(currentPosition)) + 1
        if (max(currentPosition) == min(currentPosition)):
            windowSize = len(queryTerms)

    return windowSize

"""
Driver for console application
"""
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

        if len(results) < 20:
            results += orQuery(cursor, query_terms)

        for name, url in results:
            print url

#driver()