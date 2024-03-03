# Implement your grammar here in the `grammar` variable.
# You may define additional functions, e.g. for generators.
# You may not import any other modules written by yourself.
# That is, your entire implementation must be in `grammar.py`
# and `fuzzer.py`.
import string

grammar = {
    # grammar base
    "<start>": [
        "<sql-stmt>"
    ],

    "<sql-stmt>": [
        "<sql-stmt-options>",
        "EXPLAIN <sql-stmt-options>",
        "EXPLAIN QUERY PLAN <sql-stmt-options>"
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
        #"<create-virtual-table-stmt>",
        "<delete-stmt>",
        "<delete-stmt-limited>",
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
        "<update-stmt-limited>",
        "<vacuum-stmt>"
    ],

    # grammar main statements
    "<alter-table-stmt>": [  # X
        "ALTER TABLE <table-name> RENAME TO <table-name>",
        "ALTER TABLE <table-name> RENAME <column-name> TO <column-name>",
        "ALTER TABLE <table-name> RENAME COLUMN <column-name> TO <column-name>",
        "ALTER TABLE <table-name> ADD <column-def>",
        "ALTER TABLE <table-name> ADD COLUMN <column-def>",
        "ALTER TABLE <table-name> DROP <column-name>",
        "ALTER TABLE <table-name> DROP COLUMN <column-name>"
    ],

    "<analyze-stmt>": [  # X
        "ANALYZE",
        "ANALYZE <schema-name>",
        "ANALYZE <index-or-table-name>",
    ],

    "<attach-stmt>": [  # X
        "ATTACH <expr> AS <schema-name>",
        "ATTACH DATABASE <expr> AS <schema-name>"
    ],

    "<begin-stmt>": [  # X
        "BEGIN",
        "BEGIN DEFERRED",
        "BEGIN IMMEDIATE",
        "BEGIN EXCLUSIVE",
        "BEGIN TRANSACTION",
        "BEGIN DEFERRED TRANSACTION",
        "BEGIN IMMEDIATE TRANSACTION",
        "BEGIN EXCLUSIVE TRANSACTION"
    ],

    "<commit-stmt>": [  # X
        "COMMIT",
        "END",
        "COMMIT TRANSACTION",
        "END TRANSACTION"
    ],

    "<create-index-stmt>": [  # X
        "CREATE INDEX <if-not-exists-option> <index-name> ON <table-name> (<indexed-column-reps>) <where-expr-option>",
        "CREATE UNIQUE INDEX <if-not-exists-option> <index-name> ON <table-name> (<indexed-column-reps>) <where-expr-option>"
    ],

    "<create-table-stmt>": [  # X
        "CREATE <temp-option> TABLE <if-not-exists-option> <table-name> AS <select-stmt>",
        "CREATE <temp-option> TABLE <if-not-exists-option> <table-name> (<column-def-reps> <table-constraint-option-reps>) <table-options-option>"
    ],

    "<create-trigger-stmt>": [  # X
        "CREATE <temp-option> TRIGGER <if-not-exists-option> <trigger-name> <trigger-order-options> <trigger-options> <when-expr-option> <for-each-row-option> BEGIN <stmt-options-reps> END"
    ],

    "<create-view-stmt>": [  # X
        "CREATE <temp-option> VIEW <if-not-exists-option> <view-name> AS <select-stmt>",
        "CREATE <temp-option> VIEW <if-not-exists-option> <view-name> (<column-name-reps>) AS <select-stmt>"
    ],

    "<delete-stmt>": [  # X
        "<with-option> DELETE FROM <qualified-table-name> <where-expr-option> <returning-clause-option>"
    ],

    "<delete-stmt-limited>": [  # X
        "<with-option> DELETE FROM <qualified-table-name> <where-expr-option> <returning-clause-option> <order-by-option> <limit-expr-option>"
    ],

    "<detach-stmt>": [  # X
        "DETACH <schema-name>",
        "DETACH DATABASE <schema-name>"
    ],

    "<drop-index-stmt>": [  # X
        "DROP INDEX <index-name>",
        "DROP INDEX IF EXISTS <index-name>"
    ],

    "<drop-table-stmt>": [  # X
        "DROP TABLE <table-name>",
        "DROP TABLE IF EXISTS <table-name>"
    ],

    "<drop-trigger-stmt>": [  # X
        "DROP TRIGGER <trigger-name>",
        "DROP TRIGGER IF EXISTS <trigger-name>"
    ],

    "<drop-view-stmt>": [  # X
        "DROP VIEW <view-name>",
        "DROP VIEW IF EXISTS <view-name>"
    ],

    "<insert-stmt>": [  # X
        "<with-option> REPLACE INTO <table-name> <as-alias-option> <insert-column-option> <insert-end-options> <returning-clause-option>",
        "<with-option> INSERT <insert-options> INTO <table-name> <as-alias-option> <insert-column-option> <insert-end-options> <returning-clause-option>"
    ],

    "<pragma-stmt>": [  # X
        "PRAGMA <pragma-name>",
        "PRAGMA <pragma-name>=<pragma-value>",
        "PRAGMA <pragma-name>(<pragma-value>)"
    ],

    "<reindex-stmt>": [  # X
        "REINDEX",
        "REINDEX <collation-name>",
        "REINDEX <table-name>",
        "REINDEX <index-name>"
    ],

    "<release-stmt>": [  # X
        "RELEASE <savepoint-name>",
        "RELEASE SAVEPOINT <savepoint-name>"
    ],

    "<rollback-stmt>": [  # X
        "ROLLBACK",
        "ROLLBACK TO <savepoint-name>",
        "ROLLBACK TO SAVEPOINT <savepoint-name>",
        "ROLLBACK TRANSACTION TO <savepoint-name>",
        "ROLLBACK TRANSACTION TO SAVEPOINT <savepoint-name>"
    ],

    "<savepoint-stmt>": [  # X
        "SAVEPOINT <savepoint-name>"
    ],

    "<select-stmt>": [  # X
        "<with-option> <select-core-reps> <order-by-option> <limit-expr-option>"
    ],

    "<update-stmt>": [  # X
        "<with-option> UPDATE <update-options> <qualified-table-name> SET <update-set-options-reps> <update-from-option> <where-expr-option> <returning-clause-option>"
    ],
    
    "<update-stmt-limited>": [  # X
        "<update-stmt> <order-by-option> <limit-expr-option>"
    ],
    
    "<vacuum-stmt>": [  # X
        "VACUUM",
        "VACUUM <schema-name>",
        "VACUUM INTO <filename>",
        "VACUUM <schema-name> INTO <filename>"
    ],

    "<filter-clause-option>": [
        "<filter-clause>",
        ""
    ],

    "<filter-clause>": [  # X
        "FILTER (WHERE <expr>)"
    ],

    "<order-by-option>": [
        "ORDER BY <ordering-term>",
        ""
    ],

    "<ordering-term-reps>": [
        "<ordering-term>",
        "<ordering-term>,<ordering-term-reps>"
    ],

    "<ordering-term>": [  # X
        "<expr>",
        "<expr> <collate-option> <order-option> <nulls-sort-option>"
    ],

    "<nulls-sort-option>": [
        "NULLS FIRST",
        "NULLS LAST",
        ""
    ],

    "<expr-reps>": [
        "<expr>",
        "<expr>,<expr-reps>"
    ],

    "<expr>": [  # X
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

    "<not-option>": [
        "",
        "NOT"
    ],

    "<after-not-options>": [
        "LIKE <expr>",
        "LIKE <expr> ESCAPE <expr>",
        "GLOB <expr>",
        "REGEXP <expr>",
        "MATCH <expr>"
    ],

    "<after-in-options>": [
        "()",
        "(<select-stmt>)",
        "(<expr-reps>)",
        "<table-name>",
    ],

    "<when-then-reps>": [
        "WHEN <expr> THEN <expr>",
        "WHEN <expr> THEN <expr> <when-then-reps>"
    ],

    "<column-constraint>": [  # X
        "CONSTRAINT <name> <column-constraint-options>",
        "<column-constraint-options>"
    ],

    "<column-constraint-options>": [  # X
        "PRIMARY KEY <order-option> <conflict-clause>",
        "PRIMARY KEY <order-option> <conflict-clause> AUTOINCREMENT",
        "NOT NULL <conflict-clause>",
        "UNIQUE <conflict-clause>",
        "CHECK (<expr>)",
        "DEFAULT (<expr>)",
        "DEFAULT (<literal-value>)",
        "DEFAULT (<signed-number>)",
        "COLLATE <collation-name>",
        "<foreign-key-clause>",
        "GENERATED ALWAYS AS (<expr>)",
        "GENERATED ALWAYS AS (<expr>) STORED",
        "GENERATED ALWAYS AS (<expr>) VIRTUAL",
        "AS (<expr>)",
        "AS (<expr>) STORED",
        "AS (<expr>) VIRTUAL"
    ],

    "<column-def>": [  # X
        "<column-name> <type-name-option> <column-constraint-option-reps>"
    ],

    "<column-constraint-option-reps>": [
        "<column-constraint>",
        "<column-constraint><column-constraint-option-reps>",
        ""
    ],

    "<common-table-expression>": [  # X
        "<table-name> <column-name-option> AS (<select-stmt>)",
        "<table-name> <column-name-option> AS NOT MATERIALIZED (<select-stmt>)",
        "<table-name> <column-name-option> AS MATERIALIZED (<select-stmt>)"
    ],

    "<compound-operator>": [  # X
        "UNION",
        "UNION ALL",
        "INTERSECT",
        "EXCEPT"
    ],

    "<compound-select-stmt>": [  # X
        "<with-option> <select-core-reps> <order-by-option> <limit-expr-option>"
    ],

    "<with-option>": [
        "WITH RECURSIVE <common-table-expression-reps>",
        "WITH <common-table-expression-reps>",
        ""
    ],

    "<common-table-expression-reps>": [
        "<common-table-expression>",
        "<common-table-expression>,<common-table-expression-reps>"
    ],

    "<select-core-reps>": [
        "<select-core>",
        "<select-core> <compound-operator> <select-core-reps>"
    ],

    "<limit-expr-option>": [
        "LIMIT <expr>",
        "LIMIT <expr> OFFSET <expr>",
        "LIMIT <expr>,<expr>",
        ""
    ],

    "<conflict-clause>": [  # X
        "ON CONFLICT <conflict-options>",
        ""
    ],

    "<conflict-options>": [
        "ROLLBACK",
        "ABORT",
        "FAIL",
        "IGNORE",
        "REPLACE"
    ],

    "<if-not-exists-option>": [
        "IF NOT EXISTS",
        ""
    ],

    "<indexed-column-reps>": [
        "<indexed-column>",
        "<indexed-column>, <indexed-column-reps>"
    ],

    "<indexed-column>": [  # X
        "<column-name> <collate-option> <order-option>",
        "<expr> <collate-option> <order-option>"
    ],

    "<collate-option>": [
        "",
        "COLLATE <collation-name>"
    ],

    "<order-option>": [
        "",
        "ASC",
        "DESC"
    ],

    "<where-expr-option>": [
        "WHERE <expr>",
        ""
    ],

    "<temp-option>": [
        "TEMP",
        "TEMPORARY",
        ""
    ],

    "<stmt-options-reps>": [
        "<stmt-options>",
        "<stmt-options><stmt-options-reps>"
    ],

    "<stmt-options>": [
        "<update-stmt>;",
        "<insert-stmt>;",
        "<delete-stmt>;",
        "<select-stmt>;"
    ],

    "<column-def-reps>": [
        "<column-def>",
        "<column-def>, <column-def-reps>"
    ],

    "<table-constraint-option-reps>": [
        ",<table-constraint>",
        ",<table-constraint><table-constraint-option-reps>",
        ""
    ],

    "<table-options-option>": [
        "<table-options>",
        ""
    ],

    "<trigger-order-options>": [
        "BEFORE",
        "AFTER",
        "INSTEAD OF"
    ],

    "<trigger-options>": [
        "DELETE ON <table-name>",
        "INSERT ON <table-name>",
        "UPDATE ON <table-name>",
        "UPDATE OF <column-name-reps> ON <table-name>"
    ],

    "<column-name-reps>": [
        "<column-name>",
        "<column-name>, <column-name-reps>"
    ],

    "<when-expr-option>": [
        "",
        "WHEN <expr>"
    ],

    "<for-each-row-option>": [
        "",
        "FOR EACH ROW <when-expr-option>"
    ],

    "<cte-table-name>": [  # X
        "<table-name>",
        "<table-name> (<column-name-reps>)"
    ],

    "<returning-clause-option>": [
        "<returning-clause>",
        ""
    ],

    "<function-arguments>": [  # X
        "",
        "*",
        "<expr-reps>",
        "DISTINCT <expr-reps>",
        "<expr-reps> <order-by-option>",
        "DISTINCT <expr-reps> <order-by-option>"
    ],

    "<literal-value>": [
        "<numeric-literal>",
        "<string-literal>",
        "<blob-literal>",
        "NULL",
        "TRUE",
        "FALSE",
        "CURRENT_TIME",
        "CURRENT_DATE",
        "CURRENT_TIMESTAMP"
    ],

    "<numeric-literal>": [
        "<digit-reps><digit-exponential-option>",
        "<digit-reps>.<digit-reps><digit-exponential-option>",
        ".<digit-reps><digit-exponential-option>",
        "0x<hexdigit-reps>",
        "0X<hexdigit-reps>"
    ],

    "<digit-reps>": [
        "<digit><digit-reps>",
        "<digit>"
    ],

    "<hexdigit-reps>": [
        "<hexdigit><digit-reps>",
        "<hexdigit>"
    ],

    "<digit-exponential-option>": [
        "<digit-reps>E<digit-reps>",
        "<digit-reps>e<digit-reps>",
        "<digit-reps>E+<digit-reps>",
        "<digit-reps>e+<digit-reps>",
        "<digit-reps>E-<digit-reps>",
        "<digit-reps>e-<digit-reps>",
        ""
    ],

    "<over-clause>": [  # X
        "OVER <window-name>",
        "OVER (<window-option>)"
    ],

    "<window-option>": [
        "<base-window-name-option> <partition-by-option> <order-by-option> <frame-spec-option>"
    ],

    "<base-window-name-option>": [
        "<base-window-name>",
        ""
    ],

    "<partition-by-option>": [
        "PARTITION BY <expr-reps>",
        ""
    ],

    "<frame-spec-option>": [
        "<frame-spec>",
        ""
    ],

    "<type-name-option>":
        ["Boolean", "Time", "Date", "SMALLINT", "INT", "BIGINT", "FLOAT", "REAL", "VARCHAR"],

    "<factored-select-stmt>": [  # X
        "<with-option> <select-core-reps> <order-by-option> <limit-expr-option>"
    ],

    "<foreign-key-clause>": [  # X
        "REFERENCES <foreign-table> <column-name-option> <on-match-option-reps> <deferrable-option>"
    ],

    "<column-name-option>": [
        "(<column-name-reps>)",
        ""
    ],

    "<column-name-list>": [  # X
        "(<column-name-reps>)"
    ],

    "<on-match-option-reps>": [
        "ON DELETE <on-options>",
        "ON DELETE <on-options> <on-match-option-reps>",
        "ON UPDATE <on-options>",
        "ON UPDATE <on-options> <on-match-option-reps>",
        "MATCH <name>",
        "MATCH <name> <on-match-option-reps>",
        ""
    ],

    "<on-options>": [
        "SET NULL",
        "SET DEFAULT",
        "CASCADE",
        "RESTRICT",
        "NO ACTION"
    ],

    "<deferrable-option>": [
        "NOT DEFERRABLE <deferrable-options>",
        "DEFERRABLE <deferrable-options>",
        ""
    ],

    "<deferrable-options>": [
        "INITIALLY DEFERRED",
        "INITIALLY IMMEDIATE",
        ""
    ],

    "<frame-spec>": [  # X
        "<frame-options> <frame-across-options> <exclude-option>"
    ],

    "<frame-options>": [
        "RANGE",
        "ROWS",
        "GROUPS"
    ],

    "<frame-across-options>": [
        "BETWEEN <after-between-options> AND <after-and-options>",
        "UNBOUNDED PRECEDING",
        "<expr> PRECEDING",
        "CURRENT ROW"
    ],

    "<exclude-option>": [
        "EXCLUDE NO OTHERS",
        "EXCLUDE CURRENT ROW",
        "EXCLUDE GROUP",
        "EXCLUDE TIES",
        ""
    ],

    "<after-between-options>": [
        "UNBOUNDED PRECEDING",
        "<expr> PRECEDING",
        "CURRENT ROW",
        "<expr> FOLLOWING"
    ],

    "<after-and-options>": [
        "UNBOUNDED FOLLOWING",
        "<expr> PRECEDING",
        "CURRENT ROW",
        "<expr> FOLLOWING"
    ],

    "<as-alias-option>": [
        "AS <alias>",
        ""
    ],

    "<insert-column-option>": [
        "(<column-name-reps>)",
        ""
    ],

    "<insert-end-options>": [
        "VALUES <parenthesis-expr-reps>",
        "VALUES <parenthesis-expr-reps> <upsert-clause>",
        "<select-stmt>",
        "<select-stmt> <upsert-clause>",
        "DEFAULT VALUES",
        "DEFAULT VALUES <upsert-clause>"
    ],

    "<parenthesis-expr-reps>": [
        "(<expr-reps>)",
        "(<expr-reps>), <parenthesis-expr-reps>"
    ],

    "<insert-options>": [
        "",
        "OR ABORT",
        "OR FAIL",
        "OR IGNORE",
        "OR REPLACE",
        "OR ROLLBACK"
    ],

    "<join-clause>": [  # X
        "<table-or-subquery> <join-option-reps>"
    ],

    "<join-option-reps>": [
        "<join-operator> <table-or-subquery> <join-constraint>",
        "<join-operator> <table-or-subquery> <join-constraint> <join-option-reps>",
        ""
    ],

    "<join-constraint>": [  # X
        "ON <expr>",
        "USING (<column-name-reps>)",
        ""
    ],

    "<join-operator>": [
        ",",
        "JOIN",
        "LEFT JOIN",
        "RIGHT JOIN",
        "FULL JOIN",
        "LEFT OUTER JOIN",
        "RIGHT OUTER JOIN",
        "FULL OUTER JOIN",
        "NATURAL JOIN",
        "NATURAL LEFT JOIN",
        "NATURAL RIGHT JOIN",
        "NATURAL FULL JOIN",
        "NATURAL LEFT OUTER JOIN",
        "NATURAL RIGHT OUTER JOIN",
        "NATURAL FULL OUTER JOIN",
        "INNER JOIN",
        "NATURAL INNER JOIN",
        "CROSS JOIN"
    ],

    "<pragma-value>": [
        "0",
        "no",
        "false",
        "off",
        "1",
        "yes",
        "true",
        "on"
    ],

    "<signed-number>": [
        "+<numeric-literal>",
        "-<numeric-literal>",
        "<numeric-literal>"
    ],

    "<qualified-table-name>": [
        "<table-name> <as-alias-option>",
        "<table-name> <as-alias-option> INDEXED BY <index-name>",
        "<table-name> <as-alias-option> NOT INDEXED"
    ],

    "<raise-function>": [  # X
        "RAISE (IGNORE)",
        "RAISE (ROLLBACK, <error-message>)",
        "RAISE (ABORT, <error-message>)",
        "RAISE (FAIL, <error-message>)"
    ],

    "<recursive-cte>": [  # X
        "<cte-table-name> AS (<initial-select> UNION <recursive-select>)",
        "<cte-table-name> AS (<initial-select> UNION ALL <recursive-select>)"
    ],

    "<result-column>": [  # X
        "<expr>",
        "<expr> AS <column-alias>",
        "<expr> <column-alias>",
        "*",
        "<table-name>.*"
    ],

    "<returning-clause>": [  # X
        "RETURNING <returning-options-reps>"
    ],

    "<returning-options-reps>": [
        "<returning-options>",
        "<returning-options>, <returning-options-reps>"
    ],

    "<returning-options>": [
        "<expr>",
        "<expr> AS <column-alias>",
        "<expr> <column-alias>",
        "*"
    ],

    "<select-core>": [  # X
        "SELECT <select-options> <result-column-reps> <select-from-option> <where-expr-option> <select-group-option> <select-window-option>",
        "VALUES <parenthesis-expr-reps>"
    ],

    "<select-options>": [
        "DISTINCT",
        "ALL",
        ""
    ],

    "<result-column-reps>": [
        "<result-column>",
        "<result-column>, <result-column-reps>"
    ],

    "<select-from-option>": [
        "FROM <table-or-subquery-reps>",
        "FROM <join-clause>",
        ""
    ],

    "<select-group-option>": [
        "HAVING <expr>",
        "GROUP BY <expr-reps>",
        "GROUP BY <expr-reps> HAVING <expr>",
        ""
    ],

    "<select-window-option>": [
        "WINDOW <window-name-reps>",
        ""
    ],

    "<window-name-reps>": [
        "<window-name> AS <window-defn>",
        "<window-name> AS <window-defn>, <window-name-reps>"
    ],

    "<table-or-subquery-reps>": [
        "<table-or-subquery>",
        "<table-or-subquery>, <table-or-subquery-reps>"
    ],

    "<simple-select-stmt>": [  # X
        "<with-option> <select-core> <order-by-option> <limit-expr-option>"
    ],

    "<table-constraint>": [  # X
        "CONSTRAINT <name> <table-constraint-options>",
        "<table-constraint-options>"
    ],

    "<table-constraint-options>": [
        "PRIMARY KEY (<indexed-column-reps>) <conflict-clause>",
        "UNIQUE (<indexed-column-reps>) <conflict-clause>",
        "CHECK (<expr>)",
        "FOREIGN KEY (<column-name-reps>) <foreign-key-clause>"
    ],

    "<table-options>": [  # X
        "WITHOUT ROWID",
        "STRICT",
        "WITHOUT ROWID, <table-options>",
        "STRICT, <table-options>"
    ],

    "<table-or-subquery>": [  # X
        "(<select-stmt>)",
        "(<select-stmt>) <table-alias>",
        "(<select-stmt>) AS <table-alias>",
        "(<table-or-subquery-reps>)",
        "(<join-clause>)"
    ],

    "<table-name-options>": [
        "<table-name>",
        "<table-name> <table-alias>",
        "<table-name> AS <table-alias>",
        "<table-name> INDEXED BY <index-name>",
        "<table-name> <table-alias> INDEXED BY <index-name>",
        "<table-name> AS <table-alias> INDEXED BY <index-name>",
        "<table-name> NOT INDEXED",
        "<table-name> <table-alias> NOT INDEXED",
        "<table-name> AS <table-alias> NOT INDEXED"
    ],

    "<update-options>": [
        "",
        "OR ABORT",
        "OR FAIL",
        "OR IGNORE",
        "OR REPLACE",
        "OR ROLLBACK"
    ],

    "<update-set-options-reps>": [
        "<update-set-options>",
        "<update-set-options>,<update-set-options-reps>"
    ],

    "<update-set-options>": [
        "<column-name> = <expr>",
        "<column-name-list> = <expr>"
    ],

    "<update-from-option>": [
        "FROM <table-or-subquery-reps>",
        "FROM <join-clause>",
        ""
    ],

    "<upsert-clause>": [  # X
        "ON CONFLICT <conflict-target> DO NOTHING",
        "ON CONFLICT <conflict-target> DO UPDATE SET <upsert-column-reps> <where-expr-option>",
        "ON CONFLICT <conflict-target> DO NOTHING <upsert-clause>",
        "ON CONFLICT <conflict-target> DO UPDATE SET <upsert-column-reps> <where-expr-option> <upsert-clause>"
    ],

    "<conflict-target>": [
        "(<indexed-column-reps>) <where-expr-option>",
        ""
    ],

    "<upsert-column-reps>": [
        "<column-name> = <expr>",
        "<column-name-list> = <expr>",
        "<column-name> = <expr>, <upsert-column-reps>",
        "<column-name-list> = <expr>, <upsert-column-reps> "
    ],

    "<window-defn>": [  # X
        "(<base-window-name-option> <partition-by-option> <order-by-option> <frame-spec-option>)"
    ],

    "<with-clause>": [  # X
        "WITH <with-clause-reps>",
        "WITH RECURSIVE <with-clause-options>"
    ],

    "<with-clause-reps>": [
        "<with-clause-options>",
        "<with-clause-options>, <with-clause-reps>"
    ],

    "<with-clause-options>": [
        "<cte-table-name> AS (<select-stmt>)",
        "<cte-table-name> AS MATERIALIZED (<select-stmt>)",
        "<cte-table-name> AS NOT MATERIALIZED (<select-stmt>)"
    ],

    "<schema-name>": ["<string>"],  
    "<index-name>": ["<string>"],
    "<table-name>": ["<string>"],
    "<column-name>": ["<string>"],
    "<trigger-name>": ["<string>"],
    "<view-name>": ["<string>"],
    "<collation-name>": ["<string>"],
    "<pragma-name>": ["<string>"], 
    "<savepoint-name>": ["<string>"],
    "<window-name>": [
        "<string>"
    ],
    "<base-window-name>": [
        "<string>"
    ],

    "<string-literal>": ["'<string>'"],
    "<index-or-table-name>": [
        "<index-name>",
        "<table-name>"
    ],

    "<newline>": [
        "CHAR(10)"
    ],

    "<end-of-input>": [
        "$"
    ],

    "<unary-operator>": [
        "-",
        "+",
        "~"
    ],

    "<binary-operator>": [
        "+",
        "-",
        "*",
        "/",
        "||",
        "=",
        "!=",
        "AND",
        "OR",
        "<",
        ">",
        "<=",
        ">="
    ],

    "<hexdigit>": [
        "<digit>",
        "A", "B", "C", "D", "E", "F",
        "a", "b", "c", "d", "e", "f"
    ],

    "<blob-literal>": [
        "x'<hexdigit>*'",
        "X'<hexdigit>*'"
    ],

    "<alias>": [
        "<string>"
    ],

    "<signed-literal>": [
        "<literal-value>",
        "+<literal-value>",
        "-<literal-value>"
    ],

    "<column-alias>": [
        "<string>"
    ],

    "<table-alias>": [
        "<string>"
    ],


    "<filename>": [
        "<string-literal>"
    ],


    "<foreign-table>": [
        "<table-name>"
    ],

    "<error-message>": [
        "<string-literal>"
    ],

    "<initial-select>": [
        "<select-stmt>"
    ],

    "<recursive-select>": [
        "<select-stmt>"
    ],

    "<name>": [
        "<string>"
    ],

    "<string>": [
        "<char>", "<char><string>"
    ],

    "<digit>": [
        str(i) for i in range(10)
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
}
from fuzzingbook.Grammars import trim_grammar
grammar = trim_grammar(grammar)