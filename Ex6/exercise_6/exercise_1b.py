from exercise_1a import *
import string


def get_grammar_letters():
    return {'<letter>': list(string.ascii_letters), '<letters>': ['<letter>', '<letter><letters>']}


def get_grammar_digits():
    return {'<digit>': list(string.digits), '<digits>': ['<digit>', '<digit><digits>']}


def contains_angle_brackets(rule):
    open_angle_index = rule.find('<')
    close_angle_index = rule.find('>')
    return open_angle_index != -1 and close_angle_index != -1 and close_angle_index > open_angle_index


def generalize(g: dict, cnt_inputs: int) -> dict:
    updated_grammar = {}
    for k, rules in g.items():
        if len(rules) < cnt_inputs / 2:
            updated_grammar[k] = rules
            continue
        elif any(contains_angle_brackets(rule) for rule in rules):
            updated_grammar[k] = rules
            continue
        else:
            if all(rule.isdigit() for rule in rules):
                updated_grammar[k] = ['<digits>']
                updated_grammar.update(get_grammar_digits())
            elif all(rule.isalpha() for rule in rules):
                updated_grammar[k] = ['<letters>']
                updated_grammar.update(get_grammar_letters())
            else:
                updated_grammar[k] = rules
    return updated_grammar
