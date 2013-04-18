dedi
====

A scheme like language (Dedi Programming Language), it includes a very basic parser that ignores what it cant parse  

For now, variables, parameters and functions are created and used globally

examples:  

* *;(pr (+ 5 (+ 2 4)))*

add 2 with 4, add with 5 and print

* *;(pr "asdasdsa")*

print this string

* *;(pr (+ "asdasda" "asdasdsa"))*

append strings and print

* *;(pr (sum (l 2 3 4)))*

find sum of the list and print

* *;(pr (h (la (l 2 3) 1)))*

add 1 to the list, take head and print it

* *;(la (l 1 2) (l 2 3))*

append lists

* * (sb (var a 1) (pr (l a 1 2)))

Initiate a statement block that consists of two parts, in the first one defina variable a and assign 1,
in the second statement define a list that consists of a variable, 1 and 2, and print the result

* * (sb (var a (l 1 2 3 4)) (pr (la a (l 1 2))))

Define a, assign a list to it, list_append a and another list [1,2], and print them

* * (fn cust_list (a b) (l 1 2))

Define cust_list function that creates a list from two operands

* * (sb (fn cust_list (a b) (l 1 2)) (pr(cust_list 1 2)))

Define the previously described function, and use it to create a list and print it
