# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


# from tok import ts , tokstrm2 , move_it
from setup import parsenode, Ex , mark_parsenode
from bull import KNOWNCLEVdense_notdifficult




###############################################################
###############################################################
###############################################################


PUNCTU_OPTIONS = set(["!","=","<",">","[","]","{","}","(",")",";","%",
                      "*","/","+","-",":","~",",",".","@"])
PUNCTU_PAIRS = set(["==","!=","<=",">="])


escapes = {}
escapes['n'] = '\n'
escapes['t'] = '\t' 
escapes['\''] = '\'' 
escapes['\"'] = '\"'
escapes['\\'] = '\\'

ts=0 
tokstrm=[]
tokstrm2=[]
nexttok1=""
nexttok2=""

##############################################################

token_object_stream = []

class TokenInfo() :
  pass

BEGIN_LINE_CODE = 1
WHITE_SPACE_CODE = 2
OTHER_TOKEN_CODE = 3
END_LINE_CODE = 4



##############################################################

#### November 2020, substantial modifications to tokenize function
#### Tokens for white space are not retained, however, parser needs to (rarely)
#### be sensitive to white space, hence these changes.

def tokenize(line, line_number) :
  ## this function can only be called for ONE LINE at a time!
  c = 0
  c2 = 0
  tok = None
  tok_list = []
  obj_list = []
  while c < len(line) :
    if line[c].isspace() :
      while c < len(line) and line[c].isspace() : c=c+1
      c2 = c
      tok = None
      continue
    elif line[c]=='#' :      ## Feb 8 2021, deal with # followed by comment
      return tok_list , obj_list
    elif line[c] in ('\"','\'') :
      qu = line[c] 
      c2=c+1 
      quhold=[]
      quhold.append(qu)
      while c2<len(line) and line[c2]!=qu : 
        if line[c2]=='\\' and c2+1<len(line) and line[c2+1] in escapes :
          quhold.append(escapes[line[c2+1]]) 
          c2=c2+2 
        else :
          quhold.append(line[c2]) 
          c2=c2+1 
      if c2==len(line) : raise  Ex("tokenize1")
      if line[c2]!=qu : raise   Ex("tokenize2")
      c2 = c2+1  
      quhold.append(qu)
      quall = "".join(quhold)
      tok = quall
    elif line[c].isdigit() or line[c]=='.' :
      while c2<len(line) and line[c2].isdigit() : c2=c2+1
      if c2<len(line) and line[c2]=='.' : c2=c2+1 
      while c2<len(line) and line[c2].isdigit() : c2=c2+1
      tok = line[c:c2] 
    elif line[c].isalpha() or line[c]=='_' :
      while c2<len(line) and (line[c2].isalnum() or line[c2]=='_') : c2=c2+1
      if ( line[c:c2] in ("have","thisrow") and 
               c2<len(line) and line[c2]=='?' ) : c2=c2+1
      tok = line[c:c2].lower() 
    elif line[c] in PUNCTU_OPTIONS : 
      if c+1<len(line) and line[c:c+2] in PUNCTU_PAIRS :
        tok = line[c:c+2]
        c2=c2+2
      else : 
        tok = line[c]
        c2=c2+1 
    else : raise Ex("tokenize3")


    obj = TokenInfo()
    obj.line_number = line_number
    obj.col_number = c+1       ## 1-based, not 0-based
    obj.col_one_after = c2+1

    if c==0                  :  obj.border1 = BEGIN_LINE_CODE
    elif line[c-1].isspace() :  obj.border1 = WHITE_SPACE_CODE
    else                     :  obj.border1 = OTHER_TOKEN_CODE

    if c2>=len(line)         :  obj.border2 = END_LINE_CODE
    elif line[c2].isspace()  :  obj.border2 = WHITE_SPACE_CODE
    else                     :  obj.border2 = OTHER_TOKEN_CODE

    tok_list.append(tok)
    obj_list.append(obj)
    c = c2
    tok = None
    ## very large while loop ends here

  return tok_list , obj_list
  
#end def tokenize

#################################################################

##########################################################

def move_it(howfar=1) :
  global ts , nexttok1 , nexttok2 , tokstrm2 
  ts = ts+howfar 
  if ts >= len(tokstrm2) : 
    ts=len(tokstrm2) 
    nexttok1=None 
    nexttok2=None
  else :
    nexttok1=tokstrm2[ts]
    if ts+1<len(tokstrm2) : nexttok2=tokstrm2[ts+1] 
    else : nexttok2=None 
