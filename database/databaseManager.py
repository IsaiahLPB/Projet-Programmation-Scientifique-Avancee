#!/usr/bin/env python3

from pymongo import MongoClient
import pymongo.errors
import numpy as np
import bson
import pickle

username, password, host, dbname = 'user0', 'pwd0', '127.0.0.1', 'results'
client = MongoClient('mongodb://%s:%s@%s/%s' % (username, password, host, dbname))
db = client.results

def AlreadyExist(collectionName, collectionList):
    for elt in collectionList:
        if elt == collectionName:
            return True
    return False

def AlreadyExistHash(hashCode):
    for elt in db.list_collection_names():
        exp = db[elt]
        for data in exp.find({"Init": True}):
            if data["Json_Hash"] == hashCode:
                return True
    return False

def DeleteCollection(collectionName):
    try:
        if AlreadyExist(collectionName, db.list_collection_names()):
            db.drop_collection(collectionName)
        else:
            print(collectionName + " doesn't exist, cannot delete a non existing collection")
    
    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def CreateExperience(experienceName, jsonFile, jsonHash, potential):
    try:
        if AlreadyExist(experienceName, db.list_collection_names()):
            print(experienceName + " already exist, cannot overright an existing collection")
        else:
            experience = db[experienceName]

            potentialDB = bson.binary.Binary(pickle.dumps(potential, protocol = 2))

            data = { "Init": True, "Json_File": jsonFile, "Json_Hash": jsonHash, "Potential": potentialDB }
            experience.insert_one(data)

    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def InsertMatrix(experienceName, time, psiRe, psiIm):
    try:
        if AlreadyExist(experienceName, db.list_collection_names()):
            experience = db[experienceName]

            psiReDB = bson.binary.Binary(pickle.dumps(psiRe, protocol = 2))
            psiImDB = bson.binary.Binary(pickle.dumps(psiIm, protocol = 2))

            data = { "Init": False, "Time": time, "Psi_Real": psiReDB, "Psi_Imaginary": psiImDB }
            experience.insert_one(data)
        else:
            print(experienceName + " doesn't exist, create it before inserting data")

    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def GetPotential(experienceName):
    try:
        if AlreadyExist(experienceName, db.list_collection_names()):
            experience = db[experienceName]

            for data in experience.find({"Init": True}):
                matdata = data["Potential"]
                mat = pickle.loads(matdata)

            return mat
        else:
            print(experienceName + " doesn't exist, cannot get the potential of a non existing experience")
    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def GetJsonFile(experienceName):
    try:
        if AlreadyExist(experienceName, db.list_collection_names()):
            experience = db[experienceName]

            for data in experience.find({"Init": True}):
                filedata = data["Json_File"]

            return filedata
        else:
            print(experienceName + " doesn't exist, cannot get the Json file of a non existing experience")

    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def GetLastState(experienceName):
    try:
        if AlreadyExist(experienceName, db.list_collection_names()):
            experience = db[experienceName]

            lastTime = -1
            for data in experience.find({"Init": False}):
                if data["Time"] > lastTime:
                    lastTime = data["Time"]
                    psiReData = data["Psi_Real"]
                    psiRe = pickle.loads(psiReData)
                    psiImData = data["Psi_Imaginary"]
                    psiIm = pickle.loads(psiImData)

            return (lastTime, psiRe, psiIm)
        else:
            print(experienceName + " doesn't exist, cannot get the last state of a non existing experience")
    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def GetStates(experienceName):
    try:
        if AlreadyExist(experienceName, db.list_collection_names()):
            experience = db[experienceName]

            stateList = []
            for data in experience.find({"Init": False}):
                time = data["Time"]
                psiReData = data["Psi_Real"]
                psiRe = pickle.loads(psiReData)
                psiImData = data["Psi_Imaginary"]
                psiIm = pickle.loads(psiImData)
                stateList.append((time, psiRe, psiIm))

            return stateList
        else:
            print(experienceName + " doesn't exist, cannot get the list of states of a non existing experience")
    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))



def test():
    print(db.list_collection_names())

    #test cases where the program must do nothing in the database
    CreateExperience('test', 'json.json', 'oui', np.eye(3))
    InsertMatrix('new', 0, np.eye(3),np.eye(3))
    DeleteCollection('new')
    print(db.list_collection_names())

    #test the case where DeleteCollection can delete an experience
    DeleteCollection('test')
    print(db.list_collection_names())

    #test the case where CreateExperience can create an experience
    CreateExperience('test', 'json.json', np.eye(3))
    #test the case where InsertMatrix can add an element to the experience
    InsertMatrix('test', 0, np.eye(3),np.eye(3))
    print(db.list_collection_names())

    #test the cases where getters can't find data in the database
    GetPotential('new')
    GetJsonFile('new')
    GetLastState('new')
    GetStates('new')

    #test the cases where getters find data in the database
    print(GetPotential('test'))
    print(GetJsonFile('test'))
    print(GetLastState('test'))
    print(GetStates('test'))