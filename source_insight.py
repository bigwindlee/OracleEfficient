#!/usr/bin/env python

import os, re, shutil, subprocess

def GetFlagsFromFile(filename):
    flags = set()
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line:
                flags.add(line)
    return flags
    
def CleanseFileForSI(dir, flags_path):
    flags = GetFlagsFromFile(flags_path)
    regexs = []
    extensions = ['.h', '.cpp']
    for flag in sorted(flags):
        pattern = r'{0}\s*\((.*?)\)'.format(flag)
        regexs.append(re.compile(pattern))

    for (dirname, subshere, fileshere) in os.walk(dir):
        for fname in fileshere:
            fullname = os.path.join(dirname, fname)
            subprocess.call("attrib -R " + fullname, stdout=subprocess.DEVNULL)
            if os.path.splitext(fullname)[1] in extensions:
                outfile = fullname + '.bak'
                with open(fullname, 'r', encoding='utf-8', errors='ignore') as fin, open(outfile, 'w', encoding='utf-8', errors='ignore') as fout:
                    for line in fin:
                        if line.strip() == 'PsStartProtoC' or line.strip() == 'PsEndProtoC':
                            continue
                        newline = line
                        for regex in regexs:
                            if regex.search(newline):
                                newline = regex.sub(r'\1', newline)
                                break
                        
                        fout.write(newline)
                        
                shutil.move(outfile, fullname)   
                
                
if __name__ == '__main__':
    import sys
    
    BASE_NAME = os.path.basename(sys.argv[0])
    if sys.argv[2:]:
        dir = os.path.normcase(os.path.normpath(sys.argv[1]))
        flags_path = os.path.normcase(os.path.normpath(sys.argv[2]))
    else:
        print('Usage:\n\t{0} <dir> <flags>'.format(BASE_NAME))
        os._exit(1)
        
    if not os.path.isdir(dir):
        print('%s is not a valid directory.' % dir)
        os._exit(2)
        
    if not os.path.isfile(flags_path):
        print('%s does not exist.' % flags_path)
        os._exit(3)
        
    CleanseFileForSI(dir, flags_path)