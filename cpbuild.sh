#!/usr/bin/bash

BUILD_RELEASE=$1
MAJOR_RELEASE=${BUILD_RELEASE::3}
DST_DIR=/cygdrive/d/build

BUILD_DIR=/cygdrive/z/build/pt/pt${MAJOR_RELEASE}/${BUILD_RELEASE}/debug/WINX86/pt${BUILD_RELEASE}-debug
TARGET_DIR=${DST_DIR}/pt${BUILD_RELEASE}-debug

SOURCE_DIRS=(
psconfig.bat
#ActiveX
Apps
appserv
bin
build
class
lib
#pgpsdk302
secvault
TUXEDO
utility
WEB
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

copy_jre_dir(){
    if [ "${MAJOR_RELEASE}" == "854" ]; then
        JRE=/cygdrive/z/build/pt/ptdist/pt${MAJOR_RELEASE}/${MAJOR_RELEASE}/debug/WINX86/install_Windows.ora/jre
    elif [ "${MAJOR_RELEASE}" == "853" ]; then
        JRE=/cygdrive/z/build/pt/pt${MAJOR_RELEASE}/${MAJOR_RELEASE}/debug/WINX86/install_Windows.ora/jre
    else
        JRE=/cygdrive/z/build/pt/ptdist/pt${MAJOR_RELEASE}/${BUILD_RELEASE}/debug/WINX86/install_Windows.ora/jre
    fi
    
    if [ ! -d "${JRE}" ]; then
        echo ${JRE} : No such directory
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
       
    if [ "${MAJOR_RELEASE}" == "853" ]; then
        JRE64=/cygdrive/z/build/pt/pt${MAJOR_RELEASE}/${MAJOR_RELEASE}/debug/WINX86/install_Windows.ora/jre64
        if [ ! -d "${JRE64}" ]; then
            echo ${JRE64} : No such directory
            exit
        fi
        
        echo -n "Copy JRE64 ... ... "
        cp -rf "${JRE64}" "${TARGET_DIR}"
        if [ $? != 0 ]; then
            echo failed!
            exit
        else
            echo OK
        fi
    fi
}

if [[ $# != 1  || ${BUILD_RELEASE::2} != '85' ]]; then
    print_usage
    exit
fi


if [ ! -d "${BUILD_DIR}" ]; then
    echo ${BUILD_DIR} : No such directory
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

copy_jre_dir

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

echo
echo Copying files succeeded!
