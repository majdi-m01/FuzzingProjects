"""
Use this file to provide your solutions for exercise 1-1 a.
"""
s1 = ''
s2 = 'fuzzing'

from exercise_1 import levenshtein_distance
if __name__ == '__main__':
    print(levenshtein_distance(s1, s2))