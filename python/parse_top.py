# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import reset_c_r_setting , parsenode , Ex , mark_parsenode

from bull import MODELFOOTS, MODELFOOTS_ONLYIF, MODELFOOTS_SUBPOP, \
   CLEV_TO_VNAME, KNOWNDSETS, KNOWNCLEVdense, KNOWNCLEVdense_notdifficult, \
   AVAILABLEVNAMES, THING_DSET, HAVE_NOTHAVE_DATASETS, using_shortbinstyle, \
   BINARYVNAMES, TELE_KEYWORDS, CATVNAMES, SUMMSTATOPTIONS, HAVE_SPELLINGS


from bull2 import subpopdenom_node_to_obj, produce_equal_node, \
                  inconsistent_dtypes


from parse_wed import nxWORD, getWORD, nxWED, getWED, \
     nxDOTINTEGER, parseDOTINTEGER, nxLPAREN, mvLPAREN, \
     mvRPAREN, nxRPAREN, nxSEMICOLON, mvSEMICOLON, \
     nxASTERISK, mvASTERISK, nxLBRACK, nxEXCLAM, mvEXCLAM, mvEQUAL, \
     seeBRACKSRCEQ, maybeWORD_OR_LIT, previewWED_12, addbackquotes, \
     nxLPAREN_EQUAL, getLITERALLIST, fix_to_proper_literal, \
     nxLPAR_WORD_RPAR, parseSRCEQUAL , see_and_move, parseDATREF,  \
     see_snug_fit_LPAREN


from moclarify import MODELCALLSDICT
from parse_res import parseRESTRICT
from parse_mo import parseINSIDE_OF_MO


#### Feb 2021, minor changes to several functions, 
####  call see_snug_fit_LPAREN(), to resolve parse ambiguity
####  assume it is name(parameters) only if no white space between "name" and 
####  left parenthesis  (if there is such white space, then it looks like:
####   name ( other stuff ) , where , in context of row/col statement
####   "name" is separate from "other stuff" and "other stuff" is a parenthesis
####   enclosed group of terms, in the column statement (or row statement).
#### Functions so edited are: parseMO_EXPR(), parseTELE_KEYWORD(),
####          parseCATVN_EXPR()
#### Also, nxDOTINTEGER/parseDOTINTEGER, really should require that to also be
####  a "snug fit" with previous token, maybe will implement that later.
############################################################



## 2020, modified parseMODELFOOT()
def parseMODELFOOT() :
  ctr=None
  w=getWORD()
  if w!="model" : raise Ex("modelfoot1")
  if nxDOTINTEGER() : ctr=parseDOTINTEGER()
  if ctr==None and len(MODELFOOTS)>0 : raise Ex("modelfoot2")
  if ctr!=None and ctr in MODELFOOTS : raise Ex("modelfoot3")

  p=parseMO_EXPR()
  if p.type!="m_expr" : raise Ex("modelfoot4")
  if nxSEMICOLON() : mvSEMICOLON()
  
  subpop3=None
  onlyif3=None
  for q in p.under :
    if q.text=="subpop" : 
      subpop3 = subpopdenom_node_to_obj(q)
    if q.text=="onlyif" :
      onlyif3 = q 
  
  if ctr==None and len(MODELFOOTS)==0 : ctr=1
  MODELFOOTS[ctr] = p
  MODELFOOTS_ONLYIF[ctr] = onlyif3
  MODELFOOTS_SUBPOP[ctr] = subpop3
#end def parseMODELFOOT




#############################################################

def parseMO_EXPR() :
  if not nxWORD() : raise Ex("parsemoexpr1")
  p=parsenode()
  w=getWORD()
  p.text=w
  if nxDOTINTEGER() : p.refnum = parseDOTINTEGER()
  if w in MODELCALLSDICT : p.type="m_expr"
  else : p.type="o_expr"
  ## Feb 2021, replace nxLPAREN() with see_snug_fit_LPAREN()
  if see_snug_fit_LPAREN() :
   mvLPAREN()
   q=parseINSIDE_OF_MO()
   if not nxRPAREN() : raise Ex("parsemoexpr2")
   mvRPAREN()
   p.under.append(q)
   if q.type=="commalist" :
     p.under=q.under
     p.understyle="as_commalist"
   if q.type=="spacelist" :
     p.under=q.under
     p.understyle="as_spacelist"
  mark_parsenode(p,p.text)   # July 2011 addition
  return p
#end def parseMO_EXPR

#################################################







def parseWORDEXPR() :
  w=previewWED_12()
  if w in TELE_KEYWORDS :  return parseTELE_KEYWORD()
  if using_shortbinstyle and w in BINARYVNAMES : 
                           return parseBINARYVN_EXPR()
  # Feb 1, use AVAILABLEVNAMES instead of CATVNAMES here
  if w in AVAILABLEVNAMES :      return parseCATVN_EXPR()
  if ( w in KNOWNCLEVdense_notdifficult or 
       (w in KNOWNCLEVdense and w[0] in ("\"","\'")) ) : 
    return parseCATLEV_EXPR()
  return parseMO_EXPR()
#end def parseWORDEXPR



####################################################################


def parseROW(p) :
  # c_r_setting = "r"
  reset_c_r_setting("r")
  ## DON'T FORGET: PARSENODE __INIT__ self.c_r=c_r_setting
  # p=parsenode()
  p.type="rowtop"
  see_and_move("row","parserow0")
  while (not nxSEMICOLON()) :
     p.under.append(parseMULTIPLYGRP())
  mvSEMICOLON()
  reset_c_r_setting(None)
  # return p
