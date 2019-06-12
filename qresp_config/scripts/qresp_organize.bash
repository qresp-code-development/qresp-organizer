#!/bin/bash
PROJECTDIR="$PWD"
PROJECTNAME="$1"

if [[ "$2" != "" &&  "$2" != "None" ]]; then

PROJECTDIR="$2"

fi

if [[ -d ${PROJECTDIR} && -d ${PROJECTDIR}/${PROJECTNAME} ]]; then


if [ ! -d "${PROJECTDIR}"/"${PROJECTNAME}"/charts ]; then
mkdir "${PROJECTDIR}"/"${PROJECTNAME}"/charts # the git repo with charts folder
fi

if [ ! -d "${PROJECTDIR}"/"${PROJECTNAME}"/datasets ]; then
mkdir "${PROJECTDIR}"/"${PROJECTNAME}"/datasets # the git repo with charts folder
fi

if [ ! -d "${PROJECTDIR}"/"${PROJECTNAME}"/scripts ]; then
mkdir "${PROJECTDIR}"/"${PROJECTNAME}"/scripts # the git repo with charts folder
fi

if [ ! -d "${PROJECTDIR}"/"${PROJECTNAME}"/tools ]; then
mkdir "${PROJECTDIR}"/"${PROJECTNAME}"/tools # the git repo with charts folder
fi

if [ ! -d "${PROJECTDIR}"/"${PROJECTNAME}"/doc ]; then
mkdir "${PROJECTDIR}"/"${PROJECTNAME}"/doc # the git repo with charts folder
fi
echo "Created charts, datasets,scripts,tools & doc folders in ${PROJECTDIR}/${PROJECTNAME}"
chmod 777 "${PROJECTDIR}"/"${PROJECTNAME}"

else

echo "Error: ${PROJECTDIR}/${PROJECTNAME} does not exist!"

fi

