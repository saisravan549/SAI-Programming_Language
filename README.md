# SAI-Programming_Language
A small programming language written in Python from scratch, by building a Lexer, Parser and an Interpreter. It supports all the arithmatic operations, Variable declarations, Operations with declared variables, Built-In functions like print(), Function declarations, Function Calls, Looping and Conditional statements, Recursion, Arrays and built-in methods that perform operations on these arrays, Array Indexing, String operations and built-in methods for performing additional string operations, String Indexing. The main reason for building this project is completely based on my personal preference. I always wanted to write a code without actual symbols for all arithmatic and logical operations. I always identify a symbol with the letter of the Symbol's spelling that I stress the most while speaking, rather than the symbol itself. For example, I identify '+' symbol as 'P'. This is my natural instinct and having a language that could allow me to write the code based on my preference is always awesome. Along with this, the syntax of the language is very simple and easy to understand. Below, the grammer for the language is mentioned along with some running examples of the language.

## Grammer
Code => (variable_declaration | condition  | loop | expression)[Code]

variable_declaration => var identifier assign expression
language_keywords => 'var'| 'and' | 'or' | 'if' | 'then' | 'elif' | 'else' | 'for' | 'to' | 'step' | 'while' | 'fun' | 'end'
identifier => ([a:z]([0:9]|[a:z]|'_')[a:z])
assig => "="
condition => "if" conditional_expression "then" condition_body [ "elif" condition_body|

function-declaration::= function-arguments wrapper function-body wrapper
function-arguments::= "(" [ { expression "," } ] ")"
function-body::= program

conditional::= "if" comparison wrapper program wrapper [ { "else if" ... } | "else" wrapper program wrapper ]

comparison::= expression [ comparison-operator expression ]
comparison-operator::= "=="

loop::= "from" expression "to" expression "with" identifier wrapper program wrapper

expression::= term { "+" | "-" term }
term::= factor { "*" | "/" | "%" factor }
factor::= number | string | boolean | array | identifier | "-" factor | "(" expression ")" | function-call
function-call::= identifier "(" [ { expression "," } ] ")"
identifier::= { letter }
number::= { digit } [ "." { digit } ]
string::= """ [ { * } ] """
array::= "[" [ { expression "," } ] "]"
boolean::= "true" | "false"

letter::= "a" | "b" | ... | "y" | "z" | "A" | "B" | ... | "Y" | "Z"
digit::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
