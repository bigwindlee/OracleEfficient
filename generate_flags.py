#!/usr/bin/env python

import os, re

def CollectFlags(dir, flags):
    p = re.compile(r'\b([A-Z]+?EXP[A-Z]+?)\((.*?)\).*?\(')

    for (dirname, subshere, fileshere) in os.walk(dir):
        for fname in fileshere:
            if fname.endswith('.h'):
                fullname = os.path.join(dirname, fname)
                print(fullname)
                with open(fullname, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        prog = p.search(line)
                        if prog:
                            flags.add(prog.group(1))
                    
                    
if __name__ == '__main__':
    import sys

    if sys.argv[1:]:
        dir = os.path.normcase(os.path.normpath(sys.argv[1]))
    else:
        print('Usage:')
        os._exit(1)
        
    if not os.path.isdir(dir):
        raise RuntimeError('%s is not a valid directory.' % dir)
    
    flags = set()
    CollectFlags(dir, flags)
    with open('flags.txt', 'w') as f:
        for flag in sorted(flags):
            print(flag, file=f)
        
