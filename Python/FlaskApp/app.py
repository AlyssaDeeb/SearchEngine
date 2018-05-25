import query
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


def simpleReultsHTML(results, query):
    html = "<h2>Showing Results for: \'" + query + "\'</h2><h3>" + str(len(results)) +" Results Found...</h3><thead><tr><th>File</th><th>URL</th></tr></thead><tbody>"

    for name, url in results:
        html += "<tr ><td>"+ name +"</td><td><a><href = " + url + "/> " + url + "</a></td></tr>"

    html += "</tbody>"
    return html


@app.route('/', methods=['GET','POST'])
def executeQuery():

    if request.method == 'POST':
        if(request.form['inputQuery']):
            lastQuery = request.form['inputQuery']
            results = query.webDriver(lastQuery)

            return render_template('results.html', tables = [simpleReultsHTML(results, lastQuery)], query = lastQuery)

    else:

        return render_template('home.html')

@app.route('/results', methods=['GET'])
def showResults():
    if request.method == 'GET':
        return render_template('results.html')


@app.route('/informative', methods=['GET'])
def showInformResults():

    if request.method == 'GET':

        #results = query.webDriver()
        return render_template('informativeResults.html')




if __name__ == "__main__":
    app.run()



"""
Souces: https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
"""