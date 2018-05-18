import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
import re
import os
import json

my_base_dir = "/Users/brooke/Documents/Coursework/UC Irvine/CS121/" \
              "CS121_Project4/WEBPAGES_RAW/"
my_output_dir = "/Users/brooke/Documents/Coursework/UC Irvine/CS121/" \
              "CS121_Project4/WEBPAGES_JSON/"

nltk.download('stopwords')
alphanumeric = re.compile('[^a-zA-Z0-9\'-]+')
badascii = re.compile('&(#[\d]+[;]{0,1})')
parse_fails = []


def open_bookkeeping(base_dir):
    # open book keeping file
    with open(base_dir + "/bookkeeping.json", 'r') as bookkeeping:
        return json.load(bookkeeping)


def is_visable(element):
    return element.parent.name not in \
           ['head', 'title', 'meta', 'script', 'css', 'href', 'link',
            'img', 'dl', 'a', 'style', '[document]'] and \
           not isinstance(element, BeautifulSoup.Comment)

# tokenization & term-frequency calculation


def get_visable_text(soup):
    '''
    Give a beautiful soup object, tokenizes selected text, inserts
    into a dictionary keeping track of the frequency of each term.
    :param soup: A beautiful soup object for a HTML page
    :return: Above mentioned dictionary
    '''
    text = soup.findAll(text=True)
    visable_text = filter(is_visable, text)
    token_dict = defaultdict(int)

    for line in visable_text:
        if line != u' ' and line != u'\n':
            for token in line.split():
                # removes non-alphanumeric characters
                clean_token = alphanumeric.sub('', token.lower())

                if clean_token and (clean_token not in stopwords.words("english")) and \
                        (1 < len(clean_token) < 46) and (not clean_token.isdigit()):
                    token_dict[clean_token] += 1

                # if token is non empty AND
                # token is a number AND
                # token is less than 10 characters long
                elif clean_token and clean_token.isdigit() and len(clean_token) < 10:
                    with open("/Users/brooke/Documents/Coursework/UC Irvine/CS121/CS121_Project4/numbers.txt", "a") as f:
                        f.write(clean_token + ", ")
    return token_dict

# driver...runs through all HTML files, receives term-frequency dict
# and outputs to file


def parse_files(base_dir, dict, output_dir):
    '''
    For each file in WEBPAGES_RAW we pass into beautiful soup and
    receive the term-frequency dictionary for each document via
    the above function get_visable_text
    :param base_dir: the directory leading to WEBPAGES_RAW
    :param dict: the JSON dictionary found in WEBPAGES_RAW/bookeeping.json
    :param output_dir: the directory to output the term-frequencies for
    each document (I choose to put this in WEBPAGES_JSON
    :return: None
    '''
    for file_dir in dict:
        print "Processing file: " + base_dir + file_dir

        with open(base_dir + file_dir, "r") as html:
            # removes pesky unicode characters
            html = html.read().decode('ascii', 'ignore').encode('utf-8')
            try:
                soup = BeautifulSoup.BeautifulSoup(
                    html, convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
                token_dict = get_visable_text(soup)
                soup.close()

                output_file = output_dir + file_dir + ".json"

                if not os.path.exists(os.path.dirname(output_file)):
                    try:
                        os.makedirs(os.path.dirname(output_file))
                    except OSError as exc:  # Guard against race condition
                        raise

                with open(output_file, 'w') as f:
                    json.dump(token_dict, f)

            except ValueError:
                print "BAD HTML: Error processing file: " + base_dir + file_dir
                parse_fails.append(file_dir)

                with open("/Users/brooke/Documents/Coursework/UC Irvine/CS121/CS121_Project4/errors.txt", 'a') as f:
                    f.write( str(base_dir + file_dir) )

            except Exception:
                print "UNKNOWN: Error processing file:" + base_dir + file_dir

                with open("/Users/brooke/Documents/Coursework/UC Irvine/CS121/CS121_Project4/errors.txt", 'a') as f:
                    f.write( str(base_dir + file_dir) )

    print "All Files Exported to " + my_output_dir


# NOTE:: The below funcitons deal with weirdness in the HTML
# They follow the same procedures as the above functions but do
# something a bit differently when passing to beautiful soup


def alt_get_visable_text(soup):
    text = soup.findAll(text=True)
    visable_text = filter(is_visable, text)
    token_dict = defaultdict(int)

    for line in visable_text:
        line = badascii.sub(' ', line)
        #print line
        if line != u' ' and line != u'\n':
            for token in line.split():
                # removes non-alphanumeric characters
                clean_token = alphanumeric.sub('', token.lower())

                # ensure token is not an empty string or stop-word
                if clean_token and clean_token not in stopwords.words("english"):
                    token_dict[clean_token] += 1

    return token_dict


def alt_parse_files(base_dir, dict):
    for file_dir in dict:
        print "Processing file: " + base_dir + file_dir

        with open(base_dir + file_dir, "r") as html:
            # removes pesky unicode characters
            html = html.read()#.decode('utf-8')#read().decode('ascii', 'ignore').encode('utf-8')

            try:
                soup = BeautifulSoup.BeautifulSoup(
                    html) #, convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)
                token_dict = get_visable_text(soup)
                soup.close()

                output_file = my_output_dir + file_dir + ".json"

                if not os.path.exists(os.path.dirname(output_file)):
                    try:
                        os.makedirs(os.path.dirname(output_file))
                    except OSError as exc:  # Guard against race condition
                        raise

                with open(output_file, 'w') as f:
                    json.dump(token_dict, f)
                #print "File Complete"

            except ValueError:
                print "BAD HTML: Error processing file: " + base_dir + file_dir

                with open("/Users/brooke/Documents/Coursework/UC Irvine/CS121/CS121_Project4/errors.txt", 'a') as f:
                    f.write( str(base_dir + file_dir) )

            except Exception:
                print "UNKNOWN: Error processing file:" + base_dir + file_dir

                with open("/Users/brooke/Documents/Coursework/UC Irvine/CS121/CS121_Project4/errors.txt", 'a') as f:
                    f.write( str(base_dir + file_dir) )


    print "All Files Exported to " + my_output_dir


book = open_bookkeeping(my_base_dir)
parse_files(my_base_dir, book, my_output_dir)

if parse_fails:
    print "Retrying parse for bad html files..."
    alt_parse_files(my_base_dir,parse_fails)