#end def parseROW


def parseCOL(p) :
  # c_r_setting = "c"
  reset_c_r_setting("c")
  # p=parsenode()
  p.type="coltop"
  see_and_move("col","parsecol0")
  while (not nxSEMICOLON()) :
     p.under.append(parseMULTIPLYGRP())
  mvSEMICOLON()
  reset_c_r_setting(None)
  # return p
#end def parseCOL



def parseMULTIPLYGRP() :
  p=parsenode()
  p.type="multiplygrp"
  p.under.append(parseTERM())
  while nxASTERISK() :
    mvASTERISK() 
    p.under.append(parseTERM())
  if len(p.under)>1 : return p
  else : return p.under[0]
#end def parseMULTIPLYGRP


def parseTERM() :
  p=parsenode()
  if nxLPAREN() : return parsePARENGRP()
  if seeBRACKSRCEQ() : return parseSRCEQUAL()
  if nxLBRACK() : return parseRESTRICT() 
  if maybeWORD_OR_LIT() : return parseWORDEXPR() 
  else : raise Ex("parseterm1")
#end def parseTERM



#####################################


def parsePARENGRP() :
  p=parsenode()
  p.type="parengrp"
  if not nxLPAREN() : raise Ex("parseparengrp1")
  mvLPAREN()
  while ( not nxRPAREN() ) :
     p.under.append( parseMULTIPLYGRP())
  mvRPAREN()
  return p 
#end def parsePARENGRP

######################################


def parseTELE_KEYWORD() :
  p=parsenode()
  w=getWORD()
  p.text=w
  p.type=p.text
  mark_parsenode(p,p.text)   # July 2011 addition
  #### ( or p.type = convert(p.text))
  if w=="model":
   p.type="modelref"
   if not nxDOTINTEGER() : raise Ex("parsetele1")
   p.refnum = parseDOTINTEGER()
   return p 
   
  # Feb 11 bug fix, have/nothave  a/dat1 is not a word but a datref 
  if p.text in HAVE_SPELLINGS :
    ## Feb 2021, replace nxLPAREN() with see_snug_fit_LPAREN()
    if see_snug_fit_LPAREN() :
      mvLPAREN()
      dref = parseDATREF() 
      if dref==None : raise Ex("parsetele_baddatref")
      mvRPAREN()
      p.text2nd=dref
      if dref not in KNOWNDSETS : raise Ex("parsetele_unknowndatref")
      HAVE_NOTHAVE_DATASETS.add(p.text2nd)
    return p 
  
  ## Feb 2021, replace nxLPAREN() with see_snug_fit_LPAREN()
  if see_snug_fit_LPAREN() and p.text not in HAVE_SPELLINGS :
   if not nxLPAR_WORD_RPAR() : raise Ex("parsetele2")
   mvLPAREN()
   w2=getWORD()
   p.text2nd=w2
   mvRPAREN()
   # if p.text in HAVE_SPELLINGS :
    # if p.text2nd!=None and p.text2nd not in KNOWNDSETS : raise Ex("parsetele3")
    # if p.text2nd!=None : HAVE_NOTHAVE_DATASETS.add(p.text2nd)
   if p.text in ("n","%") :
    if p.text2nd != "" and p.text2nd not in THING_DSET : raise Ex("parsetele4")
   if p.text in SUMMSTATOPTIONS :
    if p.text2nd != "" and p.text2nd not in AVAILABLEVNAMES : raise Ex("parsetele5")
  return p
#end def parseTELE_KEYWORD


###########################################


def parseCATVN_EXPR() :
  if not nxWORD() : raise Ex("parsecatvn1")
  w=getWORD()
  p=parsenode()
  p.type = "cat"
  p.text=w
  mark_parsenode(p,p.text)   # July 2011 addition
  # Feb 1, CATVNAMES not ready 
  # if w not in CATVNAMES : raise Ex("parsecatvn2")
  if w not in AVAILABLEVNAMES : raise Ex("parsecatvn2b")
  ## Feb 2021, along with nxLPAREN_EQUAL() , use also see_snug_fit_LPAREN()
  if nxLPAREN_EQUAL() and see_snug_fit_LPAREN() :
    mvLPAREN()
    mvEQUAL()
    # remember: issue of whether this range is to be global or local 
    # must decide that 
    p.literalrange = getLITERALLIST()
    p.literalrange = fix_to_proper_literal(p.literalrange) 
    if not nxRPAREN() : raise Ex("parsecatvn3")
    mvRPAREN()
    if inconsistent_dtypes(p.literalrange) : raise Ex("parsecatvn4")
  return p
#end def parseCATVN_EXPR


#############################


def parseBINARYVN_EXPR() :
  exclampt = False 
  if nxEXCLAM() : 
    mvEXCLAM()
    exclampt = True
  if exclampt==True :
    constval="0"
  else :
    constval="1"
  w=getWORD()
  p=produce_equal_node(w,constval)
  mark_parsenode(p,w)   # July 2011 addition
  return p
#end def parseBINARYVN_EXPR


def parseCATLEV_EXPR() :
  if not nxWED() : raise Ex("parsecatlev1")
  w=getWED()
  w=addbackquotes(w)
  v=CLEV_TO_VNAME(w)
  p=produce_equal_node(v,w)
  mark_parsenode(p,w)   # July 2011 addition
  return p
#end def parseCATLEV_EXPR






