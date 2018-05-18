import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
import re
import os
import json
import enchant
import operator

index_dir = "/Users/brooke/Documents/Coursework/UC Irvine/CS121/" \
              "CS121_Project4/myinvertedindex.json"

book_dir = "/Users/brooke/Documents/Coursework/UC Irvine/CS121/" \
              "CS121_Project4/WEBPAGES_RAW/"


def open_bookkeeping(base_dir):
    # open book keeping file
    with open(base_dir + "/bookkeeping.json", 'r') as bookkeeping:
        return json.load(bookkeeping)


def init_index(index_directory):
    '''
    Opens the inverted index and returns the dictionary containing it
    :param index_directory: file path to inverted index
    :return: inverted index dictionary
    '''
    with open(index_directory, 'r') as f:
        return json.load(f)


def query_index(index_dict, doc_dict, query, limit=10):
    if query not in index_dict:
        print "No results found"
        return

    term_postingslist = index_dict[query]
    result_set = sorted(term_postingslist, key=operator.itemgetter(0), reverse=True)[:limit]
    print "DocID\ttf-idf"
    for result in result_set:
        # commented code displays tf-idf score
        print doc_dict[result[1]] + "\t" + str(result[0])


def driver():
    print "Initializing Gago Search..."
    index_dict = init_index(index_dir)
    doc_dict = open_bookkeeping(book_dir)

    while 1:
        query_string = raw_input("Search term: ")
        query_index(index_dict, doc_dict, query_string)


driver()