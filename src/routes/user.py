from __main__ import app, mongo
from .errors import not_found, bad_request, internal_server_error

from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
import json
import datetime

Users = mongo.db.users

# Login
@app.route('/login', methods = ['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    if email and password:
        user = json_util.dumps(Users.find_one({'email': email}))
        usr = json.loads(user)
        
        if usr is not None:
            if check_password_hash(usr['password'], password):
                expires = datetime.timedelta(days = 30)
                access_token = create_access_token(usr['_id']['$oid'], expires_delta = expires)

                usr['_id'] = usr['_id']['$oid']
                usr['token'] = access_token
                user = json_util.dumps(usr)

                return Response(user, mimetype = 'application/json')
            else:
                return not_found("El correo electrónico y la contraseña que ingresaste no coinciden con nuestros registros. Por favor, revisa e inténtalo de nuevo.")
        else:
            return not_found("El correo electrónico y la contraseña que ingresaste no coinciden con nuestros registros. Por favor, revisa e inténtalo de nuevo.")
    else:
        return bad_request()


# Agregar un usuario nuevo
@app.route('/users', methods = ['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    enterprise = request.json['enterprise']

    if enterprise and password and email:
        hashed_password = generate_password_hash(password)
        id = Users.insert(
            {'name': name, 'email': email, 'password': hashed_password, 'enterprise': enterprise}
        )

        response = {'id': str(id), 'name': name, 'email': email,'enterprise': enterprise}
        return response
    else:
        return bad_request()

# Mstrar listado de usuarios
@app.route('/users', methods = ['GET'])
def get_users():
    users = Users.find()

    if users:
        response = json_util.dumps(users)
        return Response(response, mimetype = 'application/json')
    else:
        return not_found()
# Mostrar usuario
@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    user = Users.find_one({'_id': ObjectId(id)})

    if user:
        response = json_util.dumps(user)

        return Response(response, mimetype = 'application/json')
    else:
        return not_found()

# Modificar usuario
@app.route('/users/<id>', methods = ['PUT'])
def update_user(id):
    if request.json['enterprise'] and request.json['email'] and request.json['name']:
        user = {'name': request.json['name'], 'email': request.json['email'], 'enterprise': request.json['enterprise']}
        result = Users.update_one({'_id': ObjectId(id)}, {'$set': user})

        if result.matched_count > 0:
            if result.modified_count > 0:
                return {'message': 'User succesfully updated'}
            else:
                return internal_server_error()
        else:
            return not_found()
    else:
        return bad_request()

# Eliminar usuario
@app.route('/users/<id>', methods = ['DELETE'])
def delete_user(id):
    user = Users.delete_one({'_id': ObjectId(id)})
    
    if user.deleted_count == 1:
        response = jsonify({'message': 'Documento eliminado correctamente'})
        return response
    else:
        return not_found()