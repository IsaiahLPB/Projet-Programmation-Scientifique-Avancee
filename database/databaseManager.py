#!/usr/bin/env python3

from pymongo import MongoClient
import pymongo.errors
import numpy as np
import bson
import pickle

#the basic user of the database to be able to log in
username, password, host, dbname = 'user0', 'pwd0', '127.0.0.1', 'results'
client = MongoClient('mongodb://%s:%s@%s/%s' % (username, password, host, dbname))
#the database we use to keep our results
db = client.results

def AlreadyExist(collectionName):
    """
	@brief if the experience exists, it returns true, if the experience does not exist, it returns false.

	@param a string that is the name of a collection representing an experience.
	@return a boolean
	"""
    for elt in db.list_collection_names():
        if elt == collectionName:
            return True
    return False

def AlreadyExistHash(hashCode):
    """
	@brief if the hash code already exists in an experience, returne true, if it does not, return false.

	@param the hash code of a json file.
	@return a boolean
	"""
    for elt in db.list_collection_names():
        exp = db[elt]
        for data in exp.find({"Init": True}):
            if data["Json_Hash"] == hashCode:
                return True
    return False

def DeleteCollection(collectionName):
    """
	@brief if the collection exists, it delete it from the database.

	@param a string that is the name of a collection representing an experience.
	@return nothing
	"""
    try:
        if AlreadyExist(collectionName):
            db.drop_collection(collectionName)
        else:
            print(collectionName + " doesn't exist, cannot delete a non existing collection")
    
    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def CreateExperience(experienceName, jsonFile, jsonHash, potential):
    """
	@brief create a collection for the experience and put the json file, json hash and potential matrix into the collection.

	@param a string that is the name of a collection representing an experience, a json file, the hash of a json file, a matrix that represent the potential
	@return nothing
	"""
    try:
        experience = db[experienceName]

        potentialDB = bson.binary.Binary(pickle.dumps(potential, protocol = 2))

        data = { "Init": True, "Json_File": jsonFile, "Json_Hash": jsonHash, "Potential": potentialDB }
        experience.insert_one(data)

    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def InsertMatrix(experienceName, time, psiRe, psiIm):
    """
	@brief if the experience exists, put the state with the time and the matrixes in the collection.

	@param a string that is the name of a collection representing an experience, the time of the state you want to put in the database, a matrix that represent the real part of Psi, a matrix that represent the imaginary part of Psi
	@return nothing
	"""
    try:
        if AlreadyExist(experienceName):
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
    """
	@brief get the potential of the experience.

	@param a string that is the name of a collection representing an experience.
	@return mat: the potential of the experience.
	"""
    try:
        if AlreadyExist(experienceName):
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
    """
	@brief get the json file of the experience.

	@param a string that is the name of a collection representing an experience.
	@return filedata: the potential of the experience.
	"""
    try:
        if AlreadyExist(experienceName):
            experience = db[experienceName]

            for data in experience.find({"Init": True}):
                filedata = data["Json_File"]

            return filedata
        else:
            print(experienceName + " doesn't exist, cannot get the Json file of a non existing experience")

    except pymongo.errors.OperationFailure as e:
        print("ERROR: %s" % (e))

def GetLastState(experienceName):
    """
	@brief get the last calculated state of the experience.

	@param a string that is the name of a collection representing an experience.
	@return lastTime: the last time of the experience.
            psiRe: the real part of the last time of the experience
            psiRe: the imaginary part of the last time of the experience
	"""
    try:
        if AlreadyExist(experienceName):
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
    """
	@brief get all the states of the experience.

	@param a string that is the name of a collection representing an experience.
	@return stateList: the list of all the states of the experience.
	"""
    try:
        if AlreadyExist(experienceName):
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
    CreateExperience('test', 'json.json', 'oui', np.eye(3))
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

    print(AlreadyExistHash('non'))
    print(AlreadyExistHash('oui'))

def test_pres():
    DeleteCollection('Présentation')
    CreateExperience('Présentation', 'presentation.json', 'nosj.noitatneserp', np.eye(3))
    InsertMatrix('Présentation', 0, np.eye(3), np.eye(3))
    InsertMatrix('Présentation', 1, 2 * np.eye(3), 2 * np.eye(3))
    InsertMatrix('Présentation', 2, 3 * np.eye(3), 3 * np.eye(3))
    print(db.list_collection_names())
    print(GetJsonFile('Présentation'))
    print(GetPotential('Présentation'))
    print(GetStates('Présentation'))
test_pres()