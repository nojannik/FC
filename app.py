import requests, json
from jinja2 import Template
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import os
import random
app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/", methods=["GET", "POST"])
def login():
        # allow user into protected view
    error = None
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        payload = {"login": login, "password": password,"entity": 1,"reset": 0}
        url = "http://35.194.156.171/api/index.php/login"
        headers = {'content-type': 'application/json'}
        r = requests.post(url, headers=headers, json=payload)
        response = r.json()
        if (r.status_code is 200):
            global token
            token = response['success']['token']
            session['api_session_token'] = token

            return redirect(url_for('panel'))
        else:
            error = r.status_code,'Invalid credentials. Try again'
            return render_template('login.html', error=error)

    return render_template('login.html', error=error)


    #login to web service
@app.route("/panel")
def panel():
    error=None
    list = requests.get('http://35.194.156.171/api/index.php/products?sortfield=t.ref&sortorder=ASC&limit=99999', headers={'DOLAPIKEY': token})
    # "r" translate "response" to DICt format:
    product_list = json.loads(list.text)

    return render_template('panel.html',product_list=product_list,error=error)

@app.route("/new_item", methods=["GET", "POST"])
def new_item():
    error = None
    if request.method == 'POST':
        ref = request.form['ref']
        label = request.form['label']
        size = request.form['size']
        price = request.form['price']
        payload_newitem = {"label" : label, "ref": ref, "price": price, "description": size}
        url_newitem = "http://35.194.156.171/api/index.php/products"
        headers_newitem = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
        r = requests.post(url_newitem, headers=headers_newitem, json=payload_newitem)
        response = r.json()
        if (r.status_code is 200):
            requests.put('http://35.194.156.171/api/index.php/products/{}'.format(response),headers=headers_newitem,json={"status":"1","status_buy":"1"})
            return render_template('new_item.html')
        else:
            error = r.status_code,"Something is wrong"
            return render_template('new_item.html',error=error)
    return render_template('new_item.html',error=error)

# I SKIP THIS MODULE FOR NOW, MY SQL DOESN'T CONNECT TO EXTERNAL HOST
'''
@app.route("/aurora",methods=["GET","POST"])
def aurora():
    error=None

        #incoming = request.form['incoming']
        #outgoing = request.form['outgoing']
    date = ""
    headers = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
    url ="http://35.194.156.171/api/index.php/stockmovements?sortfield=t.rowid&sortorder=ASC&limit=100&sqlfilters=value%3E0%20or%20value%3C0%20and%20tms%20LIKE%20'%25{}%25'".format(date)
    r = requests.get(url,headers=headers)
    if request.method == 'GET':
        request.form['date']
        movements = json.loads(r.text)
        return render_template('aurora.html',movements=movements)
        if request.form['incoming'] and request.form['outgoing']== True:
            e_or_c = "E0%20or%20value%3C"
            headers = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
            url ="http://35.194.156.171/api/index.php/stockmovements?sortfield=t.rowid&sortorder=ASC&limit=100&sqlfilters=value%3{}0%20and%20tms%20LIKE%20'%25{}%25'".format(e_or_c,date)
            r = requests.get(url,headers=headers)
            movements = json.loads(r.text)
            return render_template('aurora.html',movements=movements)
        if request.form['incoming'] == True:
            e_or_c = "C"
            headers = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
            url ="http://35.194.156.171/api/index.php/stockmovements?sortfield=t.rowid&sortorder=ASC&limit=100&sqlfilters=value%3{}0%20and%20tms%20LIKE%20'%25{}%25'".format(e_or_c,date)
            r = requests.get(url,headers=headers)
            movements = json.loads(r.text)
            return render_template('aurora.html',movements=movements)
        if request.form['outgoing'] == True:
            e_or_c = "E"
            headers = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
            url ="http://35.194.156.171/api/index.php/stockmovements?sortfield=t.rowid&sortorder=ASC&limit=100&sqlfilters=value%3{}0%20and%20tms%20LIKE%20'%25{}%25'".format(e_or_c,date)
            r = requests.get(url,headers=headers)
            movements = json.loads(r.text)
            return render_template('aurora.html',movements=movements)
    return render_template('aurora.html')
'''

@app.route("/pos",methods=["GET","POST"])
def pos():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        phone = request.form['phone']
        fax = request.form['fax']
        email = request.form['email']
        json = {"name": name,"address": address,"town": city,"status": "1","phone": phone,"fax": fax,"email": email,"client": "1","code_client":name[random.randint(1,len(name))]+phone+name,"prospect": "0","fournisseur": "0","status":"1","entity":"1","country": "Philippines","country_id": "182","country_code": "PH"}
        headers = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
        url = "http://35.194.156.171/api/index.php/thirdparties"
        r = requests.post(url,headers=headers,json=json)
        response = r.json()
        if (r.status_code is 200):
            socid = response['ref']
            return render_template('pos2.html')
        else:
            error = r.status_code,"Something is wrong"
            return render_template('pos.html',error=error)
    return render_template('pos.html',error=error)
@app.route("/pos2",methods=["GET","POST"])
def pos2():
    pos()
    error= None
    if request.method == 'POST':






if __name__ == '__main__':
    app.run(debug=True)
# a=requests.post('http://35.194.156.171/api/index.php/products',json={"label": "12345", "ref": "12345666","width" : "12","height" : "12","length":"10"})
