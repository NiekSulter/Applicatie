from datetime import timedelta
from flask import Flask, render_template, url_for, request, redirect, \
    session, flash, abort, make_response
from Processing import pubmed_request as pr
from Database.databasemanager import DatabaseManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "DEVKEYCHANGEPLEASE"


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Static home page with instructions for using the application
    :return: home.html
    """
    return render_template("home.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    """
    GET: static page where the user can build a search query
    POST: retrieves data from form, and calls the make_request function.
    Afterwords a session with the search UUID is created. If the user has a
    history session the current search gets added to it. The user is
    redirected to the results page.
    :return: search.html and a genpanel names list
    """
    if request.method == 'POST':
        term = request.form['queryBox']
        date = request.form['datepicker']
        genpanel = request.form['genpanels']
        email = request.form['email']
        search_history = []
        uuid = pr.make_request(term, str(date), email, genpanel)
        make_session("uuid", uuid, 2)

        if session.get('history'):
            search_history = session['history']

        search_history.append(uuid)

        if len(search_history) > 5:
            search_history = search_history[-5:]

        session['history'] = search_history
        make_session("history", search_history, 60*24*365)

        return redirect(url_for('vis_results'))

    # Retrieving the genpanel names from the database

    dm = DatabaseManager()

    genpanels = dm.retrieve_genpanel_ids()

    dm.close_conn()

    return render_template("search.html", genpanels=genpanels)


@app.route('/results', methods=['POST', 'GET'])
def vis_results():
    """
    If this page gets loaded without an active session the user gets
    redirected to the search page, a flash message appears instructing the
    user to create a search first. If the user has an active session they
    will be shown the results of their search.
    :return: results page with all the result data.
    """
    try:
        uuid = session['uuid']
        dm = DatabaseManager()
        genes, diseases, uuiddb, query, genpanel, date \
            = dm.retreieve_zoekopdracht(uuid)

        return render_template("results.html", genes=genes, diseases=diseases,
                               uuid=uuid, query=query, genpanel=genpanel,
                               date=date)
    except KeyError:
        flash("Please run a search or retrieve one from the archived "
              "searches before visiting this page!")
        return redirect(url_for('search'))


@app.route('/history', methods=['POST', 'GET'])
def history():
    """
    Gets the UUID of a previous search and redirects the user to the
    results page, showing the results of the aforementioned search.
    :return: redirect to the vis_results function.
    """

    if request.method == 'POST':
        user_input_uuid = request.form['uuid']

        dm = DatabaseManager()
        genes, diseases, uuid, query, genpanel, date =\
            dm.retreieve_zoekopdracht(user_input_uuid)

        make_session("uuid", uuid, 2)

        return redirect(url_for('vis_results'))

    hislis = []

    if session.get('history'):
        hislis = reversed(session['history'])

    return render_template("history.html", hislis=hislis)


def make_session(name, value, expiry):
    """
    function to make a session in the user's browser.
    :param name: name of the session
    :param value: the value of the session
    :param expiry: the expiry time of the session
    :return: None
    """
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=expiry)
    session[name] = value


if __name__ == '__main__':
    app.run()
