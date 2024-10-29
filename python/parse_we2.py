# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex

from bull import VARIATORS_VARNAMESUBSTITUTES, AVAILABLEVNAMES, \
                 translateTHISROWCAT , translateSRC , addbackquotes, \
                 KNOWNCLEVdense , KNOWNCLEVdense_notdifficult 


############### helper functions non-M/O #######
###

## this function, IS_LITLISTremainder, added March 01 for coef moclarify

def IS_LITLISTremainder(p,start) :
  if ( p.understyle in ("as_commalist","as_spacelist") or 
                     p.type in ("commalist","spacelist") ) :
    vec=[]
    if len(p.under) <= start : return False
    for i in range(start,len(p.under)) :
      q = p.under[i]
      if q.type in ("strliteral","intliteral") :
         vec.append(q.text)
      elif q.type=="word" and q.text in KNOWNCLEVdense_notdifficult :
         vec.append( addbackquotes(q.text) )
      else : return False
    return vec
  return False 
#end def IS_LITLISTremainder

############################################################

def IS_LITLIST(p) :
  if p.type in ("o_expr","m_expr") and len(p.under)==1 :
     return IS_LITLIST(p.under[0])
  
  if p.type == "intliteral" : return [p.text]
  if p.type == "strliteral" : return [ p.text ] 
  
  if p.type=="word" and p.text in KNOWNCLEVdense_notdifficult :
     return  [ addbackquotes(p.text) ]
  if ( p.understyle in ("as_commalist","as_spacelist") or 
                     p.type in ("commalist","spacelist") ) :
    vec=[]
    for q in p.under :
      if q.type in ("strliteral","intliteral") :
         vec.append(q.text)
      elif q.type=="word" and q.text in KNOWNCLEVdense_notdifficult :
         vec.append( addbackquotes(q.text) )
      else : return False
    return vec
  return False 
#end def IS_LITLIST

########################################

def IS_CLEVLIST(p) :
  if p.type in ("o_expr","m_expr") and len(p.under)==1 :
     return IS_CLEVLIST(p.under[0])
  if p.type in ("strliteral","intliteral") and p.text in KNOWNCLEVdense : 
     return [p.text] 
  if p.type=="word" and p.text in KNOWNCLEVdense_notdifficult :
     return  [ addbackquotes(p.text) ]
  if ( p.understyle in ("as_commalist","as_spacelist") or 
                     p.type in ("commalist","spacelist") ) :
    vec=[]
    for q in p.under :
      if q.type in ("strliteral","intliteral") and q.text in KNOWNCLEVdense :
         vec.append(q.text)
      elif q.type=="word" and q.text in KNOWNCLEVdense_notdifficult :
         vec.append( addbackquotes(q.text) )
      else : return False
    return vec
  return False 
#end def IS_CLEVLIST

#############################################

def IS_DIFF_LITLIST(p) :
  if p.type in ("o_expr","m_expr") and len(p.under)==1 :
     return IS_DIFF_LITLIST(p.under[0])
  if p.type!="+-expr" or len(p.under)!=2 or p.opvec!=[None,"-"] :
     return False 
  c1 = IS_LITLIST(p.under[0])
  c2 = IS_LITLIST(p.under[1])
  if (c1==False or c2==False) : return False 
  else : return [c1,c2]
#end def IS_DIFF_LITLIST 


def IS_DIFF_CLEVLIST(p):
  if p.type in ("o_expr","m_expr") and len(p.under)==1 :
     return IS_DIFF_CLEVLIST(p.under[0])
  if p.type!="+-expr" or len(p.under)!=2 or p.opvec!=[None,"-"] :
     return False 
  c1 = IS_CLEVLIST(p.under[0])
  c2 = IS_CLEVLIST(p.under[1])
  if (c1==False or c2==False) : return False 
  else : return [c1,c2]
#end def IS_DIFF_CLEVLIST

################################################


def IS_VNAMEPRODUCT(p) :
  if p.type in ("o_expr","m_expr") and len(p.under)==1 :
     return IS_VNAMEPRODUCT(p.under[0])
  if p.type=="word" and p.text in AVAILABLEVNAMES :
     return [ p.text ]
  if len(p.under)==0 :
    item=getVARINAMEo(p)
    if item==None : return False
    return [ item ]
  if p.type=="*expr" :
    vec=[]
    for q in p.under :
      item=getVARINAMEo(q)
      if item==None : return False 
      vec.append(item)
    return vec
  return False 
#end def IS_VNAMEPRODUCT 

########################################################


## this newer version for O, not M
def getVARINAMEo(p) :
  vnspell=None
  if p.type=="word" :
    if p.text in AVAILABLEVNAMES : return p.text 
  ## for THISROWCAT,THISROW?,N,SRC
  if p.type in VARIATORS_VARNAMESUBSTITUTES :
    if p.type=="thisrowcat" :  vnspell=translateTHISROWCAT() 
    if p.type=="thisrow?"   :  vnspell="thisrow?"
    if p.type=="n"          :  vnspell="n" 
    if p.type=="src"        :  vnspell=translateSRC() 
  return vnspell
#end def getVARINAMEo


def isVARINAME(p) :
  return ( (p.type=="word" and p.text in AVAILABLEVNAMES) or
           (p.type in VARIATORS_VARNAMESUBSTITUTES) )
#end def isVARINAME


########################################################


########################################################

def IS_LIST(p) :
  return ( p.understyle in ("as_commalist","as_spacelist") or 
                     p.type in ("commalist","spacelist") )
#end def IS_LIST 

###########################################################

def double_vname_spelling(vnames) :
  vn2 = set()
  for v in vnames : 
    vn2.add( v+"_1" )
    vn2.add( v+"_2" )
  return vn2
#end def double_vname_spelling


