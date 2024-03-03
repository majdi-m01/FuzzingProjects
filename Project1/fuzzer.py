from fuzzingbook.GrammarFuzzer import *
from fuzzingbook.GeneratorGrammarFuzzer import opts, ProbabilisticGrammarFuzzer
import grammar
import string

Option = Dict[str, Any]
Expansion = Union[str, Tuple[str, Option]]

class ProbabilisticGrammarFuzzer(ProbabilisticGrammarFuzzer):
    """even faster with precomputed costs"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._symbol_costs: Dict[str, Union[int, float]] = {}
        self._expansion_costs: Dict[Expansion, Union[int, float]] = {}
        self.precompute_costs()

    def new_symbol_cost(self, symbol: str,
                        seen: Set[str] = set()) -> Union[int, float]:
        return self._symbol_costs[symbol]

    def new_expansion_cost(self, expansion: Expansion,
                           seen: Set[str] = set()) -> Union[int, float]:
        if isinstance(expansion, tuple):
                    expansion, probability = expansion
        return self._expansion_costs[expansion]

    def precompute_costs(self) -> None:
        for symbol in self.grammar:
            self._symbol_costs[symbol] = super().symbol_cost(symbol)
            for expansion in self.grammar[symbol]:
                # Modify the cost computation to consider probabilities
                probability = 1.0  # default probability if not specified
                if isinstance(expansion, tuple):
                    expansion, probability = expansion
                if isinstance(probability, dict):
                    probability = probability['prob']

                # Consider the probability in the cost calculation
                cost = super().expansion_cost(expansion)
                weighted_cost = cost * probability
                self._expansion_costs[expansion] = weighted_cost

        # Make sure we now call the caching methods
        self.symbol_cost = self.new_symbol_cost  # type: ignore
        self.expansion_cost = self.new_expansion_cost  # type: ignore

class Fuzzer:
    def __init__(self):
        # This function must not be changed.
        self.grammar = grammar.grammar
        self.setup_fuzzer()
    
    def setup_fuzzer(self):
        # This function may be changed.
        self.grammar.update({
            "<expr>": [
                ("<literal-value>", opts(prob=0.25)),
                "<column-name>",
                "<table-name>.<column-name>",
                "<unary-operator> <expr>",
                "<expr> <binary-operator> <expr>",
                "(<expr-reps>)",
                "CAST (<expr> AS <type-name-option>)",
                "<expr> COLLATE <collation-name>",
                "<expr> <not-option> <after-not-options>",
                "<expr> ISNULL",
                "<expr> NOTNULL",
                "<expr> NOT NULL",
                "<expr> IS <not-option> <expr>",
                "<expr> IS <not-option> DISTINCT FROM <expr>",
                "<expr> <not-option> BETWEEN <expr> AND <expr>",
                "<expr> <not-option> IN <after-in-options>",
                "<not-option> (<select-stmt>)",
                "<not-option> EXISTS (<select-stmt>)",
                "CASE <when-then-reps> END",
                "CASE <when-then-reps> ELSE <expr> END",
                "CASE <expr> <when-then-reps> END",
                "CASE <expr> <when-then-reps> ELSE <expr> END",
                "<raise-function>"
            ],
            "<string>": [
                ("<char>", opts(prob=0.95)), "<char><string>"
            ],
                "<char>": [
                    ('a', opts(prob=0.475)),
                    ('b', opts(prob=0.475)),
                    'c',
                    'd',
                    'e',
                    'f',
                    'g',
                    'h',
                    'i',
                    'j',
                    'k',
                    'l',
                    'm',
                    'n',
                    'o',
                    'p',
                    'q',
                    'r',
                    's',
                    't',
                    'u',
                    'v',
                    'w',
                    'x',
                    'y',
                    'z',
                ]
        })
        self.fuzzer = ProbabilisticGrammarFuzzer(self.grammar)

    global counter
    counter = 0

    def fuzz_one_input(self) -> str:
        # This function should be implemented, but the signature may not change.
        global counter
        if counter <= 50:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    ("<attach-stmt>",opts(prob=0.5)),
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>",
                    "<delete-stmt>",
                    ("<detach-stmt>",opts(prob=0.5)),
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<pragma-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })

        if 50 < counter <= 200:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    ("<create-table-stmt>",opts(prob=0.5)),
                    "<create-trigger-stmt>",
                    "<create-view-stmt>",
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    ("<drop-table-stmt>",opts(prob=0.5)),
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<pragma-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })

        if 200 < counter <= 230:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    ("<create-table-stmt>",opts(prob=1.0)),
                    "<create-trigger-stmt>",
                    "<create-view-stmt>",
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<pragma-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })
        if 230 < counter <= 350:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    ("<create-index-stmt>",opts(prob=0.5)),
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>",
                    "<delete-stmt>",
                    "<detach-stmt>",
                    ("<drop-index-stmt>",opts(prob=0.5)),
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<pragma-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })
        if 350 < counter <= 500:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    ("<create-view-stmt>", opts(prob=0.5)),
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    ("<drop-view-stmt>",opts(prob=0.5)),
                    "<insert-stmt>",
                    "<pragma-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })
        if 500 < counter <= 700:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    ("<create-trigger-stmt>",opts(prob=0.5)),
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    ("<drop-trigger-stmt>",opts(prob=0.5)),
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<pragma-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })
        if 700 < counter <= 900:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    ("<insert-stmt>",opts(prob=1.0)),
                    "<pragma-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })
        if 900 < counter <= 1100:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>",
                    ("<release-stmt>",opts(prob=0.333)),
                    ("<rollback-stmt>",opts(prob=0.333)),
                    ("<savepoint-stmt>",opts(prob=0.333)),
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })
        if 1100 < counter <= 1200:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    ("<pragma-stmt>",opts(prob=1.0)),
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
            })
        if 1200 < counter <= 1300:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    ("<analyze-stmt>",opts(prob=1.0)),
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>",
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"
                ],
             })
        if 1300 < counter <= 1400:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    ("<begin-stmt>", opts(prob=0.5)),
                    ("<commit-stmt>", opts(prob=0.5)),
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
             })
        if 1400 < counter <= 1500:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    ("<reindex-stmt>", opts(prob=1.0)),
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
             })
        if 1500 < counter <= 1600:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    ("<analyze-stmt>",opts(prob=0.5)),
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>", 
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    ("<vacuum-stmt>", opts(prob=0.5)),
                ],
             })
        if 1600 < counter <= 1700:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    ("<reindex-stmt>", opts(prob=1.0)),
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"
                ],
             })
        if 1700 < counter <= 1800:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    ("<alter-table-stmt>",opts(prob=1.0)),
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>", 
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"
                ],
             })
        if 1800 < counter <= 2000:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=0.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>", 
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"
                ],
             })
        if 2000 < counter <= 2100:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>", 
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    ("<select-stmt>",opts(prob=1.0)),
                    "<update-stmt>",
                    "<vacuum-stmt>"
                ],
             })
        if 2100 < counter <= 2200:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>", 
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    ("<update-stmt>",opts(prob=1.0)),
                    "<vacuum-stmt>"
                ],
             })
        if 2200 < counter <= 2300:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=1.0)),
                    "EXPLAIN <sql-stmt-options>",
                    "EXPLAIN QUERY PLAN <sql-stmt-options>",
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    ("<delete-stmt>",opts(prob=1.0)),
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>", 
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"
                ],
             })
        if 2300 < counter <= 45000:
            self.fuzzer.grammar.update({
                "<sql-stmt>": [
                    ("<sql-stmt-options>",opts(prob=0.5)),
                    ("EXPLAIN <sql-stmt-options>",opts(prob=0.25)),
                    ("EXPLAIN QUERY PLAN <sql-stmt-options>",opts(prob=0.25))
                ],
                "<sql-stmt-options>": [
                    "<alter-table-stmt>",
                    "<analyze-stmt>",
                    "<attach-stmt>",
                    "<begin-stmt>",
                    "<commit-stmt>",
                    "<create-index-stmt>",
                    "<create-table-stmt>",
                    "<create-trigger-stmt>",
                    "<create-view-stmt>", 
                    "<delete-stmt>",
                    "<detach-stmt>",
                    "<drop-index-stmt>",
                    "<drop-table-stmt>",
                    "<drop-trigger-stmt>",
                    "<drop-view-stmt>",
                    "<insert-stmt>",
                    "<reindex-stmt>",
                    "<release-stmt>",
                    "<rollback-stmt>",
                    "<savepoint-stmt>",
                    "<pragma-stmt>",
                    "<select-stmt>",
                    "<update-stmt>",
                    "<vacuum-stmt>"],
                "<expr>": [  
                    "<literal-value>",
                    "<column-name>",
                    "<table-name>.<column-name>",
                    "<unary-operator> <expr>",
                    "<expr> <binary-operator> <expr>",
                    "(<expr-reps>)",
                    "CAST (<expr> AS <type-name-option>)",
                    "<expr> COLLATE <collation-name>",
                    "<expr> <not-option> <after-not-options>",
                    "<expr> ISNULL",
                    "<expr> NOTNULL",
                    "<expr> NOT NULL",
                    "<expr> IS <not-option> <expr>",
                    "<expr> IS <not-option> DISTINCT FROM <expr>",
                    "<expr> <not-option> BETWEEN <expr> AND <expr>",
                    "<expr> <not-option> IN <after-in-options>",
                    "<not-option> (<select-stmt>)",
                    "<not-option> EXISTS (<select-stmt>)",
                    "CASE <when-then-reps> END",
                    "CASE <when-then-reps> ELSE <expr> END",
                    "CASE <expr> <when-then-reps> END",
                    "CASE <expr> <when-then-reps> ELSE <expr> END",
                    "<raise-function>"
                ],
                "<string>": [
                    "<char>", "<char><string>"
                ],
                    "<char>": [
                        'a', 
                        'b',
                        'c',
                        'd',
                        'e',
                        'f',
                        'g',
                        'h',
                        'i',
                        'j',
                        'k',
                        'l',
                        'm',
                        'n',
                        'o',
                        'p',
                        'q',
                        'r',
                        's',
                        't',
                        'u',
                        'v',
                        'w',
                        'x',
                        'y',
                        'z',
                    ]
             })
        if 45000 < counter:
            self.fuzzer.max_nonterminals=25
        
        counter+=1
        return self.fuzzer.fuzz()