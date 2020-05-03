from __main__ import app, mongo
from .errors import not_found, bad_request, internal_server_error

from flask import request, Response
from bson import json_util
from bson.objectid import ObjectId
import json, datetime, re

CV = mongo.db.CV
Jobs = mongo.db.jobs

# Agregar un usuario nuevo
@app.route('/cv', methods = ['POST'])
def create_cv():
    personalInfo = request.json['personalInfo']
    education = request.json['education']
    laboral = request.json['laboral']

    if personalInfo and education and laboral:
        cv = CV.insert(
            {'personalInfo': personalInfo, 'education': education, 'laboral': laboral}
        )
        
        jobs = Jobs.find({'profession': re.compile('^' + re.escape(personalInfo['profession']) + '$', re.IGNORECASE)})
        
        jobs = json.loads(json_util.dumps(jobs))
        cvId = json.loads(json_util.dumps(cv))['$oid']

        if len(jobs) > 0:
            for job in jobs:
                job['matchedP'] = 20
                job['cvId'] = cvId

                if matchSchooling(job['schooling'], education):
                    job['matchedP'] += 16

                if job['experience'] <= personalInfo['experience']:
                    job['matchedP'] += 16
                    
                if matchAge(job['age'], personalInfo['birthdate']):
                    job['matchedP'] += 16
                    
                job['matchedP'] += matchLanguges(job['languages'], personalInfo['languages'])
                
                job['matchedP'] += matchAptitudes(job['aptitudes'], personalInfo['aptitudes'])
                
                Jobs.update_one({'_id': ObjectId(job['_id']['$oid'])}, {'$inc': {'seen': 1}})
            
            jobs.sort(key = lambda job: job['matchedP'], reverse = True)
        else: 
            return not_found('Por el momento no hay trabajos con los que seas compatible')

        return Response(json_util.dumps(jobs), mimetype = 'application/json')
    else:
        return bad_request()

def matchSchooling(jSchool, cSchools):
    for school in cSchools:
        if school['degree'].lower() == jSchool.lower():
            return True
            
    return False

def matchAge(range, birthdate):
    ind = range.find('-')
    minA = int(range[:ind])
    maxA = int(range[ind + 1:])
    birthdate = datetime.datetime.strptime(birthdate, '%d/%M/%Y')
    age = datetime.datetime.now().year - birthdate.year

    if minA < age and maxA > age:
        return True

    return False

def matchLanguges(jLanguages, cLanguages):
    percent = 16 / len(jLanguages)
    matchedP = 0

    for JLanguage in jLanguages:
        for cLanguage in cLanguages:
            if JLanguage['language'] == cLanguage['language']:
                matchedP += percent

    return matchedP

def matchAptitudes(jAptitudes, cAptitudes):
    percent = 16 / len(jAptitudes)
    matchedP = 0

    for JAptitude in jAptitudes:
        for cAptitude in cAptitudes:
            if JAptitude['aptitude'] == cAptitude['aptitude']:
                matchedP += percent

    return matchedP

# Mostrar cv
@app.route('/cv/<id>', methods = ['GET'])
def get_cv(id):
    cv = CV.find_one({'_id': ObjectId(id)})

    if cv:
        response = json_util.dumps(cv)

        return Response(response, mimetype = 'application/json')
    else:
        return not_found()

@app.route('/cv/match/<id>/<cv>', methods=['POST'])
def match_job(id, cv):
    print(request.json)
    jb = request.json
    print('1', jb)
    del jb['_id'], jb['matchedP'], jb['cvId']
    print('2', jb)
    job = Jobs.update_one({'_id': ObjectId(id)}, {'$set': jb})
    print('3', job.matched_count, job.modified_count)

    if job.matched_count > 0:
        print('if 1')
        if job.modified_count > 0:
            print('if 2')
            return {'message': 'Job succesfully matched'}
        else:
            print('else 1')
            return internal_server_error('Se produjo un error al aplicar a este trabajo')
    else:
        print('else 2')
        return not_found('No se encontró el trabajo al que desea aplicar')