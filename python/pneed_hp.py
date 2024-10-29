
### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 




from setup import Ex

from bull import FineTunes , hodge_rows , hodge_cols , hodge_fine_0 ,  \
   hodge_fine , hodge_simple , AVAILABLEVNAMES , SUMM_STAT_NAMES ,  \
   ANY_O_SPELLINGS , STATISTICS_WHERE                  

from pneed import PROCESS_THIS_LEAF


## WHAT ARE YOUR IMPORT REQUIREMENTS FOR PNEED_HP.PY?
## access to PROCESS_THIS_LEAF()  
## access to data structures: FineTunes  hodge_rows hodge_cols
##    hodge_fine_0  hodge_fine  hodge_simple
##    AVAILABLEVNAMES   SUMM_STAT_NAMES  ANY_O_SPELLINGS    
##    crossref_statistic_ROOF()


## BE CAREFUL: for ext-stat-proc connector, there are changes to PNEED
##    so have changes from two sources , handle carefully!

## examine global status of ROOFcr in pneed.py : WHY DID YOU DO THAT?


def PROCESS_THIS_LEAF0(p,L) :
  ROOFcr = L
  
  stat_node = None
  statword = None
  substitute = False
  ROOFc = []
  ROOFr = []
  TABLEPATHi = []
  COL_CAT_CONT_VN = []
  ROW_CAT_CONT_VN = []
  too_many_stat_node = False
  placeholder_possible = True
  
  
  for t in ROOFcr :
    if   t.c_r=="c" : ROOFc.append(t)
    elif t.c_r=="r" : ROOFr.append(t)
    
  for t in ROOFc :
    if t.type=="cat" : COL_CAT_CONT_VN.append(t.text)
    if t.type=="srcreset" and t.text in AVAILABLEVNAMES : 
       COL_CAT_CONT_VN.append(t.text)
  
  for t in ROOFr :
    if t.type=="cat" : ROW_CAT_CONT_VN.append(t.text)
    if t.type=="srcreset" and t.text in AVAILABLEVNAMES : 
       ROW_CAT_CONT_VN.append(t.text)
  
  for i in range(len(ROOFcr)) :
    t = ROOFcr[i]
    TABLEPATHi.append(t.t_id)
    if t.type in SUMM_STAT_NAMES or t.type=="o_expr" :
      if stat_node!=None :
        too_many_stat_node = True
        break
      stat_node = t
      statword = t.text
      if t.c_r not in ("c","r") : raise Ex("pleaf0: c or r")
      index_c_r = t.c_r
      index_stat_node = i
  
  TABLEPATHi = tuple(TABLEPATHi)
  
  if stat_node==None or too_many_stat_node==True :
    return
  
  if TABLEPATHi in hodge_fine_0 : return
  
  
  ## OLD CODE FROM OLD PNEED SCRIPT , MOVE HERE
  ## you will need to remove this code from it's original location
  #### 2011 and 2021 : for PRINT-STAT feature, decide to abort or not abort :
  if stat_node.c_r=="c" : ROOFw = ROOFr    # these 4 lines related to 
  else                  : ROOFw = ROOFc    # old PRINT-STAT statement
  go_nogo = crossref_statistic_ROOF(stat_node,ROOFw)
  if go_nogo==False : return    # do not do this statistic, no PCALL build
  
  
  if statword==None or statword=="" or statword in AVAILABLEVNAMES or  \
     statword in SUMM_STAT_NAMES or statword in ANY_O_SPELLINGS or  \
     stat_node.refnum!=None or stat_node.under!=[] :
    placeholder_possible = False
  
  
  
  # NEXT SECTION: still early in PNEED script, cross-ref with hodge_BLA 
  #              and derive vec_stats
  
  substitute = False
  
  if placeholder_possible and (not substitute) and TABLEPATHi in hodge_fine :
    ## you actually DO still need placeholder stat spelling , explain later
    if statword==hodge_fine[TABLEPATHi][0] :
      substitute = True
      sub_fmt = hodge_fine[TABLEPATHi][1]
      vec_stats = hodge_fine[TABLEPATHi][2]
  
  
  ## PICK ONE OF THE TWO, DITCH THE OTHER 
  if stat_node.c_r=="c" : 
    cat_and_cont = ROW_CAT_CONT_VN
    container = hodge_rows 
  elif stat_node.c_r=="r" :
    cat_and_cont = COL_CAT_CONT_VN
    container = hodge_cols
  else : raise Ex("not_cr")
  
  ## PICK ONE OF THE TWO, DITCH THE OTHER
  ## container , cat_and_cont = hodge_rows , ROW_CAT_CONT_VN  if stat_node.c_r=="c"  else (
  ##                           hodge_cols , COL_CAT_CONT_VN  )
  
  
  if placeholder_possible and (not substitute) and statword in container :
    entry_list = container[statword]
    for entry in entry_list :
      v = entry[0]
      if v in cat_and_cont or v==None :
        substitute = True
        sub_fmt = entry[1]
        vec_stats = entry[2]
        break
  
  if placeholder_possible and (not substitute) and statword in hodge_simple :
    substitute = True 
    sub_fmt = hodge_simple[statword][0]
    vec_stats = hodge_simple[statword][1]
  
  if not substitute :
    sub_fmt = None
    vec_stats = [None]    
  
  
  
  ## NEXT SECTION : maybe put in retrofit_digit_specs_to_fit_stat_vector() ?
  
  digit_vec = None
  if TABLEPATHi in FineTunes : 
    m = len(vec_stats)
    digits = FineTunes[TABLEPATHi].num_digits
    digits_as_list = FineTunes[TABLEPATHi].num_digits_as_list
    if (digits!=None and digits_as_list!=None) : raise Ex("pleaf0: dvec")
    if digits!=None : digit_vec = [digits]*m
    if digits_as_list!=None and digits_as_list!=[] :
      digit_vec = digits_as_list
      if len(digits_as_list) != len(vec_stats) :
        if len(digits_as_list) > len(vec_stats) :
          digit_vec = digits_as_list[0:len(vec_stats)]
        else :
          shortfall = len(vec_stats) - len(digits_as_list)
          digit_vec = digits_as_list + [ digits_as_list[0] ]*shortfall
  
  
  ## here is the fourth page:
  
  pos = index_stat_node
  slot_fmt = sub_fmt
  num_slots = len(vec_stats)
  
  if substitute==True :
    for slot in range(num_slots) :
      stat_node_2 = vec_stats[slot]
      if stat_node_2.c_r!=None : raise Ex("pleaf0: c_r=None")
      stat_node_2.c_r = stat_node.c_r
      ROOFmod = ROOFcr[0:pos] + [stat_node_2] + ROOFcr[pos+1:]
      PROCESS_THIS_LEAF(p,ROOFmod,ROOFcr,slot,num_slots,slot_fmt,digit_vec)
      stat_node_2.c_r = None
  else :    ## no swap-out
    PROCESS_THIS_LEAF(p,ROOFcr,ROOFcr,0,1,None,digit_vec)
  
### end def PROCESS_THIS_LEAF0()
  






##########################################################################


def crossref_statistic_ROOF(stat_node,ROOF) :
  stat1 = stat_node.mark1
  stat2 = stat_node.mark2 
  if stat2 in STATISTICS_WHERE : stat3 = stat2 
  elif stat1 in STATISTICS_WHERE : stat3 = stat1 
  else : return True   # go ahead and print statistic
  
  list_options = STATISTICS_WHERE[stat3]
  
  ROOF_set = set()
  for t in ROOF : ROOF_set.update((t.mark1,t.mark2))

  go_ahead = False 
  for option in list_options :
    if option.issubset(ROOF_set) : go_ahead=True
  return go_ahead
##  end-def crossref_statistic_ROOF()




