# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import parsenode , Ex

from bull import printto_filename_set, VNAME_CLEVEL, KNOWNDSETS,  \
               request_convert_ab, DSETS_USED_WITH_THINGS, \
               THING_DSET, THING_KEYVARS, THINGCHOICES, THINGDEFNS, \
               KEYVARS_OF_THING, BOOLLOG_PH, SUBPOPglobal_set, \
               DENOMglobal_set, ONLYIFstack, SD_VARIATORS, CATVNAMES, \
               thingglobalsetting_reset, DIRREFS, LABELS, \
               declared_categorical, declared_continuous, AVAILABLEVNAMES, \
               thingglobalsetting_reset , \
               VN_FORMAT , format_filename_set , title_text_set , \
               KNOWNCLEVdense_notdifficult , \
               STATISTICS_WHERE   # this data structure added July 2011

from bull2 import subpopdenom_node_to_obj, inconsistent_dtypes

from known import KNOWNCLEVupdate, previewCOLSPECSasc, previewCOLSPECSvdt 

from parse_res import parseRESTRICT


from parse_wed import \
    nxWORD, getWORD, parseWORD, nxLPAREN, mvLPAREN, nxLBRACK, nxRPAREN, mvRPAREN, \
    nxSEMICOLON, mvSEMICOLON, mvWORD, nxDOTINTEGER, parseDOTINTEGER, parseDATREF, \
    see, see2nd, see_and_move, nxLITERAL, getLITERAL,  nxASTERISK , \
    gonnabeLITERALLIST, getSTRLITERALLISTstrict , \
    nxWED , addbackquotes ,   getWED_DOT_CR_INT    # this fctn added July 2011




# REMEMBER: DENOMglobal + SUBPOPglobal must be intialized as empty objects with 3 members
# NOT None !
# DENOMglobal = subpopdemomobject()   # not None! , and __init__ adds 3 members 
# SUBPOPglobal= subpopdemomobject()

# where do you put DENOMglobal, SUBPOPglobal ?

# need VNAME_CLEVEL as {}

# MODELFOOTS MODELFOOTS_ONLYIF MODELFOOTS_SUBPOP 
# parseMO_EXPR UNIQUIZE_RESTRICT subpopdenomobject
# KNOWNCLEVdense KNOWNCLEVdense_notdifficult KNOWNCLEVdense_VNAME



##################################################

def parseSUBPOP_DENOM() :
  parenstyle=False
  p=parsenode()
  p.type=getWORD()
  ### July 2017 add this:
  p.text=p.type
  if nxLPAREN() :
    mvLPAREN()
    parenstyle=True
  while True :
    if nxLBRACK() : p.under.append(parseRESTRICT())
    elif nxWORD() :
      q=parseWORD()
      if q.text in SD_VARIATORS : q.type=q.text
      else : 
        q.type="cat"
        # Feb 1 , comment out , CATVNAMES not ready 
        # if q.text not in CATVNAMES : raise Ex("parsesubpopdenomcatvn")
        if q.text not in AVAILABLEVNAMES : raise Ex("parsesubpopdenomcatvn2")
      p.under.append(q)
    else : break 
  
  if parenstyle : 
    if not nxRPAREN() : raise Ex("parsesubpopdenomparen")
    mvRPAREN()
  if nxSEMICOLON() : mvSEMICOLON()
  return p
#end def parseSUBPOP_DENOM



def parseONLYIF() :
  ## if nexttok1!="onlyif" or nexttok2!="[" : raise Ex("ponlyif-nexttok")
  if not (see("onlyif") and see2nd("[")) : raise Ex("ponlyifnexttok")
  mvWORD()
  p=parsenode()
  p.type="onlyif"
  p.under.append(parseRESTRICT())
  if nxSEMICOLON() : mvSEMICOLON()
  return p
#end def parseONLYIF



def parseSUBPOP_DENOM_ONLYIF() :
  ## if nexttok1=="onlyif" : return parseONLYIF()
  ## elif nexttok1 in ("subpop","denom") : return parseSUBPOP_DENOM()
  if see("onlyif") : return parseONLYIF()
  elif see("subpop") or see("denom") : return parseSUBPOP_DENOM()
  else : raise Ex("psubdenonly-nexttok")
#end def parseSUBPOP_DENOM_ONLYIF


def nxSUBPOPONLYIF() :
  ## return nexttok1 in ("subpop","onlyif")
  return see("subpop") or see("onlyif") 
#end def nxSUBPOPONLYIF



########################################



###############################################


#######################################

def parseONLYIFFOOT() :
  p=parseONLYIF()
  ONLYIFstack.append(p.under[0])
#end def parseONLYIFFOOT

def parseSUBPOPFOOT() :
  p=parseSUBPOP_DENOM()
  # NEED SET/GET FOR THIS
  # SUBPOPglobal=subpopdenom_node_to_obj(p)
  SUBPOPglobal_set(subpopdenom_node_to_obj(p))
#end def parseSUBPOPFOOT

