import os
import stat
import configparser
import errno
import sys
flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
#current working directory
cwd = os.getcwd()

bash_cmd= """#!/bin/bash
PROJECTDIR="$PWD"
PROJECTNAME="$1"

if [[ "$2" != "" &&  "$2" != "None" ]]; then

	PROJECTDIR="$2"

fi

if [ -d "${PROJECTDIR}" ]; then

	if [[ -d ${PROJECTDIR}/${PROJECTNAME} || -d ${PROJECTDIR}/${PROJECTNAME}.git ]]; then

		echo "Error: ${PROJECTDIR}/${PROJECTNAME} already exists, doing nothing!"

	else

		mkdir "${PROJECTDIR}"/"${PROJECTNAME}".git # the git repo
		mkdir "${PROJECTDIR}"/"${PROJECTNAME}"     # the latest snapshot of the repo

		cd "${PROJECTDIR}"
		git init --bare "${PROJECTNAME}".git

		cd ${PROJECTNAME}.git/hooks

		cat > post-receive << EOF
#!/bin/bash
TARGET="${PROJECTDIR}/${PROJECTNAME}"
GIT_DIR="${PROJECTDIR}/${PROJECTNAME}.git"
BRANCH="master"

while read oldrev newrev ref
do
# only checking out the master (or whatever branch you would like to deploy)
if [[ \$ref = refs/heads/\$BRANCH ]]; then
echo "Ref \$ref received. Deploying \${BRANCH} branch to production..."
git --work-tree=\$TARGET --git-dir=\$GIT_DIR checkout -f
else
echo "Ref \$ref received. Doing nothing: only the \${BRANCH} branch may be deployed on this server."
fi
done
EOF
		chmod +x post-receive

		echo "In order to push data: git clone ssh://<username>@<servername>:${PROJECTDIR}/${PROJECTNAME}.git"

		cd "${PROJECTDIR}"/"${PROJECTNAME}"
		cat > "${PROJECTNAME}".log << EOF
"In order to push data: git clone ssh://<username>@<servername>:${PROJECTDIR}/${PROJECTNAME}.git"
EOF
		chmod 0775 "${PROJECTNAME}".log
		fi

else

	echo "Error: Project Directory does not exist or is not valid"

fi





"""

def make_executable(filename):
	""" Makes files executable
	:param filename: path to file
	:return: None
	"""
	st = os.stat(filename)
	os.chmod(filename, st.st_mode | stat.S_IEXEC)

def create_folder(folder):
	""" Creates folder for paper collection
	:param folder: folder path
	:return: folder
	"""
	if not os.path.exists(folder):
		os.makedirs(folder)
		os.chmod(folder, stat.S_IRGRP | stat.S_IWGRP | stat.S_IWUSR | stat.S_IRUSR | stat.S_IROTH | stat.S_IXUSR | stat.S_IXGRP)
	return folder

def create_config(isHttpService,isGlobusService,isGitService,httpServicePath,globusServicePath,directory):
	""" Creates config file for qresp to read
	:param isHttpService: (Y/N) is there a http service running
	:param isGlobusService: (Y/N) is there a globus endpoint for file transfer
	:param isGitService: (Y/N) is git running in the server
	:param httpServicePath: http url for paper collection
	:param globusServicePath: globus url for data transfer
	:param directory: path containing qresp ini
	:return: None
	"""
	config = configparser.ConfigParser()
	config['SERVICE'] = {}
	config['SERVICE.PATH'] = {}
	config['SERVICE']['isHttpService'] = isHttpService
	config['SERVICE']['isGlobusService'] = isGlobusService
	config['SERVICE']['isGitService'] = isGitService
	if httpServicePath:
		config['SERVICE.PATH']['http_Service_Path'] = httpServicePath
	if globusServicePath:
		config['SERVICE.PATH']['globus_Service_Path'] = globusServicePath
	with open(directory+'/qresp.ini', 'w+') as configfile:
		config.write(configfile)

def create_metadata(title,description,authors):
	""" Creates the metadata json for zenodo
	:param title: Title for data uploaded to zenodo
	:param description: Description for dataset
	:param authors: Authors for dataset
	:return: json
	"""
	data = {}
	data['metadata'] = {}
	data['metadata']['title'] = str(title)
	data['metadata']['upload_type'] = 'dataset'
	data['metadata']['description'] = str(description)
	data['metadata']['creators'] = authors
	return data

def create_authors_list(prompt):
	""" Creates a list of authors
	:param prompt: Prompts to ask user
	:return: list: authors
	"""
	authorList = []
	while True:
		authors = input(prompt).strip()
		authorDict = {}
		authorAfflTemp = authors.split(",")
		authorDict['name'] = authorAfflTemp[0]
		if len(authorAfflTemp) > 1:
			authorDict['affiliation'] = authorAfflTemp[1]
		authorList.append(authorDict)
		service = input("Do you want to add another author? (Y/N)")
		if service == "Y" :
			continue
		elif service == "N" :
			break
	return authorList

def request_metadata(prompt):
	""" Prompts for services
	:param prompt: Prompts to ask user
	:return: service
	"""
	while True:
		service = input(prompt).strip().upper()
		if service:
			break
	return service


def check_services(prompt,type):
	""" Prompts for services
		:param prompt: Prompts to ask user
		:param type: Type of service
		:return: service
	"""
	while True:
		service = input(prompt).strip().upper()
		if service == "Y":
			break
		elif service == "N":
			print("Please refer to http://qresp.org/Data_Organization.html#data-location-and-access to run a, ", type," service.")
			break
		else:
			print("Invalid input")
			continue
	return service

def check_path(prompt):
	""" Check for path
	:param prompt: prompts to ask for service
	:return: path
	"""
	while True:
		path = input(prompt).strip().upper()
		if path:
			break
		else:
			print("Path cannot be empty, recheck your input")
			continue
	return path

def checkIfLogExists(directory,paper_name):
	""" Check if log exists in the directory
	:param directory: Path where log file exists
	:param paper_name: Name of paper
	:return: None
	"""
	if not os.path.exists(directory+"/"+paper_name):
		sys.exit(directory + "not found")
	else:
		try:
			fobj = open(directory+"/"+paper_name+"/"+paper_name+".log")
			print(fobj.readline())
		except:
			sys.exit(directory+"/"+paper_name+"/"+paper_name+".log" + " not found")


def checkIfGitExists(directory):
	""" Check if Git exists in the directory
	:param directory: Path for directory
	:return: None
	"""
	if not os.path.exists(directory):
		sys.exit(directory + "not found")
	else:
		try:
			config = configparser.ConfigParser()
			config.read(directory+'/qresp.ini')
			if "N" in config['SERVICE']['isgitservice']:
				sys.exit("Cannot run qresp_config paper or info without git service")
		except Exception as e:
			print(e)
			sys.exit("Cannot run qresp_config paper or info without git service. qresp.ini file not found in "+directory)

def createFile(directory):
	""" Creates bash file in directory
	:param directory: Path where bash file
	:return: None
	"""
	try:
		file_handle = os.open(directory+'/qresp_version_control.bash', flags)
	except OSError as e:
		if e.errno == errno.EEXIST:
			pass
		else:
			raise
	else:
		with os.fdopen(file_handle, 'w') as file_obj:
			file_obj.write(bash_cmd)

