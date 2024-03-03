from fuzzingbook.ConfigurationFuzzer import OptionGrammarMiner
import exercise_1a

def mine_ebnf_grammar():
    mined_grammar = None
    # TODO:
    # 1. Mine ebnf grammar from exercise_1a.main
    optionGrammarMiner = OptionGrammarMiner(exercise_1a.main)
    # 2. Return this grammar
    mined_grammar = optionGrammarMiner.mine_ebnf_grammar()
    return mined_grammar

def main():
    grammar = mine_ebnf_grammar()
    print(grammar)

if __name__ == "__main__":
    main()