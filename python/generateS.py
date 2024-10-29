# -*- coding: utf-8 -*-

### Copyright 2023 : Robert Wilkins, graduated from Newton North High School 
###                  in 1984, in Massachusetts, USA 

# MAINAPP uses : generate_S_chi generate_S_lm print_importst_S

# spelling mismatch? : 
# pwise uses : entire$pairwise entire$coef entire$fstat  
# change where you print the source() prelude 

from setup import Ex

def generate_S_lm(out_and_param,inputfile,bylist,catvn,contvn,modeleqn_str) :
  ## ??? secn0 = print_prelude_S()   no not anymore , do elsewhere
  secn1 = print_firstsecn_S(out_and_param,inputfile,bylist,catvn,contvn)
  secn2 = print_beforeMcall_intcatmatters()
  secn3 = print_lmcall(modeleqn_str)     # both lm & lm_wrapper
  secn4 = print_lastsecn_S()
  s =   secn1 + "\n" + secn2 + "\n" + secn3 + "\n" + secn4
  return s 
#end def generate_S_lm



def generate_S_chi(out_and_param,inputfile,bylist,vnames,countvar) :
  secn1 = print_firstsecn_S(out_and_param,inputfile,bylist,(),())
  secn2 = print_beforeMcall_simple()
  secn3 = print_chicall(vnames,countvar)     # both chi & chi_wrapper
  secn4 = print_lastsecn_S()
  s = secn1 + "\n" + secn2 + "\n" + secn3 + "\n" + secn4
  return s 
#end def generate_S_chi



def generate_S_ttest(out_and_param,inputfile,bylist,cont_vn,cat_vn,clev1,clev2):
  secn1 = print_firstsecn_S(out_and_param,inputfile,bylist,(),())
  secn2 = print_beforeMcall_simple()
  secn3 = print_ttestcall(cont_vn,cat_vn,clev1,clev2)    
  secn4 = print_lastsecn_S()
  s = secn1 + "\n" + secn2 + "\n" + secn3 + "\n" + secn4
  return s 
#end def generate_S_ttest



def generate_S_q1q3med(out_and_param,inputfile,bylist,cont_vn):
  secn1 = print_firstsecn_S(out_and_param,inputfile,bylist,(),())
  secn2 = print_beforeMcall_simple()
  secn3 = print_q1q3call(cont_vn)    
  secn4 = print_lastsecn_S()
  s = secn1 + "\n" + secn2 + "\n" + secn3 + "\n" + secn4
  return s 
#end def generate_S_q1q3med


#####################


s_firstsecn_leadin = \
"""
desiredparams <- list()
outfiles <- list()
"""


def print_firstsecn_S(out_and_param,inputfile,bylist,catvn,contvn) :
  outsecn = []
  paramsecn = []
  for infotype in out_and_param :
    outs = []
    params = []
    for g in out_and_param[infotype] :
      outs.append(g[0])
      params.append(g[1])
    st1 = "outfiles[[\"" + infotype + "\"]] <- " + printScombine(outs)
    st2 = "desiredparams[[\"" + infotype + "\"]] <- " + printScombine(params)
    outsecn.append(st1)
    paramsecn.append(st2)
  inpst = "inputfile <- \"" + inputfile + "\""
  byst = "bylist <- " + printScombine(bylist)
  catst = "catvnames <- " + printScombine(catvn)
  contst = "contvnames <- " + printScombine(contvn)
  
  
  s = ( s_firstsecn_leadin + "\n" +  
        "\n".join( paramsecn + outsecn + [inpst,byst,catst,contst] ) )
  return s 
#end def print_firstsecn_S


###################################

def printScombine(vec,dt="str") :
  if dt=="str" :
    if len(vec)==0 : return "character()"
    vec2 = []
    for w in vec : vec2.append( "\"" + w + "\"" )
    s = "c(" + ",".join(vec2) + ")" 
  if dt=="int" :
    if len(vec)==0 : return "integer()"
    vec2 = []
    for w in vec : vec2.append( str(w) )
    s = "c(" + ",".join(vec2) + ")" 
  return s 
#end def printScombine

#######################################