#end def move_it

####################################

## this function re-written Feb 8 2021
def load_to_token_stream(rowsofcode,line_num_reset) :
  global tokstrm2 , ts , nexttok1 , nexttok2 , token_object_stream
  ts = 0
  tokstrm2=[]
  nexttok1=None
  nexttok2=None
  token_object_stream=[]
  numlines = len(rowsofcode)
  for k in range(numlines) :
    row = rowsofcode[k]
    j = line_num_reset + k 
    row_of_tokens , row_of_tok_objects = tokenize(row,j)
    tokstrm2.extend(row_of_tokens)
    token_object_stream.extend(row_of_tok_objects)
  if 0<len(tokstrm2) : nexttok1 = tokstrm2[0]
  if 1<len(tokstrm2) : nexttok2 = tokstrm2[1] 
#end def load_to_token_stream

#####################################


###############################################################
###############################################################
###############################################################

def nxWORD(ts2=None) :
  if ts2==None : ts2=ts
  if ts2>=len(tokstrm2) : return False 
  return ( tokstrm2[ts2][0].isalpha() or tokstrm2[ts2][0]=='_' or 
           tokstrm2[ts2]=='%' )
#end def nxWORD


def parseWORD() :
  if ts>=len(tokstrm2) : raise Ex("parseword1")
  p=parsenode() 
  p.text=tokstrm2[ts]
  p.type="word"
  if not (p.text[0].isalpha() or p.text[0]=='_' or 
          p.text=='%')  : raise Ex("parseword2")
  move_it()
  return p
#end def parseWORD


def getWORD() :
  if ts>=len(tokstrm2) : raise Ex("getword1")
  txt=tokstrm2[ts]
  if not (txt[0].isalpha() or txt[0]=='_' or 
          txt=='%')  : raise Ex("getword2")
  move_it()
  return txt
#end def getWORD



#################################


def nxWED(ts2=None) :
  if ts2==None : ts2=ts
  if ts2>=len(tokstrm2) : return False 
  if tokstrm2[ts2][0].isalpha() or tokstrm2[ts2][0]=='_' : return True
  if tokstrm2[ts2][0] in ('\"','\'') : return True 
  if tokstrm2[ts2][0].isdigit() : return True 
  if ( len(tokstrm2[ts2])>=2 and 
       tokstrm2[ts2][0]=='.' and tokstrm2[ts2][1].isdigit() ) : return True 
  if tokstrm2[ts2]=='%' : return True 
  return False 
#end def nxWED



def parseWED() :
  if ts>=len(tokstrm2) : raise Ex("parsewed1")
  p=parsenode() 
  p.text=tokstrm2[ts]
  if p.text[0].isalpha() or p.text[0]=='_' or  p.text=='%'  : p.type="word"
  elif p.text[0] in ('\"','\'') : p.type="strliteral"
  elif p.text[0].isdigit() :
    if '.' in p.text : p.type="floliteral"
    else : p.type="intliteral"
  elif p.text[0]=='.' : 
    if len(p.text)<2 : raise Ex("parsewed2")
    if p.text[1].isdigit() : p.type="floliteral"
    else : raise Ex("parsewed3")
  else : raise Ex("parsewed4")
  move_it()
  return p
#end def parseWED



#####################################


def parseLITERAL() :
  if ts>=len(tokstrm2) : raise Ex("parseliteral1")
  p=parsenode() 
  p.text=tokstrm2[ts]
  if p.text[0].isalpha() or p.text[0]=='_'  : p.type="word"
  ## im assuming already verified it is known clev
  elif p.text[0] in ('\"','\'') : p.type="strliteral"
  elif p.text[0].isdigit() and  '.' not in p.text : p.type="intliteral"
  elif p.text[0].isdigit() and  '.'     in p.text : p.type="floliteral"
  elif ( p.text[0]=='.' and len(p.text)>=2 and  
         p.text[1].isdigit() ) : p.type="floliteral"
  else : raise Ex("parseliteral2")
  move_it()
  return p
#end def parseLITERAL



def getLITERALLIST() :
  litvec=[]
  while nxLITERAL() :
    litvec.append(getLITERAL())
  return litvec
#end def getLITERALLIST


#################################################




