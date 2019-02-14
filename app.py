import requests, json
from jinja2 import Template
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import os
import random
from datetime import datetime
#from flask_paginate import Pagination, get_page_args
app = Flask(__name__)
app.secret_key = os.urandom(16)
#users = list(range(200))
@app.route("/", methods=["GET", "POST"])
def login():
        # allow user into protected view
    error = None
    if request.method == 'POST':
        login = request.form['username']
        password = request.form['password']
        payload = {"login": login, "password": password,"entity": 1,"reset": 0}
        url = "http://35.187.251.233/api/index.php/login"
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

#def get_users(offset=0, per_page=200):
#    return users[offset: offset + per_page]
    #login to web service
@app.route("/panel",methods=["GET","POST"])
def panel():
    error=None
    if request.method == 'POST':
        search = request.form['search']
    #page, per_page,offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    #list = requests.get('http://35.187.251.233/api/index.php/products?sortfield=t.ref&sortorder=ASC&limit=200&page={}'.format(page), headers={'DOLAPIKEY': token})
        list = requests.get("http://35.187.251.233/api/index.php/products?sortfield=t.ref&sortorder=ASC&sqlfilters=ref%20LIKE%20'%25{}%25'".format(search), headers={'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'})
    # "r" translate "response" to DICT format:
        product_list = json.loads(list.text)
        return render_template('panel.html',product_list=product_list,error=error)
    #total = len(users)
    #pagination_users = get_users(offset=offset, per_page=per_page)
    #pagination = Pagination(page=page,per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('panel.html',error=error)
    #users=pagination_users,page=page,per_page=per_page,pagination=pagination,

@app.route("/new_item", methods=["GET", "POST"])
def new_item():
    error = None
    if request.method == 'POST':
        ref = request.form['ref']
        label = request.form['label']
        size = request.form['size']
        price = request.form['price']
        payload_newitem = {"label" : label, "ref": ref, "price": price, "description": size}
        url_newitem = "http://35.187.251.233/api/index.php/products"
        headers_newitem = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
        r = requests.post(url_newitem, headers=headers_newitem, json=payload_newitem)
        response = r.json()
        if (r.status_code is 200):
            requests.put('http://35.187.251.233/api/index.php/products/{}'.format(response),headers=headers_newitem,json={"status":"1","status_buy":"1"})
            return render_template('new_item.html')
        else:
            error = r.status_code,"Something is wrong"
            return render_template('new_item.html',error=error)
    return render_template('new_item.html',error=error)


@app.route("/aurora",methods=["GET","POST"])
def aurora():
    error=None
        #incoming = request.form['incoming']
        #outgoing = request.form['outgoing']
    if request.method == 'POST':
        date = request.form['date']
        headers = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
        url ="http://35.187.251.233/api/index.php/stockmovements?sortfield=t.rowid&sortorder=ASC&sqlfilters=tms%20like%20'%25{}%25'".format(date)
        r = requests.get(url,headers=headers)
        movements = json.loads(r.text)


        return render_template('aurora.html',movements=movements)

    return render_template('aurora.html')

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
        json = {"name": name,"address": address,"town": city,"status": "1","phone": phone,"fax": fax,"email": email,"client": "1","code_client":name+datetime.now().isoformat(timespec='seconds')+phone\
        +name[random.randint(1,len(name))],"prospect": "0","fournisseur": "0","status":"1","entity":"1","country": "Philippines","country_id": "182","country_code": "PH"}
        headers = {'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'}
        url = "http://35.187.251.233/api/index.php/thirdparties"
        r = requests.post(url,headers=headers,json=json)
        response = r.json()
        if (r.status_code is 200):
            global socid
            socid = response
            return redirect(url_for('pos2'))
        else:
            error = r.status_code,"Something is wrong"
            return render_template('pos.html',error=error)
    return render_template('pos.html',error=error)

