#/bin/bash

overage run --source="." manage.py test
REPORT=`coverage report`
echo "${REPORT}"
RESULT=`echo ${REPORT} | sed -e 's/.* //g' | sed -e 's/%//g'`
COMMENT=${1:-"This is auto commit by coverage"}
if [ ${RESULT} -gt 80 ]; then
    git remote set-url origin `git remote -v | awk '{print $2}' | sed -e "s#https://github.com/#git@github.com:#g" | head -1`
    git add -A
    git commit -a -m "${COMMENT}"
    git push
    exit 0
else
    "WARN: Coverage report value less than 80%"
    exit 1
fi