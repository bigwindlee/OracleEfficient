#!/usr/bin/env python

import os

def generate_config_list(ps_home, appserver_name):
    conf = []
    
    PS_CFG_HOME = os.path.join(ps_home, appserver_name)
    PS_CFG_HOME = os.path.normpath(PS_CFG_HOME)
    PS_CFG_HOME = os.path.normcase(PS_CFG_HOME)
    PS_CFG_HOME = PS_CFG_HOME.replace('\\', '/');
    
    index = PS_CFG_HOME.rfind('pt85')
    if index == -1:
        raise RuntimeError('Cannot get PT version from ' + PS_CFG_HOME)
    else:
        PT_VERSION = PS_CFG_HOME[index+2:index+5]
    
    JSL_PORT = PT_VERSION + '0'
    HTTP_PORT = '8' + PT_VERSION
    
    if PT_VERSION == '856':
        BEA_HOME = 'C:/wls/wls1221'  # starting from 856-802-I1
    elif PT_VERSION == '855':
        BEA_HOME = 'C:/wls/wls1213'
    elif PT_VERSION == '854':
        BEA_HOME = 'C:/wls/Wls1212WithJAVA725Installed'
    else:
        raise RuntimeError('Not supported')    
    
    # PS_CFG_HOME
    conf.append('PS_CFG_HOME=' + PS_CFG_HOME);

    # Where you want to install the PeopleSoft Pure Internet Architecture
    # The default installation directory: <PIA_HOME>\webserv\<DOMAIN_NAME>
    # The default location for PIA_HOME is the same as PS_CFG_HOME
    conf.append('PIA_HOME=' + PS_CFG_HOME)

    # Oracle WebLogic domains
    conf.append('SERVER_TYPE=weblogic')
    conf.append('BEA_HOME=' + BEA_HOME)
    conf.append('USER_ID=system')
    conf.append('USER_PWD=Passw0rd')
    conf.append('USER_PWD_RETYPE=Passw0rd')

    conf.append('INSTALL_ACTION=CREATE_NEW_DOMAIN')
    conf.append('DOMAIN_TYPE=NEW_DOMAIN')
    conf.append('DOMAIN_NAME=peoplesoft')
    conf.append('INSTALL_TYPE=SINGLE_SERVER_INSTALLATION')

    # the Integration Gateway User and Password
    conf.append('IGW_USERID=administrator')
    conf.append('IGW_PWD=Passw0rd')
    conf.append('IGW_PWD_RETYPE=Passw0rd')

    # the AppServer Domain Connection Password
    # This value would be the same value you assign for Domain Connection Password in PSADMIN, if one provided. 
    conf.append('APPSRVR_CONN_PWD=Passw0rd')
    conf.append('APPSRVR_CONN_PWD_RETYPE=Passw0rd')

    # Specify a name for the PeopleSoft website
    conf.append('WEBSITE_NAME=ps')

    # Enter port numbers and summaries
    conf.append('APPSERVER_NAME=' + appserver_name)
    conf.append('JSL_PORT=' + JSL_PORT)
    conf.append('HTTP_PORT=' + HTTP_PORT)
    conf.append('HTTPS_PORT=443')
    conf.append('AUTH_DOMAIN=.us.oracle.com')     # Authentication Token Domain:(optional)

    # Please enter the Name of the Web Profile used to configure the webserver. The user id and
    # password will be used to retrieve the web profile from the database. (NOTE: Available
    # preset web profile names are "PROD", "TEST", "DEV", and "KIOSK")
    conf.append('WEB_PROF_NAME=DEV')
    conf.append('WEB_PROF_PWD=Passw0rd')
    conf.append('WEB_PROF_PWD_RETYPE=Passw0rd')

    # Select the Report Repository location
    conf.append('REPORTS_DIR=C:/psreports')    
    
    return conf
    

def generate_resp_file(filename, conflist):
    with open(filename, 'w') as resp:
        for line in conflist:
            resp.write(line + '\n');


if __name__ == '__main__':
    import sys, socket
    import subprocess
    
    if not sys.argv[1:]:
        print('Usage:\n\t%s PS_HOME_DIR [APPSERVER_NAME]' % os.path.basename(sys.argv[0]))
        os._exit(1)

    PS_HOME = sys.argv[1]
    PS_HOME = os.path.normpath(PS_HOME)
    
    if sys.argv[2:]:
        APPSERVER_NAME = sys.argv[2]
    else:
        APPSERVER_NAME = socket.gethostname()
        
    if os.path.exists(os.path.join(PS_HOME, APPSERVER_NAME)):
        print('Error: Existing file or directory: ' + os.path.join(PS_HOME, APPSERVER_NAME))
        os._exit(2)
    
    RESP_FILE = os.path.join(PS_HOME, r'SETUP\PsMpPIAInstall\scripts\resp_file_feng.txt')
    CMD = os.path.join(PS_HOME, r'SETUP\PsMpPIAInstall\setup.bat')
    
    if not os.path.isfile(CMD):
        print('Error: No such file: ' + CMD)
        os._exit(3)
    
    CMD += r' -i silent -DRES_FILE_PATH='
    CMD += RESP_FILE
        
    generate_resp_file(RESP_FILE, generate_config_list(PS_HOME, APPSERVER_NAME))
    subprocess.check_call(CMD)
    
    LOG_FILE = os.path.join(PS_HOME, APPSERVER_NAME, r'webserv\piainstall_peoplesoft.log')
    if os.path.isfile(LOG_FILE):
        subprocess.check_call('start ' + LOG_FILE, shell=True)
        
