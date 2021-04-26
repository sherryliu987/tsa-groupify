from flask import send_from_directory, redirect, url_for, render_template, request
from .make_groups import compute_groups, generate_graphs

from application import app

GROUPS = {}
GRAPH = ""
csv_file = ""


@app.route("/", methods=['GET', 'POST'])
@app.route("/main", methods=['GET', 'POST'])
def home():
    global csv_file
    if request.method == 'POST':
        csv_file = request.form.get('people_csv')
        print(csv_file)
        num_groups = request.form.get('num_groups')

        return redirect(url_for('calc_groups', num_groups=num_groups))
    global GROUPS
    global GRAPH
    GROUPS = {}
    GRAPH = ""
    csv_file = ""
    return render_template("main.html")


@app.route("/calc_groups/<num_groups>")
def calc_groups(num_groups):
    global GROUPS
    GROUPS = compute_groups(csv_file, num_groups)
    global GRAPH
    GRAPH = generate_graphs()
    # print(GRAPH)
    return redirect(url_for('groups'))

@app.route("/graphs")
def graphs():
    return GRAPH + "<a href=/groups><button>Back to groups</button></a>"

@app.route("/groups")
def groups():
    return render_template("groups.html", groups=GROUPS)


@app.route("/about")
def about():
    return render_template("about.html")

