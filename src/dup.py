#!/usr/bin/env python2.7

import sys
import copy

def print_expr(expr):
	output = ""
	for ex in expr:
		if len(ex) == 0:
			pass
		elif list(ex[0]) == "list":
			output += print_expr(ex)
		else:
			output += "".join(ex)
	return output

def list_expr(expr):
	## Strip outside parenthesis
	new_expr = expr[1:-1]
	## Loop through expression and get inside expressions
	expressions = list()
	embedded = 0
	curr_expr = list()
	for char in new_expr:
		if char == "(" and embedded == 0:
			embedded += 1
			if len(curr_expr): 
				expressions.append(curr_expr)
				curr_expr = list()
			curr_expr.append(char)
			# Start new expre block
		elif char == ")" and embedded == 1:
			embedded -= 1
			curr_expr.append(char)
			expressions.append(curr_expr)
			curr_expr = list()
		elif char == "(":
			embedded += 1
			curr_expr.append(char)
		elif char == ")":
			embedded -= 1
			curr_expr.append(char)
		else:
			curr_expr.append(char)
	if len(curr_expr): expressions.append(curr_expr)
	return expressions

def evaluate(expr):
	expressions = list_expr(expr)
	ind = 0
	## ((Ia)(Ib))
	while ind < len(expressions):
		old = copy.deepcopy(expressions)
		print expressions
		if len(expressions[ind]) == 0:
			expressions.pop(ind)
		elif expressions[ind][0] == "I":
			expressions[ind].pop(0)
			print print_expr(old) + " => " + print_expr(expressions)
		elif expressions[ind][0] == "K":
			expressions[ind].pop(0)
			expressions[ind].pop(1)
			print print_expr(old) + " => " + print_expr(expressions)
		elif expressions[ind][0] == "(":
			# get children expressions
			new_expressions = list_expr(expressions[ind])
			expressions.pop(ind)
			for i, exp in enumerate(new_expressions):
				expressions.insert(ind+i, exp)
			print print_expr(old) + " => " + print_expr(expressions)
		else:
			expressions[ind] = "".join(expressions[ind])
			ind += 1

	return "".join(expressions)



	
	
def main():
	stop = False
	for line in sys.stdin:
		if line.rstrip() == "---------":
			stop = True
		if stop:
			print line.rstrip()
		else:
			expr = list(line.rstrip())
			expr.insert(0, "(")
			expr.append(")")
			print evaluate(expr)



if __name__ == "__main__":
	main()