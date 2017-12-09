#!/usr/bin/env python2.7

import sys
import copy

def print_expr(expr):
	output = ""
	for ex in expr:
		if len(ex) == 0:
			pass
		elif len(ex) > 1:
			output += "("
			output += ex
			output += ")"
		else:
			output += ex
	return output

def list_expr(expr):
	## Make subsets of strings
	opened = 0
	expressions = list()
	curr = list()
	for char in list(expr):
		if char == "(" and opened == 0:
			opened += 1
			if len(curr): expressions.append("".join(curr))
			curr = list()
		elif char == ")" and opened == 1:
			opened -= 1
			if len(curr): expressions.append("".join(curr))
			curr = list()
		elif char == "(":
			opened += 1
			curr.append(char)
		elif char == ")":
			opened -= 1
			curr.append(char)
		elif opened != 0:
			curr.append(char)
		else:
			expressions.append(char)
			curr = list()
	if len(curr): expressions.append("".join(curr))
	return expressions

def evaluate(expr):
	expressions = list_expr(expr)
	ind = 0
	while ind < len(expressions):
		old = copy.deepcopy(expressions)
		if len(expressions[ind]) == 0:
			## Remove empty lists
			expressions.pop(ind)
		elif expressions[ind] == "I" and len(expressions[ind]) == 1:
			## Remove I's for identities
			expressions.pop(ind)
			print print_expr(old) + " => " + print_expr(expressions)
		elif expressions[ind] == "K" and len(expressions[ind]) == 1:
			## Need to be able to pop the first and third arguments
			expressions.pop(ind)
			expressions.pop(ind + 1)
			print print_expr(old) + " => " + print_expr(expressions)
		elif expressions[ind] == "S" and len(expressions[ind]) == 1:
			## Pop the S
			expressions.pop(ind)
			expressions.insert(ind + 1, expressions[ind+2])
			## Make bc the next arguemnt
			new_arg = expressions[ind+2] + expressions[ind+3]
			expressions.insert(ind + 2, new_arg)
			expressions.pop(ind + 3)
			expressions.pop(ind + 3)
			print print_expr(old) + " => " + print_expr(expressions)
		elif len(expressions[ind]) != 1:
			## Get children expressions and add them to expressions
			new_expressions = list_expr(expressions[ind])
			expressions.pop(ind)
			for i, exp in enumerate(new_expressions):
				expressions.insert(ind+i, exp)
			print print_expr(old) + " => " + print_expr(expressions)
		else:
			ind += 1

	return "".join(expressions)
	
def main():
	stop = False
	for line in sys.stdin:
		if line.rstrip()[0] == "-":
			stop = True
		if stop:
			print line.rstrip()
		else:
			expr = line.rstrip()
			evaluate(expr)
			print ""

if __name__ == "__main__":
	main()