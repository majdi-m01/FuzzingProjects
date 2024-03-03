import time
from fuzzingbook.WebFuzzer import WebRunner
from server import RegisterHTTPRequestHandler, init_db
from exercise_1 import get_fuzzer
import importlib
import os
import multiprocessing
from http.server import HTTPServer
from urllib.parse import urljoin
from fuzzingbook.Fuzzer import Runner
from http import HTTPStatus

timeout = 0.05

def run_httpd_forever(handler_class, p):
    host = "127.0.0.1"  # localhost IP
    for port in range(8800, 9000):
        httpd_address = (host, port)

        try:
            httpd = HTTPServer(httpd_address, handler_class)
            break
        except OSError:
            continue

    p.value = port
    httpd.serve_forever()


class WebRunner(WebRunner):
    def run(self, url):
        if self.base_url is not None:
            url = urljoin(self.base_url, url)

        import requests  # for imports
        r = requests.get(url)
        time.sleep(timeout)
        if r.status_code == HTTPStatus.OK:
            return url, Runner.PASS
        elif r.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            return url, Runner.FAIL
        else:
            return url, Runner.UNRESOLVED
    
    
def test():
    try:
        os.remove('bugs.py')
    except:
        pass
    
    init_db()
    port = multiprocessing.Value('i', 0)
    httpd_process = multiprocessing.Process(target=run_httpd_forever, args=(RegisterHTTPRequestHandler, port))
    httpd_process.start()
    
    time.sleep(1)
    httpd_url = "http://127.0.0.1:" + repr(port.value)

    web_fuzzer = get_fuzzer(httpd_url)
    web_runner = WebRunner(httpd_url)
    if httpd_process.is_alive:
        web_fuzzer.runs(web_runner, 200)
    
    time.sleep(5)
    httpd_process.terminate()
    httpd_process.join()
    
    try:
        b = __import__('bugs')
        importlib.reload(b)
        return len(b.bugs)
    except:
        return 0
    

if __name__ == '__main__':
    print(f'Passed {test()} of 8 tests')
        