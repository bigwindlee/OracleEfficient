#!/usr/bin/env python

import os, sys, shutil
import subprocess


SOURCE_DIRS = [
    'psconfig.bat', 
    'ActiveX',      # not in 856
    'Apps', 
    'appserv', 
    'bin', 
    'build', 
    'class', 
    'lib', 
    'pgpsdk302',    # not in 856
    'secvault',   
    'TUXEDO', 
    'utility', 
    'WEB', 
    'src' ]

OPTIONAL_DIRS = ['ActiveX', 'pgpsdk302']   
    
def WINDOWS_COPY_TREE(src, dst):
    COPY_DIR_CMD = ' '.join(['Robocopy', '/E', src, dst])
    if subprocess.call(COPY_DIR_CMD, stdout=subprocess.DEVNULL) != 1:
        raise RuntimeError('Robocopy failed. From: ' + src + ' To: ' + dst)


def COPY_BUILD(BUILD_RELEASE, LOG=sys.stdout):    
    MAJOR_RELEASE = BUILD_RELEASE[:3]
    TARGET_DIR = 'pt' + BUILD_RELEASE + '-debug'
    BUILD_DIR = os.path.join(r'\\psbldfs\dfs\build\pt', 'pt' + MAJOR_RELEASE, 
        BUILD_RELEASE + '\\debug\\WINX86\\' + TARGET_DIR)
        
    # Check BUILD_DIR or input manually
    if not os.path.exists(BUILD_DIR):
        raise RuntimeError('TODO: Input remote build directory manually?')     # TODO
    
    # Check source directories ready
    for item in SOURCE_DIRS:
        if item not in OPTIONAL_DIRS:
            if not os.path.exists(os.path.join(BUILD_DIR, item)):
                LOG_ITEM = 'Error: No such file or directory: ' + os.path.join(BUILD_DIR, item)
                print(LOG_ITEM, file=LOG)
                raise RuntimeError(LOG_ITEM)
    
    # Check target directory
    TARGET_DIR = os.path.join(r'D:\build', TARGET_DIR)
    if os.path.exists(TARGET_DIR):
        LOG_ITEM = 'Error: Already existing directory: ' + TARGET_DIR
        print(LOG_ITEM, file=LOG)
        raise RuntimeError(LOG_ITEM)
    else:
        os.mkdir(TARGET_DIR)
    
    # Copy JRE
    if MAJOR_RELEASE in ['854', '855']:
        JRE = os.path.join(r'\\psbldfs\dfs\build\pt\ptdist\pt' + MAJOR_RELEASE, MAJOR_RELEASE, 
            r'debug\WINX86\install_Windows.ora\jre')
    elif MAJOR_RELEASE == '856':
        JRE = os.path.join(r'\\psbldfs\dfs\build\pt\ptdist\pt' + MAJOR_RELEASE, BUILD_RELEASE, 
            r'debug\WINX86\install_Windows.ora\jre')
    else:
        JRE = None
       
    if os.path.isdir(JRE):
        print('Copy JRE'.ljust(40, '.'), end='', file=LOG, flush=True)
        WINDOWS_COPY_TREE(JRE, os.path.join(TARGET_DIR, 'jre'))       
        print(' OK', file=LOG)
    else:
        print('Warning: JRE need copy manually for ' + BUILD_RELEASE, file=LOG)
    
    #Copy setup
    if os.path.isdir(os.path.join(BUILD_DIR, r'SETUP\PsMpPIAInstall')):
        print(r'Copy SETUP\PsMpPIAInstall'.ljust(40, '.'), end='', file=LOG, flush=True)
        WINDOWS_COPY_TREE(os.path.join(BUILD_DIR, r'SETUP\PsMpPIAInstall'), 
            os.path.join(TARGET_DIR, r'SETUP\PsMpPIAInstall'))
        print(' OK', file=LOG)
    
    # Copy source directory to target
    for item in SOURCE_DIRS:
        full_item = os.path.join(BUILD_DIR, item)
        if item in OPTIONAL_DIRS and not os.path.exists(full_item):
            continue
        print(' '.join(['Copy', item]).ljust(40, '.'), end='', file=LOG, flush=True)
        if os.path.isdir(full_item):
            WINDOWS_COPY_TREE(full_item, os.path.join(TARGET_DIR, item))
        else:
            shutil.copy(full_item, TARGET_DIR)
        print(' OK', file=LOG)    
    
    print('\nCopying files succeeded!', file=LOG)    
        
        
if __name__ == '__main__':
    from datetime import date
    
    BASE_NAME = os.path.basename(sys.argv[0])
    if not sys.argv[1:]:
        print('Usage:\n\t%s <build_version>' % BASE_NAME)
        print('\tExamples:\n\t\t%s 856-808-R2' % BASE_NAME)
        os._exit(1)
    
    COPY_BUILD(sys.argv[1])
    
    #LOG_DIR = 'log'
    #LOG_NAME = BASE_NAME.split('.')[0] + str(date.today()) + '.log'
    #
    #if not os.path.isdir(LOG_DIR):
    #    os.mkdir(LOG_DIR)
    #    
    #with open(os.path.join(LOG_DIR, LOG_NAME), 'w') as f:
    #    COPY_BUILD(sys.argv[1], f)
        
        
