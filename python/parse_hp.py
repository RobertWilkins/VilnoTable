
### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex, FineTuneInfo

from bull import hodge_rows , hodge_cols, hodge_fine, hodge_fine_0,  \
  hodge_simple, FineTunes, AVAILABLEVNAMES, SUMM_STAT_NAMES, ANY_O_SPELLINGS

from parse_wed import see_and_move , see, seew, nxWORD, getWORD, mvSEMICOLON,  \
   see_az_ , see_str_lit, get_str_lit_unqu, see_int_lit, get_int_lit,  \
   get_int_list_br, see_word_colon_word, see_2nd_tok

from parse_top import parseTELE_KEYWORD, parseMO_EXPR



def parseHODGEPODGE_ROW_COL() :
  see_and_move("hodgepodge")
  see_and_move(":")
  if not nxWORD() : raise Ex("hp syntax1")
  rc = getWORD() 
  if not see_az_() : raise Ex("hp syntax2")
  if rc=="by_row" :
    container = hodge_rows
  elif rc=="by_column" :
    container = hodge_cols 
  else : raise Ex("hp syntax3")

  fakestat = getWORD()
  if fakestat in AVAILABLEVNAMES or fakestat in SUMM_STAT_NAMES or  \
     fakestat in ANY_O_SPELLINGS : raise Ex("hp: place spell in use")
  if fakestat in hodge_rows or fakestat in hodge_cols : raise Ex("hp:dup1")
  entry_list = []
  while seew()=="when" :
    see_and_move("when")
    if not see_az_() : raise Ex("hp: wordtok1")
    v = getWORD()
    if v not in AVAILABLEVNAMES : raise Ex("hp: not vname")
    see_and_move("then")
    s = None
    stats = []
    if see_str_lit() : s = get_str_lit_unqu()
    g = seew()
    while g not in (None,"when","else",";") :
      if g in SUMM_STAT_NAMES :
        stats.append(parseTELE_KEYWORD())
      else :
        if not see_az_() : raise Ex("hp: az2")
        stats.append(parseMO_EXPR())
      g = seew()
    if stats==[] : raise Ex("hp: stats empty")
    entry_list.append( [v,s,stats] )
  if seew()=="else" :
    see_and_move("else")
    v = None
    s = None
    stats = []
    if see_str_lit() : s = get_str_lit_unqu()
    g = seew()
    while g not in (None,";") :
      if g in SUMM_STAT_NAMES :
        stats.append(parseTELE_KEYWORD())
      else :
        if not see_az_() : raise Ex("hp: az3")
        stats.append(parseMO_EXPR())
      g = seew()
    if stats==[] : raise Ex("hp: stats empty2")
    entry_list.append( [v,s,stats] )
  mvSEMICOLON()
  container[fakestat] = entry_list
## end parseHODGEPODGE_ROW_COL()
## PROOF = 1

#########################################################################


def parseHODGEPODGE_FINETUNE() :
  see_and_move("hodgepodge")
  fmt_str = None 
  stats = []
  intvec = get_int_list_br()
  intvec = tuple(intvec)
  if see("0") :
    see_and_move("0")
    see_and_move(";")
    hodge_fine_0[intvec] = True
    return
  if not see_az_() : raise Ex("hpf-az")
  fakestat = getWORD()
  if see_str_lit() : fmt_str=get_str_lit_unqu()
  g = seew()
  while g not in (None,";") :
    if g in SUMM_STAT_NAMES :
      stats.append(parseTELE_KEYWORD())
    else :
      if not see_az_() : raise Ex("hpf-az2")
      stats.append(parseMO_EXPR())
    g = seew()
  mvSEMICOLON()
  if stats==[] : raise Ex("hpf-stats-empty")
  if intvec in hodge_fine : raise Ex("hpf-duplicate")
  hodge_fine[intvec] = [ fakestat, fmt_str, stats ]
##  end parseHODGEPODGE_FINETUNE()


def parseHODGEPODGE_SIMPLE() :
  see_and_move("hodgepodge")
  fmt_str = None
  stats = []
  if not see_az_() : raise Ex("hps-az")
  fakestat = getWORD()
  if see_str_lit() : fmt_str=get_str_lit_unqu()
  g = seew()
  while g not in (None,";") :
    if g in SUMM_STAT_NAMES :
      stats.append(parseTELE_KEYWORD())
    else :
      if not see_az_() : raise Ex("hps-az2")
      stats.append(parseMO_EXPR())
    g = seew()
  mvSEMICOLON()
  if stats==[] : raise Ex("hps-stats-empty")
  if fakestat in hodge_simple : raise Ex("hps-duplicate")
  hodge_simple[fakestat] = [ fmt_str, stats ]
## end parseHODGEPODGE_SIMPLE()


def parseHODGEPODGE_ANY() :
  if not see("hodgepodge") : raise Ex("hodge_bug1")
  w , w2 = see_word_colon_word() 
  if w2 in ("by_row","by_column") : parseHODGEPODGE_ROW_COL()
  elif see_2nd_tok("[") : parseHODGEPODGE_FINETUNE()
  else : parseHODGEPODGE_SIMPLE()
## end parseHODGEPODGE_ANY()


############################################################################


def parseFINETUNE() :
  see_and_move("finetune")
  if not see("[") : raise Ex("finetune no [")
  intvec = get_int_list_br()
  intvec = tuple(intvec)
  obj = FineTuneInfo()
  if see("digits") :
    see_and_move("digits")
    see_and_move("=")
    if see_int_lit() : obj.num_digits = get_int_lit()
    elif see("[")    : obj.num_digits_as_list = get_int_list_br()
    else : raise Ex("ft: digit syntax")
  mvSEMICOLON()
  if intvec in FineTunes : raise Ex("finetune dup")
  FineTunes[intvec] = obj
##  parseFINETUNE()





