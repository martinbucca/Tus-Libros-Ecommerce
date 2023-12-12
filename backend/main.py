import os
import sys
import unittest
from src.web_server import Server

cwd = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,cwd)

SERVER_HOST = 'localhost'
SERVER_PORT = 9000

def main ():
    if (len(sys.argv) > 1):
        if (sys.argv[1] == "-t"):
            run_tests()
            return
        else:
            print("[ERROR] Invalid argument")
            return 1
    start_server()


def start_server():
    print (f'Starting server on address {SERVER_HOST}:{SERVER_PORT}...\n')
    Server.run_with_host_and_port(SERVER_HOST, SERVER_PORT)
    

def run_tests():
    print ("Running tests...\n")
    test_suite = unittest.TestLoader().discover("test", pattern="test*.py")
    unittest.TextTestRunner(verbosity=2).run(test_suite)

if __name__ == '__main__':
    main()