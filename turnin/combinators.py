#!/usr/bin/env python2.7

import sys
import copy

def p_out(expr):
	output = ""
	for item in expr:
		if type(item) is not list:
			output += item
		else:
			output += p_out(item)

	return output

def remove_p(expr):
	if expr[0] != "(": return expr
	opened = 0
	for i, val in enumerate(expr):
		if val == "(":
			opened += 1
		elif val == ")" and opened == 1 and i != len(expr) - 1:
			return expr
		elif val == ")":
			opened -= 1
	return expr[1:-1]

def split_expr(expr):
	cafs = list()
	current_caf = ""
	opened = 0
	for char in expr:
		if char == "(" and opened == 0:
			if len(current_caf): cafs.append(current_caf)
			opened += 1
			current_caf = char
		elif char == ")" and opened == 1:
			opened -= 1
			current_caf += char
			cafs.append(current_caf)
			current_caf = ""
		elif char == "(":
			opened += 1
			current_caf += char
		elif char == ")":
			opened -= 1
			current_caf += char
		elif opened == 0:
			current_caf = char
			cafs.append(current_caf)
			current_caf = ""
		else:
			current_caf += char
	if len(current_caf): cafs.append(current_caf)
	return cafs

def evaluate(expr, exp2):
	ind = 0
	while ind < len(expr):
		old_exp = copy.deepcopy(exp2)
		if ind == 0:
			while expr[0][0] == "(" and ("I" in expr[ind] or "K" in expr[ind] or "S" in expr[ind] or "Y" in expr[ind] or "B" in expr[ind] or "W" in expr[ind]):
				top = expr.pop(ind)
				top = remove_p(top)
				top = split_expr(top)
				for i, val in enumerate(top):
					expr.insert(i, val)
				print p_out(old_exp) + " => " + p_out(exp2)
				old_exp = copy.deepcopy(exp2)
		if expr[ind] == "I":
			expr.pop(ind)
			print p_out(old_exp) + " => " + p_out(exp2)
		elif expr[ind] == "K":
			expr.pop(ind)
			expr.pop(ind+1)
			print p_out(old_exp) + " => " + p_out(exp2)
		elif expr[ind] == "S":
			expr.pop(ind)
			expr.insert(ind+1, expr[ind + 2])
			tmp = str(expr[ind+2]) + str(expr[ind+3])
			expr[ind+2] = "(" + tmp + ")"
			expr.pop(ind+3)
			print p_out(old_exp) + " => " + p_out(exp2)
		elif expr[ind] == "Y":
			## Yx, for example, It should produce x(Yx) 
			expr.pop(ind)
			tmp = "(" + "Y" + str(expr[ind]) + ")"
			expr.insert(ind+1, tmp)
			print p_out(old_exp) + " => " + p_out(exp2)
		elif expr[ind] == "B":
			expr[ind] = "(S(KS)K)"
			print p_out(old_exp) + " => " + p_out(exp2)
		elif expr[ind] == "W":
			expr[ind] = "(SS(SK))"
			print p_out(old_exp) + " => " + p_out(exp2)
		elif len(expr[ind]) > 1 and ("I" in expr[ind] or "K" in expr[ind] or "S" in expr[ind] or "B" in expr[ind] or "W" in expr[ind]):
			expr[ind] = remove_p(expr[ind])
			expr[ind] = split_expr(expr[ind])
			evaluate(expr[ind], exp2) ## recursion
		elif len(expr[ind]) > 1 and expr[ind] == "Y" and ind == 0:
			expr[ind] = remove_p(expr[ind])
			expr[ind] = split_expr(expr[ind])
			evaluate(expr[ind], exp2) ## recursion
		else:
			ind += 1

def main():
	stop = False
	for line in sys.stdin:
		if line[0] == "-":
			stop = True
		if not stop:
			expression = list(line.rstrip())
			expression = remove_p(expression)
			expression = split_expr(expression)
			exp2 = expression
			evaluate(expression, exp2)
			print p_out(expression)
			print ""
		else:
			print line.rstrip()

if __name__ == "__main__":
	main()