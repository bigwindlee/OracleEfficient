#!/usr/bin/env python

import os, sys, shutil, re
import subprocess
import configparser
import source_insight

#--------------------------------------------------------------------------------------------------
SOURCE_DIRS = [
     'psconfig.bat' 
    ,'ActiveX'      # not in 856
    ,'Apps' 
    ,'appserv' 
    ,'bin' 
    ,'build' 
    ,'class' 
    ,'lib' 
    ,'pgpsdk302'    # not in 856
    ,'secvault'   
    ,'TUXEDO'
    ,'utility'
    ,'WEB'
    ]

OPTIONAL_DIRS = ['ActiveX', 'pgpsdk302']

#--------------------------------------------------------------------------------------------------

def ConfigManager(filename):
    ret = {}
    config = configparser.ConfigParser()
    config.read(filename)
    ret['LocalRepos'] = config.get('DEFAULT', 'LocalRepos')
    ret['RemoteRepos'] = config.get('DEFAULT', 'RemoteRepos')
    ret['RemoteBuild'] = config.get('DEFAULT', 'RemoteBuild')
    ret['LjustWidth'] = config.getint('DEFAULT', 'LjustWidth')
    ret['JRE_DIR_TEMPL'] = config.get('DEFAULT', 'JRE_DIR_TEMPL')
    ret['VS_SLN_ZIP'] = config.get('DEFAULT', 'VS_SLN_ZIP')
    ret['FLAGS_PATH'] = config.get('DEFAULT', 'FLAGS_PATH')
    ret['MOVE_TO'] = config.get('DEFAULT', 'MOVE_TO')
    ret['SkippedDirs'] = config.get('DEFAULT', 'SkippedDirs')
    return ret
    

def WriteLog(LOG_ITEM, end='\n', file=sys.stdout, flush=False):
    if file is not None:
        print(LOG_ITEM, end=end, file=file, flush=flush)
        
    
def WINDOWS_COPY_TREE(src, dst):
    COPY_DIR_CMD = ' '.join(['Robocopy', '/E', src, dst])
    retcode = subprocess.call(COPY_DIR_CMD, stdout=subprocess.DEVNULL)
    if retcode not in [0, 1]:
        raise RuntimeError(('Robocopy failed(retcode=%d). From: ' + src + ' To: ' + dst) % retcode)


def COPY_BUILD(BUILD_RELEASE, LOG=None):    
    MAJOR_RELEASE = BUILD_RELEASE[:3]
    BUILD_DIR = DevConfig['RemoteBuild'].format(MAJOR_RELEASE, BUILD_RELEASE)
        
    # Check BUILD_DIR or input manually
    if not os.path.exists(BUILD_DIR):
        raise RuntimeError('TODO: Input remote build directory manually?')     # TODO
    
    # Check source directories ready
    for item in SOURCE_DIRS:
        if item not in OPTIONAL_DIRS:
            if not os.path.exists(os.path.join(BUILD_DIR, item)):
                LOG_ITEM = 'Error: No such file or directory: ' + os.path.join(BUILD_DIR, item)
                WriteLog(LOG_ITEM, file=LOG)
                raise RuntimeError(LOG_ITEM)
    
    # Check target directory
    TARGET_DIR = os.path.join(DevConfig['LocalRepos'], 'pt{0}-debug'.format(BUILD_RELEASE))
    if os.path.exists(TARGET_DIR):
        LOG_ITEM = 'Error: Already existing directory: ' + TARGET_DIR
        WriteLog(LOG_ITEM, file=LOG)
        raise RuntimeError(LOG_ITEM)
    else:
        os.mkdir(TARGET_DIR)
    
    #------------------------
    # Copy JRE
    #------------------------
    JRE = DevConfig['JRE_DIR_TEMPL'].format(MAJOR_RELEASE, MAJOR_RELEASE)
    if not os.path.isdir(JRE): 
        JRE = DevConfig['JRE_DIR_TEMPL'].format(MAJOR_RELEASE, BUILD_RELEASE)
        if not os.path.isdir(JRE):
            LOG_ITEM = 'Error: JRE directory is not existing.'
            WriteLog(LOG_ITEM, file=LOG)
            raise RuntimeError(LOG_ITEM)
       
    WriteLog('Copy JRE'.ljust(DevConfig['LjustWidth'], '.'), end='', file=LOG, flush=True)
    WINDOWS_COPY_TREE(JRE, os.path.join(TARGET_DIR, 'jre')) 
    WriteLog(' OK', file=LOG)

    #------------------------
    #Copy setup
    #------------------------
    if os.path.isdir(os.path.join(BUILD_DIR, r'SETUP\PsMpPIAInstall')):
        WriteLog(r'Copy SETUP\PsMpPIAInstall'.ljust(DevConfig['LjustWidth'], '.'), end='', file=LOG, flush=True)
        WINDOWS_COPY_TREE(os.path.join(BUILD_DIR, r'SETUP\PsMpPIAInstall'), 
            os.path.join(TARGET_DIR, r'SETUP\PsMpPIAInstall'))
        WriteLog(' OK', file=LOG) 
    
    # Copy source directory to target
    for item in SOURCE_DIRS:
        full_item = os.path.join(BUILD_DIR, item)
        if item in OPTIONAL_DIRS and not os.path.exists(full_item):
            continue
        WriteLog(' '.join(['Copy', item]).ljust(DevConfig['LjustWidth'], '.'), end='', file=LOG, flush=True)
        if os.path.isdir(full_item):
            WINDOWS_COPY_TREE(full_item, os.path.join(TARGET_DIR, item))
        else:
            shutil.copy(full_item, TARGET_DIR)
        WriteLog(' OK', file=LOG) 
    
    WriteLog('\nCopying files succeeded!', file=LOG)

    # Copy visual studio solution directory
    SLN_NAME = DevConfig['VS_SLN_ZIP'].format(MAJOR_RELEASE)
    if os.path.isfile(SLN_NAME):
        # Why is there "+1" below ? Because the first character '\n' is also counted but not printed.
        WriteLog('\nCopy VS solution files'.ljust(DevConfig['LjustWidth'] + 1, '.'), end='', file=LOG, flush=True)
        subprocess.check_call(' '.join(['unzip', '-q', SLN_NAME, '-d', TARGET_DIR]), stdout=subprocess.DEVNULL)
        WriteLog(' OK', file=LOG)
    else:
        WriteLog(' '.join(['\nWarning:', SLN_NAME, 'is not existing.']), file=LOG)