def nxLITERAL(ts2=None) :
  if ts2==None : ts2=ts
  if ts2>=len(tokstrm2) : return False 
  if tokstrm2[ts2][0] in ('\"','\'') : return True 
  if tokstrm2[ts2][0].isdigit() : return True 
  if ( len(tokstrm2[ts2])>=2 and 
       tokstrm2[ts2][0]=='.' and tokstrm2[ts2][1].isdigit() ) : return True 
  
  if tokstrm2[ts2][0].isalpha() or tokstrm2[ts2][0]=='_' : 
    if tokstrm2[ts2] in KNOWNCLEVdense_notdifficult : return True 
  
  return False 
#end def nxLITERAL 



def getLITERAL() :
  if ts>=len(tokstrm2) : raise Ex("getliteral1")
  txt=tokstrm2[ts]
  if not (txt[0].isalpha() or txt[0]=='_' or txt[0] in ('\"','\'') or
          txt[0].isdigit() or 
          (txt[0]=='.' and len(txt)>=2 and txt[1].isdigit()) ) : 
      raise Ex("getliteral2")
  move_it()
  return txt
#end def getLITERAL



###########################################################


def parseLISTLIT() :
  tt=ts+1
  vec=[]
  if ts+4 >= len(tokstrm2) : raise Ex("parselistlit1")
  if tokstrm2[ts]!="(" : raise Ex("parselistlit2")
  vec.append(tokstrm2[tt])
  while tt+2 < len(tokstrm2) and tokstrm2[tt+1]=="," :
    tt=tt+2
    vec.append(tokstrm2[tt])
  if tt+1>=len(tokstrm2) or tokstrm2[tt+1]!=")" : raise Ex("parselistlit3")
  
  move_it(tt+2-ts)
  
  p=parsenode()
  p.type="commalist"
  for s in vec :
    q=parsenode()
    q.text=s
    if s[0].isalpha() or s[0]=='_' : q.type="word"
    elif s[0] in ('\"','\'') : q.type="strliteral"
    elif s[0].isdigit() :
      if '.' in s : q.type="floliteral" 
      else : q.type="intliteral"
    elif s[0]=='.' :
      if len(s)>=2 and s[1].isdigit() : q.type="floliteral" 
      else : raise Ex("parselistlit4")
    else : raise Ex("parselistlit5")
    p.under.append(q)
  return p 
  
#end def parseLISTLIT

###############


##############################################


def maybeWORD_OR_LIT() :
  ts2=ts
  if ts>=len(tokstrm2) : return False 
  if tokstrm2[ts2]=='!' : ts2=ts2+1 
  if ts2>=len(tokstrm2) : return False 
  return nxWED(ts2)
#end def maybeWORD_OR_LIT



def see_possible_MARITH() :
  ts2=ts
  if ts>=len(tokstrm2) : return False 
  if tokstrm2[ts2] in ('+','-') : ts2=ts2+1
  if ts2>=len(tokstrm2) : return False 
  return nxWED(ts2) or nxLISTLIT(ts2) 
#end def see_possible_MARITH



def nxLISTLIT(ts2=None) :
  if ts2==None : ts2=ts
  if ts2+3 >= len(tokstrm2) : return False 
  return ( tokstrm2[ts2]=='('    and   nxLITERAL(ts2+1)  and 
           tokstrm2[ts2+2]==','  and   nxLITERAL(ts2+3) )
#end def nxLISTLIT


######################


def previewWED_12() :
  if ts>=len(tokstrm2) : return None 
  ts2 = ts 
  if tokstrm2[ts2]=="!" : ts2 = ts2 + 1
  if ts2>=len(tokstrm2) : return None 
  if nxWED(ts2) : return tokstrm2[ts2] 
  return None
#end def previewWED_12

######################################


def see_and_move(tk1,throwstr="seeandmove") :
  if ts>=len(tokstrm2) : raise Ex(throwstr) 
  if tokstrm2[ts]!=tk1 : raise Ex(throwstr)
  move_it()
#end def see_and_move


def see(tk1) :
  return ts<len(tokstrm2) and tokstrm2[ts]==tk1
#end def see

def see2nd(tk1) :
  return ts+1<len(tokstrm2) and tokstrm2[ts+1]==tk1
#end def see2nd

def seew() :
  if ts>=len(tokstrm2) : return None
  else : return tokstrm2[ts]
#end def seew




#########################################


def getSTRLITERALLISTstrict() :
  ## ignore knownclev not in quotes
  vec=[]
  while ts<len(tokstrm2) and tokstrm2[ts][0] in ("\"","\'") :
    vec.append(tokstrm2[ts])
    move_it()
  return vec
