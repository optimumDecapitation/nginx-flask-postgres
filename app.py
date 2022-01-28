import datetime
import os
import json
import sqlalchemy

from flask import Flask, render_template, redirect, url_for, request
from forms import SignupForm

from models import Signups
from models import AlertUsers
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
rocket_user = os.environ['ROCKET_CHAT_USER']
rocket_password = os.environ['ROCKET_CHAT_PASSWORD']

@app.route("/", methods=('GET', 'POST'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        signup = Signups(name=form.name.data, email=form.email.data, date_signed_up=datetime.datetime.now())
        db_session.add(signup)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('signup.html', form=form)

# @app.route("/success")
# def success():
#     return "success!"

@app.route("/jack")
def success():
    return "jack!"

@app.route("/addition")
def addition ():
    all_args = request.args.to_dict()
    adden = all_args["adder"]
    addest = all_args["addest"]
    sum = int(adden) + int(addest)
    return json.dumps(sum)

@app.route("/division")
def divison ():
    all_args = request.args.to_dict()
    divider = all_args["divider"]
    dividest = all_args["dividest"]
    product = int(divider) / int(dividest)
    return json.dumps(product)

@app.route("/push_alert", methods=['POST'])
def push_alert():

    return "will totally push that later"

@app.route("/register_user", methods=['POST'])
def register_user():
    payload = request.json
    new_user = AlertUsers(name=payload["username"])
    db_session.add(new_user)
    db_session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 


@app.route("/list_users", methods=['GET'])
def list_users():
    qry = sqlalchemy.text("SELECT name FROM alert_users")
    resultset = db_session.execute(qry)
    results_as_dict = resultset.mappings().all()
    data = {}
    i = 0
    for row in results_as_dict:
        data[str(i)] = row["name"]
        i += 1
    data = dict(data)
    return json.dumps(data)
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
