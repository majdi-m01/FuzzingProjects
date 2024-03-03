import sys
import random

def interpret(program):
    pos = 0
    ptr = 0
    memory = {0: 0}
    while pos < len(program):
        if program[pos] == '>':
            ptr += 1
            if ptr not in memory:
                memory[ptr+1] = 0
            pos += 1
        elif program[pos] == '<':
            ptr -= 1
            if ptr not in memory:
                memory[ptr-1] = 0
            pos += 1
        elif program[pos] == '+':
            memory[ptr] = (memory[ptr]+1)
            pos += 1
        elif program[pos] == '-':
            memory[ptr] = (memory[ptr]-1)
            pos += 1
        elif program[pos] == '.':
            print(chr(memory[ptr]), end='')
            pos += 1
        elif program[pos] == ',':
            # Read from random instead of stdin.
            memory[ptr] = random.randint(0,255)
            pos += 1
        elif program[pos] == '[':
            if memory[ptr] == 0:
                # jump after ']'
                level = 0
                pos += 1
                while pos < len(program):
                    if program[pos] == ']' and level == 0:
                        pos += 1
                        break
                    elif program[pos] == ']':
                        level -= 1
                    elif program[pos] == '[':
                        level += 1
                    pos += 1
            else:
                pos += 1
        elif program[pos] == ']':
            if memory[ptr] != 0:
                # jump after '['
                level = 0
                pos -= 1
                while pos > 0:
                    if program[pos] == '[' and level == 0:
                        pos += 1
                        break
                    elif program[pos] == ']':
                        level += 1
                    elif program[pos] == '[':
                        level -= 1
                    pos -= 1
            else:
                pos += 1
        else:
            pos += 1

    return {key: val for key, val in memory.items() if val != 0}
