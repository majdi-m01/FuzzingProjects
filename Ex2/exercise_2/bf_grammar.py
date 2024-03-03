BFGRAMMAR = {
    "<start>": ["<commands>"],
    "<commands>": ["<command><commands>", ""],
    "<command>": ["<movement>", "<change>", "<output>", "<input>", "<loop>"],
    "<movement>": [">", "<"],
    "<change>": ["+", "-"],
    "<output>": ["."],
    "<input>": [","],
    "<loop>": ["[<commands>]"]
}