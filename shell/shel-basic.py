#!/usr/bin/env python3

# Named after Shel Silverstein

import sys, os, re

redirects = re.compile(r'[<>\|]')
matches = ''

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

    return firstArgs, afterArgs, paths

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

        firstArgs, afterArgs, paths = parse(cmd)
        print(firstArgs, afterArgs)

        if afterArgs is None:
            rc = os.fork()

            if rc == 0: # child
                for dir in paths:
                    fullPath = '%s/%s' % (dir, firstArgs[0])
                    try:
                        os.execve(fullPath, firstArgs, os.environ)
                    except FileNotFoundError:
                        pass
            else: # parent
                cpid = os.wait()
        else:
            redirect = afterArgs.pop(0)
            
            if redirect == '|':
                pipe = True
                pr, pw = os.pipe()
                os.set_inheritable(pr, True)
                os.set_inheritable(pw, True)
                rc = os.fork()

                if rc == 0:
                    pass
                else:
                    pass
                
            elif redirect == '<':
                rc = os.fork()

                if rc == 0:
                    stdin = sys.stdin # save stdin
                    os.close(0) # close stdin
                    os.stdin = open(afterArgs[0], 'r')
                    os.set_inheritable(0, True)

                    for dir in paths:
                        fullPath = '%s/%s' % (dir, firstArgs[0])
                        try:
                            os.execve(fullPath, firstArgs, os.environ)
                        except FileNotFoundError:
                            pass
                    
                else: # parent
                    cpid = os.wait()
                    
            else: # redirect == '>'
                rc = os.fork()

                if rc == 0:
                    stdout = sys.stdout # save stdout
                    os.close(1) # close stdout
                    os.stdout = open(afterArgs[0], 'w')
                    os.set_inheritable(1, True)

                    for dir in paths:
                        fullPath = '%s/%s' % (dir, firstArgs[0])
                        try:
                            os.execve(fullPath, firstArgs, os.environ)
                        except FileNotFoundError:
                            pass
                else:
                    cpid = os.wait()

if __name__ == '__main__':
    main()
