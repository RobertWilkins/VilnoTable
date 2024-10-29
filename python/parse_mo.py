# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import parsenode , Ex

from bull import VARIATORS_VARNAMESUBSTITUTES 

from parse_wed import nxCOMMA, mvCOMMA, mvEQUAL, nxWORDEQUAL, mvEQUAL, \
              seePLUSMINUS, seeMULTDIV, getSINGLEOP, nxWORD, parseWORD, \
              nxLITERAL, parseLITERAL, nxLISTLIT, parseLISTLIT, \
              nxWORDEQUAL, see_possible_MARITH




from parse_aux import nxSUBPOPONLYIF, parseSUBPOP_DENOM_ONLYIF

from parse_we2 import isVARINAME


#######################################

def parseINSIDE_OF_MO() :
  p = parsenode()
  p.type = "commalist"
  p.under.append(parseMO_ARG())
  while nxCOMMA() :
   mvCOMMA()
   p.under.append(parseMO_ARG())
  if ( len(p.under) == 1 ) : return p.under[0] 
  else : return p
#end def parseINSIDE_OF_MO



##########################################
#### August change: q=parseMARITHFAC() instead of q=parseWORD() 

def parseMO_ARG() :       ## this fctn fixed Mar 20
  ### isVARINAME1 , maybe unlike isVARINAME, does not need read access to roof 
  p=parsenode()
  if nxSUBPOPONLYIF() :
    return parseSUBPOP_DENOM_ONLYIF()
  if nxWORDEQUAL() :   ## including variator
   q=parseMARITHFAC()   ## not just q=parseWORD, not anymore
   if (not isVARINAME(q)) : raise Ex("parsemoarg1")
   p.under.append(q)
   p.type = "=expr" 
   mvEQUAL()
   p.under.append(parseSPACELIST())
   return p 
  return parseSPACELIST() 
#end def parseMO_ARG


###########################


def parseSPACELIST() :
  p=parsenode()
  p.type="spacelist"
  while see_possible_MARITH() :
    p.under.append(parseMARITH()) 
  if (len(p.under) == 0 ) : raise Ex("parsespacelist1")
  if len(p.under) == 1 : return p.under[0] 
  return p
#end def parseSPACELIST



##############################


def parseMARITH() :
  p=parsenode()
  p.type="+-expr"
  p.opvec=[None]
  if seePLUSMINUS() : p.opvec[0]=getSINGLEOP()
  p.under.append(parseMARITHTERM())
  while seePLUSMINUS() :
    p.opvec.append(getSINGLEOP())
    p.under.append(parseMARITHTERM())
  if len(p.under)==1 and ( p.opvec in ([None],["+"])) : return p.under[0]
  else : return p 
#end def parseMARITH


###############################


def parseMARITHTERM() :
  p=parsenode()
  p.type="*expr"
  p.opvec=[]
  p.under.append(parseMARITHFAC())
  while seeMULTDIV() :
    p.opvec.append(getSINGLEOP())
    p.under.append(parseMARITHFAC())
  if len(p.under)==1 : return p.under[0]
  if (len(p.under)==2 and p.opvec[0]=="/" ) :
    p.type = "/expr" 
    return p 
  for t in p.opvec : 
    if t=="/" : raise Ex("parsemterm1")
  return p 
#end def parseMARITHTERM


#############################################


## August change, if variator, p.type=p.text
## June/July change, also LISTLIT handle :


def parseMARITHFAC() :
  if nxWORD() :
    p=parseWORD()
    if p.text in VARIATORS_VARNAMESUBSTITUTES :
      p.type=p.text
    return p
  if nxLITERAL() : return parseLITERAL()
  if nxLISTLIT() : return parseLISTLIT()
  else : raise Ex("parsemarithfac1") 
#end def parseMARITHFAC








