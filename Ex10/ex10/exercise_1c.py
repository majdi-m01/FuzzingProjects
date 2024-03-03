from fuzzingbook.ConfigurationFuzzer import OptionRunner, OptionFuzzer
import os

def fuzz():
    this_dir  = os.path.dirname(__file__)
    exercise_1a_program = os.path.join(this_dir, 'exercise_1a.py')
    runner = OptionRunner(exercise_1a_program)
    fuzzer =  OptionFuzzer(runner)
    for i in range(10):
	    print(fuzzer.run(runner))

def main():
    fuzz()

if __name__ == "__main__":
    main()