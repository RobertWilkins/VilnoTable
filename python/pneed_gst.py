# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 


from setup import Ex

from bull import tableprint_communicate_filename, \
          printto_filename, zdirectory, \
          COL_PARSE_TREE, ROW_PARSE_TREE, MODELFOOTS, LABELS , \
          format_filename , VN_FORMAT , title_text



tele_counter=0
TABLE_CLEV = {}
easyspell_counter = {}
RELABEL_FORMAT = {}
GCATspell = set()
STATspell = set()

RELABELprint = ""
STATprint = ""
CATprint = ""
colstatement = ""
rowstatement = ""
PRINTTOprint = ""
FORMATFILEprint = ""
TITLETEXTprint = "" 
FILEIMPORTprints = []


###########################################################
###########################################################



def prepGST1() :
  global RELABELprint , STATprint , CATprint , colstatement , rowstatement 
  global PRINTTOprint , FORMATFILEprint, TITLETEXTprint
  global COL_PARSE_TREE , ROW_PARSE_TREE
  # you will modify COL_PARSE_TREE & ROW_PARSE_TREE here 
  #global-read printto_filename
  #global-read RELABEL_FORMAT , STATspell , GCATspell , TABLE_CLEV
  
  t_id_calc(COL_PARSE_TREE)
  t_id_calc(ROW_PARSE_TREE)
  uniquespell_calc(COL_PARSE_TREE)
  uniquespell_calc(ROW_PARSE_TREE)
  colstatement = print_tele_col_or_row(COL_PARSE_TREE,"col")
  rowstatement = print_tele_col_or_row(ROW_PARSE_TREE,"row")
  
  relab1=[]
  for w in RELABEL_FORMAT :
    s = w + "~" + RELABEL_FORMAT[w] 
    relab1.append(s)
  relab1 = ["relabel"] + relab1 + [";"] 
  RELABELprint = " ".join(relab1)
  
  STATprint = "stat " 
  for s in STATspell : STATprint = STATprint + s + " " 
  STATprint = STATprint + ";"
  
  if len(GCATspell)==0 :
    CATprint = " "
  else :
    CATprint = "cat " 
    for v in GCATspell :
      v0 = v[:-1]
      s = v 
      if v in TABLE_CLEV :
        s = s + "~[" + ",".join(TABLE_CLEV[v]) + "]"
      
      ## Feb 2011 modify 
      if v0 in VN_FORMAT and v in TABLE_CLEV : raise Ex("catexpand_and_formatimport")
      if v0 in VN_FORMAT :
        s = s + "~formatfile(\"" + VN_FORMAT[v0] + "\")" 
      
      CATprint = CATprint + ( s + " " )
    CATprint = CATprint + ";"
  
  PRINTTOprint = "printto  " + printto_filename() + " ;" 
  if format_filename()!=None : 
    FORMATFILEprint = "formatfile  " + format_filename() + " ;"  
  if title_text()!=None : 
    TITLETEXTprint = "title " + title_text() + " ;" 
#end def prepGST1


#######################################################


def print_tele_col_or_row(top,rc_option) :
  sv=[]
  for q in top.under : sv.append(print_tele(q))
  if not ( len(top.under)==1 and top.under[0].type=="parengrp" and 
         len(top.under[0].under)>1 ) :
    sv = ["("] + sv + [")"] 
  sv = [ rc_option ] + sv + [";"] 
  s = " ".join(sv)
  return s 
#end def print_tele_col_or_row


def print_tele(p) :
  sv=[]
  if len(p.under)==1 and p.type in ("multiplygrp","parengrp") :
    return print_tele(p.under[0])
  if p.type=="parengrp" :
    for q in p.under : sv.append(print_tele(q))
    sv = ["("] + sv + [")"] 
    s = " ".join(sv) 
    return s
  if p.type=="multiplygrp" :
    for q in p.under : sv.append(print_tele(q))
    s = "*".join(sv)
    return s 
  return p.uniquespell
#end def print_tele


