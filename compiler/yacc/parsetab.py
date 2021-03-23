
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPlusMinusleftMultiplyDivideAsmOperation Divide EndProg Equal FunReturn Function GreaterThan GreaterThanOrEqual If Indent Jump LPAREN LowerThan LowerThanOrEqual Minus Multiply NotEqual Number Plus RPAREN RefJump StrictEqual Variableexpression : expression Plus expression\n\n    expression : expression Minus termexpression : termterm : term Multiply factorterm : term Divide factorterm : factorfactor : Numberfactor : LPAREN expression RPAREN'
    
_lr_action_items = {'Number':([0,5,6,7,8,9,],[4,4,4,4,4,4,]),'LPAREN':([0,5,6,7,8,9,],[5,5,5,5,5,5,]),'$end':([1,2,3,4,11,12,13,14,15,],[0,-3,-6,-7,-1,-2,-4,-5,-8,]),'Plus':([1,2,3,4,10,11,12,13,14,15,],[6,-3,-6,-7,6,-1,-2,-4,-5,-8,]),'Minus':([1,2,3,4,10,11,12,13,14,15,],[7,-3,-6,-7,7,-1,-2,-4,-5,-8,]),'RPAREN':([2,3,4,10,11,12,13,14,15,],[-3,-6,-7,15,-1,-2,-4,-5,-8,]),'Multiply':([2,3,4,12,13,14,15,],[8,-6,-7,8,-4,-5,-8,]),'Divide':([2,3,4,12,13,14,15,],[9,-6,-7,9,-4,-5,-8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,5,6,],[1,10,11,]),'term':([0,5,6,7,],[2,2,2,12,]),'factor':([0,5,6,7,8,9,],[3,3,3,3,13,14,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression Plus expression','expression',3,'p_expression_plus','mainYacc.py',41),
  ('expression -> expression Minus term','expression',3,'p_expression_minus','mainYacc.py',51),
  ('expression -> term','expression',1,'p_expression_term','mainYacc.py',56),
  ('term -> term Multiply factor','term',3,'p_term_multiply','mainYacc.py',61),
  ('term -> term Divide factor','term',3,'p_term_div','mainYacc.py',66),
  ('term -> factor','term',1,'p_term_factor','mainYacc.py',71),
  ('factor -> Number','factor',1,'p_factor_num','mainYacc.py',76),
  ('factor -> LPAREN expression RPAREN','factor',3,'p_factor_expr','mainYacc.py',81),
]