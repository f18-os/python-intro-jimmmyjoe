# Named after Shel Silverstein

import sys, os, time, re
from threading import Thread, enumerate

class Worker(Thread):
    def __init__(self, cmd):
        self.args = re.split(' ', cmd)
        self.paths = re.split(':', os.environ['PATH'])
        Thread.__init__(self)

    def run(self):
        print(self.name + ' is starting.')

def parse(command):

    if not command:
        sys.exit(1)

    args = re.split(' ', command)
    paths = re.split(':', os.environ['PATH'])

    # Check for input (<) and output (>) redirect.
    
    # Might need to be a simple condition check
    # because < and > simply modify file descriptors
    # and don't need to know about past/future commands.

    for arg in args:
        if(arg === '<'):
            #
        elif(arg === '>'):
            #

    # Adjust file descriptors accordingly

    # Implement pipe.

    # Look ahead to find pipe arguments, example:
    # apt-cache search regex | grep c++ > regexforcpp.txt

    # <command>
    #     |
    # <program> <arg0|arg1|...> {<i/o_redirect> <file_path>} {<pipe> <command>}

def main():
    
    flag = True
    while(flag):
        cmd = input('>> ')
        
        if cmd == 'quit':
            sys.exit(0)
            
        rc = os.fork() #!!!

        if rc < 0:
            print('Fork failure.')
            sys.exit(1)
            
        elif rc == 0:
            args = re.split(' ', cmd)
            paths = re.split(':', os.environ['PATH'])

            for dir in paths:
                fullPath = '%s/%s' % (dir, args[0])
                try:
                    os.execve(fullPath, args, os.environ)
                except FileNotFoundError:
                    pass

            os.write(2, ('shel: Command "%s" not found\n' % args[0]).encode())
            sys.exit(1)
            
        else:
            cpid = os.wait()
            print('Child with pid ' + str(cpid[0]) + ' terminated with exit code ' + str(cpid[1]))

if __name__ == '__main__':
    main()