################################################


def uniquespell_calc(p) :
  global LABELS , MODELFOOTS 
  global easyspell_counter , RELABEL_FORMAT , TABLE_CLEV , GCATspell , STATspell
  if p.type in ("rowtop","coltop","parengrp","multiplygrp") :
    for q in p.under : uniquespell_calc(q)
    return
  # Feb 2011 bug fix : cat, no premature return , add "else :" afterwards
  if p.type=="cat" :
    spell1 = p.text + "_"
    GCATspell.add(spell1)
    p.uniquespell = spell1 + str(p.t_id)
    if p.literalrange!=None : 
        TABLE_CLEV[spell1] = fix_to_proper_literal(p.literalrange)
    # return    Feb 2011 bug fix : this is premature return 
  else :    # not "cat"
    spell1 = p.type
    if p.type in ("m_expr","o_expr") : spell1 = p.text
    if spell1=="%" : spell1 = "pct"
    if spell1=="have?" : spell1 = "haveq"
    p.uniquespell = spell1 + "_" + str(p.t_id)
    if p.type in ("o_expr","n","%","mean","median","std","min","max","sum") :
      STATspell.add(p.uniquespell)
  
  ################################################
  
  # ADD THIS TO uniquespell_calc() and initialize _counter at global
  # global easyspell_counter
  
  p.easyspell=p.text
  ## usually correct: all have*3 n % mean cat srcreset m_expr o_expr
  if p.type=="modelref" : 
    ## Nov 2020 , MODELFOOTS now dictionary, index no longer p.refnum-1
    p.easyspell = MODELFOOTS[p.refnum].text
  if p.type=="restrict" : p.easyspell="boolean"
  ## different from p.boolprint 
  
  if p.easyspell in easyspell_counter :
    p.easyspell_index = easyspell_counter[p.easyspell]
    easyspell_counter[p.easyspell]=easyspell_counter[p.easyspell]+1
  else :
    p.easyspell_index = 0
    easyspell_counter[p.easyspell] = 1
  
  ## easyspell : all have have? nothave n % mean sum std min max median 
  ##             trtgrp weight chisq pval boolean
  
  RELABEL_FORMAT[p.uniquespell]= "\"" + p.easyspell + "\""
  if p.type=="restrict" : 
    RELABEL_FORMAT[p.uniquespell]= "\"" + p.boolprint + "\""
  if p.easyspell in LABELS :
    if len(LABELS[p.easyspell])==1 :
      RELABEL_FORMAT[p.uniquespell]=LABELS[p.easyspell][0]
    else :
      if p.easyspell_index>=len(LABELS[p.easyspell]) : raise Ex("labelsrangeout")
      RELABEL_FORMAT[p.uniquespell]=LABELS[p.easyspell][p.easyspell_index]
  
  ## above, all in uniquespell_calc()
#end def uniquespell_calc



####################################################


def t_id_calc(p) :
  global tele_counter
  if p.type in ("rowtop","coltop","parengrp","multiplygrp") :
    for q in p.under : t_id_calc(q) 
    return 
  p.t_id = tele_counter
  tele_counter = tele_counter + 1 
#end def t_id_calc



#####################################################

