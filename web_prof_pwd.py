#!/usr/bin/env python

import fileinput


ID_PWD = {'PTWEBSERVER':'{V1.1}JP9ukEkTssmYrzsK1yvXFg==', 'Passw0rd':'{V1.1}OS07ug4qzY5ohQ1ZVFKFDg=='}

def change_web_prof_pwd(filename):
    replaced = False
    for line in fileinput.input(filename, inplace=True):
        newline = line
        if line.strip().startswith('WebPassword='):
            if ID_PWD['PTWEBSERVER'] in line:
                newline = line.replace(ID_PWD['PTWEBSERVER'], ID_PWD['Passw0rd'])
                replaced = True
            elif ID_PWD['Passw0rd'] in line:
                newline = line.replace(ID_PWD['Passw0rd'], ID_PWD['PTWEBSERVER'])
                replaced = True
        
        print(newline, end='')

    return replaced

if __name__ == '__main__':
    import os, sys

    if sys.argv[1:]:
        filename = os.path.normcase(os.path.normpath(sys.argv[1]))
    else:
        filename = r'placeholder'

    if not filename.endswith('configuration.properties'):
        print('Not a valid filename of properties: ' + filename)
        os._exit(1)

    with open(filename) as f:
        if not 'WebPassword=' in f.read():
            print("Error: Cannot find WebPassword in " + filename)
            os._exit(2)
            
    if not change_web_prof_pwd(filename):
        print("Warning: Unknown password. Not changed.")
        
        
        
        
