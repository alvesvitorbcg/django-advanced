import os
from flask import Flask, jsonify,request, make_response,abort
import config
import json

app= Flask(__name__)

@app.before_request
def do_something_whenever_a_request_comes_in():
    auth = request.headers.get('Authorization')
    if not auth:
        return "Please provide header"

@app.route('/api/v1/calendars', methods=['GET'])
def get_calendars():

    try:
        get_json_data = read_json_file('all_calendars.json')
        return jsonify(get_json_data)
    except Exception as e:
        response = make_response(jsonify(message=str(e)),400)
        abort(response)


@app.route('/api/v1/reference-calendars', methods=['GET'])
def get_reference_calendars():

    try:
        get_json_data = read_json_file('all_reference_calendars.json')
        return jsonify(get_json_data)
    except Exception as e:
        response = make_response(jsonify(message=str(e)),400)
        abort(response)

@app.route('/api/v1/campaign-matrix', methods=['GET'])
def get_campaign_matrix():

    try:
        get_json_data = read_json_file('campaign_matrix.json')
        return jsonify(get_json_data)
    except Exception as e:
        response = make_response(jsonify(message=str(e)),400)
        abort(response)

@app.route('/api/v1/products', methods=['GET'])
def get_products():

    try:
        get_json_data = read_json_file('products.json')
        return jsonify(get_json_data)
    except Exception as e:
        response = make_response(jsonify(message=str(e)),400)
        abort(response)

@app.route('/api/v1/detailed-table', methods=['GET'])
def get_detailed_table_data():

    try:
        get_json_data = read_json_file('detailed_table_data.json')
        return jsonify(get_json_data)
    except Exception as e:
        response = make_response(jsonify(message=str(e)),400)
        abort(response)



def read_json_file(file_name:str):
    with open(config.FILE_PATH + file_name , "r") as json_file:
    # load the JSON object using json.loads()
        json_data = json.loads(json_file.read())
    return json_data


if __name__ == '__main__':
    app.run(debug= True)