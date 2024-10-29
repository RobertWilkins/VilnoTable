
### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex, parsenode,  ExternalMetaStruct , ExtOutputMetaStruct

from bull import  AVAILABLEVNAMES,  EXTERNAL_METAS ,  \
    MODELFOOTS , MODELFOOTS_ONLYIF , MODELFOOTS_SUBPOP

from bull2 import subpopdenom_node_to_obj

from parse_wed import see, seew, see_and_move, parseDOTINTEGER,  \
   getSTRING_LITERAL, nxSEMICOLON, mvSEMICOLON, nxRBRACK,  \
   double_word_list,  word_literal_pair_list,  word_list

from parse_aux import parseONLYIF, parseSUBPOP_DENOM

##########################################################################


def parseMODEL_EXTERNAL_META() :
  EM = ExternalMetaStruct()
  EXTERNAL_METAS.append(EM)
  EM.seqno = len(EXTERNAL_METAS)
  see_and_move("model")
  EM.refnum = parseDOTINTEGER()
  see_and_move("external")
  see_and_move("[")
  w = seew()
  while w!=None and w!="]" :
    if w=="input" : EM.input_vn = parseEXTERNAL_INPUT_VARIABLENAMES()
    elif w=="onlyif" : EM.onlyif = parseONLYIF()
    elif w=="subpop" : EM.subpop = subpopdenom_node_to_obj(parseSUBPOP_DENOM())
    elif w=="sortby" : EM.sortby_ext = parseEXTERNAL_SORTBY()
    elif w=="output" : EM.OUTPUT_METAS.append(parseEXT_OUTPUT_META())
    else :  raise Ex("ext syntax err")
    w = seew()
  see_and_move("]")
  for i in range(len(EM.OUTPUT_METAS)) : 
    EM.OUTPUT_METAS[i].out_seqno = i+1

  if EM.subpop!=None and EM.sortby_ext!=None : raise Ex("subpop,sortby")
  EMwrapper = parsenode()
  EMwrapper.under.append(EM)
  EMwrapper.type = "m_expr_ext"
  EMwrapper.text = "external"
  if EM.refnum in MODELFOOTS : raise Ex("index taken")
  MODELFOOTS[EM.refnum] = EMwrapper
  MODELFOOTS_ONLYIF[EM.refnum] = EM.onlyif
  MODELFOOTS_SUBPOP[EM.refnum] = EM.subpop

  if EM.input_vn==None : raise Ex("input_vn empty")
  for vn in EM.input_vn :
    if vn not in AVAILABLEVNAMES : raise Ex("input_vn bad")
  ## .input_vn must be complete listing, compare with every other vn subset
### end def parseMODEL_EXTERNAL_META()
## PROOF = 1


##########################################################################


def parseEXT_OUTPUT_META() :
  ODS = ExtOutputMetaStruct()
  see_and_move("output")
  ODS.pseudo_filename = getSTRING_LITERAL()
  see_and_move("[")
  w = seew()
  while w!=None and w!="]" :
    if   w=="cat"    : parseEXT_OUTPUT_CAT_LIST(ODS)
    elif w=="stat"   : parseEXT_OUTPUT_STAT_LIST(ODS)
    elif w=="filter" : parseEXT_OUTPUT_FILTER_LIST(ODS)
    else : raise Ex("ext-meta-out-syntax")
    w=seew()
  see_and_move("]")
  if nxSEMICOLON() : mvSEMICOLON() 
  ODS.vnames = set()
  ODS.vnames.update(ODS.cat_vn)
  ODS.vnames.update(ODS.stat_vn)
  ODS.vnames.update(ODS.filter_vn)
  return ODS
### end def parseEXT_OUTPUT_META()
## PROOF = 1

########################################################################

## parse:   cat variablenames v v v(-> v2) v ; ]
def parseEXT_OUTPUT_CAT_LIST(ODS) :
  see_and_move("cat")
  see_and_move("variablenames")
  vec1 , vec2 = double_word_list()
  w = seew()
  if w!=";" and w!="]" :  raise Ex("syntax error, eocl")
  if w==";" : mvSEMICOLON()
  ODS.cat_vn = vec1 
  ODS.cat_sendto = vec2
  explicit_recode = {}
  explicit_recode2 = {}
  auto_send = {}

  for i in range(len(vec1)) :
    if vec1[i] in explicit_recode : raise Ex("syntax err, eocl")
    explicit_recode[vec1[i]] = vec2[i]
    if vec2[i]!=None : explicit_recode2[vec1[i]] = vec2[i]

  for p in explicit_recode :
    if explicit_recode[p]!=None : continue
    if len(p)<2 : continue
    if p[-2].isdigit() : continue
    if len(p)==2 and p[0]=="_" : continue
    if p[-1]=="1" :
      p2nd = p[:-1] + "2"
      if p2nd in explicit_recode and explicit_recode[p2nd]==None :
        w = p[:-1]
        w2 = w
        if len(w)>=2 and w[-1]=="_" :  w2 = w[:-1]
        auto_send[p] = w2
        auto_send[p2nd] = w2
        for k in (3,4,5,6,7,8,9) :
          p3rd = w + str(k)
          if p3rd not in explicit_recode or p3rd in explicit_recode2 : break
          auto_send[p3rd] = w2

  ODS.requested_recodes = explicit_recode2
  ODS.auto_recodes = auto_send
## end def parseEXT_OUTPUT_CAT_LIST()
## PROOF=2

##############################################################


def parseEXT_OUTPUT_FILTER_LIST(ODS) :
  see_and_move("filter")
  see_and_move("variablenames")
  words , literals = word_literal_pair_list()
  if not ( nxSEMICOLON() or nxRBRACK() ) : raise Ex("miss ; or ], eofl")
  if nxSEMICOLON() : mvSEMICOLON()
  ODS.filter_vn = words
  ODS.filter_values = literals
## PROOF=1

def parseEXT_OUTPUT_STAT_LIST(ODS) :
  see_and_move("stat")
  see_and_move("variablenames")
  words = word_list()
  if not ( nxSEMICOLON() or nxRBRACK() ) : raise Ex("miss ; or ], eosl")
  if nxSEMICOLON() : mvSEMICOLON()
  ODS.stat_vn = words  
## PROOF=1


def parseEXTERNAL_INPUT_VARIABLENAMES() :
  see_and_move("input")
  see_and_move("variablenames")
  words = word_list()
  see_and_move(";")
  return words
## PROOF=1

def parseEXTERNAL_SORTBY() :
  see_and_move("sortby")
  words = word_list()
  see_and_move(";")
  if len(words)==1 and (words[0]=="nothing" or words[0]=="empty") :
     words = []
  return words
## drafty, proof~1




