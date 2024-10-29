# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import parsenode , Ex , mark_parsenode

from bull import BOOLLOG, BOOLLOG_PH, RESTRICT_SPELL_LOG

from bull2 import varnames_under_r, EQUAL_RESTRICT

from parse_wed import getRESTRICT_AS_STRING, \
     mvLBRACK, mvRBRACK, nxLBRACK, nxRBRACK, \
     nxLPAREN, mvLPAREN, mvRPAREN, nxRPAREN, \
     nxOR, mvOR, nxAND, mvAND, nxNOT, mvNOT, \
     seeT_N_HAS, seeWORD_EQ_LIST, parseWORD_EQ_LIST, \
     seeWORD_EQ_NULL, parseWORD_EQ_NULL, nxRELOP, getRELOP, \
     seePLUSMINUS, seeMULTDIV, getSINGLEOP, \
     nxWED, parseWED, getWORD



##################################################


def parseRESTRICT() :
  p=parsenode()
  p.boolprint = getRESTRICT_AS_STRING()
  p.type="restrict"
  mark_parsenode(p,"boolean")
  mvLBRACK()
  p.under.append(parseBOOL_OR())
  mvRBRACK()
  found=False
  for i in range(len(BOOLLOG)) :
    b=BOOLLOG[i] 
    chk=EQUAL_RESTRICT(p,b)
    if chk==True :
      p.restrict_logno=i 
      found=True 
      break
  if found==False :
    BOOLLOG.append(p) 
    ## June/July add for RESTRICT_SPELL_LOG
    RESTRICT_SPELL_LOG.append(varnames_under_r(p))
    p.restrict_logno=len(BOOLLOG)-1 
  return p 
#end def parseRESTRICT


###############################################



def parseBOOL_OR() :
  p=parsenode()
  p.type="or_expr"
  p.under.append(parseBOOL_AND())
  while nxOR() :
    mvOR() 
    p.under.append(parseBOOL_AND())
  if len(p.under) > 1 : return p 
  else : return p.under[0]
#end def parseBOOL_OR


def parseBOOL_AND() :
  p=parsenode()
  p.type="and_expr"
  p.under.append(parseBOOL_NOT())
  while nxAND() :
    mvAND()
    p.under.append(parseBOOL_NOT())
  if len(p.under) > 1 : return p 
  else : return p.under[0]
#end def parseBOOL_AND



def parseBOOL_NOT() :
  p=parsenode()
  if nxNOT() :
    p.type="not_expr" 
    mvNOT()
    p.under.append(parseBOOL_PAT()) 
    return p 
  else : return parseBOOL_PAT() 
#end def parseBOOL_NOT


######### END THIS PAGE 


def parseBOOL_PAT() :
  p=parsenode()
  if seeT_N_HAS() :
   p.type="thinghas"
   p.text=getWORD()
   p.text2nd=getWORD()
   p.under.append(parseBOOL_REL())
   BOOLLOG=BOOLLOG_PH[p.text]
   found=False
   for i in range(len(BOOLLOG)) :
     b=BOOLLOG[i] 
     chk=EQUAL_RESTRICT(p,b)
     if chk==True :
       p.restrict_logno=i 
       found=True 
       break
   if found==False :
     BOOLLOG_PH[p.text].append(p) 
     p.restrict_logno=len(BOOLLOG)-1 
   p.synthetic_vname = p.text + "_has_" + str(p.restrict_logno)
   return p 
  else : return parseBOOL_REL()
#end def parseBOOL_PAT


############################################################


def parseBOOL_REL() :
  p=parsenode()
  if seeWORD_EQ_LIST() : return parseWORD_EQ_LIST() 
  if seeWORD_EQ_NULL() : return parseWORD_EQ_NULL() 
  p.under.append(parseARITH_PLUS())
  if nxRELOP() :
   p.type=getRELOP()
   p.under.append(parseARITH_PLUS()) 
   return p
  else : 
   return p.under[0] 
#end def parseBOOL_REL


##### end this page 



def parseARITH_PLUS() :
  p=parsenode()
  p.type="+-expr" 
  p.opvec=[None]
  if seePLUSMINUS() : p.opvec[0] = getSINGLEOP()
  p.under.append(parseARITH_MULT())
  while seePLUSMINUS() :
   p.opvec.append(getSINGLEOP())
   p.under.append(parseARITH_MULT())
  if (len(p.under)==1) and (p.opvec in ([None],["+"])) : return p.under[0]
  else : return p 
#end def parseARITH_PLUS



def parseARITH_MULT() :
  p=parsenode()
  p.type="*/expr"
  p.opvec=[]
  p.under.append(parseARITH_FAC())
  while seeMULTDIV() :
   p.opvec.append(getSINGLEOP())
   p.under.append(parseARITH_FAC())
  if len(p.under)==1 : return p.under[0] 
  else : return p
#end def parseARITH_MULT


# Jan 2 2010 , fix : forgot to move lparen and rparen
def parseARITH_FAC() :
  if nxWED() : return parseWED()
  if nxLPAREN() : 
    mvLPAREN()
    return parseBOOL_OR() 
    mvRPAREN()
  else : raise Ex("parsearithfac")
#end def parseARITH_FAC

#######################################







