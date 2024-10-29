# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 

import os

# sourcefilename_base = "/home/robert/test"
from where import sourcefilename_base

from setup import Ex

from bull import zdirectory, tableprint_communicate_filename, \
COL_PARSE_TREE , ROW_PARSE_TREE, COL_PTRANS_TREE, ROW_PTRANS_TREE, \
PCALL_mode , PCALL_filename, \
ALLSECNS, ALLSECNS_line_ctr, ALLSECNS_type, ALLSECNS_borders, \
EXTERNAL_STATPROC_TEXTS, EXTERNAL_STATPROC_TEXTS2, EXTERNAL_STATPROC_refnums


from bull2 import prepare_dirref_statements,  prepare_request_converts  , \
SETUP_INFLAG_RESTRICTS

from known import getINLINE_VDT_LOG

from parse_wed import seew, load_to_token_stream, see_model_dotinteger_external

from parse_aux import parseINPUTDSET, parseTHINGDEFN, parseONLYIFFOOT, \
parseDENOMFOOT, parseSUBPOPFOOT, parseDIRREF, parsePRINTTO, \
parseLABEL, parseCATEGORICALST, parseCONTINUOUSST, parseN_NTHING , \
parseFORMATFILE , parseTITLE , parsePRINTSTAT

from parse_top import parseMODELFOOT, parseROW, parseCOL

from parse_ext import  parseMODEL_EXTERNAL_META
from parse_hp  import parseHODGEPODGE_ANY ,  parseFINETUNE

from pneed_gst import prepGST1, prepGST2

from sourcing1 import PREPARE_SOURCING_PHAS

from pcall4 import prep_for_BESTSORTWAY

from pcall import do_early_PCALL, finishPCALL

from ptrans import execPTRANS, PROCESS_EACH

#### bug check 
from pneed import gssMcrap , gssOcrap


##########################################################


# ALLSECNS = []        now these put in bull.py
# ALLSECNS_line_ctr=[]
# ALLSECNS_type = []
# ALLSECNS_borders = []
# EXTERNAL_STATPROC_TEXTS = []
# EXTERNAL_STATPROC_TEXTS2 = {}
# EXTERNAL_STATPROC_refnums = []





## 2020, ext-connector, this function totally rewritten
def load_sourcecode(sourcefilename) :
  global ALLSECNS , ALLSECNS_type , ALLSECNS_borders , ALLSECNS_line_ctr
  ## May 2021, do not use sourcefilename_base 
  ##  instead rely upon CWD (current working directory)
  ## sourcefilename2 = sourcefilename_base + "/" + sourcefilename
  f1 = open(sourcefilename,'r')    ## May 2021, sourcefilename,  
                                   ##  not sourcefilename2
  L = f1.readlines()
  f1.close()
  i=0
  while i<len(L) :
    chk = check_secn_border(L,i)
    ALLSECNS.append([])
    ALLSECNS_line_ctr.append(i)    ## added Feb 2021
      ## further down, after i+=2, twice, could readjust, but does not matter
    ALLSECNS_type.append("")
    ALLSECNS_borders.append(["","","",""])
    if chk==None :
      while i<len(L) and chk==None :
        ALLSECNS[-1].append(L[i])
        i=i+1
        chk = check_secn_border(L,i)
    elif chk=="vdt" :
      ALLSECNS_type[-1]="vdt"
      ALLSECNS_borders[-1][0] = L[i]
      ALLSECNS_borders[-1][1] = L[i+1]
      i+=2
      chk = check_endvdt(L,i)
      while i<len(L) and chk!=True :
        ALLSECNS[-1].append(L[i])
        i+=1
        chk = check_endvdt(L,i)
      if chk==True :
        ALLSECNS_borders[-1][2] = L[i]
        ALLSECNS_borders[-1][3] = L[i+1]
        i+=2

    elif chk=="ext" :
      ALLSECNS_type[-1]="ext"
      ALLSECNS_borders[-1][0] = L[i]
      ALLSECNS_borders[-1][1] = L[i+1]
      i+=2
      chk = check_endext(L,i)
      while i<len(L) and chk!=True :
        ALLSECNS[-1].append(L[i])
        i+=1
        chk = check_endext(L,i)
      if chk==True :
        ALLSECNS_borders[-1][2] = L[i]
        ALLSECNS_borders[-1][3] = L[i+1]
        i+=2
## end function load_sourcecode()
## PROOF=1



########################################################

# STILL NEED TO DEAL WITH COMMENTS , AND WHITE SPACE WITH LEFT PAREN
#   (uh-no, i believe the code for that already done)


## 2020, ext-connector, this function totally rewritten
def doit(sourcefilename) :
  global ALLSECNS, ALLSECNS_type, ALLSECNS_line_ctr, ALLSECNS_borders, \
   EXTERNAL_STATPROC_TEXTS, EXTERNAL_STATPROC_TEXTS2, EXTERNAL_STATPROC_refnums
  load_sourcecode(sourcefilename)
  i = 0
  while i<len(ALLSECNS) : 
    if ALLSECNS_type[i]=="vdt" :
      H = prepare_dirref_statements()
      G = prepare_request_converts()
      SECN2 = H + G + ALLSECNS[i]
      have_vdt_code_executed(SECN2)
      getINLINE_VDT_LOG()
      i+=1
    else :
      ###  bla!="vdt"     ->  means either standard or "ext"
      while i<len(ALLSECNS) and ALLSECNS_type[i]!="vdt" :
        if ALLSECNS_type[i]=="ext" :
          EXTERNAL_STATPROC_TEXTS.append(ALLSECNS[i])
          refnum=check_secn_border_number(ALLSECNS_borders[i][1])
          EXTERNAL_STATPROC_refnums.append(refnum)
          if refnum in EXTERNAL_STATPROC_TEXTS2 : raise Ex("doit: index")
          EXTERNAL_STATPROC_TEXTS2[refnum] = ALLSECNS[i]
          ## cannot process bylist until later
        else :
          ## Feb 8 2021, add argument ALLSECNS_line_ctr[i],  
          load_to_token_stream(ALLSECNS[i],ALLSECNS_line_ctr[i])
          parseMAIN()
        i+=1      ## subtle!, indent properly, still inside inner while loop
      ## after inner while loop, but still inside large else block
      if COL_PARSE_TREE.type != None : DO_THE_REST()

