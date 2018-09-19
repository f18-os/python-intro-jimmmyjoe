#!/usr/bin/env python3

# Named after Shel Silverstein

import sys, os, time, re
from threading import Thread, enumerate

redirects = re.compile(r'[<>\|]')
matches = ''

class Worker(Thread):
    def __init__(self, cmd):
        self.args = re.split(' ', cmd)
        self.paths = re.split(':', os.environ['PATH'])
        Thread.__init__(self)

    def run(self):
        print(self.name + ' is starting.')

def parse(command):
    
    global matches 

    if not command:
        sys.exit(1)

    matches = re.findall(redirects, command)
    match = re.search(redirects, command)

    if match is None:
        firstArgs = re.split(' ', command)
        firstArgs = [arg for arg in firstArgs if arg != '']
        afterArgs = None
        paths = re.split(':', os.environ['PATH'])
    else:
        splitIndex = match.start()
        
        firstCmd = command[:splitIndex-1]
        afterCmd = command[splitIndex:]

        firstArgs = re.split(' ', firstCmd)
        firstArgs = [arg for arg in firstArgs if arg != '']
        
        afterArgs = re.split(' ', afterCmd)
        afterArgs = [arg for arg in afterArgs if arg != '']
        
        paths = re.split(':', os.environ['PATH'])
        paths = [path for path in paths if path != '']
        
        print(firstArgs)
        print(afterArgs)
        print(paths)

    return firstArgs, afterArgs, paths
    
    # Check for input (<) and output (>) redirect.
    
    # Might need to be a simple condition check
    # because < and > simply modify file descriptors
    # and don't need to know about past/future commands.

    # Adjust file descriptors accordingly

    # Implement pipe.

    # Look ahead to find pipe arguments, example:
    # apt-cache search regex | grep c++ > regexforcpp.txt

    # <command>
    #     |
    # <program> <arg0|arg1|...> {<i/o_redirect> <file_path>} {<pipe> <command>}

def main():

    try:
        # os.system should be a subprocess instead
        os.system('cat ~/.bashrc | grep PS1 > ./ps1.txt')
        with open('./ps1.txt', 'r') as ps1:
            line = ps1.readline()
            split = re.split('\'', line)
            prompt = split[1]
    except FileNotFoundError: #Windows
        prompt = 'shel$ '
        
        
    flag = True
    while(flag):
        cmd = input(prompt)
        
        if cmd == 'quit':
            sys.exit(0)
            
        rc = os.fork() #!!!

        if rc < 0:
            print('Fork failure.')
            sys.exit(1)
            
        elif rc == 0:
            
            firstArgs, afterArgs, paths = parse(cmd)
            print(firstArgs, afterArgs, paths)

            if afterArgs is not None:
                redirect = afterArgs[0]
                print(redirect)

                if redirect == '|':
                    pr, pw = os.pipe()
                    os.set_inheritable(pr, True)
                    os.set_inheritable(pw, True)
                    
                    
                elif redirect == '<':
                    pass
                else: # > via regex

            for dir in paths:
                fullPath = '%s/%s' % (dir, firstArgs[0])
                try:
                    os.execve(fullPath, firstArgs, os.environ)
                except FileNotFoundError:
                    pass

            os.write(2, ('shel: Command "%s" not found\n' % firstArgs[0]).encode())
            sys.exit(1)
            
        else:
            cpid = os.wait()
            print('Child with pid ' + str(cpid[0]) + ' terminated with exit code ' + str(cpid[1]))

if __name__ == '__main__':
    main()