@app.route("/pos2",methods=["GET","POST"])
def pos2():
    error= None

    list = requests.get("http://35.187.251.233/api/index.php/products?sortfield=t.rowid&sortorder=ASC&limit=0", headers={'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'})
    product_list = json.loads(list.text)
    t = json.dumps(product_list)
    if request.method == 'POST':
        item1 = request.form['item1']
        item2 = request.form['item2']
        item3 = request.form['item3']
        item4 = request.form['item4']
        item5 = request.form['item5']
        item6 = request.form['item6']
        item7 = request.form['item7']
        item8 = request.form['item8']
        item9 = request.form['item9']
        item10 = request.form['item10']

        price1 = request.form['price1']
        price2 = request.form['price2']
        price3 = request.form['price3']
        price4 = request.form['price4']
        price5 = request.form['price5']
        price6 = request.form['price6']
        price7 = request.form['price7']
        price8 = request.form['price8']
        price9 = request.form['price9']
        price10 = request.form['price10']

        qty1 = request.form['qty1']
        qty2 = request.form['qty2']
        qty3 = request.form['qty3']
        qty4 = request.form['qty4']
        qty5 = request.form['qty5']
        qty6 = request.form['qty6']
        qty7 = request.form['qty7']
        qty8 = request.form['qty8']
        qty9 = request.form['qty9']
        qty10 = request.form['qty10']

        discount1 = request.form['discount1']
        discount2 = request.form['discount2']
        discount3 = request.form['discount3']
        discount4 = request.form['discount4']
        discount5 = request.form['discount5']
        discount6 = request.form['discount6']
        discount7 = request.form['discount7']
        discount8 = request.form['discount8']
        discount9 = request.form['discount9']
        discount10 = request.form['discount10']

        checkno = request.form['checkno']
        cardno = request.form['cardno']
        sino = request.form['sino']

        info = {"socid": socid,"statut": "0","billed": "1","user_author_id": "1","user_valid": "1","lines":[\
        {"qty": qty1,"subprice": price1,"product_type": "0","fk_product": item1,"remise_percent": discount1},\
        {"qty": qty2,"subprice": price2,"product_type": "0","fk_product": item2,"remise_percent": discount2},\
        {"qty": qty3,"subprice": price3,"product_type": "0","fk_product": item3,"remise_percent": discount3},\
        {"qty": qty4,"subprice": price4,"product_type": "0","fk_product": item4,"remise_percent": discount4},\
        {"qty": qty5,"subprice": price5,"product_type": "0","fk_product": item5,"remise_percent": discount5},\
        {"qty": qty6,"subprice": price6,"product_type": "0","fk_product": item6,"remise_percent": discount6},\
        {"qty": qty7,"subprice": price7,"product_type": "0","fk_product": item7,"remise_percent": discount7},\
        {"qty": qty8,"subprice": price8,"product_type": "0","fk_product": item8,"remise_percent": discount8},\
        {"qty": qty9,"subprice": price9,"product_type": "0","fk_product": item9,"remise_percent": discount9},\
        {"qty": qty10,"subprice": price10,"product_type": "0","fk_product": item10,"remise_percent": discount10},\
        ],"array_options": {"options_sino": sino,"options_checkno": checkno,"option_cardno": cardno},"ref": datetime.now().isoformat(timespec='seconds')}
        order = requests.post('http://35.187.251.233/api/index.php/orders',headers={'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'},json=info)
        r = json.loads(order.text)
        if (order.status_code is 200):
            json_validate = {"idwarehouse": 1,"notrigger": 0}
            validate = requests.post('http://35.187.251.233/api/index.php/orders/{}/validate'.format(r),headers={'DOLAPIKEY': token,'Content-Type': 'application/json','Accept': 'application/json'},json=json_validate)
            return redirect(url_for('pos'))


    return render_template('pos2.html',error=error,product_list=product_list)





if __name__ == '__main__':
    app.run(debug=True)
# a=requests.post('http://35.194.156.171/api/index.php/products',json={"label": "12345", "ref": "12345666","width" : "12","height" : "12","length":"10"})
