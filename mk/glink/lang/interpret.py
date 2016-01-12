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
	equal_var_lvl(name,var,-1)
@see
def equal_var_lvl(name, var, lvl):
	for context in contextlevels[::-1]:
		for v in context:
			if v[0] == name:
				v[1] = var
@see
def add_var(name, var):
	add_var_lvl(name,var,-1)
@see
def add_var_lvl(name, var, lvl):
	sss = None
	for v in contextlevels[lvl]:
		if v[0] == name:
		 	sss = v
		 	break
	if sss == None:
		contextlevels[lvl].append([name, var]);
	else:
		sss[1] = var
	#print(name)
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

@see
def moduleblock(name, blk):
	modules.append([name,[]]); 
	pass


@see
def execblock(blk):
	contextlevels.append([])
	ret = None
	for p in blk.parts:
		ret = evaluate(p)
		try:
			if ret[0] == "__block__return__": 
				del contextlevels[-1]
				return ret[1]
			if ret == "__break__": 
				del contextlevels[-1]
				return "__break__"
		except: pass 
	return contextlevels.pop(-1)

_glb = None

def extern_execblock(blk, glb,_seed):
	global _glb 
	global seed
	_glb = glb
	seed = _seed
	return execblock(blk)

def python_import_impl(str):
	return _glb[str]	

def list_to_list(l):
	ll = []
	for v in l.parts:
		ll.append([evaluate(v)])
	return ll


@see
def evaluate(expr):	
	if expr.type == 'int': return expr.parts[0] 
	if expr.type == 'list': return list_to_list(expr)
	if expr.type == '+': return evaluate(expr.parts[0]) + evaluate(expr.parts[1]) 
	if expr.type == '*': return evaluate(expr.parts[0]) * evaluate(expr.parts[1]) 
	if expr.type == '-': return evaluate(expr.parts[0]) - evaluate(expr.parts[1]) 
	if expr.type == '/': return evaluate(expr.parts[0]) / evaluate(expr.parts[1]) 
	if expr.type == '**': return evaluate(expr.parts[0]) ** evaluate(expr.parts[1]) 
	if expr.type == 'deffunc': add_var(expr.parts[0].parts[0], [expr.parts[0],expr.parts[1]]); return 0
	if expr.type == 'var': return get_var(expr.parts[0]) 
	if expr.type == 'module': moduleblock(expr.parts[0], expr.parts[1]); return 0 
	if expr.type == 'inblock': return execblock(expr) 
	if expr.type == 'python': return python_import_impl(evaluate(expr.parts[0])) 
	if expr.type == 'downlevel': return downlevel(evaluate(expr.parts[0])) 
	if expr.type == 'variables': return contextlevels[evaluate(expr.parts[0])]
	


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
		return execblock(parse_file(file))
	if expr.type == 'exectext': 
		return execblock(parse_text(evaluate(expr.parts[0])))
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
		v = get_var(expr.parts[0])
		contextlevels.append([])
		for z in zip(v[0].parts[1].parts, expr.parts[1].parts):
			add_var(z[0].parts[0], evaluate(z[1]))
		ret = evaluate(v[1])
		del contextlevels[-1]
		return(ret)

	if expr.type == 'equal':
		ev = evaluate(expr.parts[1])
		equal_var(expr.parts[0], ev)
		return(ev)

	if expr.type == 'define':
		ev = evaluate(expr.parts[1])
		add_var(expr.parts[0], ev)
		return(ev)
	print(expr, "EVALUATE ERROR")
	exit()