def parseDENOMFOOT() :
  p=parseSUBPOP_DENOM()
  # NEED SET/GET FOR THIS
  # DENOMglobal=subpopdenom_node_to_obj(p)
  DENOMglobal_set(subpopdenom_node_to_obj(p))
#end def parseDENOMFOOT


#######################################


def parseINPUTDSET() :
  see_and_move("inputdset","pinput1")
  if not nxWORD() : raise Ex("pinput2")
  format = getWORD()
  if format not in ("vdt","asc","ascii") : raise Ex("pinput3")
  if format=="ascii" : format="asc"
  dref = parseDATREF() 
  if dref==None : raise Ex("pinput4")
  vnlist=[]
  clevinfo={}
  par=None
  while nxWORD() :
    vn=getWORD() 
    vnlist.append(vn)
    if see("~") :
      see_and_move("~","pinput5")
      if see("[") :
        see_and_move("[","pinput6")
        literalrange = gonnabeLITERALLIST() 
        if inconsistent_dtypes(literalrange) : raise Ex("pinput7")
        see_and_move("]","pinput8")
        clevinfo[vn]=literalrange
      elif see("(") :
        see_and_move("(")
        see_and_move("format")
        see_and_move("=")
        vnformat = getWORD()
        see_and_move(")")
        VN_FORMAT[vn] = vnformat
      else : raise Ex("pinput7b")
  if see("1") :
    see_and_move("1")
    see_and_move("*","pinput9")
    see_and_move("(","pinput10")
    par=[]
    while nxWORD() : par.append(getWORD()) 
    see_and_move(")","pinput11")
  see_and_move(";","pinput12")
  vnlist2=set(vnlist)
  if vnlist==[] : raise Ex("pinput13")
  if par!=None : par=tuple(par)
  if par!=None : vnlist2.update(par)
  
  #####################################
  
  # June 2017 this is raising exception, you must find out problem and fix it
  # if ( dref in KNOWNDSETS and format!=KNOWNDSETS[dref] 
  #      and KNOWNDSETS[dref]!="a+v" ) : 
  #    print dref 
  #    print format 
  #    print KNOWNDSETS[dref] 
  #    print "thatisall"
  #    raise Ex("storageformatmismatch")
  
  if dref not in KNOWNDSETS : 
    if   format=="vdt" : 
      previewCOLSPECSvdt(dref)
    elif format=="asc" : 
      previewCOLSPECSasc(dref)
      request_convert_ab[dref] = "waiting" 
    ## open file, put COLSPECs into KNOWNDSETS , if not physically there raise
    ## if ASCII , and VDT version not registered yet, 
    ## then create VDT version automatically, ( assume it will be needed)
  
  if KNOWNDSETS[dref].input_st_seen==True : raise Ex("pinput15")
  KNOWNDSETS[dref].input_st_seen=True
  if not vnlist2.issubset(KNOWNDSETS[dref].vnames) : raise Ex("pinput16")
  KNOWNDSETS[dref].parity=par
  ## par=None different meaning from par=() (means 1 row in dset)
  KNOWNDSETS[dref].shadowed_vnames=KNOWNDSETS[dref].vnames.difference(vnlist2)
  KNOWNDSETS[dref].vnames=KNOWNDSETS[dref].vnames.intersection(vnlist2)
  if len(clevinfo)>0 and KNOWNDSETS[dref].stated_clevs==None : 
    KNOWNDSETS[dref].stated_clevs = {}
  for vn in clevinfo :
    declared_categorical.add(vn)    # Feb 1, add this 
    KNOWNDSETS[dref].stated_clevs[vn]=clevinfo[vn]
    VNAME_CLEVEL[vn]=clevinfo[vn]
    KNOWNCLEVupdate(vn,clevinfo[vn])
  
#end def parseINPUTDSET


###############################


def parseTHINGDEFN() :
  keyvars=[]
  see_and_move("thing","pthing1")
  if not nxWORD() : raise Ex("pthing1b")
  thingword=getWORD()
  see_and_move("uniqval","pthing2")
  see_and_move("(","pthing3")
  while nxWORD() : keyvars.append(getWORD())
  see_and_move(")","pthing4")
  
  dref=parseDATREF()
  if dref==None : raise Ex("pthing5")
  see_and_move(";","pthing6")
  
  keyvars2=set(keyvars)
  keyvars = tuple(keyvars)
  
  if dref not in KNOWNDSETS : raise Ex("pthing7")
  
  if KNOWNDSETS[dref].parity != None :
    if keyvars2 != set(KNOWNDSETS[dref].parity) : raise Ex("pthing8")
  else :
    if not keyvars2.issubset(KNOWNDSETS[dref].vnames) : raise Ex("pthing9")
    KNOWNDSETS[dref].parity = keyvars
  
  THING_DSET[thingword] = dref
  THING_KEYVARS[thingword] = keyvars 
  KEYVARS_OF_THING[thingword] = keyvars 
  
  # add this option for sake of prep-BESTSORTWAY :
  THINGCHOICES.append( keyvars )    # i.e. in order of appearance
  # add this 
  THINGDEFNS.add(thingword)
  
  
  DSETS_USED_WITH_THINGS[dref] = thingword
  
  BOOLLOG_PH[thingword] = []
  
