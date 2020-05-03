from flask import jsonify
from __main__ import app

@app.errorhandler(400)
def bad_request(error = "Required data wasn't sent"):
    response = jsonify({'message': error})
    response.status_code = 400

    return response

@app.errorhandler(404)
def not_found(error = "Data not found"):
    response = jsonify({"message": error})
    response.status_code = 404

    return response

@app.errorhandler(500)
def internal_server_error(error = "Internal server error"):
    response = jsonify({"message": error})
    response.status_code = 500

    return response