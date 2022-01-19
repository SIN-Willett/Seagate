#int
32435234
#float
34534534.7
#string
'hello'
'"hello world"'
#bool
true
false
print(4.5)
#\ = new line
print('hello', 45, end='\')
# change end= to | to make hello be 'hello | 45' 
print('hello', end='|')
print(45)
#default end = \ so below will print on two lines
print('hello')
print(45)

#var = no special characters bar _ as a space (snake case), can not start with number
#helloWorld = camel case
hello = 'tim'

#will print hello
print(hello)

reads top to bottom
#var can = other var

#Input must be ''
name = input('Name: ')
age = input('Age: ')
#assign input to var
print('Hello', name, 'you are', age, 'years old.')

x = 9
y = 3
result = x + y
print(result)
#int or float, / will always return float unless below
result = int(x/y)
or
#this will i believe give round down int as result
result = x // y

x = 'hello'
y = 3
print (x * y)
#hellohellohello

x = 'hello'
y = 'yes'
print (x + y)
#helloyes

#input always = '' but you can always tell it to look at the '' like an int
num = input('Number: ')
print(int(num) - 5)
#'10' -> 10


hello = 'hello'
print(type(hello))
#will print str aka '' aka string

''.upper(), ''.lower(), ''.capitalise()
#or
print(hello.upper())

'hello'.count('ll')
#returns 1
'hello'.count('l')
#returns 2

#True False = bool
comparison

== equal to
!= not equal to
<= less than or equal to
>= more than or equal to

print(x == y)
#result false (this is bool)
print(ord('a'))
#result ascii value, which is how string are compared with < >
#maths before conditional

not #first
and #between
or #last
#try not to mix these though

1 if, 1 else, as many elif as ya want inbetween

if name == 'Tim':
    print('You are great!')
else:
    print('No')

if x == 'Tim':