#end def getSTRLITERALLISTstrict



def getRESTRICT_AS_STRING() :
  ts2=ts
  if ts>=len(tokstrm2) or tokstrm2[ts]!="[" : raise Ex("getresasstr1")
  while ts2<len(tokstrm2) and tokstrm2[ts2]!="]" : ts2=ts2+1
  if ts2>=len(tokstrm2) : raise Ex("getresasstr2")
  ## assuming [] not used INSIDE boolean expr., ok for this version
  sublist = tokstrm2[ts+2:ts2]
  sofar = tokstrm2[ts+1]
  for w in sublist :
    if ( (sofar[-1].isalnum() or sofar[-1] in ("_",".","?","\'","\"") ) and 
         (w[0].isalnum() or w[0] in ("_",".","?","\'","\"") )           ) :
       sofar = sofar + (" "+w)
    else :
       sofar = sofar + w 
  # Mar bug fix , strip out ""
  sofar = sofar.replace("\"","\'")
  return sofar 
#end def getRESTRICT_AS_STRING

######################################


def gonnabeLITERALLIST() :
  vec=[]
  while nxWED() :
    w=getWED()
    if w[0].isalpha() or w[0]=="_" :
      w = "\"" + w + "\""
    vec.append(w)
  return vec
#end def gonnabeLITERALLIST



def getWED() :
  if ts>=len(tokstrm2) : raise Ex("getwed1")
  # p=parsenode() 
  txt=tokstrm2[ts]
  if not (txt[0].isalpha() or txt[0]=='_' or txt[0] in ('\"','\'') or
          txt[0].isdigit() or 
          (txt[0]=='.' and len(txt)>=2 and txt[1].isdigit()) ) : 
     raise Ex("getwed2")
  move_it()
  return txt
#end def getWED




def parseDATREF() :
  if not nxWORD() : return None
  w1 = getWORD()
  if see("/") :
    see_and_move("/")
    if not nxWORD() : raise Ex("parsedatref1")
    w2=getWORD()
    return w1 + "/" + w2 
  return w1 
#end def parseDATREF



def fix_to_proper_literal(litvec1) :
  vec2=[]
  for w in litvec1 :
    if w[0].isalpha() or w[0]=="_" : vec2.append("\""+w+"\"")
    else : vec2.append(w)
  return tuple(vec2)
#end def fix_to_proper_literal


def addbackquotes(s) :
  # July 2011 bug fix, do not add quotes to an integer literal :
  if len(s)>0 and (s[0].isdigit() or s[0]=='.') : return s   # integer literal do not touch 
  if len(s)>0 and s[0] not in ("\"","\'") and s[-1] not in ("\"","\'") :
    return  "\"" + s + "\"" 
  else : 
    return s 
#end def addbackquotes


######################################################


def seeWORD_EQ_LIST() :
  if ts+3>=len(tokstrm2) : return False
  if tokstrm2[ts+1] not in ("=","==") : return False 
  return nxWORD(ts) and nxLITERAL(ts+2) and nxLITERAL(ts+3) 
#end def seeWORD_EQ_LIST


def seeWORD_EQ_NULL() :
  if ts+2>=len(tokstrm2) : return False 
  if not nxWORD() : return False
  if not ( tokstrm2[ts+1] in ("=","==","!=") ) : return False
  if not ( tokstrm2[ts+2] in ("null",".") ) : return False 
  return True 
#end def seeWORD_EQ_NULL



def parseWORD_EQ_LIST() :
  p=parsenode()
  p.text = getWORD() 
  p.type = "=range"
  if not ( ts<len(tokstrm2) and tokstrm2[ts] in ("=","==") ) : 
     raise Ex("parsewordeqlist1")
  move_it()
  if not nxLITERAL() : raise Ex("parsewordeqlist2")
  p.literalrange = getLITERALLIST() 
  return p 
#end def parseWORD_EQ_LIST



def parseWORD_EQ_NULL() :
  p=parsenode()
  p.text=getWORD()
  if ts>=len(tokstrm2) : raise Ex("wordeqnull1")
  if tokstrm2[ts] in ("=","==") : p.type = "=null" 
  elif tokstrm2[ts] == "!="     : p.type = "!=null"
  else : raise Ex("wordeqnull2")
  move_it()
  if ts>=len(tokstrm2) : raise Ex("wordeqnull3")
  if tokstrm2[ts] not in ("null",".") : raise Ex("wordeqnull4")
  move_it()
  return p 
