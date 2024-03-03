"""
Use this file to provide your solutions for exercise 1-1 b.
"""
s1 = 'kitten'
s2 = 'sitting'

from exercise_1c import levenshtein_distance

if __name__ == '__main__':
    print(levenshtein_distance(s1, s2))