def get_skipped_dirs(filename):
    skipped = []
    if not os.path.isfile(filename):
        return skipped
        
    with open(filename, 'r') as input:
        for line in input:
            if line.strip().startswith('#'):
                skipped.append(line.strip()[1:].strip())
    
    return skipped            
        

def COPY_SRC_CODE(BUILD_RELEASE, LOG=None):    
    TARGET_DIR = os.path.join(DevConfig['LocalRepos'], 'pt{0}-debug'.format(BUILD_RELEASE))
    BUILD_DIR = DevConfig['RemoteBuild'].format(BUILD_RELEASE[:3], BUILD_RELEASE)
    REMOTE_SRC = os.path.join(BUILD_DIR, 'src')
        
    if not os.path.isdir(REMOTE_SRC):
        WriteLog('\nWarning: src is not existing.', file=LOG)
        return

    DST_SRC = os.path.join(TARGET_DIR, 'src')
    if not os.path.exists(DST_SRC):
        os.mkdir(DST_SRC)
        
    WriteLog('\nCopy src directory'.ljust(DevConfig['LjustWidth'] + 1, '.'), end='', file=LOG, flush=True)    
    for item in os.listdir(REMOTE_SRC):
        full_item = os.path.join(REMOTE_SRC, item)
        if os.path.isdir(full_item):
            if item not in get_skipped_dirs(DevConfig['SkippedDirs']):
                WINDOWS_COPY_TREE(full_item, os.path.join(DST_SRC, item))
        else:
            shutil.copy(full_item, DST_SRC)
    WriteLog(' OK', file=LOG)
                        
        
# Copy the source code into a specific directory and cleanse the code for source insight.        
def generate_src_for_si(BUILD_RELEASE, FLAGS_PATH, MOVE_TO):
    file_type = '*.h *.cpp *.java'
    src = os.path.join(DevConfig['LocalRepos'], 'pt{0}-debug'.format(BUILD_RELEASE), 'src')
    dst = os.path.join(DevConfig['LocalRepos'], BUILD_RELEASE, 'src')
    copy_cmd = 'robocopy {0} {1} {2} /S'.format(src, dst, file_type)
    retcode = subprocess.call(copy_cmd, stdout=subprocess.DEVNULL)
    if retcode not in [0, 1]:
        raise RuntimeError(('Robocopy failed(retcode=%d). From: ' + src + ' To: ' + dst) % retcode)

    source_insight.CleanseFileForSI(dst, FLAGS_PATH)
    zip_cmd = 'zip -r {0} {1}'.format(os.path.join(MOVE_TO, BUILD_RELEASE + ".zip"), "src") 
    os.chdir(dst + "\\..")
    subprocess.check_call(zip_cmd, stdout=subprocess.DEVNULL)
    os.chdir(DevConfig['LocalRepos'])
    shutil.rmtree(BUILD_RELEASE)
    
        
if __name__ == '__main__':
    from autoinstallpia import install_pia
    
    BASE_NAME = os.path.basename(sys.argv[0])
    if not sys.argv[1:]:
        print('Usage:\n\t%s <build_version>' % BASE_NAME)
        print('Examples:\n\t%s 856-808-R2' % BASE_NAME)
        print('\t%s 85429b' % BASE_NAME)
        os._exit(1)
        
    
    DevConfig = ConfigManager('config\\_ptdevenv.ini')
    COPY_BUILD(sys.argv[1], sys.stdout)
    
    print('\nInstall pia'.ljust(DevConfig['LjustWidth'] + 1, '.'), end='', file=sys.stdout, flush=True)
    install_pia(os.path.join(DevConfig['LocalRepos'], 'pt{0}-debug'.format(sys.argv[1])))
    WriteLog(' OK', file=sys.stdout)
    
    COPY_SRC_CODE(sys.argv[1], sys.stdout)
    
    print('\nCleanse source code for souce insight'.ljust(DevConfig['LjustWidth'] + 1, '.'), end='', file=sys.stdout, flush=True)
    generate_src_for_si(sys.argv[1], DevConfig['FLAGS_PATH'], DevConfig['MOVE_TO'])
    WriteLog(' OK', file=sys.stdout)
    