#end def parseWORD_EQ_NULL




def seeT_N_HAS() :
  if ts+1>=len(tokstrm2) : return False
  return nxWORD() and tokstrm2[ts+1] in ("has","nothas") 
#end def seeT_N_HAS




###########################################################
###########################################################


def mvWORD() :
  if ts>=len(tokstrm2) : raise Ex("mvword1")
  txt=tokstrm2[ts]
  if not (txt[0].isalpha() or txt[0]=='_' or 
          txt=='%')  : raise Ex("mvword2")
  move_it()
  # just move token stream , dont return a value
#end def mvWORD


def nxWORDEQUAL() :
  return nxWORD() and ts+1<len(tokstrm2) and tokstrm2[ts+1]=="="
#end def nxWORDEQUAL




def nxLPAREN() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="(" 
#end def nxLPAREN

def mvLPAREN() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]=="(" ) : raise Ex("mvlparen1")
  move_it()
#end def mvLPAREN


def nxRPAREN() :
  return ts<len(tokstrm2) and tokstrm2[ts]==")" 
#end def nxRPAREN

def mvRPAREN() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]==")" ) : raise Ex("mvrparen1")
  move_it()
#end def mvRPAREN

##################################



def nxLBRACK() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="[" 
#end def nxLBRACK

def mvLBRACK() :
  if not (  ts<len(tokstrm2) and tokstrm2[ts]=="["   ) : raise Ex("mvlbrack1")
  move_it()
#end def mvLBRACK

def nxRBRACK() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="]" 
#end def nxRBRACK

def mvRBRACK() :
  if not (  ts<len(tokstrm2) and tokstrm2[ts]=="]"   ) : raise Ex("mvrbrack1")
  move_it()
#end def mvRBRACK

###########################

def nxCOMMA() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="," 
#end def nxCOMMA

def mvCOMMA() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]=="," ) : raise Ex("mvcomma1")
  move_it()
#end def mvCOMMA


def nxSEMICOLON() :
  return ts<len(tokstrm2) and tokstrm2[ts]==";" 
#end def nxSEMICOLON

def mvSEMICOLON() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]==";" ) : raise Ex("mvsemicolon1")
  move_it()
#end def mvSEMICOLON


def nxASTERISK() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="*" 
#end def nxASTERISK

def mvASTERISK() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]=="*" ) : raise Ex("mvasterisk1")
  move_it()
#end def mvASTERISK


def nxEXCLAM() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="!" 
#end def nxEXCLAM

def mvEXCLAM() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]=="!" ) : raise Ex("mvexclam1")
  move_it()
#end def mvEXCLAM

################


# careful here : = vs == !!!
def nxEQUAL() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="=" 
#end def nxEQUAL

def mvEQUAL() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]=="=" ) : raise Ex("mvequal1")
  move_it()
#end def mvEQUAL

###################


def nxOR() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="or" 
#end def nxOR

def mvOR() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]=="or" ) : raise Ex("mvor1")
  move_it()
#end def mvOR

def nxAND() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="and" 
#end def nxAND

def mvAND() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]=="and" ) : raise Ex("mvand1")
  move_it()
#end def mvAND

def nxNOT() :
  return ts<len(tokstrm2) and tokstrm2[ts]=="not" 
#end def nxNOT

def mvNOT() :
  if not ( ts<len(tokstrm2) and tokstrm2[ts]=="not" ) : raise Ex("mvnot1")
  move_it()
#end def mvNOT

###################################################





def seePLUSMINUS() :
  return ts<len(tokstrm2) and tokstrm2[ts] in ("+","-") 
#end def seePLUSMINUS

def seeMULTDIV() :
  return ts<len(tokstrm2) and tokstrm2[ts] in ("*","/") 
#end def seeMULTDIV


def getSINGLEOP() :
  if ts>=len(tokstrm2) : raise Ex("getsingleop1") 
  if tokstrm2[ts] not in ("+","-","*","/")  : raise Ex("getsingleop2") 
  w = tokstrm2[ts]
  move_it()
  return w
#end def getSINGLEOP

####################

def nxRELOP() :
  return ( ts<len(tokstrm2) and 
           tokstrm2[ts] in ("<",">","<=",">=","!=","==") )
#end def nxRELOP

def getRELOP() :
  if not ( ts<len(tokstrm2) and 
       tokstrm2[ts] in ("<",">","<=",">=","!=","==")  ) : raise Ex("getrelop1")
  w = tokstrm2[ts]
  move_it()
  return w
