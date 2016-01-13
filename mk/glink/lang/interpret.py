#!/usr/bin/env python3
#coding: utf8

from glink.lang.pars import parse_file as parse_file 
from glink.lang.pars import parse_text as parse_text 
	
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
def equal_var(name, var):
	for context in contextlevels[::-1]:
		for v in context:
			if v[0] == name:
				v[1] = var
				return var

def new_var(name, var):
	contextlevels[-1].append([name, var]);
	
@see
def get_var(name):
	for context in contextlevels[::-1]:
		for v in context:
			if v[0] == name:
				return v[1]
	print("wrong variable " , name)
	exit()


@see
def downlevel(blk):
	for v in blk:
		add_var(v[0], v[1])
	pass

#@see
#def moduleblock(name, blk):
#	modules.append([name,[]]); 
#	pass


@see
def execblock(blk, yield_slot):
	ret = None
	repeat = 0
	while True:
		repeat = 0
		for p in blk.parts:
			ret = evaluate(p)
			try:
				if ret[0] == "__block__return__": 
					return ret[1]
			except: 
				pass
			if ret == "__break__": 
				return "__break__"
			if ret == '__yield__':
				execblock(yield_slot, 0)
			if ret == '__repeat__':
				repeat = 1
		if repeat == 0: break 
	return contextlevels[-1]

_glb = None

def global_start(blk, glb,_seed):
	global _glb 
	global seed
	_glb = glb
	seed = _seed
	contextlevels.append([])
	return execblock(blk, 0)

def python_import_impl(str):
	return _glb[str]	

def list_to_list(l):
	ll = []
	for v in l.parts:
		ll.append([evaluate(v)])
	return ll

def evaluate_block(expr, yield_slot):
	contextlevels.append([]) 
	ret = execblock(expr, 0)
	del contextlevels[-1]
	return ret 

def evaluate_func(expr):
	v = get_var(expr.parts[0])
	contextlevels.append([])
	for z in zip(v[0].parts[1].parts, expr.parts[1].parts):
		new_var(z[0].parts[0], evaluate(z[1]))
	yield_slot = expr.parts[2]
	ret = execblock(v[1], expr.parts[2])
	#print(contextlevels)
	del contextlevels[-1]
	return(ret)


@see
def evaluate(expr):	
	if expr.type == 'int': return expr.parts[0] 
	if expr.type == 'list': return list_to_list(expr)
	if expr.type == '+': return evaluate(expr.parts[0]) + evaluate(expr.parts[1]) 
	if expr.type == '*': return evaluate(expr.parts[0]) * evaluate(expr.parts[1]) 
	if expr.type == '-': return evaluate(expr.parts[0]) - evaluate(expr.parts[1]) 
	if expr.type == '/': return evaluate(expr.parts[0]) / evaluate(expr.parts[1]) 
	if expr.type == '**': return evaluate(expr.parts[0]) ** evaluate(expr.parts[1]) 
	if expr.type == 'deffunc': new_var(expr.parts[0].parts[0], [expr.parts[0],expr.parts[1]]); return 0
	if expr.type == 'var': return get_var(expr.parts[0]) 
	#if expr.type == 'module': moduleblock(expr.parts[0], expr.parts[1]); return 0 
	if expr.type == 'inblock': 
		return evaluate_block(expr, 0)
	if expr.type == 'python': return python_import_impl(evaluate(expr.parts[0])) 
	if expr.type == 'downlevel': return downlevel(evaluate(expr.parts[0])) 
	if expr.type == 'repeat': return '__repeat__' 
	if expr.type == 'variables': return contextlevels[evaluate(expr.parts[0])]
	if expr.type == 'yield': return "__yield__"
	


	if expr.type == 'loop':  
		while True:
			ret = evaluate(expr.parts[0])
			if ret == "__break__": break
		return 0

	if expr.type == 'break':
		return "__break__"

	#if expr.type == 'pfor':  return 0

	if expr.type == 'while':  
		while True:
			if evaluate(expr.parts[0]) == 0: break
			ret = evaluate(expr.parts[1])
			if ret == "__break__": break
		return 0
	

	if expr.type == 'element': return evaluate(expr.parts[0])[evaluate(expr.parts[1])]
	if expr.type == 'execfile': 
		file = open(evaluate(expr.parts[0]))
		return execblock(parse_file(file), 0)
	if expr.type == 'exectext': 
		return execblock(parse_text(evaluate(expr.parts[0])))
	if expr.type == 'str': return expr.parts[0]
	if expr.type == 'return': 
		return ["__block__return__", evaluate(expr.parts[0])]
	
	if expr.type == 'input': return input(); 
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
		return evaluate_func(expr)

	if expr.type == 'equal':
		ev = evaluate(expr.parts[1])
		equal_var(expr.parts[0], ev)
		return(ev)

	if expr.type == 'define':
		ev = evaluate(expr.parts[1])
		new_var(expr.parts[0], ev)
		return(ev)
	print(expr, "EVALUATE ERROR")
	exit()
