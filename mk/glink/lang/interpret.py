#!/usr/bin/env python3
#coding: utf8

from glink.lang.pars import parse_file as parse_file 

class context:
	def __init__(self):
		self.variables = []

	def __repr__(self):
		return str(self.variables)
	
contextlevels = []

seed = 0

def see(f):
	def func(*e):
		if seed == 1:
			print(f.__name__)
			print (*e)
		ret = f(*e)
		return ret
	return func

@see
def add_var(name, var):
	add_var_lvl(name,var,-1)
@see
def add_var_lvl(name, var, lvl):
	sss = None
	for v in contextlevels[lvl].variables:
		if v[0] == name:
		 	sss = v
		 	break
	if sss == None:
		contextlevels[lvl].variables.append([name, var]);
	else:
		sss[1] = var
	#print(name)
@see
def get_var(name):
	for context in contextlevels[::-1]:
		for v in context.variables:
			if v[0] == name:
				return v[1]
	print("wrong variable")
	exit()


@see
def downlevel(blk):
	if blk[0] == "namespace":
		for v in blk[1].variables:
			add_var(v[0], v[1])
	else:
		print("wrong namespace")
		exit()
	pass

@see
def moduleblock(name, blk):
	modules.append([name,[]]); 
	pass

@see
def execblock(blk):
	contextlevels.append(context())
	ret = None
	for p in blk.parts:
		ret = evaluate(p)
		try:
			if ret[0] == "__block__return__": 
				del contextlevels[-1]
				return ret[1]
		except: pass 
	return ['namespace', contextlevels.pop(-1)]
		

@see
def evaluate(expr):	
	if expr.type == 'int': return expr.parts[0] 
	if expr.type == '+': return evaluate(expr.parts[0]) + evaluate(expr.parts[1]) 
	if expr.type == '*': return evaluate(expr.parts[0]) * evaluate(expr.parts[1]) 
	if expr.type == '-': return evaluate(expr.parts[0]) - evaluate(expr.parts[1]) 
	if expr.type == '/': return evaluate(expr.parts[0]) / evaluate(expr.parts[1]) 
	if expr.type == '**': return evaluate(expr.parts[0]) ** evaluate(expr.parts[1]) 
	if expr.type == 'deffunc': add_var(expr.parts[0].parts[0], [expr.parts[0],expr.parts[1]]); return 0
	if expr.type == 'var': return get_var(expr.parts[0]) 
	if expr.type == 'module': moduleblock(expr.parts[0], expr.parts[1]); return 0 
	if expr.type == 'inblock': return execblock(expr) 
	if expr.type == 'downlevel': return downlevel(evaluate(expr.parts[0])) 
	if expr.type == 'variables': return contextlevels[evaluate(expr.parts[0])].variables
	if expr.type == 'import': 
		file = open(evaluate(expr.parts[0]))
		return execblock(parse_file(file))
	if expr.type == 'str': return expr.parts[0]
	if expr.type == 'return': 
		return ["__block__return__", evaluate(expr.parts[0])]
	
	if expr.type == 'input': input();return 0 
	if expr.type == 'print': 
		ev = evaluate(expr.parts[0])
		print(ev)
		return(ev)
	
	if expr.type == 'if': 
		if evaluate(expr.parts[0]):
			ret = evaluate(expr.parts[1])
		else:
			ret = evaluate(expr.parts[2])
		return(ret)

	if expr.type == 'func': 
		contextlevels.append(context())
		v = get_var(expr.parts[0])
		for z in zip(v[0].parts[1].parts, expr.parts[1].parts):
			add_var(z[0].parts[0], evaluate(z[1]))
		ret = evaluate(v[1])
		del contextlevels[-1]
		return(ret)


	if expr.type == 'define':
		ev = evaluate(expr.parts[1])
		add_var(expr.parts[0], ev)
		return(ev)
	print(expr, "EVALUATE ERROR")
	exit()