#end def getRELOP

######################

def nxDOTINTEGER() :
  return ( ts<len(tokstrm2) and len(tokstrm2[ts])>=2 and 
           tokstrm2[ts][0]=="." and tokstrm2[ts][1].isdigit() )
#end def nxDOTINTEGER

## June 2017 code change, this function has no move_it(), 
## That must be a bug: it's returning the ".3" info, but not moving the 
##   token stream at all, and it's not a preview/peek function

def parseDOTINTEGER() : 
  if not ( ts<len(tokstrm2) and len(tokstrm2[ts])>=2 and 
         tokstrm2[ts][0]=="." and tokstrm2[ts][1].isdigit() ) : 
           raise Ex("pdot1")
  value_to_return = int(tokstrm2[ts][1:])
  move_it()                          # .3 is a single token, only do this once
  return value_to_return
#end def parseDOTINTEGER

# def parseDOTINTEGER() :    (old version, not moving token stream, likely bug)
#   if not ( ts<len(tokstrm2) and len(tokstrm2[ts])>=2 and 
#          tokstrm2[ts][0]=="." and tokstrm2[ts][1].isdigit() ) : raise Ex("pdot1")
#   return int(tokstrm2[ts][1:])
#end def parseDOTINTEGER



####################################################

def seeBRACKSRCEQ() :
  return ( ts+3<len(tokstrm2) and 
           tokstrm2[ts]=="[" and tokstrm2[ts+1]=="src" and 
           tokstrm2[ts+2]=="=" )
#end def seeBRACKSRCEQ
       


def parseSRCEQUAL() :
  if ts+4<len(tokstrm2) : raise Ex("parsesrcequal1")
  if not ( tokstrm2[ts]=="[" and tokstrm2[ts+1]=="src" and 
           tokstrm2[ts+2]=="=" and 
           (tokstrm2[ts+3][0].isalpha() or tokstrm2[ts+3][0]=="_") and 
           tokstrm2[ts+4]=="]"
         ) :  raise Ex("parsesrcequal2")
  vname = tokstrm2[ts+3]
  move_it(5)
  p=parsenode()
  p.type = "srcreset" 
  p.text = vname 
  mark_parsenode(p,"srcreset")   # July 2011 addition
  return p
#end def parseSRCEQUAL



def nxLPAR_WORD_RPAR() :
  return ( ts+2<len(tokstrm2) and tokstrm2[ts]=="(" and tokstrm2[ts+2]==")" and 
           ( tokstrm2[ts+1][0].isalpha() or tokstrm2[ts+1][0]=="_" ) )
#end def nxLPAR_WORD_RPAR



def nxLPAREN_EQUAL() :
  return ts+1<len(tokstrm2) and tokstrm2[ts]=="(" and tokstrm2[ts+1]=="="
#end def nxLPAREN_EQUAL


#######################################

#########################################################
### July 2011, code for parsing PRINT-STAT statement 
#########################################################


def getWED_DOT_CR_INT() :
  if ts>=len(tokstrm2) : raise Ex("weddotcr01")
  if ( (tokstrm2[ts][0].isalpha() or tokstrm2[ts][0]=='_') or 
        tokstrm2[ts]=="%" or tokstrm2[ts][0] in ('\"','\'') ) :
    if ts+1<len(tokstrm2) and tokstrm2[ts+1]=="." :
      if ts+2>=len(tokstrm2) : raise Ex("weddotcr02")
      if ( len(tokstrm2[ts+2])<2 or tokstrm2[ts+2][0] not in ('c','r') or 
           (not tokstrm2[ts+2][1:].isdigit()) ) : raise Ex("weddotcr03") 
      g = (tokstrm2[ts],tokstrm2[ts+2][0],tokstrm2[ts+2][1:])
      move_it(3)
      return g
    else :
      g = (tokstrm2[ts],"","")
      move_it()
      return g
  
  # only int-literal situation still left 
  if (not tokstrm2[ts][0].isdigit()) : raise Ex("weddotcr04") 
  # "60."   in first token
  if tokstrm2[ts][0].isdigit() and tokstrm2[ts][-1]=='.' :
    if ts+1>=len(tokstrm2) : raise Ex("weddotcr05")
    if ( len(tokstrm2[ts+1])<2 or tokstrm2[ts+1][0] not in ('c','r') or 
         (not tokstrm2[ts+1][1:].isdigit()) ) : raise Ex("weddotcr06") 
    g = (tokstrm2[ts][:-1],tokstrm2[ts+1][0],tokstrm2[ts+1][1:])
    move_it(2)
    return g
  
  # "60" and "." in first and second token 
  if tokstrm2[ts].isdigit() and ts+1>=len(tokstrm2) and tokstrm2[ts+1]=="." :
    if ts+2>=len(tokstrm2) : raise Ex("weddotcr07")
    if ( len(tokstrm2[ts+2])<2 or tokstrm2[ts+2][0] not in ('c','r') or 
        (not tokstrm2[ts+2][1:].isdigit()) ) : raise Ex("weddotcr08") 
    g = (tokstrm2[ts],tokstrm2[ts+2][0],tokstrm2[ts+2][1:])
    move_it(3)
    return g
  
  # has to be int-literal with no ".c1" suffix 
  g = (tokstrm2[ts],"","")
  move_it()
  return g
