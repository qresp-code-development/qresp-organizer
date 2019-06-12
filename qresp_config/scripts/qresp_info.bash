#!/bin/bash
PROJECTDIR="$PWD"
PROJECTNAME="$1"

if [[ "$2" != "" &&  "$2" != "None" ]]; then

PROJECTDIR="$2"

fi
if [[ -d "${PROJECTDIR}"/"${PROJECTNAME}" && -f "${PROJECTDIR}"/"${PROJECTNAME}"/"${PROJECTNAME}.log" ]]; then
filename="${PROJECTDIR}"/"${PROJECTNAME}"/"${PROJECTNAME}.log"
while read -r line; do
echo "$line"  
done < $filename

else
echo "The path or file ${PROJECTDIR}/${PROJECTNAME}/${PROJECTNAME}.log does not exist"
fi