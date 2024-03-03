from fuzzingbook.WebFuzzer import start_httpd, WebRunner
from server import RegisterHTTPRequestHandler, init_db
from exercise_1 import get_fuzzer
import importlib
import os

def test():
    try:
        os.remove('bugs.py')
    except:
        pass
    
    init_db()
    httpd_process, httpd_url = start_httpd(RegisterHTTPRequestHandler)

    web_fuzzer = get_fuzzer(httpd_url)
    web_runner = WebRunner(httpd_url)
    web_fuzzer.runs(web_runner, 200)
    
    httpd_process.terminate()
    
    try:
        b = __import__('bugs')
        importlib.reload(b)
        return len(b.bugs)
    except:
        return 0
    

if __name__ == '__main__':
    print(f'Passed {test()} of 8 tests')
        