# May 27 2011 , new input parameter in fctn-call : OUTPUTCOL_CONST
# Feb 1, 2021 : new version of prepGST_FIV() here, swap out old version
#   because of hodgepodge/finetune features, substantial changes here
def prepGST_FIV(ROOFcr_phys,OUTPUTCOL_ROOFINDEX,statcolname,Hanal,   \
                OUTPUTCOL_CONST,slot_ctr,num_slots,slot_fmt,digit_vec) :
  global FILEIMPORTprints
  
  ROOFc = []     # because this is physical ROOFcr, not synthetic one,
  ROOFr = []     #  must calculate ROOFc and ROOFr at this late stage
  for t in ROOFcr_phys :
    if   t.c_r=="c" : ROOFc.append(t)
    elif t.c_r=="r" : ROOFr.append(t)
    else : raise Ex("cr_gfiv")

  ROOFINDEX_OUTPUTCOL={}
  pp1r=[]
  pp1c=[]
  ff2=[]
  for vn in OUTPUTCOL_ROOFINDEX :
    ROOFINDEX_OUTPUTCOL[OUTPUTCOL_ROOFINDEX[vn]]=vn
  ff = [None]*len(ROOFcr_phys)
  
  for i in range(len(ROOFcr_phys)) :
    t = ROOFcr_phys[i]
    if t.type=="cat" :
      if i in ROOFINDEX_OUTPUTCOL : ff[i]=ROOFINDEX_OUTPUTCOL[i]
      else : ff[i] = "*"
    elif t.type in ("o_expr","n","%","mean","sum","std","min","max","median"):
      ff[i] = statcolname
  
  for f in ff : 
    if f!=None : ff2.append(f)
  for t in ROOFc : pp1c.append(t.uniquespell)
  for t in ROOFr : pp1r.append(t.uniquespell)
  
  
  
  # tmpfilename = Hslot_tmpfilename(Hanal)
  # Jan 20 bug fix:
  # oops, precalculation for fullfilepath, via Href_to_fullfilename 
  # is not done soon enough for this function, so redo it by scratch 
  # since Hanal is a statistic(n,%,pvalue) it is not possible for it to 
  # be an incoming dataset, so it must be in zdirectory :
  s1 = "tmp_" + str(Hanal[0]) + "_" + str(Hanal[1]) 
  tmpfilename = zdirectory + "/" + s1 + ".txt"
  
  # May 27 2011 : catlev-subset info is handled here, instead of with GSS-prepcode 
  ex1 = "" 
  if OUTPUTCOL_CONST != {} :
    ex1 = ", "
    for v in OUTPUTCOL_CONST :
      ex1 = ex1 + v + " " + OUTPUTCOL_CONST[v] + " "  
  
  ## Jan 2021, ex2 is additional GST sytax 
  ##   ( and also, slot_ctr right after the fileimport keyword )  
  ex2 = ""
  if slot_ctr>0 or num_slots>1 or slot_fmt!=None or digit_vec!=None :
    ex2 = "+ " + str(num_slots) + " "
    if slot_fmt!=None :
      ex2 += "\"" + slot_fmt + "\"" + " "
    if digit_vec!=None :
      d = "d[" + " ".join([str(i) for i in digit_vec]) + "]"
      ex2 += d
  
  # May 27 2011 : do not forget ex1 inclusion 
  # Jan 2021 : do not forget ex2 inclusion
  fullst1 = ( ["fileimport"] + [str(slot_ctr)] +   \
              ["col["] + pp1c + ["]"] + ["row["] + pp1r + ["]"] +   \
              ["<"] + ["\"" + tmpfilename + "\""] + ff2 + [ex1,ex2,";"]  )
  fullst2 = " ".join(fullst1)
  FILEIMPORTprints.append(fullst2)
  
#end def prepGST_FIV



#############################################


def prepGST2() :
  #globalread PRINTTOprint , colstatement , rowstatement , CATprint , STATprint
  #globalread FILEIMPORTprints , RELABELprint , FORMATFILEprint
  
  gstlines = [PRINTTOprint,colstatement,rowstatement,CATprint,STATprint] 
  gstlines = gstlines + FILEIMPORTprints 
  gstlines.append(RELABELprint)
  gstlines.append(FORMATFILEprint) 
  gstlines.append(TITLETEXTprint)

  # gstlines2 = "\n".join(gstlines) 

  

  # Jan 20 bug fix, gstlines not gstlines2 in for loop
  gstlines3 = []
  for s in gstlines : gstlines3.append( s + "\n" )
  
  # now write it to file for tableprint software to access 
  # tableprint_communicate_filename is special path
  
  file2 = open(tableprint_communicate_filename,'w')
  file2.writelines(gstlines3)
  file2.close()
  
#end def prepGST2





