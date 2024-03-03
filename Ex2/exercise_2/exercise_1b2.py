'''
TODO:
Write the faulty line numbers and explanations in line1-4 and explanation_line1-4.
line1-4 must be ints. explanation_line1-4 must be strings.
'''

line1 = 20
line2 = 23
line3 = 12
line4 = 17

explanation_line1 = "The bug occured due to an overflow error: Instead of memory[ptr] = (memory[ptr]+1), the line should be memory[ptr] = (memory[ptr]+1) % 256"
explanation_line2 = "The bug occured due to an underflow error: Instead of memory[ptr] = (memory[ptr]-1), the line should be memory[ptr] = (memory[ptr]-1) % 256"
explanation_line3 = "The bug occured due to an initialization error: Instead of memory[ptr+1] = 0, the line should be memory[ptr] = 0"
explanation_line4 = "The bug occured due to an initialization error: Instead of memory[ptr-1] = 0, the line should be memory[ptr] = 0"