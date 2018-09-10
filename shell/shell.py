import sys, os, time, re
from threading import Thread, enumerate

class Worker(Thread):
    def __init__(self, cmd):
        self.args = re.split(' ', cmd)
        Thread.__init__(self)

    def run(self):
        print(self.name + ' is starting.')
        

def main():
    flag = True
    while(flag):
        cmd = input('>> ')
        
        if cmd == 'quit':
            sys.exit(0)
            
        rc = os.fork()

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

            sys.exit(1)
            
        else:
            cpid = os.wait()
            print('Child with pid ' + str(cpid[0]) + ' terminated with exit code ' + str(cpid[1]))

if __name__ == '__main__':
    main()
