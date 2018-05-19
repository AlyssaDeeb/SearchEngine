import mysql.connector
import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import defaultdict
import re
import json
import math


my_base_dir = 'C:\\Users\\alyss\\Desktop\\cs121\\WEBPAGES\\WEBPAGES_RAW\\'
my_output_dir = "C:\\Users\\alyss\\Desktop\\cs121\\JSON Output"

nltk.download('stopwords')
alphanumeric = re.compile('[^a-zA-Z0-9\'-]+')
badascii = re.compile('&(#[\d]+[;]{0,1})')
parse_fails = []

fileRefCountDict= defaultdict(int)
fileDict = defaultdict(int)
fileNameDict = defaultdict(str)
absoluteURLDict = defaultdict(str)
metaDict = defaultdict(int)
posDict = defaultdict(list)
termDict = defaultdict(int)
freqDict = defaultdict(int)
termFileDict = defaultdict(int)
termFileCountDict = defaultdict(int)
termDocCountDict = defaultdict(int)
idf_Dict = defaultdict(float)
tf_idf_Dict = defaultdict(float)

def open_bookkeeping(base_dir):
    # open book keeping file
    with open(base_dir + "\\bookkeeping.json", 'r') as bookkeeping:
        return json.load(bookkeeping)


def is_visable(element):
    return element.parent.name not in \
           ['head', 'meta', 'script', 'css', 'href', 'link', 'img', 'dl', 'a', 'style', '[document]'] and \
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


                   # if posDict.has_key((fileName, clean_token)):
                   #     posDict[(fileName, clean_token)].append(position)
                   #
                   #else:
                   #     posDict[(fileName,clean_token)] = [position]
                    #    termDocCountDict[clean_token] += 1

                    if not posDict.has_key((fileName, clean_token)):
                        termDocCountDict[clean_token] += 1

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


def get_meta_data(soup, fileName):
    '''
    Give a beautiful soup object, tokenizes meta title and header tags to update frequency count,
    additionally updates all link references to bookkeeping links.
    :param soup: A beautiful soup object for a HTML page
    :param fileName file currently being parsed
    :return: Above mentioned dictionary
    '''

    for a in soup.findAll('a', href=True):  # use BeautifulSoup to find all hyperlinks tagged  as href
        url = a['href'].replace("www.", "").replace("http://", "").replace("https://", "")
        if absoluteURLDict.has_key(url):
            fileRefCountDict[absoluteURLDict[url]] += 1
    for a in soup.findAll(['title', 'h1', 'h2', 'h3']):
        for token in a.text.split():
            token = alphanumeric.sub('', token.lower())

            if token and (token not in stopwords.words("english")) and \
                        (1 < len(token) < 46) and (not token.isdigit()):

                if termFileDict.has_key((fileName,token)):
                    metaDict[(fileDict[fileName], termDict[token])] += 1


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


    for file_dir in dict:


        print "Processing file: ", base_dir + file_dir, " Count: ", totalFiles

        fileDict[file_dir] = totalFiles
        url = dict[file_dir].replace("www.", "").replace("http://", "").replace("https://", "")
        absoluteURLDict[url] = dict[file_dir]
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
                get_meta_data(soup, file_dir)
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


    print "All Files Exported to " + my_output_dir
    return [totalFiles, totalTerms]


totalFiles = 1
totalTerms = 1
book = open_bookkeeping(my_base_dir)
results = parse_files(my_base_dir, book, my_output_dir, totalFiles, totalTerms)
totalFile = results[0] - 1
totalTerms = results[1] - 1


if parse_fails:
    print "Retrying parse for bad html files..."
    print parse_fails



'''
get tf-idf
'''
for key, value in termDict.iteritems():
    idf_Dict[value] = math.log(((1.0 * totalFile) / ((termDocCountDict[key] * 1.0))), 10)


for key, value in termFileDict.iteritems():
    tf_idf_value = (1 + math.log(1.0 * value, 10)) * idf_Dict[termDict[key[1]]]
    tf_idf_Dict[(fileDict[key[0]], termDict[key[1]])] = tf_idf_value


'''
enter into database
'''
cnx = mysql.connector.connect(user='test', password='123', host='127.0.0.1', database='searchEngine')

if (cnx.is_connected()):
    print "Connection Passes"

cursor = cnx.cursor(buffered=True)



# Insert file name into database
for key, value in fileDict.iteritems():
    inserted = 0
    fileInsert = ("INSERT IGNORE INTO `doc` (`id`,`name`, `url`, `total_terms`, `references`) VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(fileInsert,(value, key, fileNameDict[key], termFileCountDict[key], fileRefCountDict[fileNameDict[key]]))

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

    fileInsert = ("INSERT INTO `term_in_doc` (`doc_id`,`term_id`, `frequency`, `tf-idf`) VALUES (%s, %s, %s, %s)")
    cursor.execute(fileInsert,(fileDict[key[0]], termDict[key[1]], value, tf_idf_Dict[(fileDict[key[0]], termDict[key[1]])]))

    inserted += 1

    if (inserted % 1000 == 0):
        cnx.commit()
cnx.commit()


# Insert all of the positions for each word in each doc
#for key, value in posDict.iteritems():
#    for position in value:
#        inserted = 0
#        fileInsert = ("INSERT INTO `position_list` (`doc_id`,`term_id`, `position`) VALUES (%s, %s, %s)")
#        cursor.execute(fileInsert, (fileDict[key[0]], termDict[key[1]], position))
#
#        inserted += 1
#
#        if (inserted % 1000 == 0):
#            cnx.commit()

for key, value in metaDict.iteritems():
    inserted = 0

    fileInsert = ("UPDATE `term_in_doc` SET  `meta_frequency` = %s WHERE `doc_id` = %s AND `term_id` = %s")
    cursor.execute(fileInsert, (value, key[0], key[1]))

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