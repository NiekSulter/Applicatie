from flask import Flask, render_template, url_for, request
from Processing import pubmed_request as pr

app = Flask(__name__)
app.config['SECRET_KEY'] = "DEVKEYCHANGEPLEASE"

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("home.html")


@app.route('/search', methods=['POST', 'GET'])
def search():

    if request.method == 'POST':
        TOR = request.form.getlist('and')
        TAND = request.form.getlist('or')
        date = request.form['datepicker']
        genpanel = request.form['genpanels']

        pr.make_request(TOR, TAND, str(date))

    return render_template("search.html")


@app.route('/results', methods=['POST', 'GET'])
def vis_results():
    return render_template("results.html")


if __name__ == '__main__':
    app.run()
