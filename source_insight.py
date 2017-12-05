#!/usr/bin/env python

import os, re, fileinput, shutil

def GetFlagsFromFile(filename):
    flags = set()
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            flags.add(line)
    return flags

def CleanseFileInPlace(dir, flags):
    regexs = []
    extensions = ['.h', '.cpp']
    for flag in sorted(flags):
        flag = flag.strip()
        pattern = r'{0}\s*\((.*?)\)'.format(flag)
        regexs.append(re.compile(pattern))

    for (dirname, subshere, fileshere) in os.walk(dir):
        for fname in fileshere:
            fullname = os.path.join(dirname, fname)
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

    if sys.argv[1:]:
        dir = os.path.normcase(os.path.normpath(sys.argv[1]))
    else:
        print('Usage:')
        os._exit(1)
        
    if not os.path.isdir(dir):
        print('%s is not a valid directory.' % dir)
        os._exit(2)
        
    FLAGS_FILE = 'flags.txt'
    if not os.path.isfile(FLAGS_FILE):
        print('%s does not exist.' % FLAGS_FILE)
        os._exit(3)
        
    flags = GetFlagsFromFile(FLAGS_FILE)
    CleanseFileInPlace(dir, flags)
