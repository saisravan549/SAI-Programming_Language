# SAI-Programming_Language
A small programming language written in Python from scratch, by building a Lexer, Parser and an Interpreter. It supports all the arithmatic operations, Variable declarations, Operations with declared variables, Built-In functions like print(), Function declarations, Function Calls, Looping and Conditional statements, Recursion, Arrays and built-in methods that perform operations on these arrays, Array Indexing, String operations and built-in methods for performing additional string operations, String Indexing and Error Handling. The main reason for building this project is completely based on my personal preference. I always wanted to write a code without actual symbols for all arithmatic and logical operations. I always identify a symbol with the letter of the Symbol's spelling that I stress the most while speaking, rather than the symbol itself. For example, I identify '+' symbol as 'P'. This is my natural instinct and having a language that could allow me to write the code based on my preference is always awesome. Along with this, the syntax of the language is very simple and easy to understand. Below, the grammer for the language is mentioned along with some running examples of the language.

## Grammer
Code => (variable_declaration | condition  | loop | expression)[Code]

variable_declaration => var identifier assign expression | condition_expression

language_keywords => 'var'| 'and' | 'or' | 'if' | 'then' | 'elif' | 'else' | 'for' | 'to' | 'step' | 'while' | 'fun' | 'end'

arithmatic_operators => {addition : 'P', multiplication : 'L', subtraction : 'M' , division : 'D'}

logical_operators => {logical_and: 'and', logical_or : 'or', logical_not: '!'}

conditional_operators => {greater_than: '>', less_than: '<', greater_than_equal_to: '>=', less_than_equal_to: '<=', not_equal: '!~', double_equal : '~'}

identifier => [a:z][[0:9] | [a:z] | '_'][a:z]

assig => "="

condition => "if" conditional_expression "then" [Code] [ "elif" conditional_expression [Code]] | "else" [Code] [condition]

condition_expression => expression conditional_operators expression

loop => "for" identifier "from" Number|identifier "to" Number|identifier "then" [Code] | "while" Number|identifier conditional_operators Number|identifier "then" [Code] 

expression => term { "P" | "M" term }

term => factor { "L" | "D" factor }

factor => Number | string | boolean | array | identifier | "-" factor | "(" expression ")" | function_call

function_declaration => "fun" identifier function_arguments ":" [Code]

function_arguments => "(" [ { expression "," } ] ")"

function_call => identifier function_arguments

Number => { digit } [ "." { digit } ]

string => """ [ { * } ] """

array => "[" [ { expression "," } ] "]"

boolean => "True" | "False"

digit => "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

## Sample Code and its output

INPUT: Code for nth fibonaucci number

![alt text](https://github.com/saisravan549/SAI-Programming_Language/blob/main/Screen_shots/Screen%20Shot%202021-11-10%20at%206.13.58%20PM.png)

OUTPUT:

Value of 'n' is given as 7 and the output from the language is 8, which is a correct answer.

![alt text](https://github.com/saisravan549/SAI-Programming_Language/blob/main/Screen_shots/Screen%20Shot%202021-11-10%20at%206.14.40%20PM.png)
#
INPUT: Code showcasing the syntax for declaring and using the functions along with nested loops

![alt text](https://github.com/saisravan549/SAI-Programming_Language/blob/main/Screen_shots/Screen%20Shot%202021-11-10%20at%206.21.50%20PM.png)

OUTPUT:

![alt text](https://github.com/saisravan549/SAI-Programming_Language/blob/main/Screen_shots/Screen%20Shot%202021-11-10%20at%206.22.31%20PM.png)
#
INPUT: Code showcasing the operations on list and string

![alt text](https://github.com/saisravan549/SAI-Programming_Language/blob/main/Screen_shots/Screen%20Shot%202021-11-10%20at%206.35.35%20PM.png)

OUTPUT:

![alt text](https://github.com/saisravan549/SAI-Programming_Language/blob/main/Screen_shots/Screen%20Shot%202021-11-10%20at%206.36.07%20PM.png)

## Instructions for using the project

As of now, the entire code is read from a text file. So after cloning the project, the desired code should be written in 'program.txt' file and the following command should be used to run the code:

=> python3 run.py program.txt

'run.py' is the main file in the project which helps in running the code.

'main.py' acts as a dependency for 'run.py' in which the actual implementation of the entire language resides.

'error_pointer.py' is helps to print the error in the language by pointing to the exact error location.

New suggestions and improvements are always welcome :)







