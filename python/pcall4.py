# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex
from bull import THINGCHOICES, sorted_tvars 


#################################################


def inputrefs_as_tuple(obj) :
  a = []
  for w in ("inputref","inputref1","inputref2") :
    if w in obj.__dict__ and obj.__dict__[w]!=None :
      a.append(obj.__dict__[w])
  return tuple(a)
#end def inputrefs_as_tuple

##################################################





##################################################


def prep_for_BESTSORTWAY() :
  global sorted_tvars 
  # sorted_tvars = [] do this elsewhere ?
  for keyvec in THINGCHOICES :
    for v in keyvec :
      if v not in sorted_tvars :
        sorted_tvars.append(v) 
#end def prep_for_BESTSORTWAY

###########

def BEST_SORT_WAY(list1) :
  list1a = set(list1)
  list2 = []
  for v in sorted_tvars :
    if v in list1a : list2.append(v)
  list3 = list( list1a.difference(list2) )
  list3.sort()
  list4 = list3 + list2 
  return list4
#end def BEST_SORT_WAY

############

def BEST_SORT_WAYc(tuptup_vname) :
  tuptup2 = [None]*len(tuptup_vname)
  for i in range(len(tuptup2)) :
    tuptup2[i] = BEST_SORT_WAY(tuptup_vname[i]) 
  return tuptup2
#end def BEST_SORT_WAYc

##########################################




##################################################

def expand_bool(p) :
  if p.type in ("word","strliteral","intliteral","floliteral") : return p.text
  if p.type=="restrict" : return expand_bool(p.under[0])
  
  if p.type=="and_expr" : return expand_bool_and(p)
  if p.type=="or_expr"  : return expand_bool_or(p)
  if p.type=="not_expr" : return expand_bool_not(p)
  
  if p.type=="thinghas" : return expand_bool_phas(p)
  
  if p.type in ("!=null","=null") : return expand_bool_eqnull(p)
  if p.type=="=range" : return expand_bool_eqrange(p)
  
  if p.type in ("<",">","==","!=","<=",">=") : return expand_bool_rel(p)
  
  if p.type=="+-expr" : return expand_bool_plusminus(p)
  if p.type=="*/expr" : return expand_bool_multdiv(p) 
  # what is this ? should have exited function by now
  raise Ex("expandboolwhat")
#end def expand_bool

######################################################


def expand_bool_plusminus(p) :
  if len(p.opvec)!=len(p.under) : raise Ex("expandboolplus1")
  if p.type!="+-expr" : raise Ex("expandboolplus2")
  svec = []
  vec2 = []
  opvec2 = p.opvec[:]
  if opvec2[0] in (None,"+") : opvec2[0]=""
  for u in p.under :
    needparens=True
    if u.type in ("*/expr","word","strliteral","intliteral","floliteral") :
        needparens=False
    s = expand_bool(u)
    if needparens==True :  s = "(" + s + ")" 
    svec.append(s)
  for i in range(len(p.under)) :
    vec2.append(opvec2[i])
    vec2.append(svec[i])
  s3 = "".join(vec2)
  return s3 
#end def expand_bool_plusminus

############################

def expand_bool_multdiv(p) :
  if len(p.opvec) != len(p.under) - 1 : raise Ex("expandboolmult1")
  if p.type!="*/expr" : raise Ex("expandboolmult2")
  svec = []
  vec2 = []
  opvec2 = [""] + p.opvec[:]
  for u in p.under :
    needparens=True
    if u.type in ("word","strliteral","intliteral","floliteral") :
        needparens=False
    s = expand_bool(u)
    if needparens==True :  s = "(" + s + ")" 
    svec.append(s)
  for i in range(len(p.under)) :
    vec2.append(opvec2[i])
    vec2.append(svec[i])
  s3 = "".join(vec2)
  return s3 
#end def expand_bool_multdiv

################################

def expand_bool_and(p) :
  svec = []
  for u in p.under :
    needparens = True 
    if u.type in ("+-expr","*/expr","word","strliteral","intliteral","floliteral",
              "<",">","==","!=","<=",">=","thinghas","=null","!=null") :
       needparens = False 
    s = expand_bool(u)
    if needparens==True : s = "(" + s + ")" 
    svec.append(s)
  s3 = " and ".join(svec)
  return s3 
#end def expand_bool_and


def expand_bool_or(p) :
  svec = []
  for u in p.under :
    needparens = True 
    if u.type in ("+-expr","*/expr","word","strliteral","intliteral","floliteral",
              "<",">","==","!=","<=",">=","thinghas","=null","!=null") :
       needparens = False 
    s = expand_bool(u)
    if needparens==True : s = "(" + s + ")" 
    svec.append(s)
  s3 = " or ".join(svec)
  return s3 
#end def expand_bool_or


def expand_bool_not(p) :
  return " not(" + expand_bool(p.under[0]) + ")"
#end def expand_bool_not


def expand_bool_phas(p) :
  return p.synthetic_vname + "==1" 
#end def expand_bool_phas


def expand_bool_eqnull(p) :
  if p.type == "=null"    : return p.text + " is null" 
  elif p.type == "!=null" : return p.text + " is not null"
#end def expand_bool_eqnull


def expand_bool_eqrange(p) :
  sv1 = []
  for w in p.literalrange : sv1.append( p.text + "==" + w )
  s1 = " or ".join(sv1)
  return s1
#end def expand_bool_eqrange


def expand_bool_rel(p) :
  return expand_bool(p.under[0]) + " " + p.type + " " + expand_bool(p.under[1])
#end def expand_bool_rel


#####################################################################
#####################################################################
#####################################################################


# REMEMBER: need to set up fullfilepath
# REMEMBER: access get/set for PCALLbegin fix




