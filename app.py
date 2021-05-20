from datetime import timedelta
from flask import Flask, render_template, url_for, request, redirect, session, flash, abort, make_response
from Processing import pubmed_request as pr
from Database.databasemanager import DatabaseManager

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
        email = request.form['email']
        search_history = []

        genes, diseases, uuid = pr.make_request(TOR, TAND, str(date), email)
        make_session("uuid", uuid, 2)

        if session['history']:
            search_history = session['history']

        search_history.append(uuid)

        if len(search_history) > 5:
            search_history = search_history[-5:]

        session['history'] = search_history
        make_session("history", search_history, 60*24*365)

        return redirect(url_for('vis_results', genes=genes, diseases=diseases,
                                uuid=uuid))

    return render_template("search.html")


@app.route('/results', methods=['POST', 'GET'])
def vis_results():
    try:
        uuid = session['uuid']
        dm = DatabaseManager()
        genes, diseases, uuiddb = dm.retreieve_zoekopdracht(uuid)

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

        # session['uuid'] = uuid
        make_session("uuid", uuid, 2)

        return redirect(url_for('vis_results', genes=genes, diseases=diseases,
                                uuid=uuid))

    hislis = reversed(session['history'])

    return render_template("history.html", hislis=hislis)


def make_session(name, value, expiry):
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=expiry)
    session[name] = value


if __name__ == '__main__':
    app.run()
