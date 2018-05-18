import mysql.connector
import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
import re
import os
import json


my_base_dir = 'C:\\Users\\alyss\\Desktop\\cs121\\WEBPAGES\\WEBPAGES_RAW\\'
my_output_dir = "C:\\Users\\alyss\\Desktop\\cs121\\JSON Output"

nltk.download('stopwords')
alphanumeric = re.compile('[^a-zA-Z0-9\'-]+')
badascii = re.compile('&(#[\d]+[;]{0,1})')
parse_fails = []

fileRefCountDict= defaultdict(int)
fileDict = defaultdict(int)
fileNameDict = defaultdict(str)
metaDict = defaultdict(int)
posDict = defaultdict(list)
termDict = defaultdict(int)
freqDict = defaultdict(int)
termFileDict = defaultdict(int)
termFileCountDict = defaultdict(int)


def open_bookkeeping(base_dir):
    # open book keeping file
    with open(base_dir + "\\bookkeeping.json", 'r') as bookkeeping:
        return json.load(bookkeeping)


def is_visable(element):
    return element.parent.name not in \
           ['head', 'title', 'meta', 'script', 'css', 'href', 'link', 'img', 'dl', 'a', 'style', '[document]'] and \
           not isinstance(element, BeautifulSoup.Comment)

# tokenization & term-frequency calculation


def get_visable_text(soup, fileName, totalTerms):
    '''
    Give a beautiful soup object, tokenizes selected text, inserts
    into a dictionary keeping track of the frequency of each term.
    :param soup: A beautiful soup object for a HTML page
    :return: Above mentioned dictionary
    '''
    text = soup.findAll(text=True)
    visable_text = filter(is_visable, text)


    position = 0
    for line in visable_text:
        if line != u' ' and line != u'\n':
            for token in line.split():
                # removes non-alphanumeric characters
                clean_token = alphanumeric.sub('', token.lower())

                if clean_token and (clean_token not in stopwords.words("english")) and \
                        (1 < len(clean_token) < 46) and (not clean_token.isdigit()):

                    if termDict.has_key(clean_token):
                        freqDict[clean_token] += 1
                    else:
                        termDict[clean_token] = totalTerms
                        freqDict[clean_token] = 1
                        totalTerms += 1


                    if posDict.has_key((fileName, clean_token)):
                        posDict[(fileName, clean_token)].append(position)

                    else:
                        posDict[(fileName,clean_token)] = [position]

                    position += 1
                    termFileDict[(fileName,clean_token)] += 1

                # if token is non empty AND
                # token is a number AND
                # token is less than 10 characters long
                elif clean_token and clean_token.isdigit() and len(clean_token) < 10:
                    with open("C:\\Users\\alyss\\Desktop\\cs121\\numbers.txt", "a") as f:
                        f.write(clean_token + ", ")

    termFileCountDict[fileName] = position
    return totalTerms



# driver...runs through all HTML files, receives term-frequency dict
# and outputs to file


def parse_files(base_dir, dict, output_dir, totalFiles, totalTerms):
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

    testTotal = 0;

    for file_dir in dict:
        if(testTotal > 10):
            break;
        print "Processing file: ", base_dir + file_dir, " Count: ", totalFiles

        fileDict[file_dir] = totalFiles
        fileNameDict[file_dir] = dict[file_dir]
        fileRefCountDict[dict[file_dir]] = 0
        totalFiles += 1

        with open(base_dir + file_dir, "r") as html:
            # removes pesky unicode characters
            html = html.read().decode('ascii', 'ignore').encode('utf-8')
            try:
                soup = BeautifulSoup.BeautifulSoup(
                    html, convertEntities=BeautifulSoup.BeautifulStoneSoup.HTML_ENTITIES)

                totalTerms = get_visable_text(soup, file_dir, totalTerms)
                soup.close()

            except ValueError:
                print "BAD HTML: Error processing file: " + base_dir + file_dir
                parse_fails.append(file_dir)

                with open("C:\\Users\\alyss\\Desktop\\cs121\\errors.txt", 'a') as f:
                    f.write( str(base_dir + file_dir) )

            except Exception:
                print "UNKNOWN: Error processing file:" + base_dir + file_dir

                with open("C:\\Users\\alyss\\Desktop\\cs121\\errors.txt", 'a') as f:
                    f.write( str(base_dir + file_dir) )
            testTotal += 1

    print "All Files Exported to " + my_output_dir
    return [totalFiles, totalTerms]


# NOTE:: The below funcitons deal with weirdness in the HTML
# They follow the same procedures as the above functions but do
# something a bit differently when passing to beautiful soup