#end def parseTHINGDEFN 


##################################################
##################################################



def parseLABEL() :
  see_and_move("label","plabel1")
  while nxWORD() :
    w=getWORD()
    strvec=getSTRLITERALLISTstrict()
    if len(strvec)==0 : raise Ex("plabel2")
    LABELS[w] = tuple(strvec)
  see_and_move(";","plabel3")
#end def parseLABEL


def parseCONTINUOUSST() :
  see_and_move("continuous","pcontin1")
  while nxWORD() :
    w=getWORD() 
    declared_continuous.add(w)
  see_and_move(";","pcontin2")
#end def parseCONTINUOUSST


def parseCATEGORICALST() :
  see_and_move("categorical","pcateg1")
  while nxWORD() :
    w=getWORD() 
    declared_categorical.add(w)
  see_and_move(";","pcateg2")
#end def parseCATEGORICALST


def parsePRINTTO() :
  see_and_move("printto","pprintto1")
  if not nxLITERAL() : raise Ex("pprintto1b")
  w=getLITERAL()
  see_and_move(";","pprintto2")
  if w[0] not in ("\"","\'") : raise Ex("pprintto3")
  printto_filename_set(w) 
#end def parsePRINTTO

#################################################

def parseFORMATFILE() :
  see_and_move("formatfile","pformat1")
  if not nxLITERAL() : raise Ex("pformat1b")
  w=getLITERAL()
  see_and_move(";","pformat2")
  if w[0] not in ("\"","\'") : raise Ex("pformat3")
  format_filename_set(w) 
#end def parseFORMATFILE


def parseTITLE() :
  see_and_move("title","ptitle1")
  if not nxLITERAL() : raise Ex("ptitle1b")
  w=getLITERAL()
  see_and_move(";","pprintto2")
  if w[0] not in ("\"","\'") : raise Ex("ptitle3")
  title_text_set(w) 
#end def parseTITLE


##################################################

def parseDIRREF() :
  see_and_move("directoryref","pdirref1")
  while nxWORD() :
    w1=getWORD() 
    see_and_move("=","pdirref2")
    if not nxLITERAL() : raise Ex("pdirref3")
    w2=getLITERAL()
    if w2[0]  not in ("\"","\'") : raise Ex("pdirref4")
    if w2[-1] not in ("\"","\'") : raise Ex("pdirref5")
    DIRREFS[w1]=w2[1:-1]
  see_and_move(";","pdirref6")
  ## remember that quotes ARE stripped out in DIRREFS , add back in when needed
  ## @ global , have DIR_SEP="/" for linux/unix 
#end def parseDIRREF

#######################################################################

# where did you  put parseMAIN , is it in file yet ?
# if see("n") and see2nd("~") : parseN_NTHING()

def parseN_NTHING() :
  see_and_move("n","pnnthing1")
  see_and_move("~","pnnthing2")
  see_and_move("n","pnnthing3")
  see_and_move("(","pnnthing4")
  tspec = getWORD()
  thingglobalsetting_reset(tspec)
  see_and_move(")","pnnthing6")
  see_and_move(";","pnnthing7")
#end def parseN_NTHING



########################################################################
######## July 2011, add for parsePRINTSTAT 

# printstat fstat fstat.c1 pvalue.c2  @ T T*T*T T T*T T ;
# whereas T ~ trt trt.r1 literal literal.r2 all all.r1 etc.
#         T could be "red hat" "red hat".r1 60 60.r1  (literals can be t-factors)
def parsePRINTSTAT() :
  see_and_move("printstat","printstat01")
  stats_affected = []
  list_set_fac = []
  # read the list of column stats affected 
  while nxWED() :
    g = getWED_DOT_CR_INT()
    g2 = package_WED_DOT_CR_INT(g) 
    stats_affected.append(g2)
  see_and_move("@","printstat-atsign")
  
  while nxWED() :
    set_fac = set()
    g = getWED_DOT_CR_INT()
    g2 = package_WED_DOT_CR_INT(g)
    set_fac.add(g2)
    while nxASTERISK() :
      g = getWED_DOT_CR_INT()
      g2 = package_WED_DOT_CR_INT(g)
      set_fac.add(g2)
    list_set_fac.append(set_fac)
  
  see_and_move(";","printstat-semicolon")
  for f in stats_affected : 
    STATISTICS_WHERE[f] = list_set_fac
#end parsePRINTSTAT





def package_WED_DOT_CR_INT(g) :
  w = g[0]
  if (w[0].isalpha() or w[0]=='_') and w in KNOWNCLEVdense_notdifficult :
    w = addbackquotes(w)
  g2 = w
  if g[1]!="" :  g2 = w + "." + g[1] + g[2] 
  return g2








