from flask import Flask, render_template,request,redirect,url_for,session
import plotly
import json
import scripts.finance as funds ## finance.py
from bs4 import BeautifulSoup as bs
import requests


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.route("/",methods=['GET','POST'])

def stock_symbols():
    greetings = ""
    if request.method == 'POST':
        symbol= request.form['ticker']
        greetings = symbol
        session['my_var'] = symbol
        return redirect(url_for('plot'))
    return render_template("symbol.html",greetings=greetings)

@app.route("/plot")
def plot():
    symbol = session.get('my_var', None)
    greetings = "{} historical prices".format(symbol)
    ## This gets the data and create a plot
    plot = funds.get_data(symbol,"hist") 
    ## To display the plot as html we have to put into a json            ## format.
    plotly_plot = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("home.html", greetings=greetings, plotly_plot= plotly_plot)

@app.route("/dividends")
def dividends():
    symbol = session.get('my_var', None)
    greetings = "{} dividends".format(symbol)
    ## This gets the data and create a plot
    plot = funds.get_data(symbol,"dividends") 
    ## To display the plot as html we have to put into a json            ## format.
    plotly_plot = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dividends.html", greetings=greetings, plotly_plot= plotly_plot)

@app.route("/news headline")
def news():
    change=True
    symbol = session.get('my_var', None)
    headers = {'User-Agent': ""}
    url="https://ca.finance.yahoo.com/quote/{}?p={}".format(symbol,symbol)
    page = requests.get(url,headers=headers)
    soup = bs(page.text, 'html.parser')
    quote_summary_table=soup.find(id="quoteNewsStream-0-Stream")
    table_rows = quote_summary_table.find_all('a')
    text = []
    value=[]
    if change == True:
        for row in (table_rows):
            text.append(row.text)
            value.append(row['href'])
        for i in range(len(value)):
            value[i] = "www.finance.yahoo.com" + value[i]
        for i in range(len(value)):
            text[i] = tuple((text[i],value[i]))
        change = False
    greetings = "top 3 news headlines"
    return render_template("news.html", greetings=greetings,text=text)
if __name__ == "__main__":
    app.directory='/'
    app.run(host='127.0.0.1', port=5000)