importst_text =  \
"""
source("/home/robert/tallinn/R_more/functions1")
source("/home/robert/tallinn/R_more/readascii")
source("/home/robert/tallinn/R_more/parammatch")
source("/home/robert/tallinn/R_more/groupby.txt")
source("/home/robert/tallinn/R_more/pwise")
source("/home/robert/tallinn/R_more/chi")
source("/home/robert/tallinn/R_more/ttest_quart")
source("/home/robert/tallinn/R_more/transwrap")

"""


def print_importst_S() :
  return importst_text
#end def print_importst_S

########################################################

beforeMintmatters_text =  \
"""

for (infotype in names(outfiles)) 
  names(outfiles[[infotype]]) <- desiredparams[[infotype]]

data0 <- read_ascii_datafile(inputfile)
intcatvnames <- determine_intcatvnames(data0,catvnames)
data0 <- dataframe_with_factors(data0,catvnames)
g1 <- divide_dataframe(data0,bylist)
dflist <- g1[[1]]
clevs <- g1[[2]]
numgrp <- length(dflist)
res0 <- list()
res1 <- list()

"""


def print_beforeMcall_intcatmatters() :
  return beforeMintmatters_text
#end def print_beforeMcall_intcatmatters

#########################################################

beforeMsimple_text =   \
"""

for (infotype in names(outfiles)) 
  names(outfiles[[infotype]]) <- desiredparams[[infotype]]

data0 <- read_ascii_datafile(inputfile)
# intcatvnames <- determine_intcatvnames(data0,catvnames)
# data0 <- dataframe_with_factors(data0,catvnames)
g1 <- divide_dataframe(data0,bylist)
dflist <- g1[[1]]
clevs <- g1[[2]]
numgrp <- length(dflist)
res0 <- list()
res1 <- list()

"""


def print_beforeMcall_simple() :
  return beforeMsimple_text
#end def print_beforeMcall_simple


#########################################################################


def print_lmcall(modeleqnstr) :
  s1 = ( "for (k in 1:numgrp) res0[[k]] <- lm(" +
         modeleqnstr +
         ",dflist[[k]])\n" +
         "for (k in 1:numgrp) res1[[k]] <- lm_wrapper(res0[[k]],intcatvnames)\n" )
  return s1 
#end def print_lmcall

####################

def print_chicall(vnames,countvar) :
  vnames2 = tuple(vnames)
  if countvar==None : leftvar="" 
  else : leftvar=countvar
  modeleqn = leftvar + "~" + "+".join(vnames2)
  
  s1 = ( "for (k in 1:numgrp) res0[[k]] <- chisq.test(xtabs(" +
         modeleqn +
         ",dflist[[k]]))\n" +
         "for (k in 1:numgrp) res1[[k]] <- chi_wrapper(res0[[k]])\n" )
  
  return s1 
#end def print_chicall

######################################################################


def print_ttestcall(cont_varname,group_varname,clevel1,clevel2) :
  s1 = ( "for (k in 1:numgrp) res0[[k]] <- t_test(dflist[[k]],\"" + 
                   cont_varname + "\",\"" + group_varname + "\"," + 
                   clevel1 + "," + clevel2 + ")\n" + 
         "for (k in 1:numgrp) res1[[k]] <- ttest_wrapper(res0[[k]])\n" )
  return s1
# end def print_ttestcall


def print_q1q3call(cont_varname) :
  s1 = ( "for (k in 1:numgrp) res0[[k]] <- quantile(dflist[[k]][[\"" + 
                   cont_varname + "\"]])\n" + 
         "for (k in 1:numgrp) res1[[k]] <- quartile_wrapper(res0[[k]])\n" )
  return s1
# end def print_q1q3call 

######################################################################


lastsecn_text = \
"""

res3 <- transpose_stat_wrapper_output(res1,desiredparams,bylist,clevs)
for (infotype in names(res3)) 
  for (param1 in names(res3[[infotype]]))
    write_ascii_datafile(res3[[infotype]][[param1]],outfiles[[infotype]][[param1]])

"""


def print_lastsecn_S() :
  return lastsecn_text
#end def print_lastsecn_S

#######################################################################