## end function doit()
## PROOF = 1




###################################################################


def DO_THE_REST() :
  # parseMAIN just completed
  prepGST1()
  execPTRANS()  # call PTRANS twice & call embed_R_inC_1() 
                # i.e. copy over some of the code in old PTRANS file
  
  PREPARE_SOURCING_PHAS()
  SETUP_INFLAG_RESTRICTS()
  prep_for_BESTSORTWAY()
  do_early_PCALL()
  
  
  PROCESS_EACH(COL_PTRANS_TREE,[])
  
  # order matters here, prepGST2 needs fullfilepath() to be ready 
  finishPCALL()
  prepGST2()
  execute_generated_files_from_PCALL()
  execute_gst()
  
#end def DO_THE_REST

######################################################

switched_dir=False

def execute_generated_files_from_PCALL() :
  global switched_dir
  for k in range(len(PCALL_filename)) :
    if PCALL_mode[k]=="vdt" :
      cmdstr = "vilno " + PCALL_filename[k] 
      os.system(cmdstr)
    elif PCALL_mode[k]=="s" :
      if switched_dir==False :
        switched_dir=True 
        # cmdstr2 = "cd " + zdirectory
        # os.system(cmdstr2) 
        os.chdir(zdirectory)
      cmdstr = "R CMD BATCH " + PCALL_filename[k] 
      os.system(cmdstr)


def execute_gst() :
  cmdstr = "tprnt " + tableprint_communicate_filename
  os.system(cmdstr)

##########################################################




###############################################


def parseMAIN() :
  w = seew()
  while w!=None :
    if   w=="col"           : parseCOL(COL_PARSE_TREE)
    elif w=="row"           : parseROW(ROW_PARSE_TREE)
    elif w=="inputdset"     : parseINPUTDSET()
    elif w=="thing"         : parseTHINGDEFN()
    elif w=="onlyif"        : parseONLYIFFOOT()
    elif w=="denom"         : parseDENOMFOOT()
    elif w=="subpop"        : parseSUBPOPFOOT()
    elif w=="categorical"   : parseCATEGORICALST()
    elif w=="continuous"    : parseCONTINUOUSST()
    elif w=="label"         : parseLABEL()
    elif w=="printto"       : parsePRINTTO()
    elif w=="directoryref"  : parseDIRREF()
    elif w=="n"             : parseN_NTHING()
    elif w=="formatfile"    : parseFORMATFILE()
    elif w=="title"         : parseTITLE()
    elif w=="printstat"     : parsePRINTSTAT()
    ## 2020 modification: regular model statement and external statement
    elif w=="model" :
      if see_model_dotinteger_external() : parseMODEL_EXTERNAL_META()
      else                                : parseMODELFOOT()
    ## 2020-2021 more modify: hodgepodge statement and finetune statement
    elif w=="hodgepodge"    : parseHODGEPODGE_ANY()
    elif w=="finetune"      : parseFINETUNE()
    else : raise Ex("parsemainunkword")
    w = seew()
#end def parseMAIN


#################################################

inlinevdt_counter = 0 

def have_vdt_code_executed(listlines) :
  global inlinevdt_counter
  shortfilename = "inlinevdt_" + str(inlinevdt_counter) + ".src"
  inlinevdt_counter = inlinevdt_counter + 1
  filename = zdirectory + "/" + shortfilename
  
  file1 = open(filename,'w')
  file1.writelines(listlines)
  file1.close() 
  
  cmdstr = "vilno " + filename 
  os.system(cmdstr)


############################################################################


def check_secn_border(rows,i) :
  if i+1 >= len(rows) : return None
  if rows[i][0:4] != "****" : return None
  if rows[i+1][0:3] == "vdt" : return "vdt"
  if rows[i+1][0:3] == "ext" : return "ext"
  return None

def check_endvdt(rows,i) :
  if i+1 >= len(rows) : return False
  return rows[i][0:7]=="end-vdt" and rows[i+1][0:4]=="****"

def check_endext(rows,i) :
  if i+1 >= len(rows) : return False
  return rows[i][0:7]=="end-ext" and rows[i+1][0:4]=="****"


def check_secn_border_number(s) :
  if s[0:4]=="ext." :         begin=4
  elif s[0:9]=="external." :  begin=9
  else :                      raise Ex("border-num:syntax err0")
  if begin>=len(s) : raise Ex("border-num:syntax err")
  if not s[begin].isdigit() : raise Ex("border-num:syntax err2")
  k = begin
  while k<len(s) and s[k].isdigit() : k+=1
  num_string = s[begin:k]
  return int(num_string)






