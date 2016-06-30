#!/usr/bin/bash

BUILD_VERSION=$1
TERACOPY="/cygdrive/c/Program Files/TeraCopy/TeraCopy.exe"
JRE=/cygdrive/z/build/pt/ptdist/pt854/854/debug/WINX86/install_Windows.ora/jre

BUILD_DIR=/cygdrive/z/build/pt/pt854/${BUILD_VERSION}/debug/WINX86/pt${BUILD_VERSION}-debug

TARGET_DIR=/cygdrive/d/build/pt${BUILD_VERSION}-debug
SOURCE_DIRS=(
ActiveX
Apps
appserv
bin
build
class
lib
pgpsdk302
secvault
TUXEDO
utility
WEB
psconfig.bat
src
)

print_usage(){
cat <<EOF
Usage:
    $0 <build_version>  
    Example: 
        $0 85405a
EOF
}

if [ $# != 1 ]
then
    print_usage
    exit
fi

#if [ ! -x "${TERACOPY}" ]; then
#    echo ${TERACOPY} : No such file
#    exit
#fi

if [ ! -d "${BUILD_DIR}" ]; then
    echo ${BUILD_DIR} : No such directory
    exit
fi

if [ ! -d "${JRE}" ]; then
    echo ${JRE} : No such directory
    exit
fi

if [ -d "${TARGET_DIR}" ]; then
    echo WARNING: "${TARGET_DIR}" is existing!
    while true; do
        read -p "Do you want to delete it? (Y/N) " yn
        case $yn in
            [Yy]* ) 
                rm -rf "${TARGET_DIR}"
                break
                ;;
            [Nn]* ) 
                exit
                ;;
            * ) 
                echo "Please answer yes or no."
                ;;
        esac
    done
fi

mkdir -p "${TARGET_DIR}"
if [ $? != 0 ]; then
    echo mkdir -p "${TARGET_DIR}" : failed!
    exit
fi

echo -n "Copy JRE ... ... "
cp -rf "${JRE}" "${TARGET_DIR}"
if [ $? != 0 ]; then
    echo failed!
    exit
else
    echo OK
fi

for var in ${SOURCE_DIRS[@]};do
    if [ ! -e "${BUILD_DIR}/${var}" ]; then
        echo "${BUILD_DIR}/${var}" : No such file or directory
        exit
    else
        echo -n Copy "${var} ... ... "
        cp -rf "${BUILD_DIR}/${var}" "${TARGET_DIR}"
        if [ $? != 0 ]; then
            echo failed!
            exit
        else
            echo OK
        fi
    fi
done

mkdir -p "${TARGET_DIR}/SETUP"
if [ $? != 0 ]; then
    echo mkdir -p "${TARGET_DIR}/SETUP" : failed!
    exit
fi

echo -n Copy "SETUP/PsMpPIAInstall ... ... "
cp -rf "${BUILD_DIR}/SETUP/PsMpPIAInstall" "${TARGET_DIR}/SETUP"
if [ $? != 0 ]; then
    echo failed!
    exit
else 
    echo OK
fi

echo
echo Copying files succeeded!

if [ -f "~/peopletools854.tgz" ]; then
    tar zxvf ~/peopletools854.tgz -C "${TARGET_DIR}"
fi