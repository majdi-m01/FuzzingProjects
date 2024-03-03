import random
import time
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from bf import interpret
from bf_grammar import BFGRAMMAR

import multiprocessing

TIMEOUT = 1 # 1 second
ERR_EXCEPTION = "EXCEPTION"

def wrapper(queue, s):
    result = interpret(s)
    queue.put(result)
    queue.close()

def runBF(s):
    queue = multiprocessing.Queue(1) 
    proc = multiprocessing.Process(target=wrapper, args=(queue, s))
    proc.start()
    # Wait for TIMEOUT seconds
    try:
        result = queue.get(True, TIMEOUT)
        return result
    except Exception as e:
        print('Exception')
        result = ERR_EXCEPTION # can be either a real error or timeout exception
        proc.terminate()
        return result


def main():
    random.seed(time.time())
    
    fuzzer = GrammarFuzzer(BFGRAMMAR, min_nonterminals=3, max_nonterminals=10)
    for i in range(1000):
        s = fuzzer.fuzz()
        print('s: {}'.format(s))
        res = runBF(s)
        if res != ERR_EXCEPTION:
            print('res: {}'.format(res))

if __name__ == "__main__":
    main()
