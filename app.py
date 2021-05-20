from datetime import timedelta
from flask import Flask, render_template, url_for, request, redirect, session, flash, abort
from Processing import pubmed_request as pr
from Database.databasemanager import DatabaseManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "DEVKEYCHANGEPLEASE"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


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
        email = request.form['email']

        genes, diseases, uuid = pr.make_request(TOR, TAND, str(date), email)
        session['genes'] = genes
        session['diseases'] = diseases
        session['uuid'] = uuid

        return redirect(url_for('vis_results', genes=genes, diseases=diseases,
                                uuid=uuid))

    return render_template("search.html")


@app.route('/results', methods=['POST', 'GET'])
def vis_results():
    try:
        genes = session['genes']
        diseases = session['diseases']
        uuid = session['uuid']

        return render_template("results.html", genes=genes, diseases=diseases,
                               uuid=uuid)
    except KeyError:
        flash("Voer eerst een zoekopdracht uit of haal deze een op uit de "
              "database!")
        return redirect(url_for('search'))


@app.route('/history', methods=['POST', 'GET'])
def history():

    if request.method == 'POST':
        user_input_uuid = request.form['uuid']

        dm = DatabaseManager()
        genes, diseases, uuid = dm.retreieve_zoekopdracht(user_input_uuid)

        session['genes'] = genes
        session['diseases'] = diseases
        session['uuid'] = uuid

        return redirect(url_for('vis_results', genes=genes, diseases=diseases,
                                uuid=uuid))

    return render_template("history.html")


if __name__ == '__main__':
    app.run()