#end def getWED_DOT_CR_INT()

###################################################

### WARNING: some of your older small-tok functions have a bad API, need to 
###   fix it. Works fine as long as no input argument, but if pass input 
###   argument it uses in place of ts counter. Main parse functions do not know
###   where ts is, so makes no sense.

### Some of your older tok-level functions have very nuanced innards, treating
###  % as a word, accepting some known cat-levels with or without surrounding
###  quotes, sometimes treating words(identifiers) and literals as somewhat
###  equivalent, etc. 
### But in response, some of your newer tok-level functions need to be more
###  plain vanilla: for reading a single literal or a list of literals and 
###  typically knowing whether it will be a list of str lits or int lits, etc.

#### small tok-level functions that must directly access ts & tokstrm2 
#### must go in this file (no choice)
#### Year 2021, going to add some more small tok-level functions because of 
####  two upgrades: external-stat-proc-connector and hodgepodge/finetune
####  features

######## tok-level functions for ext stat proc connector follow:


def word_literal_pair_list() :
  global ts , tokstrm2
  vec1 = []
  vec2 = [] 
  while ts<len(tokstrm2) and  \
           (tokstrm2[ts][0].isalpha() or tokstrm2[ts][0]=="_") :
    vec1.append(tokstrm2[ts])
    ts+=1
    vec2.append(None)
    if ts>=len(tokstrm2) : raise Ex("wlpl: out range")
    a = tokstrm2[ts]
    if a[0] in ('\'','\"') or a[0].isdigit() or  \
       (len(a)>1 and a[0]=="." and a[1].isdigit()  ) :
      vec2[-1]=a
      ts+=1
    else :
      raise Ex("wlpl, wed3")
  return vec1 , vec2
# PROOF = 1



def double_word_list() :
  global ts , tokstrm2 
  vec1=[]
  vec2=[]
  while ts<len(tokstrm2) and  \
           (tokstrm2[ts][0].isalpha() or tokstrm2[ts][0]=="_") :
    vec1.append(tokstrm2[ts])
    ts+=1
    vec2.append(None)
    if ts<len(tokstrm2) and tokstrm2[ts]=="(" :
      ts+=1
      if ts+1<len(tokstrm2) and tokstrm2[ts]=="-" and tokstrm2[ts+1]==">" :
        ts+=2
      elif ts<len(tokstrm2) and tokstrm2[ts]=="->" :
        ts+=1
      else :
        raise Ex("wed3, dwl")
      if ts<len(tokstrm2) and  \
         (tokstrm2[ts][0].isalpha() or tokstrm2[ts][0]=="_") :
        vec2[-1]=tokstrm2[ts]
        ts+=1
      else :
        raise  Ex("wed3b, dwl")
      if ts<len(tokstrm2) and tokstrm2[ts]==")" :
        ts+=1
      else :
        raise Ex("wed3c, dwl")
      # end very large IF block
  return vec1 , vec2
## PROOF = 1


##########################################################################


def word_list() :
  global ts , tokstrm2
  vec1 = []
  while ts<len(tokstrm2) and  \
       (tokstrm2[ts][0].isalpha() or tokstrm2[ts][0]=="_"):
    vec1.append(tokstrm2[ts])
    ts+=1
  return vec1



def getSTRING_LITERAL() :
  global ts , tokstrm2
  if ts>len(tokstrm2) : raise Ex("gsl: no str lit")
  if tokstrm2[ts][0] not in ('\'','\"') : raise Ex("gsl: no str-literal")
  val = tokstrm2[ts]
  ts+=1
  return val



