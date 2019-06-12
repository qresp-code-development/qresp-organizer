#!/bin/bash
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
