#!/usr/bin/bash

print_usage(){
cat <<EOF
Usage:
    $0 <Resolution_ID>  
    Example: 
        $0 123456
EOF
}

if [ $# != 1 ]; then
    print_usage
    exit
fi

Res_ID=$1

re='^[0-9]{6}$'
if ! [[ ${Res_ID} =~ $re ]] ; then
   echo "Error: Not a valid Resolution ID"
   exit
fi

Local_DIR=/cygdrive/d/POC/POC-${Res_ID}
Remote_DIR=/cygdrive/z/pt/poc_idda/POC/POC-${Res_ID}
Logfile=${Res_ID}.log

if [ -d "${Local_DIR}" ]; then
    echo Error: Already existing directory ${Local_DIR}
    exit
fi

if [ -d "${Remote_DIR}" ]; then
    echo Error: Already existing directory ${Remote_DIR}
    exit
fi

mkdir -p ${Local_DIR}
if [ $? != 0 ]; then
    echo mkdir -p ${Local_DIR} : failed!
    exit
fi

mkdir -p ${Remote_DIR}
if [ $? != 0 ]; then
    echo mkdir -p ${Remote_DIR} : failed!
    exit
fi

echo ${Local_DIR} > /tmp/${Logfile}
echo ${Remote_DIR} >> /tmp/${Logfile}
echo cp POC-${Res_ID}-01.zip /cygdrive/z/pt/poc_idda/POC/POC-${Res_ID}\ >> /tmp/${Logfile}
echo cksum \\\\psbldfs\\dfs\\pt\\poc_idda\\POC\\POC-${Res_ID}\\*.zip >> /tmp/${Logfile}

echo Directory created. Please cat /tmp/${Logfile}