def alt_get_visable_text(soup, fileName):
    text = soup.findAll(text=True)
    visable_text = filter(is_visable, text)

    position = 0
    for line in visable_text:
        line = badascii.sub(' ', line)

        if line != u' ' and line != u'\n':
            for token in line.split():
                # removes non-alphanumeric characters
                clean_token = alphanumeric.sub('', token.lower())

                # ensure token is not an empty string or stop-word
                if clean_token and clean_token not in stopwords.words("english"):
                    if termDict.has_key(clean_token):
                        freqDict[clean_token] += 1
                    else:
                        termDict[clean_token] = 1
                        freqDict[clean_token] = 1
                    if posDict.has_key((fileName,clean_token)):
                        posDict[(fileName,clean_token)].append(position)
                    else:
                        posDict[(fileName,clean_token)] = [position]
                    position += 1
                    termFileDict[(fileName,clean_token)] += 1

    termFileCountDict[fileName] = position



def alt_parse_files(base_dir, dict, totalFiles):
    for file_dir in dict:

        fileDict[file_dir] = totalFiles
        fileNameDict[file_dir] = dict[file_dir]
        fileRefCountDict[dict[file_dir]] = 0
        totalFiles += 1

        print "Processing Alt file: " + base_dir + file_dir

        with open(base_dir + file_dir, "r") as html:
            # removes pesky unicode characters
            html = html.read()

            try:
                soup = BeautifulSoup.BeautifulSoup(
                    html)

                get_visable_text(soup, file_dir)
                soup.close()


            except ValueError:
                print "BAD HTML: Error processing file: " + base_dir + file_dir

                with open("C:\\Users\\alyss\\Desktop\\cs121\\errors.txt", 'a') as f:
                    f.write( str(base_dir + file_dir) )

            except Exception:
                print "UNKNOWN: Error processing file:" + base_dir + file_dir

                with open("C:\\Users\\alyss\\Desktop\\cs121\\errors.txt", 'a') as f:
                    f.write( str(base_dir + file_dir) )


    print "All Files Exported to " + my_output_dir
    return totalFiles


totalFiles = 1
totalTerms = 1
book = open_bookkeeping(my_base_dir)
results = parse_files(my_base_dir, book, my_output_dir, totalFiles, totalTerms)
totalFile = results[0]
totalTerms = results[1]



if parse_fails:
    print "Retrying parse for bad html files..."
    print parse_fails
    #totalFiles = alt_parse_files(my_base_dir,parse_fails, totalFiles)





cnx = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='searchEngine')

if (cnx.is_connected()):
    print "Connection Passes"

cursor = cnx.cursor(buffered=True)

"""
Insert files
"""



# Insert file name into database
for key, value in fileDict.iteritems():
    inserted = 0
    fileInsert = ("INSERT IGNORE INTO `doc` (`id`,`name`, `url`, `total_terms`) VALUES (%s, %s, %s, %s)")
    cursor.execute(fileInsert,(value, key, fileNameDict[key], termFileCountDict[key]))

    inserted += 1

    if(inserted % 1000 == 0):
        cnx.commit()

cnx.commit()

# Insert all terms into the database
for key, value in termDict.iteritems():
    inserted = 0

    fileInsert = ("INSERT INTO `term` (`id`,`name`, `total_frequency`) VALUES (%s, %s, %s)")
    cursor.execute(fileInsert, (value, key, freqDict[key]))

    inserted += 1

    if (inserted % 1000 == 0):
        cnx.commit()
cnx.commit()


# Insert the number of times a term was in a doc
for key, value in termFileDict.iteritems():
    inserted = 0

    fileInsert = ("INSERT INTO `term_in_doc` (`doc_id`,`term_id`, `frequency`) VALUES (%s, %s, %s)")
    cursor.execute(fileInsert, (fileDict[key[0]], termDict[key[1]], value))

    inserted += 1

    if (inserted % 1000 == 0):
        cnx.commit()
cnx.commit()


# Insert all of the positions for each word in each doc
for key, value in posDict.iteritems():
    for position in value:
        inserted = 0
        fileInsert = ("INSERT INTO `position_list` (`doc_id`,`term_id`, `position`) VALUES (%s, %s, %s)")
        cursor.execute(fileInsert, (fileDict[key[0]], termDict[key[1]], position))

        inserted += 1

        if (inserted % 1000 == 0):
            cnx.commit()

cnx.commit()
cursor.close()
cnx.close()


"""
Sources:
    MySQL Connector: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
"""