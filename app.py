import requests
import json
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask import session
import os
app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/login", methods=["GET", "POST"])
def login():
        # allow user into protected view
    error = None
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        payload = {"login": login, "password": password,"entity": 1,"reset": 0}
        url = "http://<url>/api/index.php/login"
        headers = {'content-type': 'application/json'}
        r = requests.post(url, headers=headers, json=payload)
        response = r.json()
        if (r.status_code is 200):
            token = response['success']['token']
            session['api_session_token'] = token
            return redirect(url_for('panel'))
        else:
            error = 'Invalid credentials. Try again'
            return render_template('login.html', error=r.status_code)

    return render_template('login.html', error=error)


    #login to web service


if __name__ == '__main__':
    app.run(debug=True)