def see_model_dotinteger_external() :
  if ts+2>=len(tokstrm2) : return False
  a=tokstrm2[ts]
  b=tokstrm2[ts+1]
  c=tokstrm2[ts+2]
  return a=="model" and b[0]=="."  and b[-1].isdigit() and c=="external"


############################################################################
############################################################################

def see_az_() :
  if ts>=len(tokstrm2) : return False 
  return ( tokstrm2[ts][0].isalpha() or tokstrm2[ts][0]=='_' )
#end def see_az_()

def see_str_lit() :
  if ts>=len(tokstrm2) : return False 
  if tokstrm2[ts][0] in ('\"','\'') : return True   
  return False 
#end def see_str_lit()

def see_int_lit() :
  if ts>=len(tokstrm2) : return False 
  if '.'  in tokstrm2[ts] : return False    ### looking for int, not float !
  if tokstrm2[ts][0].isdigit() : return True 
  return False 
#end def see_int_lit()

def get_str_lit() :
  if ts>=len(tokstrm2) : raise Ex("getstrlit1")
  txt=tokstrm2[ts]
  if txt[0] not in ('\"','\'') : raise Ex("getstrlit2")
  move_it()
  return txt
#end def get_str_lit()

def get_str_lit_unqu() :
  if ts>=len(tokstrm2) : raise Ex("getstrlitu1")
  txt=tokstrm2[ts]
  if txt[0] not in ('\"','\'') : raise Ex("getstrlitu2")
  if txt[-1] not in ('\"','\'') : raise Ex("getstrlitu2b")
  move_it()
  return txt[1:-1]
#end def get_str_lit_unqu()


def get_int_lit() :
  if ts>=len(tokstrm2) : raise Ex("getintlit1")
  txt=tokstrm2[ts]
  if (not txt[0].isdigit()) or ('.' in txt ) : raise Ex("getintlit2")
  move_it()
  return int(txt)
#end def get_int_lit()


def get_int_list_br() :
 if ts>=len(tokstrm2) : raise Ex("intlistbr1")
 if tokstrm2[ts] != '[' : raise Ex("intlistbr2")
 move_it()
 v = []
 while ts<len(tokstrm2) and tokstrm2[ts][0].isdigit() :
   v.append(int(tokstrm2[ts]))
   move_it()
 if ts>=len(tokstrm2) : raise Ex("intlistbr3")
 if tokstrm2[ts] != ']' : raise Ex("intlistbr4")
 move_it()
 return v
#end def get_int_list_br()

def see_word_colon_word() :
  if ts+2>=len(tokstrm2) : return None, None  
  if tokstrm2[ts+1]!=":" : return None, None
  if not (tokstrm2[ts][0].isalpha() or tokstrm2[ts][0]=='_') or  \
     not (tokstrm2[ts+2][0].isalpha() or tokstrm2[ts+2][0]=='_') :
        return None,None
  return tokstrm2[ts], tokstrm2[ts+2]
# end def see_word_colon_word()


def see_2nd_tok(val) :
  if ts+1 >= len(tokstrm2) : return False
  return tokstrm2[ts+1]==val
# end def see_2nd_tok

###########################################################################

### Feb 2021, add these two functions to be "white space aware".
### this is the only case where you need to know if white space precedes
###  the next token, only needed to resolve very old parse ambiguity in 
###  col/row statments :  t ( assorted stuff )  VERSUS o_spell(o-parameters)

## return True if see white space and a token after that
def see_white_space_precede_next_token() :
  ## if there is no next token, it is moot point
  if ts>=len(tokstrm2) : return False
  if len(tokstrm2) != len(token_object_stream) : raise Ex("whiteawarebug")
  w = token_object_stream[ts].border1
  return (w==BEGIN_LINE_CODE or w==WHITE_SPACE_CODE)
  ## here, newline counts as white space (or even begin of file, technically!)

## return True if next is "(" , with no white space or newline before "("
## put it this way: True if it is "(" that is right next to token just read
def see_snug_fit_LPAREN() :
  if ts>=len(tokstrm2) : return False
  if tokstrm2[ts]!="(" : return False
  return ( not see_white_space_precede_next_token() )

### above two functions are unusual, the parser is usually not white-space 
### aware, but white space (or newline) in front of "(" now matters in 
###  col/row statements, to solve parse ambiguity


