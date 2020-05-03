from __main__ import app, mongo
from .errors import not_found, bad_request, internal_server_error

from flask import request, jsonify, Response
from bson import json_util
from bson.objectid import ObjectId
import json
import datetime

Jobs = mongo.db.jobs

# Agregar trabajo nuevo
@app.route('/jobs', methods=['POST'])
def create_jobs():
    name = request.json['name']
    enterprise = request.json['enterprise']
    salary = request.json['salary']
    description = request.json['description']
    age = request.json['age']
    experience = request.json['experience']
    profession = request.json['profession']
    schooling = request.json['schooling']
    languages = request.json['languages']
    aptitudes = request.json['aptitudes']

    if name and enterprise and salary and description and age and profession and schooling:
        id = Jobs.insert(
            {'name': name, 'enterprise': enterprise, 'salary': salary, 'description': description, 'age': age, 'experience': experience,
                'profession': profession, 'schooling': schooling, 'languages': languages, 'aptitudes': aptitudes, 'seen': 0, 'matched': 0, 'cvs': []}
        )

        response = {'message': 'El trabajo fue creado exitosamente.'}
        return response
    else:
        return bad_request()

# Mstrar listado de trabajos
@app.route('/jobs/<enterprise>', methods=['GET'])
def get_jobs(enterprise):
    jobs = Jobs.find({'enterprise': enterprise})

    if Jobs:
        response = json_util.dumps(jobs)
        return Response(response, mimetype='application/json')
    else:
        return not_found()

# Eliminar trabajo
@app.route('/jobs/<id>', methods=['DELETE'])
def delete_job(id):
    job = Jobs.delete_one({'_id': ObjectId(id)})

    if job.deleted_count == 1:
        response = jsonify({'message': 'Documento eliminado correctamente'})
        return response
    else:
        return not_found()
