from flask_sqlalchemy import *
from app import *
import json

import redis

from flask import request as r, jsonify as j


@app.route("/")
def index():
    return "<h1> welcome to 273 assignment 2</h1>"


@app.route("/v1/expenses", methods=['POST'])
def postmethod():
    # find the maximunm id in the database
    exp = request.get_json(force=True)
    name = exp['name']
    email = exp['email']
    category = exp['category']
    description = exp['description']
    link = exp['link']
    estimated_costs = exp['estimated_costs']
    submit_date = exp['submit_date']
    status = "pending"
    decision_date = ""

    exp = Expenses(name, email, category, description, link, estimated_costs, status, submit_date, decision_date)
    db.session.add(exp)
    db.session.commit()
    resp = {
        'id': exp.id,
        'name': exp.name,
        'email': exp.email,
        'category': exp.category,
        'description': exp.description,
        'link': exp.link,
        'estimated_costs': exp.estimated_costs,
        'submit_date': exp.submit_date,
        'status': exp.status,
        'decision_date': exp.decision_date
    }
    res = Response(response=json.dumps(resp), status=201, mimetype='application/json')
    return res






@app.route("/v1/expenses/<int:requestID>", methods=['GET'])
def getmethod(requestID):
    rd = Expenses.query.filter_by(id=requestID).first()
    if (rd != None):  # there is a row
        resp = {
            "id": rd.id,
            "name": rd.name,
            "email": rd.email,
            "category": rd.category,
            "description": rd.description,
            "link": rd.link,
            "estimated_costs": rd.estimated_costs,
            "submit_date": rd.submit_date,
            "status": rd.status,
            "decision_date": rd.decision_date
        }

        jresp = jsonify(resp)
        jresp.status_code = 200
        return jresp

    else:
        jresp = Response(status=404)
        return jresp


@app.route('/v1/expenses/<int:requestID>', methods=['PUT'])
def putmethod(requestID):
    exp = request.get_json(force=True)
    updateRow = Expenses.query.filter_by(id=requestID)
    if (updateRow != None):

        for key, value in exp.items():
            updateRow.update({key: value})
            db.session.commit()
            res = Response(status=202)
            return res


@app.route('/v1/expenses/<int:requestID>', methods=['DELETE'])
def deletemethod(requestID):
    deleteRow = Expenses.query.filter_by(id=requestID).first()
    if(deleteRow != None):
        db.session.delete(deleteRow)
        db.session.commit()
        res= Response(status=204)
        return res





if __name__ == "__main__":
    # sockFunc()
    CreateDB()

    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    r.set(1, '5001')
    app.run(debug=True, host='0.0.0.0', port=5001)
