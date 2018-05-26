import query
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

"""
Populate URL table
"""
def simpleReultsHTML(results, query):
    html = "<h2>Showing Results for: \'" + query + "\'</h2><h3>" + str(len(results)) +" Results Found...</h3>"
    html += "<thead><tr><th>File</th><th>URL</th></tr></thead><tbody>"
    for name, url in results:
        html += "<tr ><td>"+ name +"</td><td style=\"word-wrap: break-word;min-width: 200px;max-width: 200px;\"><a><href = " + url + "/> " + url + "</a></td></tr>"

    html += "</tbody>"
    return html



"""
Populate Title table
"""
def populatedReultsHTML(results, query):
    base_dir = 'C:\\Users\\alyss\\Desktop\\cs121\\WEBPAGES\\WEBPAGES_RAW\\'

    reTerms = ""

    for terms in query:
        reTerms += terms + ".*"

    htmlTable = "<h2>Showing Results for: \'" + query + "\'</h2><h3>" + str(len(results)) +" Results Found...</h3>"

    for name, url in results:
        currentTitle = "NOT FOUND"
        with open(base_dir + name, "r") as html:
            # removes pesky unicode characters
            html = html.read().decode('ascii', 'ignore').encode('utf-8')
            try:
                soup = BeautifulSoup(html, 'html.parser')

                if(soup.title.string):
                    currentTitle = str(soup.title.string)

                else:
                    currentTitletitle = url

                wholeText = soup.text

                index = soup.text.lower().find(query)
                wholeText = wholeText[index: index + 300]


            except ValueError:
                print "BAD HTML: Error processing file: " + base_dir + name

            except Exception:
                print "UNKNOWN: Error processing file:" + base_dir + name
        htmlTable += "<tr ><td style=\"word-wrap: break-word;min-width: 200px;max-width: 200px;\"><b>"+ currentTitle +"</b><br/><a><href = " + url + "/> " + url + "<br/></a>"
        htmlTable += "<br/>" + wholeText + "...</td></tr>"

    htmlTable += "</tbody>"
    return htmlTable


"""
Home Page
"""
@app.route('/', methods=['GET','POST'])
def executeQuery():

    if request.method == 'POST':
        if(request.form['inputQuery']):
            lastQuery = request.form['inputQuery']
            results = query.tf_idf_Results(lastQuery)

            return render_template('results.html', tables = [simpleReultsHTML(results, lastQuery)], inputQuery = lastQuery)

    else:
        return render_template('home.html')


"""
Basic Results
"""
@app.route('/results', methods=['GET','POST'])
def showResults():
    if request.method == 'POST':
        if (request.args.get('inputQuery')):
            lastQuery = request.args.get('inputQuery')
            results = query.tf_idf_Results(lastQuery)

            return render_template('results.html', tables = [simpleReultsHTML(results, lastQuery)], inputQuery = lastQuery)

    else:
        if (request.args.get('inputQuery')):
            lastQuery = request.args.get('inputQuery')
            results = query.tf_idf_Results(lastQuery)

            return render_template('results.html', tables = [simpleReultsHTML(results, lastQuery)], inputQuery = lastQuery)
        return render_template('results.html')


"""
Basic Informative Results
"""
@app.route('/informative', methods=['GET','POST'])
def showInformativeResults():

    if request.method == 'POST':
        if (request.args.get('inputQuery')):
            lastQuery = request.args.get('inputQuery')
            results = query.tf_idf_Results(lastQuery)

            return render_template('informativeResults.html', tables = [populatedReultsHTML(results, lastQuery)], inputQuery = lastQuery)

    else:
        if(request.args.get('inputQuery')):
            lastQuery = request.args.get('inputQuery')
            results = query.tf_idf_Results(lastQuery)

            return render_template('informativeResults.html', tables=[populatedReultsHTML(results, lastQuery)], inputQuery=lastQuery)

    return render_template('informativeResults.html')


"""
Weighted Results
"""
@app.route('/weightedResults', methods=['GET','POST'])
def showWeightedResults():
    if request.method == 'POST':
        if (request.args.get('inputQuery')):
            lastQuery = request.args.get('inputQuery')
            results = query.tf_idf_Results(lastQuery)

            return render_template('weighted-results.html', tables = [simpleReultsHTML(results, lastQuery)], inputQuery = lastQuery)

    else:
        if (request.args.get('inputQuery')):
            lastQuery = request.args.get('inputQuery')
            results = query.tf_idf_Results(lastQuery)

            return render_template('weighted-results.html', tables = [simpleReultsHTML(results, lastQuery)], inputQuery = lastQuery)
        return render_template('weighted-results.html')


"""
Weighted Informative Results
"""
@app.route('/weightedInformative', methods=['GET','POST'])
def showWeightedInformativeResults():

    if request.method == 'POST':
        if (request.args.get('inputQuery')):
            lastQuery = request.args.get('inputQuery')
            results = query.weighted_tf_idf_Results(lastQuery)

            return render_template('weighted-informativeResults.html', tables = [populatedReultsHTML(results, lastQuery)], inputQuery = lastQuery)

    else:
        if(request.args.get('inputQuery')):
            lastQuery = request.args.get('inputQuery')
            results = query.weighted_tf_idf_Results(lastQuery)

            return render_template('weighted-informativeResults.html', tables=[populatedReultsHTML(results, lastQuery)], inputQuery=lastQuery)

    return render_template('weighted-informativeResults.html')


"""
Main
"""
if __name__ == "__main__":
    app.run()


"""
Souces: https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
"""