import nltk
import re
from nltk.corpus import stopwords
import mysql.connector
import textwrap

mysql_params = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'mydb'
}


nltk.download('stopwords')
alphanumeric = re.compile('[^a-zA-Z0-9\'-]+')


def clean_input():
    raw_query = raw_input("Enter a search term ")
    cleaned_query_list = []

    for token in raw_query.split(' '):
        clean_token = alphanumeric.sub('', token.lower().strip())

        if clean_token and \
                clean_token not in stopwords.words("english"):
            cleaned_query_list.append(clean_token)

    return cleaned_query_list


def generate_query(term_array):
    base_query = "(SELECT `name`, `url`, `weighted_tf-idf` " \
                 "FROM term_in_doc, doc WHERE " \
                 "doc.id = term_in_doc.doc_id AND " \
                 "term_in_doc.term_id ="

    query = ""

    if term_array:

        for idx, term in enumerate(term_array):
            query += base_query + \
                "(select id from term where name = \"" + term + "\"))"

            if idx < len(term_array) - 1:
                query += "UNION"
        query += "order by `weighted_tf-idf` desc limit 10;"

    print "generate_query: \n"
    print ('\n'.join(textwrap.wrap(query, width=90))) + '\n'

    return query


def pretty_print_rs(result_set):
    print "{0:10} {1:90} {2}".format("name", "url", "weighted_tf-idf")

    for page in result_set:
        print '{0:10} {1:90} {2}'.format(page[0], page[1], page[2])


def driver():
    conn = mysql.connector.connect(**mysql_params)
    cursor = conn.cursor()

    query_terms = clean_input()
    user_query = generate_query(query_terms)

    cursor.execute(user_query)
    rs = cursor.fetchall()

    pretty_print_rs(rs)

driver()