#!/usr/bin/env python3

from pymongo import MongoClient
import pymongo.errors
import numpy as np
import bson
import pickle

username, password, host, dbname = 'user0', 'pwd0', '127.0.0.1', 'results'
client = MongoClient('mongodb://%s:%s@%s/%s' % (username, password, host, dbname))

def PutMatrixInDB(experienceName, experienceHash, time, psiRe, psiIm, potential):
    try:
        db = client.results
        matrix = db.matrix

        psiReDB = bson.binary.Binary(pickle.dumps(psiRe, protocol = 2))
        psiImDB = bson.binary.Binary(pickle.dumps(psiIm, protocol = 2))
        potentialDB = bson.binary.Binary(pickle.dumps(potential, protocol = 2))

        data = { "Experience": experienceName, "Hash": experienceHash, "Time": time, "Psi_Real": psiReDB, "Psi_Imaginary": psiImDB, "Potential": potentialDB }
        matrix.insert_one(data).inserted_id

    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))
