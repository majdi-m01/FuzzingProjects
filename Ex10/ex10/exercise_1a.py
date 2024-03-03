#!/usr/bin/env python3
# Do not remove the line above
import argparse
import sys

def preprocess(preprocessing: str, strings: list[str]):
    preprocessed_list = []
    if preprocessing == 'sort':
        preprocessed_list = [''.join(sorted(s)) for s in strings]
    elif preprocessing == 'reversesort':
        preprocessed_list = [''.join(sorted(s, reverse=True)) for s in strings]
    elif preprocessing == 'identity':
        preprocessed_list = strings
    else:
        assert False, 'not allowed'

    return preprocessed_list

def get_average_string_length(strings: list[str]):
    total_length = sum(len(s) for s in strings)
    average_string_length = total_length / len(strings)
    return average_string_length

def parse_and_process(args):
    parser = argparse.ArgumentParser(description='This program concatenates strings.')

    # TODO: Implement parser.add_argument calls here
    parser.add_argument('strings', metavar='s', type=str, nargs='+', help='Strings that will be concatenated.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--identity', dest='preprocessing', action='store_const', const='identity', help='Do not change individual strings before concatenating.')
    group.add_argument('--sort', dest='preprocessing', action='store_const', const='sort', help='Sort individual strings in normal order before concatenating.')
    group.add_argument('--reversesort', dest='preprocessing', action='store_const', const='reversesort', help='Sort individual strings in reverse order before concatenating.')
    parser.add_argument('--output-average-string-length', action='store_true', dest='output_average_string_length')
    
    args = parser.parse_args(args)
    
    preprocessed_list = preprocess(args.preprocessing, args.strings)
    concatenated_string = ''.join(preprocessed_list)
    average_string_length = None
    if args.output_average_string_length:
        average_string_length = get_average_string_length(args.strings)

    return (concatenated_string, average_string_length)

def main():
    parse_and_process(sys.argv[1:])

if __name__ == "__main__":
    main()
