from collections import defaultdict
import os
import json
import math


my_base_dir = "/Users/brooke/Documents/Coursework/UC Irvine/CS121/" \
              "CS121_Project4/"
raw_dir = my_base_dir + "/WEBPAGES_RAW/"
json_dir = my_base_dir + "WEBPAGES_JSON/"
df_t_dir = my_base_dir + "df_t.json"
idf_dir = my_base_dir + "idf_t.json"
tf_dir = json_dir + "tf/"
tf_idf_dir = my_base_dir + "tf-idf/"


def open_bookkeeping(base_dir):
    # open book keeping file
    with open(base_dir + "/bookkeeping.json", 'r') as bookkeeping:
        return json.load(bookkeeping)


def get_df(base_dir, book_dict, output_dir):
    '''
    Runs through the JSON files output by frequency.parse_files and
    creates a single JSON file 'df_t.json" that holds the frequency
    of each term throughout ALL documents
    :param base_dir: the directory storing the JSON files output by
    frequency.parse_files() (/WEBPAGES_JSON)
    :param book_dict: The dictionary holding the list of files given
    in bookeeping.json
    :param output_dir: The directory to output the document frequency
    file to. In my case this is the project directory
    :return: None
    '''
    df_t = defaultdict(int)  # number of documents that contain term t
    for file_dir in book_dict:
        print 'Processing ' + file_dir
        with open(base_dir + file_dir + ".json", "r") as f:
            json_dict = json.loads(f.read())

            for token in set(json_dict.keys()):
                df_t[token] += 1

    with open(output_dir, 'w') as f:
        json.dump(df_t, f)


def get_tf(base_dir, book_dict, output_dir):
    '''
    Calculates the 'weighted' term frequency for each document,
    as described in lec 12. slide 19.
    :param base_dir: the directory holding the JSON files output by
    frequency.parse_files()
    :param book_dict: the dictionary holding the list of files givne
    in bookeeping.json
    :param output_dir: the directory to output the weighted
    term-frequency for each doc. In my case this is in /WEBPAGES_JSON
    the same as base_dir with "_tf" appended to the file name
    :return: None
    '''
    for file_dir in book_dict:
        print 'Processing ' + file_dir
        with open(base_dir + file_dir + ".json", "r") as f:
            json_dict = json.loads(f.read())

            # Ref: Lect 12. Slide 19
            # w_{t,d} = 1 + log tf_{t,d}
            for token, count in json_dict.iteritems():
                if count > 0:
                    json_dict[token] = count #1 + math.log(count, 10)

            output_file = output_dir + file_dir + "_tf.json"
            if not os.path.exists(os.path.dirname(output_file)):
                try:
                    os.makedirs(os.path.dirname(output_file))
                except OSError as exc:  # Guard against race condition
                    raise

            with open(output_file, "w") as res:
                json.dump(json_dict, res)


def get_idf(dict_dir, N, output_dir):
    '''
    For each term the idf score is calculated and
    output to the file idf_t.json
    :param dict_dir: the dictionary containing the list of files in
    bookeeping.json
    :param N: the number of documents (length of bookeeping.json)
    :param output_dir: the directory to output the idf scores. In my
    case this is the project directory.
    :return: None
    '''
    with open(dict_dir, 'r') as f:
        json_dict = json.loads(f.read())

        for token, count in json_dict.iteritems():
            json_dict[token] = math.log(1.0*N/(json_dict[token]*1.0), 10)

        output_file = output_dir + "idf_t.json"
        if not os.path.exists(os.path.dirname(output_file)):
            try:
                os.makedirs(os.path.dirname(output_file))
            except OSError as exc:  # Guard against race condition
                raise

        with open(output_file, 'w') as res:
            json.dump(json_dict, res)


def get_tf_idf(output_dir, tf_dir, idf_dir, book_dict):
    '''
    Using idf_t.json and the individual _tf.json files in
    WEBPAGES_JSON, the tf-idf is calculated for each term/document
    pair and output in the directory tf-idf/
    :param output_dir: the directory each documents tf-idf calculation
    dictionary will be written to. In my case this is tf-idf/
    written
    :param tf_dir: the directory holding the _tf.json files. In my
    case this is WEBPAGES_JSON/
    :param idf_dir: the directory holding the idf_t.josn file. In my
    case this is the project directory
    :param book_dict: the dictionary holding the document names given
    in bookeeping.json
    :return: None
    '''
    with open(idf_dir, "r") as idf_file:
        idf_t = json.loads(idf_file.read())

        for file_dir in book_dict:
            print 'Processing ' + file_dir
            with open(json_dir + file_dir + ".json", "r") as f:
                json_dict = json.loads(f.read())

                for token in json_dict.keys():
                    # Ref: Lec 12 Slide 28
                    json_dict[token] = (1 + json_dict[token]) * (idf_t[token])

                output_file = output_dir + file_dir + "tf_idf.json"
                if not os.path.exists(os.path.dirname(output_file)):
                    try:
                        os.makedirs(os.path.dirname(output_file))
                    except OSError as exc:  # Guard against race condition
                        raise
                with open(output_file, 'w') as f:
                    json.dump(json_dict, f)


def construct_inverted_index(tfidf_dir, output_dir, idf_dir, book_dict):
    '''
    Using the tf-idf values calculated in get_tf_idf, the tf-idf
    scores for each doc/term pair are compiled to form the inverted
    index. They are output in the form of {term: postings-list}
    :param tfidf_dir: the directory holding the tf-idf values for each
    document. In my case this is tf-idf/
    :param output_dir: The directory to output the inverted index to.
    In my case this is the project directory
    :param idf_dir: The directory holding the idf_t.json file. In my
    case this is the project directory.
    :param book_dict: The dictionary holding then document names for
    each document found in bookeeping.json
    :return: None
    '''
    inverted_index = {}
    #with open(idf_dir, "r") as idf_file:
    #    idf_t = json.loads(idf_file.read())

    for file_dir in book_dict:
        print 'Processing ' + file_dir
        with open(tfidf_dir + file_dir + "tf_idf.json", "r") as f:
            json_dict = json.loads(f.read())

            for token in json_dict.keys():
                if token not in inverted_index:
                    inverted_index[token] = [(json_dict[token], file_dir, )]
                else:
                    inverted_index[token].append( (json_dict[token], file_dir, ) )

    output_file = output_dir + "myinvertedindex.json"
    if not os.path.exists(os.path.dirname(output_file)):
        try:
            os.makedirs(os.path.dirname(output_file))
        except OSError as exc:  # Guard against race condition
            raise
    with open(output_file, 'w') as f:
        json.dump(inverted_index, f)


book = open_bookkeeping(raw_dir)
N = len(book)
get_df(json_dir, book, df_t_dir)
# get_tf(json_dir, book, tf_dir)
get_idf(df_t_dir, N, my_base_dir)
get_tf_idf(tf_idf_dir, tf_dir, idf_dir, book)
construct_inverted_index(tf_idf_dir, my_base_dir, idf_dir, book)


# BELOW CODE IS FOR CREATING A SORTED VERSION OF THE DOCUMENT FREQ.
'''
import operator
with open ("/Users/brooke/Documents/Coursework/UC Irvine/"
              "CS121/CS121_Project4/df_t.json", "r") as f:
    df_t = json.loads(f.read())

    sorted_df_t = sorted(df_t.items(), key=operator.itemgetter(1), reverse=True)

    with open("/Users/brooke/Documents/Coursework/UC Irvine/"
              "CS121/CS121_Project4/df_t_sorted.json", 'w') as r:
        json.dump(sorted_df_t, r)
'''
