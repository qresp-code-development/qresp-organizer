#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""qresp_config.

Usage:
  qresp_config collection <folder_name> [<path>]
  qresp_config paper <paper_name> [<path>]
  qresp_config info <paper_name> [<path>]
  qresp_config zenodo upload <paper_name> <token> [<path>] [--sandbox]
  qresp_config --version

Options:
  -h --help        Show this screen.
  --version        Show version.
  --collection	   Generates paper_collection which will host paper content of user(s) and creates a config file(qresp.ini).
  --paper_name 	   Name of the paper.
  --path 		   Path where the action should be triggered. Defaults to current location, if not specified.
  --paper		   Initializes a paper with a git repo.
  --info		   Provides information on how to clone the paper_name.git repo.
  --folder_name    Name of the paper collection.
  --token          Personal token generated from zenodo. Login to Zenodo to create an access token at https://zenodo.org/account/settings/applications/tokens/new/
  --zenodo upload  Initializes zenodo by creating metadata and registering token and uploads the paper to zenodo
  --sandbox        Uses sandbox url to upload to data
"""
from qresp_config.scripts.docopt import docopt
from qresp_config.scripts.util import *
from qresp_config.scripts.upload_to_zenodo import UploadToZenodo
import subprocess
import os


def main():
	args = docopt(__doc__, version='qresp 1.0.0')
	httpServicePath = ""
	globusServicePath = ""
	if args.get('paper'):
		paper_directory = cwd
		if args.get('<path>'):
			paper_directory = str(args.get('<path>'))
		checkIfGitExists(paper_directory)
		createFile(paper_directory)
		make_executable(paper_directory+"/"+"qresp_version_control.bash")
		subprocess.check_call([paper_directory+"/"+'qresp_version_control.bash', str(args.get('<paper_name>')), str(args.get('<path>'))])
	elif args.get('info'):
		paper_directory = cwd
		if args.get('<path>'):
			paper_directory = str(args.get('<path>'))
		checkIfGitExists(paper_directory)
		checkIfLogExists(paper_directory,str(args.get('<paper_name>')))
	elif args.get('collection'):
		folder_name = str(args.get('<folder_name>'))
		if args.get('<path>'):
			folder_name = str(args.get('<path>')) + "/" + folder_name
		else:
			folder_name = cwd + "/" + folder_name
		directory = create_folder(folder_name)
		print("Created folder ",folder_name)

		isHttpService = check_services("Is the folder " + folder_name +" publicly accessible by a http service? (Y/N) ","http")
		if isHttpService == "Y":
			httpServicePath = check_path("Enter http path/url pointing to the " + folder_name)

		isGlobusService = check_services("Is there a Globus service running on the server? (Y/N) ","globus")
		if isGlobusService == "Y":
			isGlobusServiceEndpoint = check_services("Is there a Globus endpoint pointing to the folder " + folder_name+"? (Y/N)","globus endpoint")
			if isGlobusServiceEndpoint == "Y":
				globusServicePath = check_path("Enter Globus endpoint pointing to the " + folder_name)

		isGitService =  check_services("Is there a git service running on the server? (Y/N) ","git")
		create_config(isHttpService,isGlobusService,isGitService,httpServicePath,globusServicePath,directory)
		print("Created file qresp.ini")
	elif args.get('zenodo'):
		if args.get('upload'):
			sandbox = False
			paper_name = str(args.get('<paper_name>'))
			if args.get('<path>'):
				paper_name = str(args.get('<path>')) + "/" + paper_name
			else:
				paper_name = cwd + "/" + paper_name
			if not paper_name or not os.path.exists(paper_name):
				sys.exit(paper_name+ " Missing directory or directory not found")
			token = str(args.get('<token>'))
			if not token:
				sys.exit("Please assign all scopes and generate a new token at https://zenodo.org/account/settings/applications/tokens/new/")
			checkIfZenodo = check_services("To upload to zenodo you would need to provide a title, description and a list of authors for your dataset. Would you like to continue? (Y/N) ","zenodo")
			if args.get('--sandbox'):
				sandbox = True
			if checkIfZenodo == "Y":
				title = request_metadata("Please enter a title for your dataset ")
				description = request_metadata("Please describe your dataset ")
				authorList = create_authors_list("Please enter the author and his/her affiliation as comma seperated values. For e.g. John Doe, University of Chicago ")
				metadata = create_metadata(title,description,authorList)
				print("Uploading Files. Please wait ....")
				uploadToZenodo = UploadToZenodo(token, paper_name, metadata, sandbox)
				uploadToZenodo.uploadImagesToZenodo()
				uploadToZenodo.uploadZipFileToZenodo()
				uploadToZenodo.uploadMetadaFileToZenodo()
				isPublish = check_services("Please check your upload at https://sandbox.zenodo.org/deposit. \n Would you like to publish this dataset to Zenodo. (Y/N). This is not reversible. ",
				"zenodo")
				if isPublish == "Y":
					record = uploadToZenodo.publishProjectToZenodo()
					sys.exit("Please enter "+record['links']['latest_html']+" in the Qresp curator zenodo section to curate and add metadata to this dataset")


