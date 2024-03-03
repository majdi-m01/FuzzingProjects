import json
import random
import time
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
import subprocess
from tinyc_grammar import TINYCGRAMMAR

class O:
    def __init__(self, **keys): self.__dict__.update(keys)
    def __repr__(self): return str(self.__dict__)

TIMEOUT = 1
def run(command, inp, env=None, shell=False, log=False, **args):
    command = command.split(' ')
    result = subprocess.Popen(command,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT
    )

    try: 
        stdout, stderr = result.communicate(input=bytes(inp, encoding='utf8'), timeout=TIMEOUT)
        result.kill()
        stderr = '' if stderr is None else stderr.decode('utf-8', 'ignore')
        stdout = '' if stdout is None else stdout.decode('utf-8', 'ignore')
        return O(returncode=result.returncode, stdout=stdout, stderr=stderr)
    except subprocess.TimeoutExpired as e:
        try:
            result.kill()
        except PermissionError:
            pass
        return O(returncode=255, stdout='', stderr='TIMEOUT')


def main():
    random.seed(time.time())
    fuzzer = GrammarFuzzer(TINYCGRAMMAR, min_nonterminals=3, max_nonterminals=5)
    output = ""
    # Fuzz until memory was changed
    # TinyC only has 26 variables, named a-z, which are initialized with 0.
    while output == "":
        s = fuzzer.fuzz()
        print('s: ' + s)
        o = run('./tinyc', s)
        output = o.stdout
    print(output)


if __name__ == "__main__":
    main()
