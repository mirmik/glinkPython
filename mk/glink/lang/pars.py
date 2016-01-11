# coding=utf8

from libpy.colortext  import *

from glink.lang.lex import tokens
from glink.lang.lex import lexer
import ply.yacc as yacc

from collections import Iterable

start = 'inblock'


class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)

    def __repr__(self):
        #if isinstance(self.parts, Iterable):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")
        #else:
        #    return self.type + ": " + str(self.parts)

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

def change_type(r, str):
    r2 = r; r2.type = str; return r2

def p_dblock(p):
    """dblock : block
              | divider block"""
    if len(p) == 2: p[0] = p[1]
    if len(p) == 3: p[0] = p[2]

def p_block(p):
    """block : LBRACE inblock RBRACE"""
    p[0] = p[2]

def p_inblock(p):
    """inblock :  
               | metaexpr 
               | inblock divider metaexpr
               | divider inblock
               | inblock divider"""
    if len(p) == 1: p[0] = Node("inblock", [])
    elif len(p) == 2:   p[0] = Node("inblock", [p[1]])
    elif len(p) == 3: 
        if p[2] == "divider": p[0] = p[1]
        else: p[0] = p[2]
    else:             p[0] = p[1].add_parts([p[3]])


def p_print(p):
    """print : PRINT expr"""
    p[0] = Node("print", [p[2]])

def p_module(p):
    """module : MODULE WORD COLON dblock"""
    p[0] = Node("module", [p[2], p[4]])

def p_deffunc(p):
    """deffunc : DEFFUNC func COLON dblock"""
    p[0] = Node("deffunc", [p[2], p[4]])
    
def p_application(p):
    """application : APPLICATION WORD COLON dblock"""
    p[0] = Node("application", [p[2], p[4]])

def p_define(p):
    """define : DEFINE WORD expr"""
    p[0] = Node("define", [p[2], p[3]])

def p_declare(p):
    """declare : WORD COLON expr"""
    p[0] = Node("declare", [p[1], p[3]])

def p_if(p):
    """if : IF expr QUESTION expr COLON expr"""
    p[0] = Node("if", [p[2],p[4],p[6]])

def p_divider(p):
    """divider : DIVIDER"""
    p[0] = "divider"

def p_input(p):
    """input : INPUT"""
    p[0] = Node("input", [])

def p_func(p):
    """func : WORD LPAREN args RPAREN"""
    p[0] = Node("func", [p[1], p[3]])


def p_metaexpr(p):
    """metaexpr : expr
                | deffunc
                | module
                | application
                | declare
                | define
                | downlevel
                | if
                | input"""
    p[0] = p[1]


def p_list(p):
    """list : LBRACKET comms RBRACKET"""
    #if len(p) == 2:
    #    p[0] = change_type(p[1], "list")
    #else:
    p[0] = change_type(p[2], "list")
    

def p_args(p):
    """args : 
            | comms"""
    if len(p) == 1: p[0] = Node("args", [])
    else: p[0] = change_type(p[1], "args")

def p_comms(p):
    """comms : expr
             | comms COMMA expr"""
    if len(p) == 2:
        p[0] = Node("comms", [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_equal(p):
    """equal : WORD EQUALS expr"""
    p[0] = Node("define", [p[1], p[3]])


def p_expr(p):
    """expr : exprnoalg
            | alg0
            | print
            | variables
            | python
            | import
            | equal
            | return"""
    p[0] = p[1]


def p_exprnoalg(p):
    """exprnoalg : term
            | func
            | block
            | list"""
    p[0] = p[1]

def p_return(p):
    """return : RETURN expr"""
    p[0] = Node("return", [p[2]])

def p_term(p):
    """term : str
            | float
            | int 
            | var"""
    p[0] = p[1]

def p_int(p):
    """int : NUMBER"""
    p[0] = Node("int", [p[1]])

def p_python(p):
    """python : PYTHON str"""
    p[0] = Node("python", [p[2]])

def p_import(p):
    """import : IMPORT str"""
    p[0] = Node("import", [p[2]])

def p_downlevel(p):
    """downlevel : DOWNLEVEL expr"""
    p[0] = Node("downlevel", [p[2]])

def p_float(p):
    """float : FLOAT"""
    p[0] = Node("float", [p[1]])

def p_str(p):
    """str : STRING"""
    p[0] = Node("str", [p[1]])

def p_var(p):
    """var : WORD"""
    p[0] = Node("var", [p[1]])

def p_variables(p):
    """variables : VARIABLES expr"""
    p[0] = Node("variables", [p[2]])

def parse_error(str,p):
    print(red(str), p)

def p_error(p):
    print('Unexpected token:', p)
    exit()

def p_alg0(p):
    """alg0 : alg1
            | alg0 PLUSMINUS alg1
            | PLUSMINUS alg1"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Node(p[1], [Node('int', [0]), p[2]])
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_alg1(p):
    """alg1 : alg2
            | alg1 DIVMUL alg2"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_alg2(p):
    """alg2 : alg3
            | alg2 DPROD alg3"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_alg3(p):
    """alg3 : exprnoalg"""
    p[0] = p[1]

parser = yacc.yacc()


def parse_file(file):
    lexer.lexed_file = file
    ret = parser.parse(file.read())
    return ret 