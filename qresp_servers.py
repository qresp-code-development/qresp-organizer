#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from pymongo import MongoClient
import json
import requests
		
def createJson(server_url,maintainer_emails):
	data = {}
	data['qresp_server_url'] = server_url
	qresp_maintainer_emails = [str(maintainer_email).strip() for maintainer_email in maintainer_emails.split(",")]
	data['qresp_maintainer_emails'] = qresp_maintainer_emails
	data['isActive'] = 'Yes'
	json_data = json.loads(json.dumps(data))
	return json_data

def insertServer(coll,server_url,maintainer_emails):
	json_data = createJson(server_url,maintainer_emails)
	coll.find_one_and_update({'qresp_server_url':json_data['qresp_server_url']},{"$set":json_data},upsert=True)
	all_json_data_cursor = coll.find({},{'_id': False})
	all_json_data = [all_json for all_json in all_json_data_cursor]
	return all_json_data

def deActivateServer(coll,server_url):
	coll.find_one_and_update({'qresp_server_url':json_data['qresp_server_url']},{'isActive':'No'})
	
	
def checkIfServerRunning(coll,insert_server_url=None):
	if insert_server_url is not None:
		try:
			req = requests.get(insert_server_url+"/REST/papers/GetSearchOptionsForPapers",verify=False, timeout=10)
		except:
			error_msg = "Cannot reach the server with the address " + insert_server_url +" Please recheck"
			sys.exit(error_msg)
	else:
		try:
			for doc in coll.find():
				server_url = doc['qresp_server_url']
				req = requests.get(server_url+"/REST/papers/GetSearchOptionsForPapers",verify=False, timeout=3)
				if not req.text:
					deActivateServer(coll,server_url)
		except:
			deActivateServer(coll,server_url)

if __name__ == '__main__':
	db = None
	#mongo DB properties
	ip = "paperstack.uchicago.edu:27017"
	dbname = "qresp_servers"
	collection = "servers"
	username = "qresp_server_admin"
	password = "qresp_user_pwd"
	server_url = ""
	maintainer_emails = ""
	#insertion if arguments given
	if len(sys.argv) == 3:
		server_url = str(sys.argv[1]).strip()
		maintainer_emails = str(sys.argv[2]).strip()
	client=MongoClient(ip)
	if client is not None:
		db=client[dbname]
		db.authenticate(username, password)
	if db is not None:
		coll = db[collection]
	if server_url and maintainer_emails and coll:
		checkIfServerRunning(coll,server_url)
		server_json = insertServer(coll,server_url,maintainer_emails)
		if server_json:
			print("Inserted new server with servername ",server_url," and maintainer email ",maintainer_emails)
			with open('qresp_servers.json', 'w') as outfile:
				json.dump(server_json, outfile)
	else:
		checkIfServerRunning(coll) #method call every day
		