
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import shutil

from variables import *
from core import *

sys.path.append('../libpy')
from colortext import color as color
from uassert import uassert as uassert

def saveto(p):
	uassert (len(p) != 0, "you should get new name") 
	uassert (cur_ex(), 'current directory is not exist. load any config at first.')
	uassert (not save_ex(p[0]), p[0] + ' config allready exist')
	try:
		echo_copytree(curdir, path([savedir, p[0]]))
	except IOError:
   		print('Makedir error. Mb permition???')
   		exit()
   	os.remove(path([savedir,p[0],profile]))
   	print(green("succesffualy saved"))

def copy(p):
	uassert (len(p) >= 2, "need more param") 
	uassert (not save_ex(p[1]), 'script allready exists')
	uassert (save_ex(p[0]), 'script is not exists')
	try:
		echo_copytree(path([savedir,p[0]]), path([savedir,p[1]]))
	except IOError:
   		print('Makedir error. Mb permition???')
   		exit()
   	print(green("succesffualy copy"))


def savechange(p):
	nm = []
	nm.append(current_name())
	if save_ex(nm[0]):
		remove(nm)
	saveto(nm)
	
def load(p):
	uassert(len(p)>=1 ,"You should get template conf name.")
	echo_rmtree('./conf')
	echo_copytree('./saveconf/' + p[0], './conf')
	current_name_set(p[0])
	print green("operation success")

def superload(p):
	uassert(len(p)>=1 ,"You should get template conf name.")
	echo_rmtree(curdir)
	echo_copytree(path([superdir,p[0]]), curdir)
	current_name_set(p[0])
	print green("operation success")

def supersave(p):
	uassert (len(p) != 0, "you should get new name") 
	uassert (cur_ex(), 'current directory is not exist. load any config at first.')
	uassert (not super_ex(p[0]), p[0] + ' config allready exist')
	try:
		echo_copytree(curdir, path([superdir, p[0]]))
	except IOError:
   		print('Makedir error. Mb permition???')
   		exit()
   	os.remove(path([superdir,p[0],profile]))
   	print(green("new template has been created"))	
#Name set

def setname(p):
	uassert(len(p)>=1 ,"You should get new conf name.")
	print("Set conf name: " + p[0])
	current_name_set(p[0])


def name(p):
	print(current_name())

def remove(p):
	uassert (len(p) >= 1, "need more param") 
	are_you_sure()
	echo_rmtree(path([savedir, p[0]]))


def ls(p):
	print(os.listdir(savedir))
	
def lsreserve(p):
		dirs = os.listdir(cm_basket)
		dirst = []
		print sorted(dirs, key=lambda d: os.path.getmtime('.cm_basket/' + d))

def templatels(p):
	print(os.listdir(superdir))